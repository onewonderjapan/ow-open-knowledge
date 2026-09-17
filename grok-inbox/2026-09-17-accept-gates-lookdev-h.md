# 验收门增量（2026-09-17h）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-17-accept-gates-lookdev-h.md`
- **LEDGER_REF**：T2 `358914990553432064` / T3B `358915097483018240` / cycle 20260917h
- **SOURCE**：EigenFlux cycle 20260917h（已脱敏）
- **写入方**：管仓库的 · 2026-09-17
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 g 篇 `grok-inbox/2026-09-17-accept-gates-lookdev-g.md`；本篇只收相对 g 的全新八形。17g/f/e/d/c/b/a 已落盘，无需补写。

## 假绿又八形

1. **TRUNCATION_UNBOUND**：limit+1 / 空集过但 limit 减半覆盖率漂移；上限未绑定记录。
2. **SELF_SERVED_CACHE_HIT**：`served_by` == `snapshot.issuer`；不进独立命中率分母。
3. **EPOCH_MIXED_INCOMPARABLE**：跨 epoch 并表不可比（≠ UNMAPPED_REASON）。
4. **WINDOW_UNCLOSED_EVENT_MISSING**：轮换冻结缺窗未闭合事件 → UNVERIFIED_WINDOW。
5. **DIEGETIC_UNANCHORED**：角色可闻声未进 `timeline_events`；分段重渲。
6. **OVERRIDE_UNTRACKED**：参数覆盖无 prev / next digest 回执。
7. **GRAPH_RECONSTRUCTED**：事后补引用图谱不进缺陷率分母；计数用事件流最大重放值。
8. **COMPOSITE_SUITE_STALE**：`fields_rev` 变更未重签组合用例；与 `skillset_digest` 分列。

## 去重说明

g 已覆盖 DENOMINATOR_ORPHAN、AUTO_CLOSE_REJECTED、CACHE_EVENT_INCOMPLETE、UNMAPPED_REASON、UNANCHORED_WINDOW、IDENTITY_RECEIPT_REWRITE、READBACK_RETRY_JITTER、LABEL_GATE_INCOMPLETE。本篇收 20260917h 续八形（全部新码）。