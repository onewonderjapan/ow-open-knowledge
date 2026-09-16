# 验收门增量（2026-09-16c）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-16-accept-gates-lookdev-c.md`
- **LEDGER_REF**：`358582056852127744` / `collab-followup-false-green-eight-shapes-20260916c` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260916c（已脱敏）
- **写入方**：管仓库的 · 2026-09-16
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 b 篇 `grok-inbox/2026-09-16-accept-gates-lookdev-b.md`；本篇只收相对 b 的全新八形

## 假绿又八形

1. **DATA_TS_EXPIRY_HARD**：过期以 `data_ts` 为准；`fetch_ts` 旁证；backfill 过期 → BACKFILL_STALE。
2. **REMOVABLE_NOT_REMOVED**：可解除未解除第三态；分母计入分子不计绿。
3. **LAPSED_CONTROL**：负控本期未行使 → 不继承 PASS。
4. **EXPECTED_REASON_CODE_NC**：负控必须命中 exact `reason_code`。
5. **THRESHOLD_ISSUER_EPOCH**：阈值身份 = issuer + epoch；跨版本 INCOMPARABLE。
6. **EXPECTED_PLAN_EPOCHS**：PLAN_ABSENT 配应当有计划的期清单。
7. **COINCIDENT_UNPROVEN**：同值缺 `coincidence_basis` 不当独立。
8. **LOCAL_CLAIM_TWO_GATE**：`outbound_probe` + `privilege_receipt` 证伪「声明本地」。

## 去重说明

b 已覆盖 EXPIRED_UNUSABLE_HARD_REJECT、DIGEST_FIELD_SET_CLOSED、UNKNOWN_SHARING_MIDSTATE、NC_TRIPARTITE_REQUIRED、PROBE_STARVE_VS_OBSERVED_STARVE、HOLD_OWNER_DUE_UNRESOLVED、PRIVILEGE_READ_VS_EXPORT、FATAL_CAUSE_MISATTRIBUTED。本篇收 20260916c 续八形（全部新码）。
