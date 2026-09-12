# -*- coding: utf-8 -*-
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate import validate_workflow  # noqa: E402


class ValidateWorkflowTests(unittest.TestCase):
    def test_bundled_template_is_valid(self) -> None:
        findings = validate_workflow(ROOT / "template")
        self.assertEqual(findings, [])

    def test_rejects_invalid_mode_and_broken_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "sample"
            shutil.copytree(ROOT / "template", dest)
            (dest / "config.yml").write_text(
                "name: sample\nmode: production\n",
                encoding="utf-8",
            )
            (dest / "state" / "ledger.jsonl").write_text(
                '{"run_key": "2026-01-01", "ts": "t", "schema_version": 1}\n'
                "not-json\n",
                encoding="utf-8",
            )
            findings = validate_workflow(dest)
        self.assertTrue(any("mode" in f for f in findings))
        self.assertTrue(any("jsonl" in f.lower() or "JSON" in f for f in findings))

    def test_rejects_duplicate_run_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "sample"
            shutil.copytree(ROOT / "template", dest)
            line = '{"run_key": "2026-01-01", "ts": "t", "schema_version": 1}\n'
            (dest / "state" / "ledger.jsonl").write_text(line + line, encoding="utf-8")
            findings = validate_workflow(dest)
        self.assertTrue(any("run_key" in f for f in findings))


if __name__ == "__main__":
    unittest.main()
