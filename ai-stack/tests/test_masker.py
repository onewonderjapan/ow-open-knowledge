# -*- coding: utf-8 -*-
"""脱敏層の回帰テスト（CLAUDE.md: 脱敏ルールはテストなしで変更しない）

標準ライブラリのみ。実行:
  python3 -m unittest discover -s ai-stack/tests
  python3 ai-stack/tests/test_masker.py
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from masking.masker import Masker, company_label, normalize  # noqa: E402

ENTITIES = str(ROOT / "masking" / "entities.json")


def make_masker(companies=None, persons=None, custom=None) -> Masker:
    """一時的な entities.json で Masker を作る（本体の辞書に依存しないケース用）。"""
    tmp = tempfile.mkdtemp()
    p = Path(tmp) / "entities.json"
    p.write_text(json.dumps({
        "companies": companies or [],
        "persons": persons or [],
        "custom": custom or {},
    }, ensure_ascii=False), encoding="utf-8")
    return Masker(str(p))


class TestNormalize(unittest.TestCase):
    def test_fullwidth_digits_and_at(self):
        self.assertEqual(normalize("０３"), "03")
        self.assertEqual(normalize("ａ＠ｂ．ｃｏｍ"), "a@b.com")

    def test_prolonged_sound_mark_preserved(self):
        # U+30FC は電話番号の区切りにも長音符にも使われる。正規化で潰すと日本語が壊れる
        self.assertEqual(normalize("承認フロー"), "承認フロー")

    def test_japanese_text_survives_normalization(self):
        for word in ("承認フロー", "サーバー", "データ", "ポータル"):
            self.assertEqual(normalize(word), word)


class TestPhoneLeaks(unittest.TestCase):
    """区切りなし・空白区切り・全角はいずれも旧実装で素通りしていた（漏洩）。"""

    def setUp(self):
        self.m = make_masker()

    def assert_masked(self, text):
        out, _ = self.m.mask(text)
        self.assertIn("[PHONE]", out, f"未マスク: {text!r} -> {out!r}")

    def test_hyphen_separated(self):
        self.assert_masked("TEL 03-1234-5678")

    def test_no_separator(self):
        self.assert_masked("TEL 0312345678")

    def test_space_separated(self):
        self.assert_masked("TEL 03 1234 5678")

    def test_parenthesised(self):
        self.assert_masked("TEL 03(1234)5678")

    def test_mobile(self):
        self.assert_masked("携帯 090-1234-5678")

    def test_fullwidth_with_minus_sign(self):
        self.assert_masked("TEL ０３−１２３４−５６７８")

    def test_eleven_digits(self):
        self.assert_masked("TEL 09012345678")

    def test_does_not_eat_amounts(self):
        out, _ = self.m.mask("社員約800名、席数は1234席")
        self.assertNotIn("[PHONE]", out)

    def test_does_not_eat_dates(self):
        out, _ = self.m.mask("2024/03/12 に開始")
        self.assertNotIn("[PHONE]", out)


class TestEmail(unittest.TestCase):
    def setUp(self):
        self.m = make_masker()

    def test_normal(self):
        out, _ = self.m.mask("sato@example.co.jp まで")
        self.assertIn("[EMAIL]", out)

    def test_internal_host_without_dot(self):
        out, _ = self.m.mask("連絡先 user@localhost まで")
        self.assertIn("[EMAIL]", out)

    def test_fullwidth_at(self):
        out, _ = self.m.mask("連絡先 user＠example．com まで")
        self.assertIn("[EMAIL]", out)


class TestCompanyLegalForms(unittest.TestCase):
    """法人格は実体と一体で消化する（「株式会社A社」のような壊れた出力を出さない）。"""

    def setUp(self):
        self.m = make_masker(companies=["田中商事"])

    def test_prefix_form(self):
        out, mp = self.m.mask("株式会社田中商事の件")
        self.assertEqual(out, "A社の件")
        self.assertEqual(mp, {"田中商事": "A社"})

    def test_suffix_form(self):
        out, _ = self.m.mask("田中商事株式会社の件")
        self.assertEqual(out, "A社の件")

    def test_bare_form(self):
        out, _ = self.m.mask("田中商事の件")
        self.assertEqual(out, "A社の件")

    def test_yugen_form(self):
        out, _ = self.m.mask("有限会社田中商事の件")
        self.assertEqual(out, "A社の件")

    def test_real_name_never_survives(self):
        for text in ("株式会社田中商事", "田中商事株式会社", "合同会社田中商事", "田中商事"):
            out, _ = self.m.mask(text)
            self.assertNotIn("田中商事", out, f"実名が残った: {text!r} -> {out!r}")


class TestLongestMatchWins(unittest.TestCase):
    """短い custom が長い会社名の内部を先に食い潰してはいけない。"""

    def test_custom_does_not_break_longer_company(self):
        m = make_masker(companies=["田中商事"], custom={"田中": "X地名"})
        out, mp = m.mask("株式会社田中商事の件")
        self.assertEqual(out, "A社の件")
        self.assertNotIn("X地名", out)
        self.assertEqual(mp, {"田中商事": "A社"})

    def test_custom_still_applies_standalone(self):
        m = make_masker(companies=["田中商事"], custom={"田中": "X地名"})
        out, _ = m.mask("田中エリアの件")
        self.assertEqual(out, "X地名エリアの件")

    def test_longer_company_preferred_over_shorter(self):
        m = make_masker(companies=["みどり銀行", "みどり"])
        out, mp = m.mask("みどり銀行の件")
        self.assertNotIn("銀行", out)
        self.assertEqual(list(mp), ["みどり銀行"])


class TestLabelPool(unittest.TestCase):
    """旧実装は14社でラベルが枯れ、15社目以降が静默で N社 に潰れていた（監査性の破壊）。"""

    def test_label_sequence_backwards_compatible(self):
        self.assertEqual([company_label(i) for i in range(3)], ["A社", "B社", "C社"])
        self.assertEqual(company_label(13), "N社")

    def test_label_beyond_z(self):
        self.assertEqual(company_label(25), "Z社")
        self.assertEqual(company_label(26), "AA社")
        self.assertEqual(company_label(27), "AB社")

    def test_thirty_companies_get_unique_labels(self):
        names = [f"テスト商事{i:02d}" for i in range(30)]
        m = make_masker(companies=names)
        out, mp = m.mask(" ".join(f"株式会社{n}" for n in names))
        self.assertEqual(len(mp), 30)
        self.assertEqual(len(set(mp.values())), 30, "ラベル衝突: 監査の1:1対応が壊れている")
        for n in names:
            self.assertNotIn(n, out)


class TestPersonPatterns(unittest.TestCase):
    def setUp(self):
        self.m = make_masker(persons=["佐藤健一"])

    def test_honorific_masked(self):
        out, _ = self.m.mask("佐藤健一様よりご連絡")
        self.assertEqual(out, "担当者01様よりご連絡")

    def test_unknown_person_with_honorific_masked(self):
        # 辞書外でも敬称が付けば伏せる（漏れより過剰マスクを選ぶ）
        out, _ = self.m.mask("田村様よりご連絡")
        self.assertIn("担当者01様", out)

    def test_org_word_before_title_not_a_person(self):
        for text in ("人事部長の承認フロー", "営業部長に確認", "総務課長へ提出"):
            out, mp = self.m.mask(text)
            self.assertEqual(out, text, f"職務名を人名と誤判定: {text!r} -> {out!r}")
            self.assertEqual(mp, {}, f"監査表に架空の人物が入った: {mp}")

    def test_real_person_with_title_masked(self):
        out, _ = self.m.mask("田村部長に確認")
        self.assertIn("担当者01部長", out)

    def test_label_not_remasked(self):
        out, _ = self.m.mask("担当者01様、担当者02様")
        self.assertEqual(out, "担当者01様、担当者02様")


class TestConsistency(unittest.TestCase):
    def test_same_entity_same_label(self):
        m = make_masker(companies=["田中商事", "山崎物流"])
        out, mp = m.mask("田中商事と山崎物流。再び田中商事の件。")
        self.assertEqual(out, "A社とB社。再びA社の件。")
        self.assertEqual(mp, {"田中商事": "A社", "山崎物流": "B社"})

    def test_mapping_values_unique(self):
        m = make_masker(companies=["田中商事", "山崎物流", "みどり銀行"])
        _, mp = m.mask("田中商事 山崎物流 みどり銀行")
        self.assertEqual(len(set(mp.values())), len(mp))


class TestDemoCorpus(unittest.TestCase):
    """同梱デモ要件書が実名を1つも漏らさないこと（end-to-end の砦）。"""

    def test_demo_rfp_fully_masked(self):
        rfp = ROOT / "demo_data" / "incoming" / "new_rfp.md"
        m = Masker(ENTITIES)
        raw = rfp.read_text(encoding="utf-8")
        out, mp = m.mask(raw)
        entities = json.loads(Path(ENTITIES).read_text(encoding="utf-8"))
        for name in entities["companies"] + entities["persons"]:
            self.assertNotIn(name, out, f"実名が masked 出力に残っている: {name}")
        self.assertNotIn("@", out, "メールアドレスが残っている")
        self.assertNotIn("株式会社", out, "法人格が伏せ字と二重に残っている")
        self.assertTrue(mp, "何もマスクされていない")


if __name__ == "__main__":
    unittest.main(verbosity=2)
