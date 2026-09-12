"""Investigator Agent - 事前コード調査・テスト後問題調査."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agents.base import BaseAgent
from core.config import Config
from core.models import (
    InvestigationReport,
    FileInfo,
    PostTestInvestigation,
    IssueCause,
    TestReport,
)

# ── 事前調査プロンプト ────────────────────────────────────────

PRE_INVESTIGATION_PROMPT = """\
あなたはシニアコードリサーチャーです。既存のコードベースを調査し、以下を分析してください：

1. プロジェクトの概要と目的
2. 使用技術スタック
3. アーキテクチャ構成
4. 重要なファイルとその役割
5. 外部依存関係
6. 注意すべき点

JSON 形式で出力（簡潔に）：
```json
{
  "project_overview": "プロジェクト概要（1-2文）",
  "tech_stack": ["Python", "Flask"],
  "architecture": "アーキテクチャの簡単な説明",
  "key_files": [
    {"path": "app.py", "description": "メインエントリー", "language": "python"}
  ],
  "dependencies": ["flask>=2.0", "requests"],
  "notes": "開発時の注意事項"
}
```

key_files は最大10件。各フィールドは簡潔に。JSON のみ出力。
"""

# ── 要件調査プロンプト（コードなし、技術リサーチ）────────────────

REQUIREMENT_INVESTIGATION_PROMPT = """\
あなたはシニアITコンサルタント兼テクニカルリサーチャーです。
ユーザーの要件について、技術的な調査・分析を行い、詳細なレポートを Markdown で出力してください。

レポートに含めるべき内容：
- エグゼクティブサマリー
- 実現性の評価（技術的に可能か、制約・リスクは何か）
- 実現イメージ（アーキテクチャ概要、構成図をテキストで表現）
- 具体的な製品・サービスの比較（コスト、機能、制約）
- 推奨案と次のステップ
- 参考URL（製品公式ドキュメント等のエビデンス）

出力形式：Markdown テキストのみ（JSON不要）。見出し・表・箇条書きを使って読みやすく構成すること。
"""

# ── テスト後問題調査プロンプト ────────────────────────────────

POST_INVESTIGATION_PROMPT = """\
あなたはシニアデバッグエンジニアです。テストで検出された不具合と脆弱性の原因を調査してください。

各問題について：
1. 根本原因を特定
2. 影響を受けるファイルを列挙
3. 具体的な修正方針を提案

JSON 形式で出力（簡潔に）：
```json
{
  "issue_causes": [
    {
      "issue_id": "tc-1 または vuln-1",
      "title": "問題のタイトル",
      "root_cause": "根本原因の説明",
      "affected_files": ["app.py"],
      "fix_suggestion": "具体的な修正方針"
    }
  ],
  "summary": "全体の総括（1文）"
}
```

各フィールドは簡潔に。JSON のみ出力。
"""


class InvestigatorAgent(BaseAgent):
    """調査 Agent：事前コード調査とテスト後問題調査を担当."""

    name = "investigator"

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    # ── 事前調査（分析前） ──────────────────────────────────

    def investigate_codebase(self) -> InvestigationReport:
        """既存コードベースを調査し、詳細なレポートを生成."""
        self.logger.info("事前コード調査を開始...")

        code_summary = self._scan_all_code()
        if not code_summary:
            self.logger.info("  コードなし、事前調査をスキップ")
            return InvestigationReport(project_overview="新規プロジェクト（既存コードなし）")

        user_message = f"以下のコードベースを調査してください：\n\n{code_summary}"
        prompt = self.load_evolved_prompt(PRE_INVESTIGATION_PROMPT)
        data = self.call_llm_json(prompt, user_message)

        report = InvestigationReport(
            project_overview=data.get("project_overview", ""),
            tech_stack=data.get("tech_stack", []),
            architecture=data.get("architecture", ""),
            key_files=[
                FileInfo(
                    path=f.get("path", ""),
                    description=f.get("description", ""),
                    language=f.get("language", ""),
                )
                for f in data.get("key_files", [])
            ],
            dependencies=data.get("dependencies", []),
            notes=data.get("notes", ""),
        )

        output_path = self.config.output_dir / "investigator" / "investigation.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        report.save(output_path)

        readable_path = self.config.output_dir / "investigator" / "investigation.md"
        readable_path.write_text(self._format_investigation_report(report), encoding="utf-8")

        self.logger.info(f"事前調査完了 -> {readable_path}")

        self.reflect_and_learn(
            f"コード調査: {report.project_overview}",
            f"技術スタック: {report.tech_stack}, ファイル: {len(report.key_files)}件",
            success=True,
        )

        return report

    # ── 要件調査（コードなし、技術リサーチ） ────────────────────

    def investigate_requirement(self, requirement: str) -> str:
        """要件に基づく技術調査レポートを生成（Investigator 単独実行用）."""
        self.logger.info("要件調査を開始...")

        prompt = self.load_evolved_prompt(REQUIREMENT_INVESTIGATION_PROMPT)
        report_text = self.call_llm(prompt, requirement)

        output_dir = self.config.output_dir / "investigator"
        output_dir.mkdir(parents=True, exist_ok=True)

        report_path = output_dir / "investigation.md"
        report_path.write_text(report_text, encoding="utf-8")

        self.logger.info(f"要件調査完了 -> {report_path}")

        self.reflect_and_learn(
            f"要件調査: {requirement[:200]}",
            f"レポート生成完了（{len(report_text)}文字）",
            success=True,
        )

        return report_text

    # ── テスト後問題調査 ────────────────────────────────────

    def investigate_issues(self, test_report: TestReport) -> PostTestInvestigation:
        """テスト結果の不具合・脆弱性の原因を調査."""
        # 失敗したテストと脆弱性を収集
        issues = []
        for tc in test_report.test_cases:
            if tc.status.value == "failed":
                issues.append(f"[不合格] {tc.id}: {tc.name} - {tc.error_message}")
        for v in test_report.vulnerabilities:
            issues.append(f"[脆弱性 {v.severity.value}] {v.id}: {v.title} - {v.description} ({v.location})")

        if not issues:
            self.logger.info("  問題なし、テスト後調査をスキップ")
            return PostTestInvestigation(summary="問題は検出されませんでした")

        self.logger.info(f"テスト後問題調査を開始（{len(issues)} 件）...")

        # 関連コードを収集
        code_summary = self._scan_all_code()

        user_message = f"""\
