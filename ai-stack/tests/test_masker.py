# -*- coding: utf-8 -*-
"""脱敏层回归テスト。ルール変更時は漏れ=事故なので先にテストを直すこと。"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from masking.masker import Masker  # noqa: E402

DEMO_RFP = ROOT / "demo_data" / "incoming" / "new_rfp.md"
ENTITIES = ROOT / "masking" / "entities.json"


class MaskerTests(unittest.TestCase):
    def setUp(self):
        self.masker = Masker(str(ENTITIES))

    def test_demo_rfp_masks_contact_and_budget(self):
        raw = DEMO_RFP.read_text(encoding="utf-8")
        masked, mapping = self.masker.mask(raw)
        self.assertIn("[EMAIL]", masked)
        self.assertIn("[PHONE]", masked)
        self.assertIn("[MONEY]", masked)
        self.assertNotIn("sato@tanaka-shoji.co.jp", masked)
        self.assertNotIn("03-1234-5678", masked)
        self.assertNotIn("佐藤健一", masked)
        self.assertIn("田中商事", mapping)
        self.assertTrue(any(v.startswith("担当者") for v in mapping.values()))

    def test_same_entity_gets_stable_label(self):
        text = "田中商事の案件。田中商事の担当者と再協議。"
        masked, mapping = self.masker.mask(text)
        label = mapping["田中商事"]
        self.assertEqual(masked.count(label), 2)
        self.assertEqual(len([k for k in mapping if k == "田中商事"]), 1)

    def test_person_honorific_is_not_remasked(self):
        """PITFALLS #1: 置換後ラベルを再度人名と誤認しない。"""
        masked, mapping = self.masker.mask("佐藤健一様よりご相談。")
        self.assertNotIn("佐藤健一", masked)
        self.assertIn("様", masked)
        self.assertNotIn("担当者担当者", masked)
        self.assertEqual(mapping["佐藤健一"], "担当者01")

    def test_company_labels_do_not_collide_after_alphabet_exhausted(self):
        """PITFALLS #8 の会社版: A-N を超えても同一ラベルに潰さない。"""
        names = [f"株式会社テスト{i:02d}商事" for i in range(1, 21)]
        text = "、".join(names)
        masked, mapping = self.masker.mask(text)
        labels = [mapping[n] for n in names]
        self.assertEqual(len(labels), len(set(labels)))
        self.assertTrue(any(lab.startswith("会社") for lab in labels))
        for name in names:
            self.assertNotIn(name, masked)

    def test_custom_overrides_win(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "entities.json"
            path.write_text(
                json.dumps(
                    {
                        "companies": [],
                        "persons": [],
                        "custom": {"大阪データセンター": "[拠点01]"},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            masked, mapping = Masker(str(path)).mask("大阪データセンターに設置。")
            self.assertEqual(mapping["大阪データセンター"], "[拠点01]")
            self.assertIn("[拠点01]", masked)

    def test_regex_rules_cover_postal_url_and_email(self):
        masked, _ = self.masker.mask(
            "〒100-0001 連絡は info@example.com と https://example.com/path です。"
        )
        self.assertIn("[POSTAL]", masked)
        self.assertIn("[EMAIL]", masked)
        self.assertIn("[URL]", masked)


if __name__ == "__main__":
    unittest.main()
