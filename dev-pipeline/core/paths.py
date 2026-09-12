# -*- coding: utf-8 -*-
"""workspace 境界の強制.

Agent が扱うファイルパスは LLM の出力に由来する = **信頼できない入力**。
`workspace / "../../etc/passwd"` は workspace の外を指すため、素朴に連結して
書き込み・削除すると任意ファイル操作になる。書き込み・削除・読み取りの前に
必ず `resolve_in_workspace()` を通す。
"""
from pathlib import Path


class PathEscapeError(ValueError):
    """指定パスが workspace の外を指していた."""


def resolve_in_workspace(workspace: Path, relative: str) -> Path:
    """workspace 配下に解決する。外に出るパスは拒否する.

    拒否する例: "../secrets.txt" / "/etc/passwd" / "a/../../b"
    シンボリックリンク経由の脱出も防ぐため resolve() 後に判定する。
    """
    if not relative or not relative.strip():
        raise PathEscapeError("ファイルパスが空です")

    candidate = Path(relative)
    if candidate.is_absolute():
        raise PathEscapeError(f"絶対パスは許可されていません: {relative}")

    root = workspace.resolve()
    target = (root / candidate).resolve()
    if target != root and root not in target.parents:
        raise PathEscapeError(f"workspace の外を指しています: {relative}")
    return target
