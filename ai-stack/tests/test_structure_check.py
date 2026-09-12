# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evalkit.structure_check import REQUIRED_SECTIONS, check  # noqa: E402
from llm.providers import StubProvider  # noqa: E402


class StructureCheckTests(unittest.TestCase):
    def test_prompt_and_qc_share_the_same_eight_sections(self):
        self.assertEqual(
            REQUIRED_SECTIONS,
            ["概要", "システム構成", "機能一覧", "画面設計", "データ設計", "外部連携", "非機能要件", "移行・運用"],
        )

    def test_stub_draft_passes(self):
        draft = StubProvider().complete("unused")
        result = check(draft)
        self.assertTrue(result["ok"], result["findings"])

    def test_missing_section_is_reported(self):
        draft = "# 基本設計書\n## 1. 概要\n内容\n"
        result = check(draft)
        self.assertFalse(result["ok"])
        self.assertTrue(any("必須章" in f for f in result["findings"]))

    def test_empty_h2_is_reported_but_h1_is_not(self):
        draft = (
            "# 基本設計書\n\n"
            "## 1. 概要\n\n"
            "## 2. システム構成\n本文\n"
        )
        result = check(draft)
        self.assertTrue(any("空の章" in f and "概要" in f for f in result["findings"]))
        self.assertFalse(any("基本設計書" in f for f in result["findings"]))

    def test_known_real_name_is_a_leak(self):
        draft = StubProvider().complete("unused") + "\n佐藤健一が担当。\n"
        result = check(draft, known_real_names=["佐藤健一"])
        self.assertFalse(result["ok"])
        self.assertTrue(any("実名の混入" in f for f in result["findings"]))

    def test_email_pattern_is_flagged(self):
        result = check("## 概要\ncontact@example.com\n")
        self.assertTrue(any("EMAIL" in f for f in result["findings"]))


if __name__ == "__main__":
    unittest.main()
