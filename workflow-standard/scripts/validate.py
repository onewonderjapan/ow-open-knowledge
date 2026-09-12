#!/usr/bin/env python3
"""Validate a workflow directory against STANDARD.md machine-checkable rules.

Checks:
  - required files exist
  - config.yml mode is paper|live and gates are declared
  - jsonl ledgers are valid JSON lines with run_key / ts / schema_version
  - run_key values are unique (idempotency)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_FILES = [
    "SKILL.md",
    "config.yml",
    "steps/1-ingest.md",
    "steps/2-decide.md",
    "steps/3-evaluate.md",
    "steps/4-improve.md",
    "state/strategy.md",
]

JSONL_FILES = ["state/ledger.jsonl", "state/scorecard.jsonl"]
VALID_MODES = {"paper", "live"}


def _simple_yaml_value(text: str, key: str) -> str | None:
    prefix = f"{key}:"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if line.startswith(prefix) or stripped.startswith(prefix):
            return stripped.split(":", 1)[1].strip().strip("\"'")
    return None


def validate_workflow(root: Path) -> list[str]:
    findings: list[str] = []
    root = Path(root)
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            findings.append(f"missing file: {rel}")

    cfg_path = root / "config.yml"
    if cfg_path.exists():
        cfg = cfg_path.read_text(encoding="utf-8")
        mode = _simple_yaml_value(cfg, "mode")
        if mode not in VALID_MODES:
            findings.append(f"config.yml mode must be paper or live, got {mode!r}")
        if "gates:" not in cfg:
            findings.append("config.yml missing gates:")

    for rel in JSONL_FILES:
        path = root / rel
        if not path.exists():
            findings.append(f"missing file: {rel}")
            continue
        seen: dict[str, int] = {}
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                findings.append(f"{rel} line {index}: invalid JSON ({exc})")
                continue
            if not isinstance(obj, dict):
                findings.append(f"{rel} line {index}: JSON object required")
                continue
            for field in ("run_key", "ts", "schema_version"):
                if field not in obj:
                    findings.append(f"{rel} line {index}: missing {field}")
            key = obj.get("run_key")
            if isinstance(key, str) and key:
                if key in seen:
                    findings.append(f"{rel}: duplicate run_key {key!r}")
                seen[key] = index
    return findings


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("usage: validate.py <workflow-dir> [...]", file=sys.stderr)
        return 2
    status = 0
    for raw in args:
        root = Path(raw)
        findings = validate_workflow(root)
        if findings:
            status = 1
            print(f"{root}: FAIL")
            for item in findings:
                print(f"  - {item}")
        else:
            print(f"{root}: OK")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
