#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公開している SKILL.md が skill ローダから読める形かを検証する（標準ライブラリのみ）。

usage:
  python3 scripts/check_skills.py           # リポジトリ全体
  python3 scripts/check_skills.py cloud-patterns/

frontmatter の `name` / `description` が無い SKILL.md は、Claude Code 系でも
Codex 系でも「スキルとして認識されない」。README で配布を謳っているのに
ローダが無視する、という食い違いを防ぐための門番。

パースは `task-orchestrator/scripts/scan_skills.py::parse_skill` をそのまま使う。
門番用に二本目の YAML パーサを書くと、ローダが受理する `description: >` を
CI が落とす（またはその逆）ことになる。

`name` はディレクトリ名と一致していないと、カタログ上の名前と実際の
参照パスがずれて追跡できなくなるため、これも検証する。
テンプレート（`CHANGE-ME` で始まる名前）は穴埋め前提なので一致検証から外す。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}
PLACEHOLDER_PREFIX = "CHANGE-ME"
MIN_DESCRIPTION_CHARS = 10
SCANNER_PATH = Path(__file__).resolve().parents[1] / "task-orchestrator" / "scripts" / "scan_skills.py"


def _load_scanner():
    spec = importlib.util.spec_from_file_location("scan_skills", SCANNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCANNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_skill_files(root: Path):
    for p in sorted(root.rglob("SKILL.md")):
        if SKIP_DIRS & set(p.parts):
            continue
        yield p


def check(root: Path, scanner=None) -> list[str]:
    scanner = scanner or _load_scanner()
    problems = []
    for path in iter_skill_files(root):
        try:
            fields = scanner.parse_skill(path)
        except (OSError, UnicodeError, ValueError) as error:
            problems.append(f"{path}: ローダが読めません ({error})")
            continue

        description = fields.get("description", "")
        if len(description) < MIN_DESCRIPTION_CHARS:
            problems.append(
                f"{path}: `description` が短すぎます（いつ使うかを書く）: {description!r}"
            )

        name = fields.get("name", "")
        directory = path.parent.name
        if name and not name.startswith(PLACEHOLDER_PREFIX) and name != directory:
            problems.append(f"{path}: `name: {name}` がディレクトリ名 `{directory}` と一致しません")
    return problems


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    default_root = Path(__file__).resolve().parents[1]
    explicit = bool(args)
    root = Path(args[0]) if args else default_root
    if explicit and not root.exists():
        print(f"パスが存在しません: {root}", file=sys.stderr)
        return 2
    files = list(iter_skill_files(root))
    if explicit and not files:
        print(f"SKILL.md がありません: {root}", file=sys.stderr)
        return 2
    problems = check(root)
    if problems:
        print(f"SKILL.md の問題 {len(problems)} 件:")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"OK: {len(files)} 個の SKILL.md は frontmatter を持ち、名前も一致しています")
    return 0


if __name__ == "__main__":
    sys.exit(main())
