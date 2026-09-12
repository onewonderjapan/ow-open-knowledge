# Agent パイプライン 使用手順

## 1. 環境準備（初回のみ）

### 1.1 前提条件

- Python 3.9+
- Git
- Claude Code CLI（`claude` コマンド）※ Claude サブスクリプションで動作

### 1.2 Python 依存パッケージのインストール

```bash
cd <プロジェクトルート>
pip install -r requirements.txt
```

### 1.3 Claude Code CLI の確認

```bash
claude --version
```

> 本ツールは Claude Code CLI（OAuth サブスクリプション認証）を使用します。
> Anthropic API Key は不要です。

---

## 2. 要件ファイルの形式

すべての要件ファイルは `requirements/` ディレクトリに配置し、以下の形式で記述します：

```markdown
branch: feature/add-todo-api
repo: https://github.com/user/project.git
---

## 要件説明

ここに要件本文を記述...
```

### フィールド説明

| フィールド | 必須 | 説明 |
|-----------|------|------|
| `branch` | いいえ | 作業ブランチ名。コード開発タスクでは推奨。調査のみの場合は省略可 |
| `repo` | いいえ | Git リポジトリ URL。workspace が既にリポジトリの場合は省略可 |
| `---` | はい | 区切り線。これ以降が要件本文 |

---

## 3. 使い方

### 3.1 フルパイプライン（Dispatcher 自動分類 + Agent 連携）

```bash
python main.py -f 要件ファイル名.md
```

実行フロー：
1. **Dispatcher** が要件を分析し、作業種別を自動判定（機能開発/基盤構築/調査/設計レビュー）
2. 判定結果に基づき、適切なパイプラインを自動選択・実行

| 種別 | 判定例 | 実行されるパイプライン |
|------|--------|---------------------|
| 機能開発 | 「TODO API を作成」 | 全6フェーズ |
| 基盤構築 | 「MCC サーバの設計書を作成」 | 全6フェーズ（設計書中心） |
| 調査 | 「Azure vs AWS の比較調査」 | Investigator のみ |
| 設計レビュー | 「既存設計書のレビュー」 | Analyst + Developer |

### 3.2 単独 Agent 実行

各 Agent を個別に呼び出せます（Dispatcher をスキップ）：

```bash
# Investigator のみ（調査）
python main.py --investigate -f 要件.md

# Analyst のみ（要件分析・サブタスク分割）
python main.py --analyze -f 要件.md

# Developer まで（Analyst → Developer）
python main.py --develop -f 要件.md

# Tester まで（Analyst → Developer → Tester）
python main.py --test -f 要件.md
```

> `--develop` と `--test` は前提となる Agent を自動的に先に実行します。

### 3.3 自己進化（学習・最適化）

```bash
# 全 Agent のメモリを表示
python main.py --memory

# 全 Agent のメモリを整理・統合（重複排除、圧縮）
python main.py --consolidate

# 全 Agent のプロンプトを自己最適化（学習記録に基づきプロンプトを改善）
python main.py --optimize
```

### 3.4 その他の使い方

```bash
# コマンドラインで branch や repo を上書き（ファイル内の値より優先）
python main.py -f todo-api.md -b hotfix/urgent --repo https://github.com/other/repo.git

# ローカルの既存プロジェクト + 要件ファイル
python main.py -w ./my-project -f todo-api.md

# ファイルなし、要件テキストを直接指定（git なし）
python main.py "ユーザー管理システムを開発"

# 対話モード
python main.py -i
```

---

## 4. Agent 一覧（6つ）

| Agent | コマンド | 役割 | 入力 | 出力 |
|-------|---------|------|------|------|
| **Dispatcher** | (自動) | 要件を分類し、パイプラインを選択 | 要件テキスト | `dispatcher/dispatch.json` |
| **Investigator** | `--investigate` | コード調査 / 技術リサーチ | コードベース or 要件 | `investigator/investigation.md` |
| **Analyst** | `--analyze` | 要件分析・サブタスク分割・実行者判定 | 要件テキスト | `analyst/analysis.md` |
| **Developer** | `--develop` | コード・ドキュメント生成 | サブタスク | `developer/development.md` |
| **Reviewer** | (自動) | 成果物レビュー・クロスシステム検査・修正指示 | 成果物一覧 + 要件 | `reviewer/review.md` |
| **Tester** | `--test` | テスト・セキュリティ監査 | コード + 受入基準 | `tester/test_report.md` |

### Dispatcher（分類者）

フルパイプライン実行時に最初に動作。要件を4種別に分類：

| 種別 | 判断基準 | パイプライン |
|------|---------|------------|
| **development** | コードの新規作成・修正が主目的。API/UI/ツール実装 | 全6フェーズ |
| **infrastructure** | サーバ/NW/クラウド基盤の設計書作成が主目的 | 全6フェーズ |
| **investigation** | 技術調査、比較検討、実現性分析 | Investigator のみ |
| **design_review** | 既存設計書のレビュー・補強 | Analyst + Developer |

