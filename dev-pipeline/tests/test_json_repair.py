# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.base import BaseAgent, _repair_truncated_json  # noqa: E402
from agents.developer import DeveloperAgent  # noqa: E402
from core.config import Config  # noqa: E402


class JsonRepairTests(unittest.TestCase):
    def test_closes_truncated_object(self) -> None:
        repaired = _repair_truncated_json('{"lessons": [{"content": "keep going"')
        data = json.loads(repaired)
        self.assertEqual(data["lessons"][0]["content"], "keep going")

    def test_extract_json_from_fence(self) -> None:
        raw = 'note\n```json\n{"ok": true}\n```\n'
        self.assertEqual(BaseAgent._extract_json(raw), {"ok": True})


class StructuredOutputTests(unittest.TestCase):
    def test_parses_file_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            agent = DeveloperAgent(Config(workspace=root / "ws", output_dir=root / "out"))
            raw = """```json
{"status": "done", "changes": [{"file_path": "app.py", "action": "create", "description": "demo"}]}
```
<<<FILE:app.py>>>
print("hi")
<<<END>>>
"""
            metadata, files = agent._parse_structured_output(raw)
            self.assertEqual(metadata["changes"][0]["file_path"], "app.py")
            self.assertEqual(files["app.py"], 'print("hi")')


if __name__ == "__main__":
    unittest.main()
