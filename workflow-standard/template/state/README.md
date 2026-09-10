# state/ —— 持久化状态（STANDARD.md §5）

- `strategy.md`  当前逻辑，唯一真源，人可读，改善时追加变更日志。
- `portfolio.json` 当前状态快照，可覆盖；旧值可从 ledger 复原。
- `ledger.jsonl`  只追加：操作/交易流水（每行含 run_key/ts/schema_version）。
- `scorecard.jsonl` 只追加：每轮评分。

规则：历史行永不删改；机密绝不入库；schema 变更递增 schema_version。
