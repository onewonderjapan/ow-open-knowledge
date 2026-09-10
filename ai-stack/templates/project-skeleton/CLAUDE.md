# <プロジェクト名> — Agent規約

> STARTUP標準 v1.0 準拠。コピー元: ai-stack/templates/project-skeleton/（本リポジトリ）
> 原則の正本: ../../agent-cultivation/AGENT育成標準.md

## Day-0 決定事項（最初に埋める）

- **正典（ground truth）**: <何が正しさの基準か。ファイル/場所を明記>
- **機密等級**: <なし / 社内 / 顧客機密 — 顧客機密なら local_data/ 分離+gitignore 必須>
- **生成/QC分離**: 生成=<agent名> / QC=<agent名>（兼務禁止）
- **借用する共用ツール**: <ai-stack: md→pptx渲染器・構造検査器・脱敏器 / 他PJ: lora-train 等>

## 鉄則（全agentが従う）

1. 正典と派生物を混同しない。同一性/正しさの判定は必ず正典と比べる。
2. 生成のたびに `library/outcomes/outcomes.jsonl` へ1行（成功も失敗も）。未記録の成功は工程違反。
3. 坑を踏んだら同セッション内に `docs/PITFALLS.md` へ記録し、固化先（コード/規律/記憶）を決める。
4. 採用作で強かったものは `library/gold/` へ注釈付きで回流。
5. QCは疑わしきは不合格。数えられるものは1つずつ数える。
