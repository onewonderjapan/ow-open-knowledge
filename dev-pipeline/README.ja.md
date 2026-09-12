# Agent Pipeline - AI 駆動型開発パイプライン

[English](README.md) | 日本語（オリジナル版）

![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue)

6つの AI Agent が連携して、**要件分類 → 事前調査 → 要件分析 → 実装 → レビュー → テスト → 問題調査**を自動実行する開発支援ツールです。各 Agent は実行ごとに自己学習し、使うほど賢くなります。

> **このディレクトリの位置づけ。** ここは要件ファイルからコードを書くパイプライン。育成方法論は [agent-cultivation](../agent-cultivation/)。定期 cron ワークフローは [workflow-standard](../workflow-standard/)。計画承認付きの一度きり自然言語タスクは [task-orchestrator](../task-orchestrator/)。[USAGE.md](USAGE.md) の Human / Hybrid はサブタスクの実行者判定であり、task-orchestrator の計画承認でも [workflow-standard/STANDARD.md](../workflow-standard/STANDARD.md) P4 の対外副作用ゲートでもない。`agents/memory/` は実行記憶であり、[AGENT育成標準.md](../agent-cultivation/AGENT育成標準.md) の三層固化とは別物。

---

## 概要

要件ファイルを入力として受け取り、Dispatcher が要件を自動分類し、適切なパイプラインを選択して実行します。

```text
要件 ──→ [Dispatcher] ──→ パイプライン選択
              │
              ├─ 機能開発      ──→ 全6フェーズ実行
              ├─ 基盤構築      ──→ 全6フェーズ実行（設計書中心）
              ├─ 調査          ──→ Investigator のみ
              └─ 設計レビュー  ──→ Analyst + Developer

フルパイプライン（6フェーズ）:
[Investigator] → [Analyst] → [Developer] → [Reviewer] → [Tester] → [Investigator]
   事前調査        分析         実装         レビュー      テスト       問題調査
                          ↓ 各 Agent は実行後に自動学習 ↓
                            agents/memory/<name>.md
```

## 6つの Agent

| Agent | コマンド | 役割 | 出力 |
|-------|---------|------|------|
| **Dispatcher** | (自動) | 要件を分類し、適切なパイプラインを選択 | `dispatcher/dispatch.json` |
| **Investigator** | `--investigate` | コード調査 / 技術リサーチ | `investigator/investigation.md` |
| **Analyst** | `--analyze` | 要件分析・タスク分割・実行者判定（AI/Human/Hybrid） | `analyst/analysis.md` |
| **Developer** | `--develop` | サブタスクごとにコード・ドキュメント生成 | `developer/development.md` |
| **Reviewer** | (自動) | 成果物の品質検証・クロスシステム検査・修正指示 | `reviewer/review.md` |
| **Tester** | `--test` | 機能テスト + セキュリティ脆弱性スキャン | `tester/test_report.md` |

### Dispatcher（分類者）

フルパイプライン実行時に自動で動作し、要件を以下の4種別に分類：

| 種別 | ラベル | パイプライン |
|------|--------|------------|
| `development` | 機能開発 | 全6フェーズ（コード生成中心） |
| `infrastructure` | 基盤構築 | 全6フェーズ（設計書中心） |
| `investigation` | 調査 | Investigator のみ |
| `design_review` | 設計レビュー | Analyst + Developer |

### Reviewer（レビュー者）

Developer の成果物を自動検証し、問題があれば Developer に修正を指示：

- **ファイル完全性チェック** — 0バイトファイル、内容切れの検出
- **要件カバレッジ** — 要件の各ポイントが成果物に反映されているか
- **クロスシステム検査** — 関連するが未対応のシステム設計を自動検出（DNS/FW/認証/監視等）
- **修正ループ** — 問題検出時に Developer へ修正指示 → 修正後に再レビュー（最大1回）

---

## 使い方

```bash
# フルパイプライン（Dispatcher が自動分類 → 適切なパイプラインを実行）
python main.py -f task.md

# 単独 Agent 実行
python main.py --investigate -f 調査.md     # Investigator のみ
python main.py --analyze -f task.md         # Analyst のみ
python main.py --develop -f task.md         # Analyst → Developer
python main.py --test -f task.md            # Analyst → Developer → Tester

# 自己進化（学習・最適化）
python main.py --memory                     # 全 Agent のメモリを表示
python main.py --consolidate                # メモリを整理・圧縮
python main.py --optimize                   # 全 Agent のプロンプトを自己最適化
```

## 要件ファイル形式

`requirements/` ディレクトリに配置：

```markdown
branch: feature/add-login
repo: https://github.com/user/project.git
---

要件の本文をここに記述...
```

- `branch`：作業ブランチ（任意。コード開発時は推奨）
- `repo`：Git リポジトリ URL（任意）
- `---` 以降：要件本文

---

## 実行フロー

### フルパイプライン（6フェーズ）

```text
[Dispatcher]    要件を自動分類（機能開発/基盤構築/調査/設計レビュー）
[█░░░░░] 1/6   Investigator  - 既存コードベースの事前調査
[██░░░░] 2/6   Analyst       - 要件分析、サブタスク分割、実行者判定
[███░░░] 3/6   Developer     - サブタスクごとにコード/ドキュメント生成
[████░░] 4/6   Reviewer      - 成果物レビュー + 修正ループ（不合格時）
[█████░] 5/6   Tester        - 機能テスト + セキュリティ脆弱性スキャン
[██████] 6/6   Investigator  - 検出された問題の原因調査・修正方針提案
```

### 進捗表示

- **TTY 環境**（ターミナル直接実行）：スピナーアニメーション + リアルタイム経過時間
- **非 TTY 環境**（バックグラウンド実行）：30秒ごとの経過時間ログ

---

## 自己進化システム

```text
┌─ 自動（毎回） ─────────────────────────────────┐
│ 実行 → 振り返り → 教訓抽出 → agents/memory/     │
└────────────────────────────────────────────────┘
         ↓ --optimize（手動）
┌─ 自己最適化 ───────────────────────────────────┐
│ 教訓を分析 → prompt を改善 → agents/prompts/    │
└────────────────────────────────────────────────┘
         ↓
  次回実行時に進化版 prompt を自動適用
```

---

## ディレクトリ構成

```text
dev-pipeline/
├── main.py              # CLI エントリーポイント
├── core/
│   ├── config.py        # 設定
│   ├── models.py        # Agent 間共有データモデル
│   ├── orchestrator.py  # パイプラインオーケストレーター
│   └── requirement_parser.py
├── agents/
│   ├── base.py          # 基底クラス（CLI + 自己学習 + 自己最適化）
│   ├── dispatcher.py    # Dispatcher Agent（要件分類）
│   ├── investigator.py  # Investigator Agent（調査）
│   ├── analyst.py       # Analyst Agent（分析）
│   ├── developer.py     # Developer Agent（実装）
│   ├── reviewer.py      # Reviewer Agent（レビュー）
│   ├── tester.py        # Tester Agent（テスト）
│   ├── memory/          # 各 Agent の学習記録（自動蓄積）
│   └── prompts/         # 各 Agent の進化版プロンプト（--optimize）
├── requirements/         # 要件ファイル
├── workspace/            # コード出力（要件名ごとに分離）
└── output/               # レポート出力（要件名ごとに分離）
```

## 動作環境

- Python 3.9+
- Git
- Claude Code CLI（Claude サブスクリプション）

---

詳細な使い方は [USAGE.md](USAGE.md) を参照してください。

## License

MIT — 詳細は [../LICENSE](../LICENSE) を参照。
