# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.requirement_parser import parse_requirement_file  # noqa: E402
from agents.dispatcher import DEFAULT_PIPELINES  # noqa: E402
from core.models import WorkType  # noqa: E402


class RequirementParserTests(unittest.TestCase):
    def _write(self, tmp: str, text: str) -> Path:
        path = Path(tmp) / "task.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_parses_header_and_utf8_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(
                tmp,
                "branch: feature/add-login\n"
                "repo: https://github.com/example/app.git\n"
                "---\n\n"
                "社員研修の申込管理を追加する。\n",
            )
            spec = parse_requirement_file(path)
            self.assertEqual(spec.branch, "feature/add-login")
            self.assertEqual(spec.repo, "https://github.com/example/app.git")
            self.assertIn("社員研修", spec.content)

    def test_keeps_horizontal_rule_inside_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(
                tmp,
                "branch: feature/x\n---\n前段\n---\n後段\n",
            )
            spec = parse_requirement_file(path)
            self.assertIn("前段", spec.content)
            self.assertIn("後段", spec.content)

    def test_missing_body_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "branch: feature/x\n---\n\n")
            with self.assertRaises(ValueError):
                parse_requirement_file(path)

    def test_full_pipeline_includes_reviewer(self):
        for work_type in (WorkType.DEVELOPMENT, WorkType.INFRASTRUCTURE):
            self.assertIn("reviewer", DEFAULT_PIPELINES[work_type])


if __name__ == "__main__":
    unittest.main()
