# ai-stack — 企業AI導入の参考実装（薄切片）

[English](README.md) | 日本語（オリジナル版）

![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue)

「要件書 → 脱敏 → 社内先例検索(RAG) → クラウドLLM起草 → ローカル質検」の
エンドツーエンド最小実装。営業デモ・社内ドッグフーディング・顧客PoCの土台。

## クイックスタート

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt    # janome（任意。RAG の形態素解析）

# ネット不要のデモ(スタブ応答)
python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub

# 本物のClaude(Claude Code サブスク認証を流用、APIキー不要)
python pipeline/run.py demo_data/incoming/new_rfp.md --provider claude-cli

# 本番向け(要 ANTHROPIC_API_KEY)
pip install -r requirements-llm.txt
python pipeline/run.py demo_data/incoming/new_rfp.md --provider anthropic-api

# デモ用Web UI（標準ライブラリ。janome は任意）
python ui/app.py   # → http://127.0.0.1:7877
```

出力: `out/<name>_draft.md`(設計書ドラフト) / `out/<name>_masked.md`(脱敏後の送信内容) / `out/<name>_report.json`(監査レポート)

## 構成と「本格版」への差し替え計画

| ディレクトリ | 薄切片の実装 | 本格版(差し替え先) |
|---|---|---|
| `masking/` | 正規表現+辞書+パターン | + GiNZA(NER)、法務レビュー済みルール |
| `rag/` | janome+BM25 | multilingual-e5 + Qdrant、権限フィルタ |
| `llm/` | stub / claude-cli / anthropic-api | + AIゲートウェイ(LiteLLM)経由で多社対応 |
| `evalkit/` | 決定論的構造検査 | + LLM-as-judge rubric採点、回帰テスト集 |
| `pipeline/` | CLI一本道 | ジョブキュー化、Web UI |

インターフェースは据え置きで各層を独立に厚くできる設計。

## デモの見せ方（営業向け）

1. `demo_data/incoming/new_rfp.md` を開いて見せる — 実名・電話・予算が入った"生"の要件書
2. パイプライン実行 → `out/new_rfp_masked.md` を見せる — **「クラウドに渡ったのはこれだけです」**（実名ゼロ）
3. `out/new_rfp_draft.md` — 社内の章立て通りの設計書ドラフト、過去2案件を参照済み
4. `out/new_rfp_report.json` — 誰が何を送りどう検査したかの監査証跡

## 注意

- `demo_data/` は全て架空の会社・人物・案件です
- `claude-cli` プロバイダは PoC/社内利用専用（サブスク規約準拠）。顧客本番は API 契約に切替
- 踩んだ坑は `../agent-cultivation/PITFALLS.md` に追記していくこと（これ自体が商品）
- 段階的アップグレードは [../ROADMAP.md](../ROADMAP.md)

## ディレクトリ構成

```text
ai-stack/
├── pipeline/run.py        # CLI 一本道（mask → RAG → draft → check）
├── masking/               # 脱敏層（正規表現+辞書 / masker.py・entities.json）
├── rag/                   # 社内先例検索（janome+BM25、未導入時はバイグラム）
├── llm/                   # provider 差し替え（stub / claude-cli / anthropic-api）
├── evalkit/               # 決定論的構造検査（structure_check.py）
├── ui/app.py              # 標準ライブラリのデモ Web UI
├── tests/                 # 脱敏・質検・stub パイプライン
├── tools/                 # md→pptx 変換・pptx抽出
├── demo_data/             # 全て架空のデモデータ
└── templates/             # 新プロジェクトのスケルトン
```

方法論（育成標準・STARTUP標準・PITFALLS 等）は [../agent-cultivation/](../agent-cultivation/) を参照。

## License

MIT — 詳細は [../LICENSE](../LICENSE) を参照。