## 検出された問題
{chr(10).join(issues)}

## コードベース
{code_summary}

上記の問題について原因を調査し、修正方針を提案してください。"""

        prompt = self.load_evolved_prompt(POST_INVESTIGATION_PROMPT)
        data = self.call_llm_json(prompt, user_message)

        investigation = PostTestInvestigation(
            issue_causes=[
                IssueCause(
                    issue_id=ic.get("issue_id", f"issue-{i+1}"),
                    title=ic.get("title", ""),
                    root_cause=ic.get("root_cause", ""),
                    affected_files=ic.get("affected_files", []),
                    fix_suggestion=ic.get("fix_suggestion", ""),
                )
                for i, ic in enumerate(data.get("issue_causes", []))
            ],
            summary=data.get("summary", ""),
        )

        output_path = self.config.output_dir / "investigator" / "post_investigation.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        investigation.save(output_path)

        # 可読レポートも生成
        readable_path = self.config.output_dir / "investigator" / "post_investigation.md"
        readable_path.write_text(self._format_readable_report(investigation), encoding="utf-8")

        self.logger.info(f"テスト後調査完了 -> {readable_path}")

        return investigation

    # ── 内部ヘルパー ────────────────────────────────────────

    def _scan_all_code(self) -> str:
        """workspace 内の全コードファイルを読み取って概要を生成."""
        ws = self.config.workspace
        sections = []
        total_chars = 0
        max_chars = 3000

        code_suffixes = {
            ".py", ".js", ".ts", ".go", ".rs", ".java", ".rb",
            ".html", ".css", ".sh", ".sql", ".yaml", ".yml",
            ".json", ".toml", ".cfg", ".ini",
        }

        for f in sorted(ws.rglob("*")):
            if not f.is_file():
                continue
            if ".git" in f.parts or "__pycache__" in f.parts or "node_modules" in f.parts:
                continue
            if f.suffix not in code_suffixes:
                continue

            try:
                content = f.read_text(encoding="utf-8")
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

    @staticmethod
    def _format_investigation_report(report: InvestigationReport) -> str:
        """Markdown形式の事前調査レポートを生成."""
        lines = [
            "# コード調査レポート",
            "",
            "## プロジェクト概要",
            "",
            report.project_overview,
            "",
        ]

        if report.tech_stack:
            lines.extend(["## 技術スタック", ""])
            for tech in report.tech_stack:
                lines.append(f"- {tech}")
            lines.append("")

        if report.architecture:
            lines.extend(["## アーキテクチャ", "", report.architecture, ""])

        if report.key_files:
            lines.extend([
                "## 主要ファイル",
                "",
                "| ファイル | 言語 | 説明 |",
                "|---------|------|------|",
            ])
            for f in report.key_files:
                lang = f.language or "-"
                lines.append(f"| `{f.path}` | {lang} | {f.description} |")
            lines.append("")

        if report.dependencies:
            lines.extend(["## 依存関係", ""])
            for dep in report.dependencies:
                lines.append(f"- `{dep}`")
            lines.append("")

        if report.notes:
            lines.extend(["## 注意事項", "", report.notes, ""])

        lines.extend(["---", "", f"*生成日時: {report.timestamp}*"])

        return "\n".join(lines)

    @staticmethod
    def _format_readable_report(investigation: PostTestInvestigation) -> str:
        """Markdown形式のテスト後調査レポートを生成."""
        lines = ["# 問題調査レポート", ""]

        for ic in investigation.issue_causes:
            affected = ", ".join(f"`{f}`" for f in ic.affected_files)
            lines.extend([
                f"## [{ic.issue_id}] {ic.title}",
                "",
                f"**根本原因：** {ic.root_cause}",
                "",
                f"**影響ファイル：** {affected}",
                "",
                f"**修正方針：** {ic.fix_suggestion}",
                "",
                "---",
                "",
            ])

        lines.extend([
            "## 総括",
            "",
            investigation.summary,
            "",
            "---",
            "",
            f"*生成日時: {investigation.timestamp}*",
        ])

        return "\n".join(lines)
