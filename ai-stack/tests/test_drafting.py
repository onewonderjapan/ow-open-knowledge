# -*- coding: utf-8 -*-
"""プロンプト組立の回帰テスト

守りたい性質:
  1. 出境するテキスト（要件書 + RAG召回した先例）に実名が残らない。
  2. 章立てはQC側と同一の真実源から生成される。
  3. 複数文書を跨いでラベル採番が一貫している（監査表の1:1対応）。
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evalkit.structure_check import REQUIRED_SECTIONS, check   # noqa: E402
from pipeline.drafting import PROMPT_TEMPLATE, build_prompt, build_references   # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_masker import make_masker   # noqa: E402


class TestReferencesAreMasked(unittest.TestCase):
    """旧実装は先例文書を生テキストのままプロンプトに載せていた（出境漏洩）。"""

    def test_reference_body_masked(self):
        m = make_masker(companies=["田中商事"])
        hits = [{"title": "design_portal", "text": "株式会社田中商事向けの予約ポータル設計書"}]
        refs, mapping = build_references(hits, m)
        self.assertNotIn("田中商事", refs)
        self.assertIn("A社", refs)
        self.assertEqual(mapping, {"田中商事": "A社"})

    def test_reference_title_masked(self):
        # ファイル名(=title)に顧客名が入るのは実務では普通
        m = make_masker(companies=["田中商事"])
        hits = [{"title": "design_田中商事_portal", "text": "本文"}]
        refs, _ = build_references(hits, m)
        self.assertNotIn("田中商事", refs)

    def test_mask_before_truncate(self):
        """切り詰めてから脱敏すると境界で実体が分断され断片が漏れる。"""
        from pipeline.drafting import REF_MAX_CHARS
        m = make_masker(companies=["田中商事"])
        padding = "あ" * (REF_MAX_CHARS - 2)
        hits = [{"title": "t", "text": padding + "田中商事の件"}]
        refs, mapping = build_references(hits, m)
        self.assertNotIn("田中", refs)
        self.assertEqual(mapping, {"田中商事": "A社"})

    def test_no_hits(self):
        refs, mapping = build_references([], make_masker())
        self.assertEqual(refs, "(先例なし)")
        self.assertEqual(mapping, {})

    def test_prompt_carries_no_real_name(self):
        m = make_masker(companies=["田中商事"], persons=["佐藤健一"])
        masked_req, mapping = m.mask("株式会社田中商事の佐藤健一様より")
        hits = [{"title": "t", "text": "田中商事の過去案件"}]
        refs, mapping = build_references(hits, m, mapping)
        prompt = build_prompt(masked_req, refs)
        for real in ("田中商事", "佐藤健一"):
            self.assertNotIn(real, prompt, "プロンプトに実名が残っている")


class TestCrossDocumentLabels(unittest.TestCase):
    def test_same_entity_same_label_across_documents(self):
        m = make_masker(companies=["田中商事"])
        masked_req, mapping = m.mask("田中商事の件")
        refs, mapping = build_references(
            [{"title": "t", "text": "田中商事の過去案件"}], m, mapping)
        self.assertIn("A社", masked_req)
        self.assertIn("A社", refs)
        self.assertEqual(mapping, {"田中商事": "A社"})

    def test_different_entities_never_share_a_label(self):
        """採番を引き継がないと別文書の別会社が両方 A社 になり監査表が壊れる。"""
        m = make_masker(companies=["田中商事", "山崎物流"])
        _, mapping = m.mask("田中商事の件")
        _, mapping = build_references(
            [{"title": "t", "text": "山崎物流の過去案件"}], m, mapping)
        self.assertEqual(len(set(mapping.values())), 2, f"ラベル衝突: {mapping}")


class TestSectionsSingleSource(unittest.TestCase):
    def test_prompt_lists_every_required_section(self):
        for sec in REQUIRED_SECTIONS:
            self.assertIn(sec, PROMPT_TEMPLATE, f"プロンプトに章が無い: {sec}")

    def test_qc_requires_the_sections_the_prompt_asks_for(self):
        """旧実装はプロンプト8章 / QC6章で、外部連携と移行・運用が検査されていなかった。"""
        draft = "# 設計書\n" + "".join(f"## {s}\n内容\n" for s in REQUIRED_SECTIONS)
        self.assertTrue(check(draft)["ok"], check(draft)["findings"])
        for missing in ("外部連携", "移行・運用"):
            partial = "# 設計書\n" + "".join(
                f"## {s}\n内容\n" for s in REQUIRED_SECTIONS if s != missing)
            self.assertFalse(check(partial)["ok"], f"{missing} の欠落が検出されない")


class TestQCLeakDetection(unittest.TestCase):
    def test_qc_uses_same_patterns_as_masker(self):
        """検査者が生成者より緩いと検査の意味がない。"""
        draft = "# 設計書\n## 概要\n連絡先 0312345678\n"
        self.assertFalse(check(draft)["ok"])
        self.assertTrue(any("PHONE" in f for f in check(draft)["findings"]))

    def test_qc_detects_fullwidth_leak(self):
        draft = "# 設計書\n## 概要\n連絡先 ０３−１２３４−５６７８\n"
        self.assertTrue(any("PHONE" in f for f in check(draft)["findings"]))

    def test_qc_detects_real_name_in_fullwidth_form(self):
        draft = "# 設計書\n## 概要\nＡＢＣ商事の件\n"
        self.assertTrue(any("実名" in f for f in check(draft, ["ABC商事"])["findings"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