### Investigator（調査者）

| モード | 条件 | 動作 |
|--------|------|------|
| コード調査 | `repo` が指定されている | 既存コードの技術スタック・アーキテクチャを分析 |
| 要件調査 | `repo` が未指定 | 要件に基づく技術リサーチ（実現性・コスト比較等） |
| 問題調査 | フェーズ6 | テストで検出された不具合の根本原因を特定 |

### Analyst（分析者）

各サブタスクの実行者を判定：

| 区分 | 説明 | 例 |
|------|------|-----|
| 🤖 AI | AI Agent が自動で完了可能 | コード生成、ドキュメント作成、テスト |
| 👤 Human | 人間が手動で行う必要あり | 外部サービス契約、承認、本番デプロイ |
| 🤝 Hybrid | AI が下書き → 人間が確認・実行 | 設計レビュー、コスト承認 |

### Developer（開発者）

- サブタスクを順番に実装
- **分離型出力形式**: JSON メタデータ + `<<<FILE:パス>>>` マーカーで文件内容を分離
  - JSON にはファイルパス・操作種別のみ（content フィールドなし）
  - ファイル内容はエスケープ不要で直接出力
  - 大型 Markdown / HTML ドキュメントでも安定して生成可能

### Reviewer（レビュー者）

Developer の成果物を自動検証し、不合格なら修正ループを実行：

```text
Developer 成果物 → Reviewer 検証 → 不合格？ → Developer 修正 → Reviewer 再検証
                                    │
                                    └─ 合格 → Tester へ
```

検証観点：
1. **ファイル完全性** — 空ファイル、内容切れの検出
2. **要件カバレッジ** — 要件の全ポイントが反映されているか
3. **クロスシステム整合性** — 要件が明示していない関連システムの設計漏れを検出
   - 例: MCC 設計書に対し、DNS/FW/Netskope/VPN/Intune の設計が不足 → 自動で補完指示
4. **品質チェック** — 設計の論理性、設定値の根拠、エビデンス URL

### Tester（テスター）

- 受入基準に基づく機能テスト
- コード品質レビュー
- セキュリティ脆弱性スキャン（OWASP Top 10 等）

---

## 5. 自己進化システム（学習 + 最適化）

各 Agent は **自己学習**（自動）と **自己最適化**（手動トリガー）の 2 段階で進化します。

### 学習記録

```text
agents/memory/
├── dispatcher.md      # Dispatcher の学習記録
├── investigator.md    # Investigator の学習記録
├── analyst.md         # Analyst の学習記録
├── developer.md       # Developer の学習記録
├── reviewer.md        # Reviewer の学習記録
└── tester.md          # Tester の学習記録
```

### 推奨運用サイクル

```text
① 通常運行    python main.py -f task.md     # 自動学習が蓄積される
② 数回実行後  python main.py --consolidate  # メモリを整理
③ 整理後     python main.py --optimize      # プロンプトを自己最適化
④ 次の実行    python main.py -f task.md     # 改善されたプロンプトで実行
→ ①に戻る
```

---

## 6. 実行フロー

### フルパイプライン（6フェーズ）

```text
[Dispatcher]      要件を自動分類（機能開発/基盤構築/調査/設計レビュー）
[█░░░░░] 1/6     Investigator  - 既存コードベースの事前調査
[██░░░░] 2/6     Analyst       - 要件分析、サブタスク分割、実行者判定
[███░░░] 3/6     Developer     - サブタスクごとにコード/ドキュメント生成
[████░░] 4/6     Reviewer      - 成果物レビュー → 不合格時は Developer 修正 → 再レビュー
[█████░] 5/6     Tester        - 機能テスト + セキュリティ脆弱性スキャン
[██████] 6/6     Investigator  - 検出された問題の原因調査・修正方針提案
                  ↓ 各フェーズ完了後に自己学習（教訓をメモリに保存）
```

### 単独 Agent の依存関係

```text
--investigate  : Investigator のみ
--analyze      : Analyst のみ
--develop      : Analyst → Developer
--test         : Analyst → Developer → Tester
（フル）        : Dispatcher → Investigator → Analyst → Developer → Reviewer → Tester → Investigator
```

### 進捗表示

| 環境 | 表示方法 |
|------|---------|
| TTY（ターミナル直接） | `⠹ [developer] 処理中... 03:24` スピナーアニメーション |
| 非 TTY（バックグラウンド） | `[developer] 生成中... 03:30 経過` 30秒ごとのログ |
| 共通 | `[███░░░] フェーズ 3/6 コード開発...` 進捗バー |

---

## 7. 結果の確認

### 7.1 生成されたコード / ドキュメント

```bash
ls workspace/<要件名>/
```

### 7.2 レポートファイル

