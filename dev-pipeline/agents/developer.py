"""Developer Agent - 要件に基づいてコードを実装."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from agents.base import BaseAgent
from core.config import Config
from core.paths import PathEscapeError, resolve_in_workspace
from core.models import (
    AnalysisResult,
    AllDevelopmentResults,
    CodeChange,
    DevelopmentResult,
    TaskStatus,
)

SYSTEM_PROMPT = """\
あなたはシニアソフトウェアエンジニアです。要件に基づいてコードを作成・修正してください。

既存コードが提供された場合：
- 既存コードをベースに修正し、コードスタイルを統一する
- action:"modify" で既存ファイルの修正を示し、修正後の完全な内容を提供
- action:"create" で新規ファイル作成を示す

ルール：
1. コードは簡潔・安全・そのまま実行可能
2. 各ファイルの完全な内容を提供

出力形式：まず JSON メタデータ、次にファイル内容を <<<FILE:パス>>> マーカーで区切って出力。

```json
{
  "status": "done",
  "changes": [
    {"file_path": "app.py", "action": "create", "description": "説明"},
    {"file_path": "utils.py", "action": "create", "description": "説明"}
  ],
  "notes": "簡単な説明"
}
```
<<<FILE:app.py>>>
import flask
app = flask.Flask(__name__)

@app.route("/")
def index():
    return "Hello"
<<<FILE:utils.py>>>
def helper():
    return True
<<<END>>>

重要：
- JSON には content フィールドを含めない（ファイル内容は <<<FILE:パス>>> の後に記述）
- <<<FILE:パス>>> のパスは JSON の file_path と一致させること
- ファイル内容はエスケープ不要、そのまま記述
- 最後に <<<END>>> を付けること
"""


class DeveloperAgent(BaseAgent):
    """コード実装 Agent：分析結果に基づいてコードを作成."""

    name = "developer"

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def run(self, analysis: AnalysisResult, codebase_summary: str = "") -> AllDevelopmentResults:
        """分析結果に基づいてサブタスクを順次実装."""
        self.logger.info(f"開発開始、全 {len(analysis.subtasks)} 件のサブタスク...")

        all_results = AllDevelopmentResults()
        completed_context = []

        total = len(analysis.subtasks)
        for idx, subtask in enumerate(analysis.subtasks):
            self.logger.info(f"  [{idx + 1}/{total}] サブタスク: [{subtask.id}] {subtask.title}")

            context_text = ""
            if completed_context:
                context_text = "\n\n完了済みファイル：\n"
                for ctx in completed_context:
                    context_text += f"- {', '.join(ctx['files'])}\n"

            # サブタスクに関連する既存ファイルの内容を読み取り
            existing_code = ""
            if codebase_summary:
                existing_code = self._read_relevant_files(subtask.description)

            user_message = f"""\
プロジェクト：{analysis.project_name}
技術スタック：{', '.join(analysis.tech_stack)}

