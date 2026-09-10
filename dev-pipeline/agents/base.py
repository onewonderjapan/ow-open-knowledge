"""Agent 基底クラス。Claude Code CLI + 自己学習 + 自己最適化."""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
from abc import ABC
from datetime import datetime
from pathlib import Path
from typing import Any

from core.config import Config

logger = logging.getLogger(__name__)

MEMORY_DIR = Path(__file__).parent / "memory"
PROMPTS_DIR = Path(__file__).parent / "prompts"

# ── 自己学習用プロンプト ──────────────────────────────────────

REFLECTION_PROMPT = """\
あなたは AI Agent の自己改善アドバイザーです。
以下の Agent の実行結果を分析し、次回の実行に活かせる教訓を抽出してください。

ルール：
- 既に記憶にある内容と重複しないこと
- 具体的かつ実用的な教訓のみ抽出（抽象的な感想は不要）
- 最大3件まで
- 教訓がない場合は空配列を返す

JSON 形式で出力：
```json
{
  "lessons": [
    {
      "category": "success|failure|improvement",
      "content": "具体的な教訓（1-2文）",
      "action": "次回こうすべき（1文）"
    }
  ]
}
```
JSON のみ出力。教訓がなければ {"lessons": []} を返す。
"""

# ── 自己最適化用プロンプト ────────────────────────────────────

OPTIMIZE_PROMPT = """\
あなたは AI Agent のシステムプロンプト最適化エンジニアです。
以下の Agent の現在の system prompt と過去の実行ログ（成功/失敗/教訓）を分析し、
system prompt を改善してください。

## 最適化の方針
1. 過去の失敗パターンを防ぐルールを追加
2. 成功パターンを強化する指示を追加
3. 冗長・矛盾する指示を整理
4. 出力品質を上げる具体的なガイドラインを追加
5. 元の prompt の目的・構造は維持する

## 出力形式
改善後の system prompt 全文を出力してください。
```prompt で始まり ``` で終わるコードブロック内に記述すること。
prompt 以外のテキスト（説明等）は不要。
"""