```text
output/<要件名>/
├── dispatcher/
│   └── dispatch.json              # 要件分類結果
├── investigator/
│   ├── investigation.json / .md   # 事前調査レポート
│   └── post_investigation.json / .md # 問題調査レポート
├── analyst/
│   └── analysis.json / .md        # 要件分割結果（実行者判定付き）
├── developer/
│   └── development.json / .md     # 開発変更記録
├── reviewer/
│   ├── review.json                # レビュー結果（JSON）
│   └── review.md                  # レビューレポート（Markdown）
└── tester/
    └── test_report.json / .md     # テストレポート
```

---

## 8. ディレクトリ構成

```text
dev-pipeline/
├── main.py              # CLI エントリーポイント
├── requirements.txt     # Python 依存パッケージ
├── USAGE.md             # 本ドキュメント
├── README.md            # プロジェクト概要
├── core/
│   ├── config.py        # 設定（モデル、パス等）
│   ├── models.py        # Agent 間共有データモデル
│   ├── orchestrator.py  # パイプラインオーケストレーター
│   └── requirement_parser.py  # 要件ファイルパーサー
├── agents/
│   ├── base.py          # 基底クラス（CLI + 自己学習 + 自己最適化）
│   ├── dispatcher.py    # Dispatcher Agent（要件分類）
│   ├── investigator.py  # Investigator Agent（調査）
│   ├── analyst.py       # Analyst Agent（分析）
│   ├── developer.py     # Developer Agent（実装）
│   ├── reviewer.py      # Reviewer Agent（レビュー）
│   ├── tester.py        # Tester Agent（テスト）
│   ├── memory/          # 各 Agent の学習記録（自動蓄積）
│   └── prompts/         # 各 Agent の進化版プロンプト（--optimize で生成）
├── requirements/         # 要件ファイル配置ディレクトリ
├── workspace/            # コード出力（要件名ごとに分離）
└── output/               # レポート出力（要件名ごとに分離）
```

---

## 9. パラメータ一覧

| パラメータ | 説明 | 例 |
|-----------|------|-----|
| `要件テキスト` | 要件を直接指定 | `python main.py "要件の説明"` |
| `-f` | 要件ファイル（requirements/ 内を自動検索） | `-f todo-api.md` |
| `-i` | 対話モード | `--interactive` |
| `--investigate` | Investigator のみ実行 | `--investigate -f 調査.md` |
| `--analyze` | Analyst のみ実行 | `--analyze -f task.md` |
| `--develop` | Developer まで実行 | `--develop -f task.md` |
| `--test` | Tester まで実行 | `--test -f task.md` |
| `--memory` | 全 Agent のメモリを表示 | `--memory` |
| `--consolidate` | 全 Agent のメモリを整理・統合 | `--consolidate` |
| `--optimize` | 全 Agent のプロンプトを自己最適化 | `--optimize` |
| `--repo` | Git リポジトリ URL（ファイル内の値を上書き） | `--repo https://github.com/...` |
| `-b` | Git ブランチ名（ファイル内の値を上書き） | `-b feature/xxx` |
| `-w` | 作業ディレクトリを指定 | `-w ./my-project` |
| `-o` | レポート出力ディレクトリ | `-o ./reports` |
| `-m` | LLM モデルを指定 | `-m claude-opus-4-6` |
| `-v` | 詳細ログを表示 | `-v` |

---

## 10. よくある質問

### Q: Dispatcher はどうやって要件を分類する？
要件テキストを LLM に渡し、内容から自動判定します。コード実装なら `development`、設計書なら `infrastructure`、調査なら `investigation` を選択します。

### Q: Reviewer が不合格にしたらどうなる？
Reviewer の修正指示が Developer に自動で渡され、Developer が修正を実行します。修正後に Reviewer が再チェックします（修正ループは最大1回）。

### Q: Reviewer のクロスシステム検査とは？
1つのシステム変更は通常、複数の関連システムに影響します。例えば MCC サーバの設計書に対して、DNS/FW/Netskope/VPN/Intune の設計が不足していれば自動で検出し、追加の設計書作成を指示します。

### Q: 調査だけしたい（コード生成不要）
フルパイプラインで実行すれば Dispatcher が自動判定します。手動で指定する場合：
```bash
python main.py --investigate -f 調査.md
```

### Q: 大きなドキュメントの生成で失敗する？
Developer は分離型出力形式（JSON メタデータ + <<<FILE:>>> マーカー）を使用しており、大型 Markdown ドキュメントでも安定して生成できます。LLM 呼び出しのタイムアウトは最大30分です。

### Q: Agent はどうやって進化する？
2段階の仕組み：
1. **自己学習（自動）**: 毎回実行後に教訓を `agents/memory/` に蓄積
2. **自己最適化（手動）**: `--optimize` で教訓に基づき system prompt を自動改善

### Q: 最適化を元に戻したい
```bash
rm agents/prompts/developer.md   # Developer だけ戻す
rm agents/prompts/*.md           # 全 Agent を戻す
```
