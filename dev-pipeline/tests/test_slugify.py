# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from main import _slugify  # noqa: E402


class SlugifyTests(unittest.TestCase):
    def test_ascii_name(self) -> None:
        self.assertEqual(_slugify("Add Login"), "add_login")

    def test_cjk_name_is_stable(self) -> None:
        first = _slugify("ログイン機能")
        second = _slugify("ログイン機能")
        self.assertEqual(first, second)
        self.assertTrue(first.startswith("req_"))
        self.assertEqual(len(first), len("req_") + 8)


if __name__ == "__main__":
    unittest.main()
