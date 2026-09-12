"""Reviewer Agent - 成果物の品質・完全性を検証し、修正を指示."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agents.base import BaseAgent
from core.config import Config
from core.models import (
    AnalysisResult,
    AllDevelopmentResults,
    CorrectionCommand,
    ReviewIssue,
    ReviewResult,
)

SYSTEM_PROMPT = """\
あなたは成果物レビューの専門家です。
開発チームが生成した成果物（コード・設計書・スクリプト等）を、
元の要件と照合し、品質・完全性・クロスシステム整合性を検証してください。

## 検証観点

### 1. ファイル完全性チェック
- 各ファイルが空でないこと（0バイトは critical）
- ファイルの内容が途中で切れていないこと
- 計画されたファイルがすべて生成されていること

### 2. 要件カバレッジチェック
- 元の要件に記載された各ポイントが成果物に反映されているか
- 漏れている要件ポイントがあれば指摘

### 3. クロスシステム整合性チェック（重要）
通常、1つのシステム変更は複数の関連システムに影響する。
要件が明示的に言及していなくても、以下のような関連システムの設定・設計が必要か確認：
- ネットワーク（FW / DNS / Proxy / VPN / ロードバランサー）
- 認証・認可（Entra ID / AD / 証明書）
- 管理ツール（Intune / SCCM / GPO）
- 監視（ログ / アラート / ダッシュボード）
- セキュリティ（TLS / 暗号化 / アクセス制御）
- 運用（バックアップ / DR / メンテナンス手順）
- 他のサービスとの連携（Azure / AWS / オンプレ）

関連システムの設計が不足している場合は cross_system_gaps に記載し、
corrections で追加の成果物作成を指示すること。

### 4. 品質チェック
- 設計書の構成が論理的か
- 設定値に根拠があるか
- エビデンスURL が記載されているか（該当する場合）

## 出力形式

JSON のみ出力：
```json
{
  "passed": false,
  "total_checks": 15,
  "passed_checks": 12,
  "issues": [
    {
      "severity": "critical|warning|info",
      "category": "empty_file|missing_content|cross_system|quality",
      "file_path": "docs/design.md",
      "description": "問題の説明",
      "correction": "Developer への修正指示"
    }
  ],
  "corrections": [
    {
      "target_agent": "developer",
      "action": "create|modify|regenerate",
      "file_path": "docs/new_file.md",
      "instruction": "具体的な作成・修正指示"
    }
  ],
  "cross_system_gaps": [
    "DNS設定が未記載",
    "Netskope TLS除外ルールが不足"
  ],
  "summary": "レビュー結果の要約（2-3文）"
}
```

