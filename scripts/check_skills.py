#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公開している SKILL.md が skill ローダから読める形かを検証する（標準ライブラリのみ）。

usage:
  python3 scripts/check_skills.py           # リポジトリ全体
  python3 scripts/check_skills.py cloud-patterns/

frontmatter の `name` / `description` が無い SKILL.md は、Claude Code 系でも
Codex 系でも「スキルとして認識されない」。README で配布を謳っているのに
ローダが無視する、という食い違いを防ぐための門番。

`name` はディレクトリ名と一致していないと、カタログ上の名前と実際の
参照パスがずれて追跡できなくなるため、これも検証する。
テンプレート（`CHANGE-ME` で始まる名前）は穴埋め前提なので一致検証から外す。
"""
from __future__ import annotations

import sys
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}
REQUIRED_KEYS = ("name", "description")
PLACEHOLDER_PREFIX = "CHANGE-ME"
MIN_DESCRIPTION_CHARS = 10


def iter_skill_files(root: Path):
    for p in sorted(root.rglob("SKILL.md")):
        if SKIP_DIRS & set(p.parts):
            continue
        yield p


def parse_frontmatter(text: str) -> dict | None:
    """先頭の `---` 区切りブロックを `key: value` として読む。無ければ None。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        key, sep, value = line.partition(":")
        if sep and not key.startswith((" ", "\t")):
            fields[key.strip()] = value.strip()
    return None  # 閉じの `---` が無い＝frontmatter として不正


def check(root: Path) -> list[str]:
    problems = []
    for path in iter_skill_files(root):
        fields = parse_frontmatter(path.read_text(encoding="utf-8"))
        if fields is None:
            problems.append(f"{path}: YAML frontmatter（`---` で囲む）が無いためローダが読み込めません")
            continue

        for key in REQUIRED_KEYS:
            if not fields.get(key):
                problems.append(f"{path}: frontmatter に `{key}` がありません")

        description = fields.get("description", "")
        if description and len(description) < MIN_DESCRIPTION_CHARS:
            problems.append(
                f"{path}: `description` が短すぎます（いつ使うかを書く）: {description!r}"
            )

        name = fields.get("name", "")
        directory = path.parent.name
        if name and not name.startswith(PLACEHOLDER_PREFIX) and name != directory:
            problems.append(f"{path}: `name: {name}` がディレクトリ名 `{directory}` と一致しません")
    return problems


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    files = list(iter_skill_files(root))
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
