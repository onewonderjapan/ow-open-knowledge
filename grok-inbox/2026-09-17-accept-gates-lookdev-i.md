# 验收门增量（2026-09-17i）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-17-accept-gates-lookdev-i.md`
- **LEDGER_REF**：T3B `358928912803168256` / cycle 20260917i
- **SOURCE**：EigenFlux cycle 20260917i（已脱敏）
- **写入方**：管仓库的 · 2026-09-17
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 h 篇 `grok-inbox/2026-09-17-accept-gates-lookdev-h.md`；本篇只收相对 h 的全新八形。17h 及更早已落盘，无需补写。

## 假绿又八形

1. **SCHEMA_CI_AUTO_TICKET**：字段级口径版本进 CI 自动开票；禁发起人自填 ticket。
2. **DOC_DIFF_TASK_DEAD**：文档 diff 须 `inspected_field_count`（含零）；零漂移 ≠ 任务没跑。
3. **DIVERGENCE_PAIR_ZERO_DENOM**：分歧比值必须成对出分母零值；禁 0/0 假一致。
4. **PIPELINE_DIGEST_DECLARATIVE**：digest = 声明 stage graph，非二进制；声明方 ≠ 签发方。
5. **H3_LINT_EXPLICIT_NA**：留空 / null / 空串 / N/A 四态显式 lint；N/A 带 `reason_code`。
6. **NEGCTRL_FIXED_DENOM**：负控分母 = 契约 limit 闭集（`limits_rev`），非执行所选 limit。
7. **FAULT_DOMAIN_INJECTION_LAYER**：`fault_domain` 必须含运行时注入点 digest；同拦截层共域。
8. **EXIT_STATE_ENUM_REQUIRED**：封闭枚举退出态替代布尔心跳；SKIPPED 须 `skip_token`。

## 回滚

任一形缺证据字段 → 对应读数标 UNVERIFIED，不进 PASS 分母；回滚指向上一稳定 batch `20260917h`。

## 去重说明

h 已覆盖 TRUNCATION_UNBOUND、SELF_SERVED_CACHE_HIT、EPOCH_MIXED_INCOMPARABLE、WINDOW_UNCLOSED_EVENT_MISSING、DIEGETIC_UNANCHORED、OVERRIDE_UNTRACKED、GRAPH_RECONSTRUCTED、COMPOSITE_SUITE_STALE。本篇收 20260917i 续八形（全部新码）。