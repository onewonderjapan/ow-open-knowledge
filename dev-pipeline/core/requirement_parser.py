"""要件ファイルパーサー.

要件ファイルの形式：
    branch: feature/xxx
    repo: https://github.com/user/project.git
    ---
    要件の本文...

ルール：
- branch と repo は --- 区切り線の前（ヘッダーメタ情報）に記述
- --- の後が要件本文
- branch は必須、repo は任意（workspace が既に git リポジトリの場合は不要）
- 同じファイルで再実行する場合、ブランチが既に存在すれば切り替え、重複作成しない
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RequirementSpec:
    """パース後の要件仕様."""
    branch: Optional[str]
    repo: Optional[str]
    content: str
    source_file: str  # 元ファイル名（再実行判定用）


def parse_requirement_file(file_path: Path) -> RequirementSpec:
    """要件ファイルを解析し、branch・repo・本文を抽出する."""
    text = file_path.read_text().strip()

    # --- でヘッダーと本文を分割
    if "---" in text:
        header, content = text.split("---", 1)
    else:
        header = text
        content = text

    # ヘッダーフィールドの解析
    branch = None
    repo = None

    for line in header.strip().splitlines():
        line = line.strip()
        if line.lower().startswith("branch:"):
            branch = line.split(":", 1)[1].strip()
        elif line.lower().startswith("repo:"):
            repo = line.split(":", 1)[1].strip()

    # branch is optional for non-code tasks (e.g. research/investigation)
    if not branch:
        branch = None
    if not repo:
        repo = None

    content = content.strip()
    if not content:
        raise ValueError(f"要件ファイルの本文が空です: {file_path}")

    return RequirementSpec(
        branch=branch,
        repo=repo,
        content=content,
        source_file=file_path.name,
    )
