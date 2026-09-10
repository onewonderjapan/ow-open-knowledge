# ow-open-knowledge

OneWonder Japan の公開ナレッジベース。実戦で検証してきた AI エージェント育成の方法論、企業 AI 導入の最小構成アーキテクチャ、自動化ワークフロー標準、マルチエージェント開発パイプライン、クラウドパターン、チーム規範をオープンソースとしてまとめたものです。

[English](README.md) | [简体中文](README.zh-CN.md) | 日本語

![License](https://img.shields.io/badge/license-MIT-blue)

## このリポジトリについて

**これは**: 実務ラインで繰り返し検証された働き方の知見です——AI エージェントの育て方、クローズドループ型自動ワークフローの作り方、企業 AI 導入の最小パイプラインの姿。参考実装はそのまま動きます。

**こうではない**: 顧客事例集でもプロダクトのコードベースでもありません。顧客情報・社内戦略・未公開 IP は含まず、デモデータはすべて架空です。

**言語**: README は英語が主体です。元ドキュメントは原文（日本語・中国語、またはその混在——チームが実際に書いたまま）です。中核となる方法論ドキュメントの翻訳は歓迎します。

## 目次

| ディレクトリ | 内容 |
|------|------|
| ⭐ [agent-cultivation/](agent-cultivation/) | **最重要資産**。AIエージェント育成標準（5箇条＋三層固化）、既存エージェント訓練ガイド、新プロジェクト STARTUP 標準、データ分類ルール、個人ワークベース skill セット |
| [ai-stack/](ai-stack/) | 企業 AI 導入の参考実装：要件書→マスキング→社内先例検索（RAG）→LLM 起草→ローカル質検の E2E 薄切片 |
| [workflow-standard/](workflow-standard/) | 自動化ワークフロー構築標準：四段階クローズドループ＋7つの鉄則＋新規ワークフロー用スキャフォールド |
| [task-orchestrator/](task-orchestrator/) | 自然言語タスクのマスター skill：skill ルーティング→計画承認→継続実行→層別学習（標準ライブラリのみ） |
| [dev-pipeline/](dev-pipeline/) | 6 エージェント開発パイプライン：Dispatcher / Investigator / Analyst / Developer / Reviewer / Tester＋自己学習 |
| [cloud-patterns/](cloud-patterns/) | クラウドパターン skill 集：Glue×RDS 結合、API Gateway＋Lambda＋SES 問い合わせフォーム、Form→IAM、Terraform の落とし穴 |
| [team-norms/](team-norms/) | チーム規範（日本語）：Git 使用規範、Teams チャットマナー、ビジネスメール基礎 |

## クイックスタート

一番速く全体像を掴む方法——ai-stack のオフラインデモ（API キー不要、動作検証済み）：

```bash
cd ai-stack
python -m venv .venv
# Windows (Git Bash / PowerShell)：
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub
# macOS / Linux：
# source .venv/bin/activate && pip install -r requirements.txt
# python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub
```

出力は3点セット：送信内容のマスキング結果（`out/*_masked.md`）、設計書ドラフト（`out/*_draft.md`）、監査レポート（`out/*_report.json`）。

依存ゼロのデモ Web UI（標準ライブラリのみ）もあります：

```bash
python ui/app.py    # → http://127.0.0.1:7877
```

> 注意：パイプライン自体は stub モードでも `janome`（RAG 層）が必要です。`anthropic` は API プロバイダ利用時のみ。Web UI のみ完全に依存ゼロです。

## 関連公開リポジトリ

- [form2cloudbuilder](https://github.com/onewonderjapan/form2cloudbuilder) — Microsoft Form の入力から AWS/Azure リソースを作成
- [wonder-contact-terraform](https://github.com/onewonderjapan/wonder-contact-terraform) — ホームページ問い合わせフォームのインフラ（Terraform）
- [rds-glue-s3-etl-pipeline](https://github.com/onewonderjapan/rds-glue-s3-etl-pipeline) — AWS Glue (PySpark) ETL：S3 JSON と RDS の結合、Secrets Manager 認証情報管理、Slack 通知
- [owd-knowledge-hub](https://github.com/onewonderjapan/owd-knowledge-hub) — 組織ナレッジポータル

## コントリビュート

Issue・PR を歓迎します。詳しくは [CONTRIBUTING.md](CONTRIBUTING.md) を参照。

## License

[MIT](LICENSE)
