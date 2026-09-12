"""要件ファイルパーサー.

要件ファイルの形式：
    branch: feature/xxx
    repo: https://github.com/user/project.git
    ---
    要件の本文...

ルール：
- branch と repo は --- 区切り線の前（ヘッダーメタ情報）に記述
- --- の後が要件本文
- branch も repo も任意（調査タスクなど、コードを書かない作業では不要）
- 区切り線を省略してもよい。先頭の連続する `branch:` / `repo:` 行だけをヘッダーと見なす
- 先頭を --- で囲む YAML フロントマター形式も受け付ける
- 同じファイルで再実行する場合、ブランチが既に存在すれば切り替え、重複作成しない
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

HEADER_KEYS = ("branch", "repo")


@dataclass
class RequirementSpec:
    """パース後の要件仕様."""
    branch: Optional[str]
    repo: Optional[str]
    content: str
    source_file: str  # 元ファイル名（再実行判定用）


def _is_separator(line: str) -> bool:
    """`---` / `-----` などの区切り線か."""
    s = line.strip()
    return len(s) >= 3 and set(s) == {"-"}


def _first_nonblank(lines: list[str], start: int = 0) -> int | None:
    for i in range(start, len(lines)):
        if lines[i].strip():
            return i
    return None


def parse_requirement_file(file_path: Path) -> RequirementSpec:
    """要件ファイルを解析し、branch・repo・本文を抽出する.

    素朴に `text.split("---", 1)` すると2つの壊れ方をする:
      1. 区切り線が無いファイルでは `branch:` 行が本文に残り、そのまま Agent に渡る。
      2. 本文中の Markdown 水平線が区切り線と誤認され、その手前の本文が捨てられる。
    そのため「先頭の連続するヘッダー行」だけをヘッダーとして扱う。
    """
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    branch: Optional[str] = None
    repo: Optional[str] = None

    i = 0
    first = _first_nonblank(lines)
    # YAML フロントマター形式（先頭が区切り線）
    in_frontmatter = first is not None and _is_separator(lines[first])
    if in_frontmatter:
        i = first + 1

    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        if _is_separator(stripped):
            i += 1
            break
        key, sep, value = stripped.partition(":")
        if sep and key.strip().lower() in HEADER_KEYS:
            if key.strip().lower() == "branch":
                branch = value.strip() or None
            else:
                repo = value.strip() or None
            i += 1
            continue
        if in_frontmatter:
            i += 1          # フロントマター内の未知キーは無視して読み進める
            continue
        break               # 区切り線なし: ここから本文

    content = "\n".join(lines[i:]).strip()
    if not content:
        raise ValueError(f"要件ファイルの本文が空です: {file_path}")

    return RequirementSpec(
        branch=branch,
        repo=repo,
        content=content,
        source_file=file_path.name,
    )
