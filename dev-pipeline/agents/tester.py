"""Tester Agent - コードテスト・レポート生成・脆弱性検出."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agents.base import BaseAgent
from core.config import Config
from core.paths import PathEscapeError, resolve_in_workspace
from core.models import (
    AnalysisResult,
    AllDevelopmentResults,
    TestReport,
    TestCase,
    Vulnerability,
    TaskStatus,
    Severity,
)

SYSTEM_PROMPT = """\
あなたはテストエンジニア兼セキュリティ監査の専門家です。コードの機能テストとセキュリティ監査を行ってください。

JSON で出力（簡潔に、テストケース最大10件、脆弱性最大5件）：
```json
{
  "total_tests": 5,
  "passed": 4,
  "failed": 1,
  "test_cases": [
    {"id": "tc-1", "name": "名前", "description": "説明", "status": "done", "error_message": ""}
  ],
  "vulnerabilities": [
    {"id": "vuln-1", "title": "タイトル", "severity": "high", "location": "file:line", "description": "説明", "recommendation": "推奨対策"}
  ],
  "summary": "一文で総括"
}
```

重要：status は done（合格）または failed（不合格）。severity は critical/high/medium/low/info。
各フィールド値は簡潔に（20文字以内）。JSON のみ出力し、他のテキストは不要。
"""


class TesterAgent(BaseAgent):
    """テスト Agent：テスト実行・レポート生成・脆弱性スキャン."""

    name = "tester"

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def run(
        self,
        analysis: AnalysisResult,
        dev_results: AllDevelopmentResults,
    ) -> TestReport:
        """開発結果に対してテストとセキュリティ監査を実施."""
        self.logger.info("テスト・セキュリティ監査を開始...")

        # コード収集：workspace から優先、dev_results にフォールバック
        code_contents = self._collect_code_from_workspace()
        if not code_contents:
            code_contents = self._collect_code_from_results(dev_results)
        if not code_contents:
            self.logger.warning("テスト対象のコードがありません")
            return TestReport(summary="テスト対象のコードがありません")

        criteria_text = self._build_criteria_text(analysis)

        user_message = f"""\
プロジェクト：{analysis.project_name}

## 要件と受入基準
{criteria_text}

## コードファイルの内容
{code_contents}

以上のコードに対して以下を実施してください：
1. 機能テスト（受入基準に基づく）
2. コード品質レビュー
3. セキュリティ脆弱性スキャン

