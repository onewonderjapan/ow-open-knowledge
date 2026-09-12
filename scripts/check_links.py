#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""リポジトリ内の Markdown 相対リンクが実在するか検証する（標準ライブラリのみ）。

usage:
  python3 scripts/check_links.py           # リポジトリ全体
  python3 scripts/check_links.py docs/     # ディレクトリを絞る

ファイル名に空白を含む日本語ドキュメントがあるため、`%20` などの
パーセントエンコーディングをデコードしてから存在確認する
（GitHub のレンダラと同じ挙動）。
"""
import re
import sys
import urllib.parse
from pathlib import Path

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "data:")


def iter_markdown(root: Path):
    for p in sorted(root.rglob("*.md")):
        if SKIP_DIRS & set(p.parts):
            continue
        yield p


def check(root: Path) -> list[str]:
    problems = []
    for path in iter_markdown(root):
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in LINK_RE.finditer(line):
                label, target = match.group(1), match.group(2)
                if target.startswith(EXTERNAL_PREFIXES):
                    continue
                target = target.split("#", 1)[0].strip()
                if not target:
                    continue
                decoded = urllib.parse.unquote(target)
                if not (path.parent / decoded).exists():
                    problems.append(f"{path}:{lineno}: [{label}]({target}) -> 見つかりません")
    return problems


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    files = list(iter_markdown(root))
    problems = check(root)
    if problems:
        print(f"壊れた相対リンク {len(problems)} 件:")
        for p in problems:
            print(f"  {p}")
        return 1
    print(f"OK: {len(files)} 個の Markdown の相対リンクは全て解決しました")
    return 0


if __name__ == "__main__":
    sys.exit(main())
