#!/usr/bin/env python3
"""Offline verification for ow-open-knowledge. No API keys required."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path) -> None:
    print(f"\n$ {' '.join(cmd)}\n  cwd={cwd}")
    completed = subprocess.run(cmd, cwd=cwd)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def main() -> int:
    py = sys.executable
    run([py, "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"], ROOT / "task-orchestrator")
    run([py, "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"], ROOT / "ai-stack")
    run([py, "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"], ROOT / "dev-pipeline")

    out = ROOT / "ai-stack" / "out"
    run(
        [
            py,
            "pipeline/run.py",
            "demo_data/incoming/new_rfp.md",
            "--provider",
            "stub",
            "--out",
            str(out),
        ],
        ROOT / "ai-stack",
    )
    print("\n[OK] all verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
