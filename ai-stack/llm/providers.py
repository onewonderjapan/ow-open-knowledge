# -*- coding: utf-8 -*-
"""LLMプロバイダ抽象層 — 「モデル追加=設定1行」の原型

  stub          : ネット不要のダミー応答（デモ/テスト用）
  claude-cli    : Claude Code CLI (`claude -p`) 経由 = 月額サブスク認証で動く。API key不要。
                  ※PoC/社内狗糧用。顧客本番はAPI版に切替。
  anthropic-api : Anthropic API (要 ANTHROPIC_API_KEY)。本番向け。
"""
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
        # shutil.which で実行ファイルを解決してから shell=False で起動する。
        # shell=True は不要（かつ POSIX ではリストと組み合わせると cmd[0] しか実行されない）。
        # Windows の claude.cmd も which が PATHEXT 経由で解決するのでシェルは要らない。
        exe = shutil.which("claude")
        if exe is None:
            raise RuntimeError(
                "claude コマンドが見つかりません。Claude Code CLI を入れて PATH に通すか、"
                "--provider stub / anthropic-api を使ってください。"
            )
        cmd = [exe, "-p"]
        if self.model:
            cmd += ["--model", self.model]
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                           encoding="utf-8", timeout=600)
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


_REGISTRY: dict[str, type[BaseProvider]] = {
    "stub": StubProvider,
    "claude-cli": ClaudeCLIProvider,
    "anthropic-api": AnthropicAPIProvider,
}


def register_provider(name: str, cls: type[BaseProvider]) -> None:
    """プロバイダを追加する。「モデル追加=設定1行」を外部からも成立させるための口。

    if/elif の分岐に手を入れさせると、追加のたびにコア側を書き換える必要が出る。
    """
    _REGISTRY[name] = cls


def available_providers() -> list[str]:
    return sorted(_REGISTRY)


def get_provider(name: str, **kwargs) -> BaseProvider:
    try:
        cls = _REGISTRY[name]
    except KeyError:
        raise ValueError(
            f"unknown provider: {name} ({' / '.join(available_providers())})"
        ) from None
    return cls(**kwargs)