サブタスク：{subtask.title}
説明：{subtask.description}
受入基準：{'; '.join(subtask.acceptance_criteria)}
{context_text}"""

            if existing_code:
                user_message += f"\n\n## 既存の関連コード\n{existing_code}\n"

            user_message += "\nコードを実装してください。JSON メタデータ + <<<FILE:パス>>> 形式で出力してください。"

            try:
                prompt = self.load_evolved_prompt(SYSTEM_PROMPT)
                metadata, file_contents = self._call_and_parse(prompt, user_message)

                changes = []
                for c in metadata.get("changes", []):
                    fp = c["file_path"]
                    changes.append(CodeChange(
                        file_path=fp,
                        action=c["action"],
                        description=c.get("description", ""),
                        content=file_contents.get(fp, ""),
                    ))

                result = DevelopmentResult(
                    subtask_id=subtask.id,
                    status=TaskStatus.DONE,
                    changes=changes,
                    notes=metadata.get("notes", ""),
                )

                self._apply_changes(changes)

                completed_context.append({
                    "files": [c.file_path for c in changes],
                })

            except Exception as e:
                self.logger.error(f"  サブタスク {subtask.id} 失敗: {e}")
                result = DevelopmentResult(
                    subtask_id=subtask.id,
                    status=TaskStatus.FAILED,
                    notes=str(e),
                )

            all_results.results.append(result)

        output_dir = self.config.output_dir / "developer"
        output_dir.mkdir(parents=True, exist_ok=True)
        all_results.save(output_dir / "development.json")

        md_path = output_dir / "development.md"
        md_path.write_text(self._format_md_report(all_results, analysis))
        self.logger.info(f"開発完了 -> {md_path}")

        done = sum(1 for r in all_results.results if r.status.value == "done")
        failed = sum(1 for r in all_results.results if r.status.value == "failed")
        self.reflect_and_learn(
            f"開発: {len(all_results.results)}タスク",
            f"完了:{done} 失敗:{failed} ファイル:{sum(len(r.changes) for r in all_results.results)}",
            success=(failed == 0),
        )

        return all_results

    def _call_and_parse(
        self, system: str, user_message: str, max_retries: int = 1,
    ) -> tuple[dict, dict[str, str]]:
        """LLM を呼び出し、構造化出力（JSON + <<<FILE:>>> ）を解析。失敗時リトライ."""
        for attempt in range(max_retries + 1):
            raw = self.call_llm(system, user_message)
            try:
                return self._parse_structured_output(raw)
            except ValueError as e:
                if attempt < max_retries:
                    self.logger.warning(
                        f"[{self.name}] 構造化出力の解析失敗、リトライ {attempt + 1}/{max_retries}..."
                    )
                    user_message = (
                        f"{user_message}\n\n"
                        f"【重要】前回の出力を解析できませんでした。以下を厳守してください：\n"
                        f"- まず ```json ... ``` で JSON メタデータを出力（content フィールドは不要）\n"
                        f"- 次に <<<FILE:ファイルパス>>> でファイル内容を区切って出力\n"
                        f"- 最後に <<<END>>> を付ける\n"
                        f"- ファイル内容はエスケープ不要、そのまま記述"
                    )
                else:
                    raise

    def _parse_structured_output(self, raw: str) -> tuple[dict, dict[str, str]]:
        """構造化出力を解析: JSON メタデータ + <<<FILE:パス>>> ファイル内容."""
        # JSON メタデータを抽出
        json_str = None
        json_match = re.search(r"```json\s*\n(.*?)\n```", raw, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()
        else:
            # ``` ... ``` フォールバック
            code_match = re.search(r"```\s*\n(\{.*?\})\n```", raw, re.DOTALL)
            if code_match:
                json_str = code_match.group(1).strip()
            else:
                # 直接 JSON オブジェクトを検索
                obj_match = re.search(r"\{[^{}]*\"changes\"[^{}]*\[.*?\][^{}]*\}", raw, re.DOTALL)
                if obj_match:
                    json_str = obj_match.group(0)

        if not json_str:
            raise ValueError(f"JSON メタデータが見つかりません。先頭200文字: {raw[:200]}")

        try:
            metadata = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON メタデータの解析失敗: {e}\n先頭200文字: {json_str[:200]}")

        # <<<FILE:パス>>> ブロックを抽出（複数パターン対応）
        file_contents: dict[str, str] = {}
        # パターン1: <<<FILE:path>>>
        file_pattern = r"<<<\s*FILE\s*:\s*(.*?)\s*>>>\n(.*?)(?=<<<\s*FILE\s*:|<<<\s*END\s*>>>|\Z)"
        for match in re.finditer(file_pattern, raw, re.DOTALL):
            file_path = match.group(1).strip()
            content = match.group(2).rstrip("\n")
            file_contents[file_path] = content

        # パターン2: --- FILE: path --- や === FILE: path ===
        if not file_contents:
            alt_pattern = r"(?:---|\*\*\*|===)\s*FILE\s*:\s*(.*?)\s*(?:---|\*\*\*|===)\n(.*?)(?=(?:---|\*\*\*|===)\s*FILE\s*:|(?:---|\*\*\*|===)\s*END\s*(?:---|\*\*\*|===)|\Z)"
            for match in re.finditer(alt_pattern, raw, re.DOTALL | re.IGNORECASE):
                file_path = match.group(1).strip()
                content = match.group(2).rstrip("\n")
                file_contents[file_path] = content

        # 旧形式フォールバック: JSON 内の content フィールド
        if not file_contents:
            for c in metadata.get("changes", []):
                if c.get("content"):
                    file_contents[c["file_path"]] = c["content"]

        # ファイルパスのマッチング: JSON の file_path と FILE マーカーの差異を吸収
        if file_contents:
            expected_paths = {c["file_path"] for c in metadata.get("changes", [])}
            matched = set(file_contents.keys()) & expected_paths
            if matched != expected_paths:
                # ベースネームで再マッチング
                basename_map = {}
                for fp, content in list(file_contents.items()):
                    base = Path(fp).name
                    basename_map[base] = content
                for c in metadata.get("changes", []):
                    fp = c["file_path"]
                    if fp not in file_contents:
                        base = Path(fp).name
                        if base in basename_map:
                            file_contents[fp] = basename_map[base]
                            self.logger.debug(f"    パス補正: {base} -> {fp}")

        if file_contents:
            self.logger.info(f"    解析: JSON OK, {len(file_contents)}ファイル抽出")
        else:
            self.logger.warning(f"    解析: JSON OK, ファイル内容なし（LLM が content を JSON 内に記述した可能性）")

        return metadata, file_contents

    @staticmethod
    def _format_md_report(all_results: AllDevelopmentResults, analysis: AnalysisResult) -> str:
        """Markdown形式の開発レポートを生成."""
        subtask_map = {st.id: st.title for st in analysis.subtasks}

        lines = ["# 開発レポート", ""]

        for result in all_results.results:
            title = subtask_map.get(result.subtask_id, result.subtask_id)
            status_icon = "✅" if result.status == TaskStatus.DONE else "❌"
            lines.extend([f"## {status_icon} {result.subtask_id}: {title}", ""])

            if result.changes:
                lines.extend([
                    "**変更ファイル：**",
                    "",
                    "| ファイル | 操作 | 説明 |",
                    "|---------|------|------|",
                ])
                for change in result.changes:
                    lines.append(f"| `{change.file_path}` | {change.action} | {change.description} |")
                lines.append("")

            if result.notes:
                lines.extend([f"**備考：** {result.notes}", ""])

            lines.extend(["---", ""])

        timestamp = all_results.results[-1].timestamp if all_results.results else ""
        if timestamp:
            lines.append(f"*生成日時: {timestamp}*")

        return "\n".join(lines)

    def _read_relevant_files(self, description: str) -> str:
        """workspace 内のサブタスクに関連するコードファイルを読み取り."""
        ws = self.config.workspace
        sections = []
        total_chars = 0
        max_chars = 2000

        for f in sorted(ws.rglob("*")):
            if not f.is_file():
                continue
            if ".git" in f.parts or "__pycache__" in f.parts or "node_modules" in f.parts:
                continue
            if f.suffix not in {".py", ".js", ".ts", ".go", ".rs", ".java", ".rb",
                                ".html", ".css", ".yaml", ".yml", ".toml", ".json",
                                ".sh", ".sql", ".env.example", ".cfg", ".ini"}:
                continue

            try:
                content = f.read_text()
            except Exception:
                continue

            if total_chars + len(content) > max_chars:
                content = content[:max_chars - total_chars] + "\n... (truncated)"

            rel = f.relative_to(ws)
            sections.append(f"### {rel}\n```\n{content}\n```")
            total_chars += len(content)

            if total_chars >= max_chars:
                break

        return "\n\n".join(sections)

    def _apply_changes(self, changes: list[CodeChange]) -> None:
        """コード変更を workspace ディレクトリに書き込み.

        パスは LLM 出力由来なので workspace 境界を必ず検証する。
        1件が不正でも他の変更は適用する（拒否した事実はログに残す）。
        """
        for change in changes:
            try:
                file_path = resolve_in_workspace(self.config.workspace, change.file_path)
            except PathEscapeError as e:
                self.logger.error(f"    拒否: {change.file_path} ({e})")
                continue
            if change.action == "delete":
                if file_path.exists():
                    file_path.unlink()
                    self.logger.info(f"    削除: {change.file_path}")
            else:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(change.content, encoding="utf-8")
                self.logger.info(f"    書込: {change.file_path}")
