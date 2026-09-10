#!/usr/bin/env python3
"""Agent パイプライン CLI エントリーポイント.

使い方：
  # フルパイプライン（要件ファイルから）
  python main.py -f todo-api.md

  # 単独 Agent 実行
  python main.py --investigate -f 调查.md        # Investigator のみ
  python main.py --analyze -f task.md            # Analyst のみ
  python main.py --develop -f task.md            # Developer のみ
  python main.py --test -f task.md               # Tester のみ

  # 要件テキストを直接指定
  python main.py "要件の説明"

  # 対話モード
  python main.py --interactive
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from core.config import Config
from core.orchestrator import Orchestrator
from core.requirement_parser import parse_requirement_file


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(name)s] %(message)s",
        datefmt="%H:%M:%S",
    )


IGNORED_FILES = {"template.md", "example.md"}


def resolve_requirement_file(name: str) -> Path:
    """要件ファイルのパスを解決：元のパス → requirements/ ディレクトリの順で検索."""
    if Path(name).name in IGNORED_FILES:
        print(f"エラー：{name} はテンプレート/サンプルファイルです。要件としては使用できません。")
        print(f"  コピーして別名で保存してください：")
        print(f"    cp requirements/{Path(name).name} requirements/my-task.md")
        sys.exit(1)

    path = Path(name)
    if path.exists():
        return path
    req_dir = Path(__file__).parent / "requirements"
    fallback = req_dir / name
    if fallback.exists():
        return fallback
    print(f"エラー：要件ファイルが見つかりません: {name}")
    print(f"  検索パス:")
    print(f"    - {path.resolve()}")
    print(f"    - {fallback.resolve()}")
    print(f"\n  要件ファイルを requirements/ ディレクトリに配置してください:")
    print(f"    {req_dir.resolve()}/")
    sys.exit(1)


def _slugify(name: str) -> str:
    """ファイル名を ASCII セーフなスラッグに変換."""
    import hashlib
    import re
    import unicodedata

    original = name
    # Unicode正規化
    name = unicodedata.normalize("NFKD", name)
    # ASCII文字・数字・ハイフン・アンダースコア以外を除去
    ascii_part = re.sub(r"[^\w\-]", "_", name, flags=re.ASCII)
    ascii_part = re.sub(r"_+", "_", ascii_part).strip("_").lower()

    if ascii_part:
        return ascii_part

    # ASCII部分がない場合（純粋なCJK文字列等）：短いhashで一意性を確保
    short_hash = hashlib.md5(original.encode("utf-8")).hexdigest()[:8]
    return f"req_{short_hash}"


def _resolve_req_name(args: argparse.Namespace) -> str:
    """要件ファイル名から ASCII セーフなプロジェクト名を取得."""
    if args.file:
        return _slugify(Path(args.file).stem)
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _resolve_output_dir(args: argparse.Namespace) -> Path:
    """output_dir を需求名で分類: output/<requirement_name>/"""
    return Path(args.output) / _resolve_req_name(args)


def _resolve_workspace(args: argparse.Namespace) -> Path:
    """workspace を需求名で分類: workspace/<requirement_name>/"""
    return Path(args.workspace) / _resolve_req_name(args)


def _parse_args_common(args: argparse.Namespace):
    """共通の引数解析：要件ファイルから repo/branch/requirement を読み取り."""
    repo_url = args.repo
    branch = args.branch
    requirement = None

    if args.file:
        file_path = resolve_requirement_file(args.file)
        spec = parse_requirement_file(file_path)
        requirement = spec.content
        if not repo_url and spec.repo:
            repo_url = spec.repo
        if not branch:
            branch = spec.branch
    elif hasattr(args, 'requirement') and args.requirement:
        requirement = args.requirement

    config = Config(
        workspace=_resolve_workspace(args),
        output_dir=_resolve_output_dir(args),
        repo_url=repo_url,
        branch=branch,
    )
    if args.model:
        config.model = args.model

    return config, requirement, repo_url, branch


# ── 単独 Agent 実行 ──────────────────────────────────────────


def run_investigate_only(args: argparse.Namespace) -> None:
    """Investigator Agent を単独実行."""
    setup_logging(args.verbose)
    config, requirement, repo_url, branch = _parse_args_common(args)

    from agents.investigator import InvestigatorAgent
    investigator = InvestigatorAgent(config)

    if repo_url:
        orchestrator = Orchestrator(config)
        report = orchestrator.run_investigation_only()

        print("\n" + "=" * 50)
        print("  [Investigator] コード調査完了")
        print("=" * 50)
        print(f"  概要: {report.project_overview}")
        if report.tech_stack:
            print(f"  技術スタック: {', '.join(report.tech_stack)}")
        if report.architecture:
            print(f"  アーキテクチャ: {report.architecture}")
        print(f"  主要ファイル: {len(report.key_files)} 件")
    else:
        if not requirement:
            print("エラー：調査対象がありません（-f で要件ファイルを指定してください）")
            sys.exit(1)

        investigator.investigate_requirement(requirement)
        print("\n" + "=" * 50)
        print("  [Investigator] 要件調査完了")
        print("=" * 50)

    report_path = config.output_dir.resolve() / "investigator" / "investigation.md"
    print(f"  レポート: {report_path}")
    print("=" * 50)


def run_analyze_only(args: argparse.Namespace) -> None:
    """Analyst Agent を単独実行."""
    setup_logging(args.verbose)
    config, requirement, repo_url, branch = _parse_args_common(args)

    if not requirement:
        print("エラー：要件がありません（-f で要件ファイルを指定してください）")
        sys.exit(1)

    from agents.analyst import AnalystAgent
    analyst = AnalystAgent(config)

    # コードベースがあれば事前調査を実施
    codebase_summary = ""
    if repo_url or (config.workspace / ".git").exists():
        from agents.investigator import InvestigatorAgent
        investigator = InvestigatorAgent(config)
        investigation = investigator.investigate_codebase()
        codebase_summary = Orchestrator(config)._build_context(investigation)

    result = analyst.run(requirement, codebase_summary)

    print("\n" + "=" * 50)
    print("  [Analyst] 要件分析完了")
    print("=" * 50)
    print(f"  プロジェクト: {result.project_name}")
    print(f"  サブタスク: {len(result.subtasks)} 件")

    executor_icons = {"ai": "🤖", "human": "👤", "hybrid": "🤝"}
    for st in result.subtasks:
        icon = executor_icons.get(st.executor, "❓")
        print(f"    {icon} [{st.priority.value.upper()}] {st.id}: {st.title}")

    ai_count = sum(1 for st in result.subtasks if st.executor == "ai")
    human_count = sum(1 for st in result.subtasks if st.executor == "human")
    hybrid_count = sum(1 for st in result.subtasks if st.executor == "hybrid")
    print(f"\n  🤖 AI: {ai_count}  👤 Human: {human_count}  🤝 Hybrid: {hybrid_count}")

    report_path = config.output_dir.resolve() / "analyst" / "analysis.md"
    print(f"  レポート: {report_path}")
    print("=" * 50)


def run_develop_only(args: argparse.Namespace) -> None:
    """Developer Agent を単独実行（Analyst の結果が必要）."""
    setup_logging(args.verbose)
    config, requirement, repo_url, branch = _parse_args_common(args)

    if not requirement:
        print("エラー：要件がありません（-f で要件ファイルを指定してください）")
        sys.exit(1)

    # まず Analyst で分析
    from agents.analyst import AnalystAgent
    from agents.developer import DeveloperAgent
    analyst = AnalystAgent(config)
    developer = DeveloperAgent(config)

    codebase_summary = ""
    if repo_url or (config.workspace / ".git").exists():
        from agents.investigator import InvestigatorAgent
        investigator = InvestigatorAgent(config)
        investigation = investigator.investigate_codebase()
        codebase_summary = Orchestrator(config)._build_context(investigation)

    print("[Phase 1/2] Analyst で要件分析中...")
    analysis = analyst.run(requirement, codebase_summary)

    print(f"[Phase 2/2] Developer で {len(analysis.subtasks)} 件のサブタスクを実装中...")
    dev_results = developer.run(analysis, codebase_summary)
    done_count = sum(1 for r in dev_results.results if r.status.value == "done")

    print("\n" + "=" * 50)
    print("  [Developer] 開発完了")
    print("=" * 50)
    print(f"  完了: {done_count}/{len(dev_results.results)} 件")
    report_path = config.output_dir.resolve() / "developer" / "development.md"
    print(f"  レポート: {report_path}")
    print(f"  コード: {config.workspace.resolve()}")
    print("=" * 50)


def run_test_only(args: argparse.Namespace) -> None:
    """Tester Agent を単独実行（Analyst + Developer の結果が必要）."""
    setup_logging(args.verbose)
    config, requirement, repo_url, branch = _parse_args_common(args)

    if not requirement:
        print("エラー：要件がありません（-f で要件ファイルを指定してください）")
        sys.exit(1)

    from agents.analyst import AnalystAgent
    from agents.developer import DeveloperAgent
    from agents.tester import TesterAgent
    analyst = AnalystAgent(config)
    developer = DeveloperAgent(config)
    tester = TesterAgent(config)

    codebase_summary = ""
    if repo_url or (config.workspace / ".git").exists():
        from agents.investigator import InvestigatorAgent
        investigator = InvestigatorAgent(config)
        investigation = investigator.investigate_codebase()
        codebase_summary = Orchestrator(config)._build_context(investigation)

    print("[Phase 1/3] Analyst で要件分析中...")
    analysis = analyst.run(requirement, codebase_summary)

    print(f"[Phase 2/3] Developer で実装中...")
    dev_results = developer.run(analysis, codebase_summary)

    print("[Phase 3/3] Tester でテスト中...")
    test_report = tester.run(analysis, dev_results)

    print("\n" + "=" * 50)
    print("  [Tester] テスト完了")
    print("=" * 50)
    print(f"  合格: {test_report.passed}/{test_report.total_tests}")
    print(f"  脆弱性: {len(test_report.vulnerabilities)} 件")
    report_path = config.output_dir.resolve() / "tester" / "test_report.md"
    print(f"  レポート: {report_path}")
    print("=" * 50)


# ── メモリ管理 ────────────────────────────────────────────────


def run_consolidate(args: argparse.Namespace) -> None:
    """全 Agent のメモリを整理・統合."""
    setup_logging(args.verbose)
    config = Config()
    if args.model:
        config.model = args.model

    from agents.investigator import InvestigatorAgent
    from agents.analyst import AnalystAgent
    from agents.developer import DeveloperAgent
    from agents.tester import TesterAgent

    agents = [
        InvestigatorAgent(config),
        AnalystAgent(config),
        DeveloperAgent(config),
        TesterAgent(config),
    ]

    for agent in agents:
        print(f"  [{agent.name}] メモリ整理中...")
        agent.consolidate_memory()

    print("\n  全 Agent のメモリ整理完了")


def run_show_memory() -> None:
    """全 Agent のメモリを表示."""
    from agents.base import MEMORY_DIR

    print("\n" + "=" * 50)
    print("  Agent メモリ一覧")
    print("=" * 50)

    agent_names = ["investigator", "analyst", "developer", "tester"]
    for name in agent_names:
        path = MEMORY_DIR / f"{name}.md"
        if path.exists():
            content = path.read_text(encoding="utf-8").strip()
            lines = content.count("\n") + 1
            print(f"\n  [{name}] ({len(content)} 文字, {lines} 行)")
            print("  " + "-" * 40)
            for line in content.splitlines()[:10]:
                print(f"  {line}")
            if lines > 10:
                print(f"  ... (+{lines - 10} 行)")
        else:
            print(f"\n  [{name}] （メモリなし）")

    print("\n" + "=" * 50)


def run_optimize(args: argparse.Namespace) -> None:
    """全 Agent の system prompt を自己最適化."""
    setup_logging(args.verbose)
    config = Config()
    if args.model:
        config.model = args.model

    from agents.investigator import InvestigatorAgent, PRE_INVESTIGATION_PROMPT
    from agents.analyst import AnalystAgent, SYSTEM_PROMPT as ANALYST_PROMPT
    from agents.developer import DeveloperAgent, SYSTEM_PROMPT as DEVELOPER_PROMPT
    from agents.tester import TesterAgent, SYSTEM_PROMPT as TESTER_PROMPT

    agent_prompts = [
        (InvestigatorAgent(config), PRE_INVESTIGATION_PROMPT),
        (AnalystAgent(config), ANALYST_PROMPT),
        (DeveloperAgent(config), DEVELOPER_PROMPT),
        (TesterAgent(config), TESTER_PROMPT),
    ]

    print("\n" + "=" * 50)
    print("  Agent 自己最適化")
    print("=" * 50)

    for agent, default_prompt in agent_prompts:
        print(f"\n  [{agent.name}] 最適化中...")
        evolved = agent.optimize(default_prompt)
        if evolved != default_prompt:
            print(f"  [{agent.name}] プロンプト更新完了 -> agents/prompts/{agent.name}.md")
        else:
            print(f"  [{agent.name}] 変更なし（学習記録不足）")

    print("\n" + "=" * 50)
    print("  全 Agent の自己最適化完了")
    print("  次回実行時から改善されたプロンプトが自動適用されます")
    print("=" * 50)


# ── フルパイプライン ──────────────────────────────────────────


def run_full_pipeline(args: argparse.Namespace) -> None:
    """フルパイプライン実行（Dispatcher による自動分類付き）."""
    setup_logging(args.verbose)

    repo_url = args.repo
    branch = args.branch
    requirement = None

    if args.file:
        file_path = resolve_requirement_file(args.file)
        spec = parse_requirement_file(file_path)

        requirement = spec.content
        if not branch:
            branch = spec.branch
        if not repo_url and spec.repo:
            repo_url = spec.repo

        logging.getLogger(__name__).info(f"要件ファイル: {file_path}")
        logging.getLogger(__name__).info(f"  branch: {branch}")
        if repo_url:
            logging.getLogger(__name__).info(f"  repo: {repo_url}")

    elif args.interactive:
        print("要件を入力してください（空行で終了）：")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        requirement = "\n".join(lines)

    elif args.requirement:
        requirement = args.requirement

    else:
        return None

    if not requirement or not requirement.strip():
        print("エラー：要件が空です")
        sys.exit(1)

    config = Config(
        workspace=_resolve_workspace(args),
        output_dir=_resolve_output_dir(args),
        repo_url=repo_url,
        branch=branch,
    )
    if args.model:
        config.model = args.model

    # Dispatcher: 要件を自動分類
    from agents.dispatcher import DispatcherAgent
    dispatcher = DispatcherAgent(config)
    dispatch = dispatcher.classify(requirement)

    orchestrator = Orchestrator(config)
    result = orchestrator.run_dispatched(requirement, dispatch)

    # サマリー表示
    print("\n" + "=" * 50)
    print("  実行サマリー")
    print("=" * 50)
    print(f"  種別: {dispatch.label} ({dispatch.work_type.value})")
    if result.analysis:
        print(f"  プロジェクト: {result.analysis.project_name}")
    if branch:
        print(f"  ブランチ: {branch}")
    if result.analysis:
        print(f"  サブタスク: {len(result.analysis.subtasks)}")
    if result.development:
        print(f"  コードファイル: {sum(len(r.changes) for r in result.development.results)}")
    if result.review:
        status = "合格" if result.review.passed else "要修正"
        print(f"  レビュー: {result.review.passed_checks}/{result.review.total_checks} ({status})")
        if result.review.cross_system_gaps:
            print(f"  クロスシステム不足: {len(result.review.cross_system_gaps)} 件")
    if result.test_report:
        print(f"  テスト合格: {result.test_report.passed}/{result.test_report.total_tests}")
        print(f"  脆弱性: {len(result.test_report.vulnerabilities)}")
    if result.post_investigation and result.post_investigation.issue_causes:
        print(f"  原因特定: {len(result.post_investigation.issue_causes)} 件")
    if repo_url:
        print(f"\n  リポジトリ: {repo_url}")
    print(f"  コードディレクトリ: {config.workspace.resolve()}")
    print(f"  レポートディレクトリ: {config.output_dir.resolve()}")
    print("=" * 50)


# ── CLI ──────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="4 Agent 協調パイプライン",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
単独 Agent 実行:
  --investigate  Investigator のみ（調査）
  --analyze      Analyst のみ（要件分析）
  --develop      Analyst + Developer（分析→実装）
  --test         Analyst + Developer + Tester（分析→実装→テスト）

フルパイプライン:
  -f FILE        全5フェーズ実行（調査→分析→実装→テスト→問題調査）
""",
    )
    parser.add_argument("requirement", nargs="?", help="要件テキスト")
    parser.add_argument("-f", "--file", help="要件ファイル（requirements/ 内を自動検索）")
    parser.add_argument("-i", "--interactive", action="store_true", help="対話モード")

    # 単独 Agent 実行
    agent_group = parser.add_mutually_exclusive_group()
    agent_group.add_argument("--investigate", action="store_true", help="Investigator のみ実行")
    agent_group.add_argument("--analyze", action="store_true", help="Analyst のみ実行")
    agent_group.add_argument("--develop", action="store_true", help="Developer まで実行（Analyst→Developer）")
    agent_group.add_argument("--test", action="store_true", help="Tester まで実行（Analyst→Developer→Tester）")
    agent_group.add_argument("--consolidate", action="store_true", help="全 Agent のメモリを整理・統合")
    agent_group.add_argument("--optimize", action="store_true", help="全 Agent のプロンプトを自己最適化")
    agent_group.add_argument("--memory", action="store_true", help="全 Agent のメモリを表示")

    parser.add_argument("--repo", help="Git リポジトリ URL（ファイル内の値を上書き）")
    parser.add_argument("-b", "--branch", help="Git ブランチ名（ファイル内の値を上書き）")
    parser.add_argument("-m", "--model", default=None, help="モデルを指定")
    parser.add_argument("-w", "--workspace", default="workspace", help="コードディレクトリ")
    parser.add_argument("-o", "--output", default="output", help="レポート出力ディレクトリ")
    parser.add_argument("-v", "--verbose", action="store_true", help="詳細ログ")
    args = parser.parse_args()

    if args.investigate:
        run_investigate_only(args)
    elif args.analyze:
        run_analyze_only(args)
    elif args.develop:
        run_develop_only(args)
    elif args.test:
        run_test_only(args)
    elif args.consolidate:
        run_consolidate(args)
    elif args.optimize:
        run_optimize(args)
    elif args.memory:
        run_show_memory()
    elif args.file or args.interactive or args.requirement:
        run_full_pipeline(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
