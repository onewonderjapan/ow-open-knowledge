# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evalkit.structure_check import REQUIRED_SECTIONS, check  # noqa: E402

SECTIONS = "\n\n".join(f"## {i}. {sec}\n本文" for i, sec in enumerate(REQUIRED_SECTIONS, 1))


class StructureCheckTests(unittest.TestCase):
    def test_h1_followed_by_h2_is_not_an_empty_chapter(self) -> None:
        draft = f"# 基本設計書（ドラフト）\n\n{SECTIONS}\n"
        result = check(draft)
        self.assertTrue(result["ok"], result["findings"])

    def test_empty_h2_is_reported(self) -> None:
        body = "\n\n".join(
            f"## {i}. {sec}\n" + ("" if i == 1 else "本文")
            for i, sec in enumerate(REQUIRED_SECTIONS, 1)
        )
        result = check(f"# 基本設計書\n\n{body}\n")
        self.assertFalse(result["ok"])
        self.assertTrue(any("空の章" in f for f in result["findings"]))

    def test_known_real_name_is_a_finding(self) -> None:
        draft = f"# 基本設計書\n\n{SECTIONS.replace('本文', '田中商事向け', 1)}\n"
        result = check(draft, known_real_names=["田中商事"])
        self.assertFalse(result["ok"])
        self.assertTrue(any("実名" in f for f in result["findings"]))

    def test_surname_fragment_from_known_name_is_flagged(self) -> None:
        draft = f"# 基本設計書\n\n{SECTIONS.replace('本文', '佐藤が主担当', 1)}\n"
        result = check(draft, known_real_names=["佐藤健一"])
        self.assertFalse(result["ok"])
        self.assertTrue(any("断片" in f for f in result["findings"]))


if __name__ == "__main__":
    unittest.main()
