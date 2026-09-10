"""Orchestrator - Agent を直列実行するパイプライン."""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from agents.analyst import AnalystAgent
from agents.developer import DeveloperAgent
from agents.investigator import InvestigatorAgent
from agents.reviewer import ReviewerAgent
from agents.tester import TesterAgent
from core.config import Config
from core.models import (
    AnalysisResult,
    AllDevelopmentResults,
    DispatchResult,
    InvestigationReport,
    PostTestInvestigation,
    Priority,
    ReviewResult,
    SubTask,
    TestReport,
    WorkType,
)

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """パイプラインの最終出力."""
    dispatch: Optional[DispatchResult] = None
    investigation: Optional[InvestigationReport] = None
    analysis: Optional[AnalysisResult] = None
    development: Optional[AllDevelopmentResults] = None
    review: Optional[ReviewResult] = None
    test_report: Optional[TestReport] = None
    post_investigation: Optional[PostTestInvestigation] = None


class Orchestrator:
    """4つの Agent を順次実行するパイプラインオーケストレーター."""

    def __init__(self, config: Config | None = None) -> None:
        self.config = config or Config()
        self.investigator = InvestigatorAgent(self.config)
        self.analyst = AnalystAgent(self.config)
        self.developer = DeveloperAgent(self.config)
        self.reviewer = ReviewerAgent(self.config)
        self.tester = TesterAgent(self.config)

    def run_investigation_only(self) -> InvestigationReport:
        """調査のみ実行：リポジトリ準備 -> 事前調査."""
        logger.info("=" * 50)
        logger.info("  調査モード開始")
        logger.info("=" * 50)

        if self.config.repo_url:
            self._clone_repo()
        if self.config.branch:
            self._setup_branch()

        logger.info("\n[調査] 既存コードベースを調査中...")
        report = self.investigator.investigate_codebase()

        if report.tech_stack:
            logger.info(f"  -> 技術スタック: {', '.join(report.tech_stack)}")
        logger.info(f"  -> 主要ファイル: {len(report.key_files)} 件")

        logger.info("\n" + "=" * 50)
        logger.info("  調査完了")
        logger.info("=" * 50)

        return report

    @staticmethod
    def _progress_bar(phase: int, total: int, label: str) -> None:
        """フェーズ進捗バーを表示."""
        filled = "█" * phase
        empty = "░" * (total - phase)
        logger.info(f"\n[{filled}{empty}] フェーズ {phase}/{total}  {label}")

    def run_dispatched(self, requirement: str, dispatch: DispatchResult) -> PipelineResult:
        """Dispatcher の結果に基づいてパイプラインを実行."""
        if dispatch.work_type == WorkType.INVESTIGATION:
            return self._run_investigation_pipeline(requirement, dispatch)
        elif dispatch.work_type == WorkType.DESIGN_REVIEW:
            return self._run_review_pipeline(requirement, dispatch)
        else:
            # DEVELOPMENT / INFRASTRUCTURE → フルパイプライン
            return self.run(requirement, dispatch)

    def _run_investigation_pipeline(self, requirement: str, dispatch: DispatchResult) -> PipelineResult:
        """調査パイプライン: Investigator のみ."""
        import time
        pipeline_start = time.time()

        logger.info("=" * 50)
        logger.info(f"  パイプライン開始 [{dispatch.label}]")
        logger.info("=" * 50)

        self._progress_bar(1, 1, "要件調査...")
        self.investigator.investigate_requirement(requirement)

        elapsed = time.time() - pipeline_start
        mins, secs = divmod(int(elapsed), 60)
        logger.info(f"\n[█] パイプライン完了  合計 {mins}分{secs}秒")
        logger.info("=" * 50)

        return PipelineResult(dispatch=dispatch)

    def _run_review_pipeline(self, requirement: str, dispatch: DispatchResult) -> PipelineResult:
        """設計レビューパイプライン: Analyst + Developer."""
        import time
        pipeline_start = time.time()

        logger.info("=" * 50)
        logger.info(f"  パイプライン開始 [{dispatch.label}]")
        logger.info("=" * 50)

        self._progress_bar(1, 2, "要件分析...")
        analysis = self.analyst.run(requirement, "")
        logger.info(f"  -> {len(analysis.subtasks)} 件のサブタスクに分割")

        self._progress_bar(2, 2, "ドキュメント作成...")
        dev_results = self.developer.run(analysis, "")
        done_count = sum(1 for r in dev_results.results if r.status.value == "done")
        logger.info(f"  -> {done_count}/{len(dev_results.results)} 件完了")

        elapsed = time.time() - pipeline_start
        mins, secs = divmod(int(elapsed), 60)
        logger.info(f"\n[██] パイプライン完了  合計 {mins}分{secs}秒")
        logger.info("=" * 50)

        return PipelineResult(
            dispatch=dispatch,
            analysis=analysis,
            development=dev_results,
        )

    def run(self, requirement: str, dispatch: DispatchResult | None = None) -> PipelineResult:
        """フルパイプライン実行：調査 -> 分析 -> 開発 -> テスト -> 問題調査."""
        import time
        pipeline_start = time.time()

        label = dispatch.label if dispatch else "フルパイプライン"
        logger.info("=" * 50)
        logger.info(f"  パイプライン開始 [{label}]")
        logger.info("=" * 50)

        # フェーズ 0: Git 準備（クローン + ブランチ）
        if self.config.repo_url:
            self._clone_repo()
        if self.config.branch:
            self._setup_branch()

        # フェーズ 1: 事前調査（Investigator）
        self._progress_bar(1, 6, "事前コード調査...")
        investigation = self.investigator.investigate_codebase()
        if investigation.tech_stack:
            logger.info(f"  -> 技術スタック: {', '.join(investigation.tech_stack)}")

        # 調査結果をコンテキストとして構築
        codebase_summary = self._build_context(investigation)

        # フェーズ 2: 要件分析（Analyst）
        self._progress_bar(2, 6, "要件分析...")
        analysis = self.analyst.run(requirement, codebase_summary)
        logger.info(f"  -> {len(analysis.subtasks)} 件のサブタスクに分割")

        # フェーズ 3: コード開発（Developer）
        self._progress_bar(3, 6, "コード開発...")
        dev_results = self.developer.run(analysis, codebase_summary)
        done_count = sum(
            1 for r in dev_results.results if r.status.value == "done"
        )
        logger.info(f"  -> {done_count}/{len(dev_results.results)} 件完了")

        # フェーズ 4: レビュー + 修正ループ（Reviewer）
        self._progress_bar(4, 6, "成果物レビュー...")
        review_result = self.reviewer.review(requirement, analysis, dev_results)

        # 修正が必要な場合: Reviewer の指示で Developer を再実行（最大1回）
        if not review_result.passed and review_result.corrections:
            logger.info(f"  -> レビュー不合格、{len(review_result.corrections)}件の修正を実行...")
            fix_analysis = self._corrections_to_analysis(
                review_result, analysis.project_name, analysis.tech_stack
            )
            fix_results = self.developer.run(fix_analysis, codebase_summary)
            fix_done = sum(1 for r in fix_results.results if r.status.value == "done")
            logger.info(f"  -> 修正完了: {fix_done}/{len(fix_results.results)} 件")

            # 修正後の結果をマージ
            dev_results.results.extend(fix_results.results)

            # 再レビュー
            review_result = self.reviewer.review(requirement, analysis, dev_results)

        # フェーズ 5: テスト・セキュリティ監査（Tester）
        self._progress_bar(5, 6, "テスト・セキュリティ監査...")
        test_report = self.tester.run(analysis, dev_results)
        logger.info(
            f"  -> 合格 {test_report.passed}/{test_report.total_tests}  "
            f"脆弱性 {len(test_report.vulnerabilities)} 件"
        )

        # フェーズ 6: テスト後問題調査（Investigator）
        self._progress_bar(6, 6, "問題原因調査...")
        post_investigation = self.investigator.investigate_issues(test_report)
        if post_investigation.issue_causes:
            logger.info(f"  -> {len(post_investigation.issue_causes)} 件の原因を特定")
        else:
            logger.info("  -> 問題なし")

        elapsed = time.time() - pipeline_start
        mins, secs = divmod(int(elapsed), 60)

        logger.info(f"\n[██████] パイプライン完了  合計 {mins}分{secs}秒")
        logger.info("=" * 50)

        return PipelineResult(
            dispatch=dispatch,
            investigation=investigation,
            analysis=analysis,
            development=dev_results,
            review=review_result,
            test_report=test_report,
            post_investigation=post_investigation,
        )

    @staticmethod
    def _corrections_to_analysis(
        review: ReviewResult, project_name: str, tech_stack: list[str],
    ) -> AnalysisResult:
        """Reviewer の修正コマンドを Developer 用の AnalysisResult に変換."""
        subtasks = []
        for i, cmd in enumerate(review.corrections):
            subtasks.append(SubTask(
                id=f"fix-{i + 1}",
                title=f"修正: {cmd.file_path}",
                description=cmd.instruction,
                priority=Priority.HIGH,
                executor="ai",
                acceptance_criteria=[cmd.instruction],
            ))
        return AnalysisResult(
            project_name=f"{project_name} (レビュー修正)",
            summary=f"Reviewer からの修正指示 ({len(subtasks)}件)",
            subtasks=subtasks,
            tech_stack=tech_stack,
        )

    def _build_context(self, investigation: InvestigationReport) -> str:
        """Investigator の調査結果をコンテキスト文字列に変換."""
        if not investigation.project_overview or investigation.project_overview == "新規プロジェクト（既存コードなし）":
            return ""

        lines = [
            f"プロジェクト概要: {investigation.project_overview}",
            f"技術スタック: {', '.join(investigation.tech_stack)}",
            f"アーキテクチャ: {investigation.architecture}",
        ]

        if investigation.key_files:
            lines.append("主要ファイル：")
            for f in investigation.key_files:
                lines.append(f"  - {f.path}: {f.description}")

        if investigation.dependencies:
            lines.append(f"依存関係: {', '.join(investigation.dependencies)}")

        if investigation.notes:
            lines.append(f"注意事項: {investigation.notes}")

        return "\n".join(lines)

    # ── Git 操作 ────────────────────────────────────────────────

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        """workspace ディレクトリで git コマンドを実行."""
        cmd = ["git", "-C", str(self.config.workspace)] + list(args)
        return subprocess.run(cmd, capture_output=True, text=True)

    def _is_git_repo(self) -> bool:
        return (self.config.workspace / ".git").exists()

    def _clone_repo(self) -> None:
        """リポジトリを workspace にクローン（既存の場合は pull で更新）."""
        if self._is_git_repo():
            logger.info("リポジトリ既存、最新コードを取得中...")
            result = self._git("pull", "--ff-only")
            if result.returncode != 0:
                logger.warning(f"  git pull スキップ: {result.stderr.strip()}")
            else:
                logger.info(f"  -> {result.stdout.strip()}")
        else:
            logger.info(f"リポジトリをクローン: {self.config.repo_url}")
            cmd = ["git", "clone", self.config.repo_url, str(self.config.workspace)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"クローン失敗: {result.stderr.strip()}")
            logger.info("  -> クローン完了")

    def _setup_branch(self) -> None:
        """対象ブランチの作成または切り替え."""
        if not self._is_git_repo():
            logger.warning("workspace は git リポジトリではありません。ブランチ操作をスキップ")
            return

        branch = self.config.branch
        current = self._git("branch", "--show-current").stdout.strip()

        if current == branch:
            logger.info(f"  現在のブランチ: {branch}")
            return

        local_branches = self._git("branch", "--list", branch).stdout.strip()
        if local_branches:
            logger.info(f"  既存ブランチに切り替え: {branch}")
            result = self._git("checkout", branch)
            if result.returncode != 0:
                raise RuntimeError(f"ブランチ切り替え失敗: {result.stderr.strip()}")
            return

        self._git("fetch", "--prune")
        remote_check = self._git("branch", "-r", "--list", f"origin/{branch}").stdout.strip()
        if remote_check:
            logger.info(f"  リモートブランチをチェックアウト: {branch}")
            result = self._git("checkout", "-b", branch, f"origin/{branch}")
            if result.returncode != 0:
                raise RuntimeError(f"リモートブランチのチェックアウト失敗: {result.stderr.strip()}")
            return

        logger.info(f"  新規ブランチを作成: {branch}")
        result = self._git("checkout", "-b", branch)
        if result.returncode != 0:
            raise RuntimeError(f"ブランチ作成失敗: {result.stderr.strip()}")
