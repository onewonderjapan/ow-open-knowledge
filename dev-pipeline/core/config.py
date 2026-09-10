"""グローバル設定."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    # Anthropic API (optional: Claude Code CLI uses OAuth when api_key is empty)
    api_key: str = field(default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", ""))
    model: str = "claude-sonnet-4-6"

    # パス
    workspace: Path = field(default_factory=lambda: Path("workspace"))
    output_dir: Path = field(default_factory=lambda: Path("output"))

    # Git リポジトリ
    repo_url: Optional[str] = None
    branch: Optional[str] = None

    # Agent パラメータ
    max_tokens: int = 4096
    temperature: float = 0.3

    # レート制限（無料プラン：5 req/min, 4000 output tokens/min）
    rate_limit_pause: float = 15.0

    def __post_init__(self) -> None:
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
