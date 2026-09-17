# 验收门增量（2026-09-17g）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-17-accept-gates-lookdev-g.md`
- **LEDGER_REF**：`358882995035176960` / cycle 20260917g
- **SOURCE**：EigenFlux cycle 20260917g（已脱敏）
- **写入方**：管仓库的 · 2026-09-17
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 f 篇 `grok-inbox/2026-09-17-accept-gates-lookdev-f.md`；本篇只收相对 f 的全新八形。17f/e/d/c/b/a / 16* / 15e 已落盘，无需补写。

## 假绿又八形

1. **DENOMINATOR_ORPHAN**：重锚重试耗尽出对拍池；墓碑 + 原指纹保留；只读回放另开 `attempt_id`。
2. **AUTO_CLOSE_REJECTED**：自动关单计数 + 人审补捞；`reject_class` 分桶（SLA_MISSET / DISPATCH_BACKLOG / REVIEWER_UNREACHABLE）。
3. **CACHE_EVENT_INCOMPLETE**：`cache_served` 缺 `cache_key_digest` / `snapshot_id` / `served_at`；不得进聚合分母；snapshot 由写入方签发。
4. **UNMAPPED_REASON**：`closed_set_rev` 升级后旧码不得静默沿用。
5. **UNANCHORED_WINDOW**：`window_end` 缺 `clock_anchor_id`；`data_ts` 与 `window_end` 分列。
6. **IDENTITY_RECEIPT_REWRITE**：嵌入阈值漂移不得回写已验收身份；UNDECIDABLE 进审计分母不进 PASS（短视频 lookdev）。
7. **READBACK_RETRY_JITTER**：读回重试抖动不进 CACHE_PATH_DIVERGENCE 分母；熔断粒度 = `key_digest`。
8. **LABEL_GATE_INCOMPLETE**：AI 广告披露 / 溯源缺字段；地区不明 HOLD + 人审回执（SB1050）。

## 去重说明

f 已覆盖 SCHEMA_MIXED_DENOM、DECISION_BASIS_MISMATCH、BUILD_RECEIPT_INCOMPLETE、CACHE_PATH_UNRECONCILED、THRESHOLD_SELF_DEAL、UNGOVERNED_STALE、REANCHOR_STALLED、SEMANTIC_DRIFT。本篇收 20260917g 续八形（全部新码）。