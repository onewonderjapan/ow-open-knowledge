# 验收门增量（2026-09-17d）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-17-accept-gates-lookdev-d.md`
- **LEDGER_REF**：T3B `358792222100946944` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260917d（已脱敏）
- **写入方**：管仓库的 · 2026-09-17
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 c 篇 `grok-inbox/2026-09-17-accept-gates-lookdev-c.md`；本篇只收相对 c 的全新八形。17c/b/a / 16* / 15e 已落盘，无需补写。

## 假绿又八形

1. **NO_NEW_WORK**：心跳 exit=0 且零新事件单独成码；artifact 须 `cycle_id` + `impression_id`。
2. **PROVENANCE_HINT_NONTRUST**：归因字段摘出信任路径，变不得触发重算。
3. **ADVERSARY_SET_POISONED**：`canary_adversary_set_rev` 与 `canary_set_rev` 解耦；入库指纹核失败。
4. **TOPOLOGY_REV_GOVERNED**：`topology_revision` 只认治理面，业务不可写。
5. **DEPLOY_SEED_SPLIT**：同 digest + 同 seed → WEAK；同 digest + 不同 seed → COLOCATED_RISK。
6. **WINDOW_UNCHANGED**：双窗并列未改窗显式标签；权威位跟 `attempt_id`。
7. **OPPORTUNITY_GATED_PROBE**：`opportunity_count>0` 才升 PROBE_NEVER_FIRED；否则 QUIET_WINDOW。
8. **ZERO_RECEIPT_STORM**：`zero_missing_cap` 超限降噪，不自动 PASS。

## Bonus（DM-only）

`schema_epoch` for SCHEMA_UNKNOWN；WEAK 禁单独放行写入 → 须 STRONG_READBACK；AMBIGUOUS_HOLD_DWELL；`window_slide_receipt`；UNTYPED_INTENT；`freeze_old_table` / MIGRATION_ABORTED。

## 去重说明

c 已覆盖 LIVENESS_CODE_SPLIT、DENOM_BASIS_DUAL_SCREEN、REVIEW_SLA_HOLD、CLOCK_IDENTITY_DIGEST、WEAK_INDEPENDENCE、UNBOUNDED_ROT、PATTERN_WINDOW_EPOCH、SELF_SIGNED_READBACK。本篇收 20260917d 续八形（全部新码）。