完全なテストレポートを出力してください。"""

        prompt = self.load_evolved_prompt(SYSTEM_PROMPT)
        data = self.call_llm_json(prompt, user_message)

        report = TestReport(
            total_tests=data.get("total_tests", 0),
            passed=data.get("passed", 0),
            failed=data.get("failed", 0),
            test_cases=[
                TestCase(
                    id=tc.get("id", f"tc-{i+1}"),
                    name=tc.get("name", "未命名テスト"),
                    description=tc.get("description", ""),
                    status=TaskStatus.DONE if tc.get("status") in ("done", "pass", "passed") else TaskStatus.FAILED,
                    error_message=tc.get("error_message", tc.get("error", "")),
                )
                for i, tc in enumerate(data.get("test_cases", []))
            ],
            vulnerabilities=[
                Vulnerability(
                    id=v.get("id", f"vuln-{i+1}"),
                    title=v.get("title", v.get("name", "未命名脆弱性")),
                    severity=Severity(v.get("severity", "info")),
                    location=v.get("location", v.get("file", "")),
                    description=v.get("description", ""),
                    recommendation=v.get("recommendation", v.get("fix", "")),
                )
                for i, v in enumerate(data.get("vulnerabilities", []))
            ],
            summary=data.get("summary", ""),
        )

        # テストレポートを保存
        output_dir = self.config.output_dir / "tester"
        output_dir.mkdir(parents=True, exist_ok=True)
        report.save(output_dir / "test_report.json")

        readable_path = output_dir / "test_report.md"
        readable_path.write_text(self._format_readable_report(report))

        self.logger.info(f"テスト完了 -> {readable_path}")
        self.logger.info(
            f"  合格: {report.passed}/{report.total_tests}  "
            f"脆弱性: {len(report.vulnerabilities)}"
        )

        self.reflect_and_learn(
            f"テスト: {report.total_tests}件",
            f"合格:{report.passed} 失敗:{report.failed} 脆弱性:{len(report.vulnerabilities)}",
            success=(report.failed == 0),
        )

        return report

    def _collect_code_from_workspace(self) -> str:
        """workspace ディレクトリから全コードファイルを読み取り."""
        ws = self.config.workspace
        sections = []
        total_chars = 0
        max_chars = 3000

        code_suffixes = {".py", ".js", ".ts", ".go", ".rs", ".java", ".rb",
                         ".html", ".css", ".sh", ".sql", ".yaml", ".yml"}

        for f in sorted(ws.rglob("*")):
            if not f.is_file():
                continue
            if ".git" in f.parts or "__pycache__" in f.parts or "node_modules" in f.parts:
                continue
            if f.suffix not in code_suffixes:
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

    def _collect_code_from_results(self, dev_results: AllDevelopmentResults) -> str:
        """開発結果からコードを収集（フォールバック用）."""
        sections = []
        for result in dev_results.results:
            for change in result.changes:
                if change.action == "delete":
                    continue
                # パスは LLM 出力由来。workspace 外を読ませない（任意ファイル読み取り防止）
                try:
                    disk_path = resolve_in_workspace(self.config.workspace, change.file_path)
                except PathEscapeError as e:
                    self.logger.error(f"  読取拒否: {change.file_path} ({e})")
                    continue
                if disk_path.exists():
                    content = disk_path.read_text(encoding="utf-8")
                else:
                    content = change.content
                sections.append(f"### {change.file_path}\n```\n{content}\n```")
        return "\n\n".join(sections)

    def _build_criteria_text(self, analysis: AnalysisResult) -> str:
        """受入基準テキストを構築."""
        lines = []
        for st in analysis.subtasks:
            lines.append(f"### {st.id}: {st.title}")
            for ac in st.acceptance_criteria:
                lines.append(f"  - {ac}")
        return "\n".join(lines)

    @staticmethod
    def _format_readable_report(report: TestReport) -> str:
        """Markdown形式のテストレポートを生成."""
        pass_rate = f"{report.passed / report.total_tests * 100:.1f}%" if report.total_tests > 0 else "N/A"
        lines = [
            "# テストレポート",
            "",
            "## 概況",
            "",
            "| 項目 | 値 |",
            "|------|-----|",
            f"| 総テスト数 | {report.total_tests} |",
            f"| 合格 | {report.passed} |",
            f"| 不合格 | {report.failed} |",
            f"| 合格率 | {pass_rate} |",
            "",
            "## テストケース",
            "",
            "| ID | テスト名 | 説明 | 結果 | エラー |",
            "|----|---------|------|------|--------|",
        ]

        for tc in report.test_cases:
            status = "✅ PASS" if tc.status == TaskStatus.DONE else "❌ FAIL"
            error = tc.error_message or ""
            lines.append(f"| {tc.id} | {tc.name} | {tc.description} | {status} | {error} |")

        lines.append("")

        if report.vulnerabilities:
            lines.extend(["## セキュリティ脆弱性", ""])
            for v in report.vulnerabilities:
                lines.extend([
                    f"### [{v.severity.value.upper()}] {v.title}",
                    "",
                    f"- **場所：** `{v.location}`",
                    f"- **説明：** {v.description}",
                    f"- **推奨対策：** {v.recommendation}",
                    "",
                ])

        lines.extend([
            "## 総括",
            "",
            report.summary,
            "",
            "---",
            "",
            f"*生成日時: {report.timestamp}*",
        ])

        return "\n".join(lines)
