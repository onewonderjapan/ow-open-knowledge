# -*- coding: utf-8 -*-
"""stub プロバイダでのエンドツーエンド。ネットワーク不要。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "pipeline" / "run.py"
RFP = ROOT / "demo_data" / "incoming" / "new_rfp.md"


class PipelineStubTests(unittest.TestCase):
    def test_stub_pipeline_writes_three_artifacts_and_passes_qc(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(RUN),
                    str(RFP),
                    "--provider",
                    "stub",
                    "--out",
                    tmp,
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("[OK]", result.stdout)
            stem = RFP.stem
            draft = Path(tmp) / f"{stem}_draft.md"
            masked = Path(tmp) / f"{stem}_masked.md"
            report = Path(tmp) / f"{stem}_report.json"
            self.assertTrue(draft.exists())
            self.assertTrue(masked.exists())
            self.assertTrue(report.exists())
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(payload["provider"], "stub")
            self.assertTrue(payload["qc"]["ok"], payload["qc"]["findings"])
            self.assertGreaterEqual(len(payload["masked_entities"]), 1)
            self.assertNotIn("sato@tanaka-shoji.co.jp", masked.read_text(encoding="utf-8"))

    def test_unknown_provider_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(RUN),
                    str(RFP),
                    "--provider",
                    "no-such-provider",
                    "--out",
                    tmp,
                ],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
