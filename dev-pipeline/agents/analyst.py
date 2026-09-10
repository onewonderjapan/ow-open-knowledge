"""Analyst Agent - 要件分析・タスク分割."""

from __future__ import annotations

from typing import Any

from agents.base import BaseAgent
from core.config import Config
from core.models import AnalysisResult, SubTask, Priority

SYSTEM_PROMPT = """\
あなたはシニア要件アナリストです。ユーザーの要件を実行可能なサブタスクに分割してください。

既存コード構造が提供された場合：
- 既存プロジェクトの技術スタックとアーキテクチャを理解する
- ゼロからではなく、既存コードに基づいて修正計画を立てる
- 新規ファイルと既存ファイルの修正を明記する

重要：各サブタスクについて、実行者（executor）を必ず判定してください：
- "ai"：AI Agent が自動で完了できるタスク（コード生成、ドキュメント作成、テスト等）
- "human"：人間が手動で行う必要があるタスク（外部サービス契約、物理作業、承認、本番デプロイ、アカウント作成、機密情報の入力等）
- "hybrid"：AI が下書き・提案を作成し、人間が確認・実行するタスク（設計レビュー、コスト承認、顧客への提案等）

executor_reason には、なぜその実行者が適切かを簡潔に説明してください。

JSON 形式で出力：
```json
{
  "project_name": "プロジェクト名",
  "summary": "要件の概要（1文）",
  "tech_stack": ["Python", "Flask"],
  "subtasks": [
    {
      "id": "task-1",
      "title": "サブタスクのタイトル",
      "description": "実装内容",
      "priority": "high|medium|low",
      "executor": "ai|human|hybrid",
      "executor_reason": "AIが自動生成可能 / 人間の承認が必要 等",
      "acceptance_criteria": ["基準1", "基準2"],
      "dependencies": []
    }
  ]
}
```

重要な制約：
- サブタスク数は 3〜5 個に抑える
- 各受入基準は簡潔に（10文字以内）
- description は簡潔に記述
- executor の判定は現実的に行うこと（AIにできないことをAIに割り当てない）
"""


class AnalystAgent(BaseAgent):
    """要件分析 Agent：要件を受け取り、構造化されたサブタスクリストを出力."""

    name = "analyst"

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def run(self, requirement: str, codebase_summary: str = "") -> AnalysisResult:
        """要件を分析してサブタスクに分割."""
        self.logger.info("要件分析を開始...")

        user_message = "以下の要件を分析し、サブタスクに分割してください：\n\n"
        if codebase_summary:
            user_message += f"## 既存コードベース\n{codebase_summary}\n\n## 要件\n"
        user_message += requirement

        prompt = self.load_evolved_prompt(SYSTEM_PROMPT)
        data = self.call_llm_json(prompt, user_message)

        result = AnalysisResult(
            project_name=data["project_name"],
            summary=data["summary"],
            tech_stack=data.get("tech_stack", []),
            subtasks=[
                SubTask(
                    id=st["id"],
                    title=st["title"],
                    description=st["description"],
                    priority=Priority(st["priority"]),
                    executor=st.get("executor", "ai"),
                    executor_reason=st.get("executor_reason", ""),
                    acceptance_criteria=st.get("acceptance_criteria", []),
                    dependencies=st.get("dependencies", []),
                )
                for st in data["subtasks"]
            ],
        )

        output_dir = self.config.output_dir / "analyst"
        output_dir.mkdir(parents=True, exist_ok=True)
        result.save(output_dir / "analysis.json")

        md_path = output_dir / "analysis.md"
        md_path.write_text(self._format_md_report(result))
        self.logger.info(
            f"要件分析完了：{len(result.subtasks)} 件のサブタスク -> {md_path}"
        )

        executors = [st.executor for st in result.subtasks]
        self.reflect_and_learn(
            f"要件分析: {result.project_name} ({len(result.subtasks)}タスク)",
            f"AI:{executors.count('ai')} Human:{executors.count('human')} Hybrid:{executors.count('hybrid')}",
            success=True,
        )

        return result

    @staticmethod
    def _format_md_report(result: AnalysisResult) -> str:
        """Markdown形式の分析レポートを生成."""
        EXECUTOR_LABELS = {
            "ai": "AI Agent",
            "human": "Human",
            "hybrid": "AI + Human",
        }
        EXECUTOR_ICONS = {
            "ai": "🤖",
            "human": "👤",
            "hybrid": "🤝",
        }

        lines = [
            f"# 要件分析レポート：{result.project_name}",
            "",
            "## 概要",
            "",
            result.summary,
            "",
        ]

        if result.tech_stack:
            lines.extend(["## 技術スタック", ""])
            for tech in result.tech_stack:
                lines.append(f"- {tech}")
            lines.append("")

        # 実行者サマリーテーブル
        ai_tasks = [st for st in result.subtasks if st.executor == "ai"]
        human_tasks = [st for st in result.subtasks if st.executor == "human"]
        hybrid_tasks = [st for st in result.subtasks if st.executor == "hybrid"]

        lines.extend([
            "## 実行者サマリー",
            "",
            "| 区分 | 件数 | タスク |",
            "|------|------|--------|",
            f"| 🤖 AI Agent | {len(ai_tasks)} | {', '.join(st.id for st in ai_tasks) or '-'} |",
            f"| 👤 Human | {len(human_tasks)} | {', '.join(st.id for st in human_tasks) or '-'} |",
            f"| 🤝 AI + Human | {len(hybrid_tasks)} | {', '.join(st.id for st in hybrid_tasks) or '-'} |",
            "",
        ])

        lines.extend(["## サブタスク", ""])

        for st in result.subtasks:
            icon = EXECUTOR_ICONS.get(st.executor, "❓")
            label = EXECUTOR_LABELS.get(st.executor, st.executor)
            lines.extend([
                f"### {st.id}: {st.title} `[{st.priority.value.upper()}]` {icon} {label}",
                "",
                f"**説明：** {st.description}",
                "",
                f"**実行者：** {icon} {label}",
                "",
            ])
            if st.executor_reason:
                lines.append(f"**理由：** {st.executor_reason}")
                lines.append("")
            if st.acceptance_criteria:
                lines.append("**受入基準：**")
                for ac in st.acceptance_criteria:
                    lines.append(f"- {ac}")
                lines.append("")
            if st.dependencies:
                lines.append(f"**依存タスク：** {', '.join(st.dependencies)}")
                lines.append("")
            lines.extend(["---", ""])

        lines.append(f"*生成日時: {result.timestamp}*")

        return "\n".join(lines)