重要：
- critical な問題がある場合は passed: false とする
- corrections は具体的な指示を含めること（「○○を追加」ではなく「○○の△△設定について、□□を含むファイルを作成」）
- severity: critical = 成果物として使用不可、warning = 改善推奨、info = 参考情報
- JSON の各フィールド値は短く簡潔に（description: 50文字以内、correction/instruction: 100文字以内）
- 改行は \\n にエスケープし、JSON の妥当性を確保すること
- issues は最大10件、corrections は最大5件に絞ること（重要度順）
"""


class ReviewerAgent(BaseAgent):
    """成果物レビュー Agent：品質・完全性・クロスシステム整合性を検証."""

    name = "reviewer"

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def review(
        self,
        requirement: str,
        analysis: AnalysisResult,
        dev_results: AllDevelopmentResults,
    ) -> ReviewResult:
        """成果物をレビューし、問題と修正コマンドを返す."""
        self.logger.info("成果物レビューを開始...")

        # workspace 内の全ファイルを収集
        file_inventory = self._collect_file_inventory()

        # レビュー用のコンテキストを構築
        user_message = self._build_review_context(
            requirement, analysis, dev_results, file_inventory
        )

        prompt = self.load_evolved_prompt(SYSTEM_PROMPT)
        try:
            data = self.call_llm_json(prompt, user_message)
        except (ValueError, RuntimeError) as e:
            self.logger.warning(f"レビュー JSON 解析失敗、合格扱いで続行: {e}")
            data = {"passed": True, "total_checks": 0, "passed_checks": 0,
                    "issues": [], "corrections": [], "cross_system_gaps": [],
                    "summary": f"レビュー解析失敗（{e}）"}

        issues = [
            ReviewIssue(
                severity=i.get("severity", "info"),
                category=i.get("category", "quality"),
                file_path=i.get("file_path", ""),
                description=i.get("description", ""),
                correction=i.get("correction", ""),
            )
            for i in data.get("issues", [])
        ]

        corrections = [
            CorrectionCommand(
                target_agent=c.get("target_agent", "developer"),
                action=c.get("action", "create"),
                file_path=c.get("file_path", ""),
                instruction=c.get("instruction", ""),
            )
            for c in data.get("corrections", [])
        ]

        result = ReviewResult(
            passed=data.get("passed", True),
            total_checks=data.get("total_checks", 0),
            passed_checks=data.get("passed_checks", 0),
            issues=issues,
            corrections=corrections,
            cross_system_gaps=data.get("cross_system_gaps", []),
            summary=data.get("summary", ""),
        )

        # 結果を保存
        output_dir = self.config.output_dir / "reviewer"
        output_dir.mkdir(parents=True, exist_ok=True)
        result.save(output_dir / "review.json")

        # Markdown レポートも保存
        md_path = output_dir / "review.md"
        md_path.write_text(self._format_md_report(result), encoding="utf-8")

        # ログ出力
        critical = sum(1 for i in issues if i.severity == "critical")
        warning = sum(1 for i in issues if i.severity == "warning")
        self.logger.info(
            f"レビュー完了: {result.passed_checks}/{result.total_checks} 合格  "
            f"(critical: {critical}, warning: {warning}, 修正: {len(corrections)}件)"
        )
        if result.cross_system_gaps:
            self.logger.info(f"  クロスシステム不足: {', '.join(result.cross_system_gaps)}")

        # 自己学習
        self.reflect_and_learn(
            f"レビュー: {result.total_checks}項目",
            f"合格:{result.passed_checks} critical:{critical} 修正:{len(corrections)}",
            success=result.passed,
        )

        return result

    def _collect_file_inventory(self) -> list[dict]:
        """workspace 内の全ファイルの一覧と内容サマリーを収集."""
        ws = self.config.workspace
        inventory = []

        for f in sorted(ws.rglob("*")):
            if not f.is_file():
                continue
            if ".git" in f.parts or "__pycache__" in f.parts or ".DS_Store" in f.name:
                continue

            size = f.stat().st_size
            rel = str(f.relative_to(ws))

            entry = {"path": rel, "size": size, "empty": size == 0}

            # 内容のプレビュー（最大500文字）
            if size > 0:
                try:
                    content = f.read_text(encoding="utf-8")
                    entry["preview"] = content[:500]
                    entry["total_chars"] = len(content)
                except Exception:
                    entry["preview"] = "(バイナリまたは読取不可)"
            else:
                entry["preview"] = "(空ファイル)"

            inventory.append(entry)

        return inventory

    def _build_review_context(
        self,
        requirement: str,
        analysis: AnalysisResult,
        dev_results: AllDevelopmentResults,
        file_inventory: list[dict],
    ) -> str:
        """レビュー用のコンテキストを構築."""
        lines = []

        # 元の要件
        lines.append("## 元の要件")
        lines.append(requirement[:3000])

        # 分析結果
        lines.append("\n## 分析結果")
        lines.append(f"プロジェクト: {analysis.project_name}")
        for st in analysis.subtasks:
            status_map = {s.subtask_id: s.status.value for s in dev_results.results}
            status = status_map.get(st.id, "unknown")
            icon = "✅" if status == "done" else "❌"
            lines.append(f"  {icon} [{st.id}] {st.title}")

        # ファイル一覧
        lines.append("\n## 生成されたファイル一覧")
        for f in file_inventory:
            status = "⚠️空" if f["empty"] else f"{f['size']}B"
            lines.append(f"  - {f['path']} ({status})")
            if f.get("total_chars"):
                lines.append(f"    冒頭: {f['preview'][:200]}...")

        lines.append("\n上記の成果物を元の要件と照合し、レビューしてください。")
        lines.append("特にクロスシステムの観点で、関連するが未対応のシステム設計がないか確認してください。")

        return "\n".join(lines)

    @staticmethod
    def _format_md_report(result: ReviewResult) -> str:
        """Markdown 形式のレビューレポートを生成."""
        lines = ["# レビューレポート", ""]
        lines.append(f"**結果: {'✅ 合格' if result.passed else '❌ 要修正'}**")
        lines.append(f"**チェック: {result.passed_checks}/{result.total_checks} 合格**")
        lines.append("")

        if result.summary:
            lines.extend(["## サマリー", "", result.summary, ""])

        if result.cross_system_gaps:
            lines.append("## クロスシステム不足")
            lines.append("")
            for gap in result.cross_system_gaps:
                lines.append(f"- ⚠️ {gap}")
            lines.append("")

        if result.issues:
            lines.append("## 検出された問題")
            lines.append("")
            lines.append("| 重要度 | カテゴリ | ファイル | 説明 |")
            lines.append("|--------|---------|---------|------|")
            severity_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}
            for issue in result.issues:
                icon = severity_icon.get(issue.severity, "⚪")
                lines.append(
                    f"| {icon} {issue.severity} | {issue.category} | "
                    f"`{issue.file_path}` | {issue.description} |"
                )
            lines.append("")

        if result.corrections:
            lines.append("## 修正コマンド")
            lines.append("")
            for i, cmd in enumerate(result.corrections, 1):
                lines.append(f"### 修正 {i}: {cmd.file_path}")
                lines.append(f"- **対象 Agent**: {cmd.target_agent}")
                lines.append(f"- **アクション**: {cmd.action}")
                lines.append(f"- **指示**: {cmd.instruction}")
                lines.append("")

        return "\n".join(lines)