class BaseAgent(ABC):
    """全 Agent の基底クラス。自己学習 + 自己最適化機能を内蔵."""

    name: str = "base"

    def __init__(self, config: Config) -> None:
        self.config = config
        self.logger = logging.getLogger(f"agent.{self.name}")
        self._memory_path = MEMORY_DIR / f"{self.name}.md"
        self._evolved_prompt_path = PROMPTS_DIR / f"{self.name}.md"

    # ── 進化型プロンプト ──────────────────────────────────────

    def load_evolved_prompt(self, default_prompt: str) -> str:
        """進化型プロンプトがあればそれを返す。なければデフォルトを返す."""
        if self._evolved_prompt_path.exists():
            evolved = self._evolved_prompt_path.read_text(encoding="utf-8").strip()
            if evolved:
                self.logger.debug(f"[{self.name}] 進化型プロンプトを使用")
                return evolved
        return default_prompt

    # ── メモリ（自己学習） ────────────────────────────────────

    def load_memory(self) -> str:
        """過去の学習記録を読み込み、system prompt に追加するテキストを返す."""
        if not self._memory_path.exists():
            return ""
        content = self._memory_path.read_text(encoding="utf-8").strip()
        if not content:
            return ""
        return (
            f"\n\n## 過去の学習記録（自己改善メモ）\n"
            f"以下は過去の実行から学んだ教訓です。これらを考慮して今回のタスクに取り組んでください。\n\n"
            f"{content}"
        )

    def reflect_and_learn(self, task_description: str, result: str, success: bool) -> None:
        """実行結果を振り返り、教訓をメモリに保存."""
        existing_memory = ""
        if self._memory_path.exists():
            existing_memory = self._memory_path.read_text(encoding="utf-8")

        if len(existing_memory) > 5000:
            self.logger.info(f"[{self.name}] メモリが上限に近い、consolidate を推奨")
            return

        status = "成功" if success else "失敗"
        user_message = f"""\
## Agent 情報
名前: {self.name}

## 今回のタスク
{task_description[:500]}

## 実行結果（{status}）
{result[:1000]}

## 既存の記憶
{existing_memory[:1000] if existing_memory else "（なし）"}

上記を分析し、次回に活かせる教訓を抽出してください。既存の記憶と重複しないこと。"""

        try:
            raw = self.call_llm(REFLECTION_PROMPT, user_message)
            data = self._extract_json(raw)
            lessons = data.get("lessons", [])

            if not lessons:
                self.logger.info(f"[{self.name}] 新しい教訓なし")
                return

            MEMORY_DIR.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_entries = [f"\n### {timestamp}\n"]
            for lesson in lessons:
                category = lesson.get("category", "improvement")
                icon = {"success": "✅", "failure": "❌", "improvement": "💡"}.get(category, "📝")
                content = lesson.get("content", "")
                action = lesson.get("action", "")
                new_entries.append(f"- {icon} {content}")
                if action:
                    new_entries.append(f"  → **次回アクション:** {action}")

            with open(self._memory_path, "a", encoding="utf-8") as f:
                f.write("\n".join(new_entries) + "\n")

            self.logger.info(f"[{self.name}] {len(lessons)} 件の教訓を記録")

        except Exception as e:
            self.logger.warning(f"[{self.name}] 振り返り失敗（スキップ）: {e}")

    def consolidate_memory(self) -> None:
        """メモリを整理・要約して圧縮する."""
        if not self._memory_path.exists():
            self.logger.info(f"[{self.name}] メモリなし、整理不要")
            return

        existing = self._memory_path.read_text(encoding="utf-8")
        if len(existing) < 1000:
            self.logger.info(f"[{self.name}] メモリが小さい、整理不要")
            return

        consolidate_prompt = """\
あなたは AI Agent のメモリ管理者です。
以下の学習記録を整理・統合してください。

ルール：
- 重複を排除し、関連する教訓を統合
- 古くなった教訓や矛盾する教訓を整理
- 最も重要な教訓を優先（最大10件）
- Markdown 箇条書き形式で出力
- 各教訓は「→ 次回アクション:」付き
- タイトル行なし、箇条書きのみ出力
"""
        try:
            consolidated = self.call_llm(consolidate_prompt, f"## 現在の学習記録\n{existing}")
            self._memory_path.write_text(
                f"<!-- 統合日時: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->\n{consolidated}\n",
                encoding="utf-8",
            )
            self.logger.info(f"[{self.name}] メモリを統合（{len(existing)} → {len(consolidated)} 文字）")
        except Exception as e:
            self.logger.warning(f"[{self.name}] メモリ統合失敗: {e}")

    # ── 自己最適化 ────────────────────────────────────────────

    def optimize(self, current_prompt: str) -> str:
        """過去の学習記録に基づいて system prompt を自動改善."""
        self.logger.info(f"[{self.name}] 自己最適化を開始...")

        memory = ""
        if self._memory_path.exists():
            memory = self._memory_path.read_text(encoding="utf-8")

        if not memory.strip():
            self.logger.info(f"[{self.name}] 学習記録がないため最適化スキップ")
            return current_prompt

        user_message = f"""\
## Agent 名
{self.name}

## 現在の System Prompt
```
{current_prompt}
```

## 過去の学習記録（成功/失敗/教訓）
{memory}

上記の学習記録を分析し、同じ失敗を繰り返さず、成功パターンを強化するように
System Prompt を改善してください。"""

        try:
            raw = self.call_llm(OPTIMIZE_PROMPT, user_message)

            # ```prompt ... ``` または ``` ... ``` から抽出
            evolved = raw
            for marker in ["```prompt", "```"]:
                if marker in raw:
                    start = raw.index(marker) + len(marker)
                    end_idx = raw.find("```", start)
                    if end_idx != -1:
                        evolved = raw[start:end_idx].strip()
                        break

            # 保存
            PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
            self._evolved_prompt_path.write_text(
                f"<!-- 最適化日時: {datetime.now().strftime('%Y-%m-%d %H:%M')} -->\n{evolved}\n",
                encoding="utf-8",
            )

            self.logger.info(
                f"[{self.name}] プロンプト最適化完了 "
                f"({len(current_prompt)} → {len(evolved)} 文字) -> {self._evolved_prompt_path}"
            )
            return evolved

        except Exception as e:
            self.logger.warning(f"[{self.name}] 最適化失敗: {e}")
            return current_prompt

    # ── LLM 呼び出し ─────────────────────────────────────────

    # ── タイムアウト設定 ─────────────────────────────────────
    _MAX_TIMEOUT = 1800   # 絶対最大タイムアウト（秒）= 30分

    def call_llm(self, system: str, user_message: str) -> str:
        """Claude Code CLI を Popen で呼び出し、長時間生成を許容."""
        self.logger.info(f"[{self.name}] Claude Code CLI を呼び出し中...")

        # 過去の学習記録を system prompt に追加
        memory_context = self.load_memory()
        full_system = system + memory_context

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as sf:
            sf.write(full_system)
            system_file = sf.name

        env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}

        proc = subprocess.Popen(
            [
                "claude",
                "-p",
                "--system-prompt-file", system_file,
                "--output-format", "text",
                "--model", self.config.model,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/tmp",
            env=env,
        )

        start_time = time.time()
        stdout_data: list[str] = []

        def read_stdout() -> None:
            stdout_data.append(proc.stdout.read())

        try:
            proc.stdin.write(user_message)
            proc.stdin.close()

            reader = threading.Thread(target=read_stdout, daemon=True)
            reader.start()

            # タイムアウト監視 + 進捗表示
            is_tty = sys.stderr.isatty()
            frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            idx = 0
            last_log_time = start_time  # 非TTY用: 最終ログ出力時刻
            _LOG_INTERVAL = 30          # 非TTY用: ログ出力間隔（秒）

            while proc.poll() is None:
                elapsed = time.time() - start_time

                if elapsed > self._MAX_TIMEOUT:
                    proc.kill()
                    proc.wait()
                    raise RuntimeError(
                        f"[{self.name}] 最大タイムアウト ({self._MAX_TIMEOUT}秒超過)")

                if is_tty:
                    mins, secs = divmod(int(elapsed), 60)
                    frame = frames[idx % len(frames)]
                    sys.stderr.write(
                        f"\r  {frame} [{self.name}] 処理中... {mins:02d}:{secs:02d} ")
                    sys.stderr.flush()
                    idx += 1
                else:
                    # 非TTY: 定期的にログ出力（進捗が見えるように）
                    if time.time() - last_log_time >= _LOG_INTERVAL:
                        mins, secs = divmod(int(elapsed), 60)
                        self.logger.info(f"  [{self.name}] 生成中... {mins:02d}:{secs:02d} 経過")
                        last_log_time = time.time()

                time.sleep(0.5)

            reader.join(timeout=10)

            if is_tty:
                sys.stderr.write("\r" + " " * 50 + "\r")
                sys.stderr.flush()

        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            os.unlink(system_file)

        elapsed = time.time() - start_time

        if proc.returncode != 0:
            stderr_output = proc.stderr.read()
            raise RuntimeError(
                f"[{self.name}] Claude CLI failed (exit {proc.returncode}): "
                f"{stderr_output.strip() or 'Unknown error'}")

        text = (stdout_data[0] if stdout_data else "").strip()
        self.logger.info(f"[{self.name}] 応答完了 ({elapsed:.0f}秒, {len(text)}文字)")
        return text

    def call_llm_json(self, system: str, user_message: str, max_retries: int = 2) -> dict | list:
        """LLM を呼び出して JSON 応答を解析。失敗時は自動リトライ."""
        for attempt in range(max_retries + 1):
            raw = self.call_llm(system, user_message)
            try:
                return self._extract_json(raw)
            except ValueError as e:
                if attempt < max_retries:
                    self.logger.warning(
                        f"[{self.name}] JSON 解析失敗、リトライ {attempt + 1}/{max_retries}..."
                    )
                    user_message = (
                        f"{user_message}\n\n"
                        f"【重要】前回の出力は JSON 解析に失敗しました。以下を厳守してください：\n"
                        f"- description や acceptance_criteria 内の改行は \\n にエスケープ\n"
                        f"- ダブルクォート内のダブルクォートは \\\" にエスケープ\n"
                        f"- JSON のみ出力し、他のテキストは含めない\n"
                        f"- 各フィールドの値は短く簡潔に（20文字以内推奨）"
                    )
                else:
                    raise

    @staticmethod
    def _extract_json(text: str) -> Any:
        """LLM 応答から JSON を抽出。コードブロックと切り詰め修復に対応."""
        if "```json" in text:
            start = text.index("```json") + 7
            end_idx = text.find("```", start)
            text = text[start:end_idx].strip() if end_idx != -1 else text[start:].strip()
        elif "```" in text:
            start = text.index("```") + 3
            end_idx = text.find("```", start)
            text = text[start:end_idx].strip() if end_idx != -1 else text[start:].strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        repaired = _repair_truncated_json(text)
        try:
            return json.loads(repaired)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失敗（修復済み試行含む）: {e}\n先頭200文字: {text[:200]}")


def _repair_truncated_json(text: str) -> str:
    """切り詰められた JSON 文字列の修復を試行."""
    text = text.rstrip()

    bracket_stack = []
    in_string = False
    escape = False
    last_valid = 0

    for i, ch in enumerate(text):
        if escape:
            escape = False
            continue
        if ch == '\\' and in_string:
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            if not in_string:
                last_valid = i
            continue
        if in_string:
            continue
        if ch in '{[':
            bracket_stack.append(ch)
        elif ch in '}]':
            if bracket_stack:
                bracket_stack.pop()
            last_valid = i
        elif ch in ',':
            last_valid = i

    if in_string:
        text = text[:last_valid + 1]
        text = re.sub(r'[,:\s]+$', '', text)

    bracket_stack = []
    in_string = False
    escape = False
    for ch in text:
        if escape:
            escape = False
            continue
        if ch == '\\' and in_string:
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == '{':
            bracket_stack.append('}')
        elif ch == '[':
            bracket_stack.append(']')
        elif ch in '}]' and bracket_stack:
            bracket_stack.pop()

    text = re.sub(r',\s*$', '', text)

    for closer in reversed(bracket_stack):
        text += closer

    return text
