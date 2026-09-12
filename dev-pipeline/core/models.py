"""Agent 間で通信するデータモデル."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class WorkType(str, Enum):
    """Dispatcher が判定する作業種別."""
    DEVELOPMENT = "development"          # 機能開発（コード生成）
    INFRASTRUCTURE = "infrastructure"    # 基盤構築（設計書生成）
    INVESTIGATION = "investigation"      # 調査（レポートのみ）
    DESIGN_REVIEW = "design_review"      # 設計レビュー（既存設計の補強）


@dataclass
class DispatchResult:
    """Dispatcher Agent の出力."""
    work_type: WorkType
    label: str          # 日本語ラベル（例: "基盤構築"）
    reason: str         # 判断理由
    pipeline: list[str] = field(default_factory=list)  # 使用する Agent リスト
    notes: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")


# ── Reviewer Agent 出力 ──────────────────────────────────────


@dataclass
class ReviewIssue:
    """レビューで検出された問題."""
    severity: str       # critical / warning / info
    category: str       # empty_file / missing_content / cross_system / quality
    file_path: str
    description: str
    correction: str     # Developer への修正指示


@dataclass
class CorrectionCommand:
    """Reviewer から他 Agent への修正コマンド."""
    target_agent: str   # "developer"
    action: str         # "create" / "modify" / "regenerate"
    file_path: str
    instruction: str


@dataclass
class ReviewResult:
    """Reviewer Agent の出力."""
    passed: bool = True
    total_checks: int = 0
    passed_checks: int = 0
    issues: list[ReviewIssue] = field(default_factory=list)
    corrections: list[CorrectionCommand] = field(default_factory=list)
    cross_system_gaps: list[str] = field(default_factory=list)
    summary: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


# ── Investigator Agent 出力 ──────────────────────────────────────


@dataclass
class FileInfo:
    """ファイルの調査情報."""
    path: str
    description: str
    language: str = ""


@dataclass
class InvestigationReport:
    """Investigator Agent の事前調査出力."""
    project_overview: str
    tech_stack: list[str] = field(default_factory=list)
    architecture: str = ""
    key_files: list[FileInfo] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    notes: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "InvestigationReport":
        data = json.loads(path.read_text(encoding="utf-8"))
        data["key_files"] = [FileInfo(**f) for f in data.get("key_files", [])]
        return cls(**data)


@dataclass
class IssueCause:
    """不具合・脆弱性の原因分析."""
    issue_id: str
    title: str
    root_cause: str
    affected_files: list[str] = field(default_factory=list)
    fix_suggestion: str = ""


@dataclass
class PostTestInvestigation:
    """Investigator Agent のテスト後問題調査出力."""
    issue_causes: list[IssueCause] = field(default_factory=list)
    summary: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "PostTestInvestigation":
        data = json.loads(path.read_text(encoding="utf-8"))
        data["issue_causes"] = [IssueCause(**ic) for ic in data.get("issue_causes", [])]
        return cls(**data)


# ── Analyst Agent 出力 ──────────────────────────────────────────


@dataclass
class SubTask:
    """要件分析後のサブタスク."""
    id: str
    title: str
    description: str
    priority: Priority
    executor: str = "ai"  # "ai" | "human" | "hybrid"
    executor_reason: str = ""  # なぜ AI/人工/両方が必要かの説明
    acceptance_criteria: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)  # 依存する subtask id


@dataclass
class AnalysisResult:
    """Analyst Agent の出力."""
    project_name: str
    summary: str
    subtasks: list[SubTask] = field(default_factory=list)
    tech_stack: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "AnalysisResult":
        data = json.loads(path.read_text(encoding="utf-8"))
        data["subtasks"] = [
            SubTask(**{**st, "priority": Priority(st["priority"])})
            for st in data["subtasks"]
        ]
        return cls(**data)


# ── Developer Agent 出力 ─────────────────────────────────────────


@dataclass
class CodeChange:
    """単一のコード変更."""
    file_path: str
    action: str  # create / modify / delete
    description: str
    content: str = ""


@dataclass
class DevelopmentResult:
    """Developer Agent の出力."""
    subtask_id: str
    status: TaskStatus
    changes: list[CodeChange] = field(default_factory=list)
    notes: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AllDevelopmentResults:
    """全サブタスクの開発結果."""
    results: list[DevelopmentResult] = field(default_factory=list)

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(
            [asdict(r) for r in self.results], ensure_ascii=False, indent=2
        ), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "AllDevelopmentResults":
        data = json.loads(path.read_text(encoding="utf-8"))
        results = []
        for r in data:
            r["status"] = TaskStatus(r["status"])
            r["changes"] = [CodeChange(**c) for c in r["changes"]]
            results.append(DevelopmentResult(**r))
        return cls(results=results)


# ── Tester Agent 出力 ────────────────────────────────────────────


@dataclass
class TestCase:
    """単一のテストケース."""
    id: str
    name: str
    description: str
    status: TaskStatus  # done = pass, failed = fail
    error_message: str = ""


@dataclass
class Vulnerability:
    """検出されたセキュリティ脆弱性."""
    id: str
    title: str
    severity: Severity
    location: str  # file:line
    description: str
    recommendation: str


@dataclass
class TestReport:
    """Tester Agent の出力."""
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    test_cases: list[TestCase] = field(default_factory=list)
    vulnerabilities: list[Vulnerability] = field(default_factory=list)
    summary: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "TestReport":
        data = json.loads(path.read_text(encoding="utf-8"))
        data["test_cases"] = [
            TestCase(**{**tc, "status": TaskStatus(tc["status"])})
            for tc in data["test_cases"]
        ]
        data["vulnerabilities"] = [
            Vulnerability(**{**v, "severity": Severity(v["severity"])})
            for v in data["vulnerabilities"]
        ]
        return cls(**data)
