# -*- coding: utf-8 -*-
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The pipeline shells out to run.py, which imports the janome-backed RAG layer.
# Without janome this test cannot exercise anything, so skip instead of failing:
# a missing optional dependency is not a regression in the code under test.
HAS_JANOME = importlib.util.find_spec("janome") is not None


@unittest.skipUnless(HAS_JANOME, "janome is not installed; the stub pipeline cannot run")
class PipelineStubTests(unittest.TestCase):
    def test_stub_pipeline_writes_artifacts_without_real_names_in_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "pipeline" / "run.py"),
                    str(ROOT / "demo_data" / "incoming" / "new_rfp.md"),
                    "--provider",
                    "stub",
                    "--out",
                    str(out),
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            masked = (out / "new_rfp_masked.md").read_text(encoding="utf-8")
            report = json.loads((out / "new_rfp_report.json").read_text(encoding="utf-8"))
            mapping = json.loads((out / "new_rfp_mapping.json").read_text(encoding="utf-8"))
            self.assertIn("[EMAIL]", masked)
            self.assertNotIn("佐藤健一", masked)
            self.assertGreaterEqual(report["masked_entity_count"], 3)
            report_text = json.dumps(report, ensure_ascii=False)
            self.assertNotIn("佐藤健一", report_text)
            self.assertNotIn("田中商事", report_text)
            self.assertIn("佐藤健一", mapping)
            self.assertTrue(report["qc"]["ok"], report["qc"])
            self.assertIn(str(out), proc.stdout)


if __name__ == "__main__":
    unittest.main()
