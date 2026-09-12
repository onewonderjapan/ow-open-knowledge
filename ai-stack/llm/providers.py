# -*- coding: utf-8 -*-
"""LLMプロバイダ抽象層 — 「モデル追加=設定1行」の原型

  stub          : ネット不要のダミー応答（デモ/テスト用）
  claude-cli    : Claude Code CLI (`claude -p`) 経由 = 月額サブスク認証で動く。API key不要。
                  ※PoC/社内狗糧用。顧客本番はAPI版に切替。
  anthropic-api : Anthropic API (要 ANTHROPIC_API_KEY)。本番向け。
"""
from __future__ import annotations

import shutil
import subprocess


class BaseProvider:
    name = "base"

    def complete(self, prompt: str) -> str:
        raise NotImplementedError


class StubProvider(BaseProvider):
    name = "stub"

    def complete(self, prompt: str) -> str:
        return (
            "# 基本設計書（ドラフト）\n\n"
            "## 1. 概要\n（スタブ応答: 実際のLLM出力はここに要件の要約が入ります）\n\n"
            "## 2. システム構成\n（スタブ）\n\n## 3. 機能一覧\n（スタブ）\n\n"
            "## 4. 画面設計\n（スタブ）\n\n## 5. データ設計\n（スタブ）\n\n"
            "## 6. 外部連携\n（スタブ）\n\n## 7. 非機能要件\n（スタブ）\n\n"
            "## 8. 移行・運用\n（スタブ）\n"
        )


class ClaudeCLIProvider(BaseProvider):
    """Claude Code の -p (print) モードを子プロセスで叩く。サブスク認証を流用。"""
    name = "claude-cli"

    def __init__(self, model: str | None = None):
        self.model = model

    def complete(self, prompt: str) -> str:
        binary = shutil.which("claude") or "claude"
        cmd = [binary, "-p"]
        if self.model:
            cmd += ["--model", self.model]
        # shell=False: on POSIX, shell=True + a list only runs cmd[0] as the
        # script and treats the rest as extra *shell* arguments — broken on Linux.
        r = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=600,
            shell=False,
        )
        if r.returncode != 0:
            raise RuntimeError(f"claude-cli failed: {r.stderr[:500]}")
        return r.stdout.strip()


class AnthropicAPIProvider(BaseProvider):
    name = "anthropic-api"

    def __init__(self, model: str = "claude-sonnet-5"):
        import anthropic  # 遅延import
        self.client = anthropic.Anthropic()  # ANTHROPIC_API_KEY を読む
        self.model = model

    def complete(self, prompt: str) -> str:
        msg = self.client.messages.create(
            model=self.model, max_tokens=8000,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in msg.content if b.type == "text")


def get_provider(name: str) -> BaseProvider:
    if name == "stub":
        return StubProvider()
    if name == "claude-cli":
        return ClaudeCLIProvider()
    if name == "anthropic-api":
        return AnthropicAPIProvider()
    raise ValueError(f"unknown provider: {name} (stub / claude-cli / anthropic-api)")
