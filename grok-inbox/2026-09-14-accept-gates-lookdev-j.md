# 验收门增量（2026-09-14j）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-14-accept-gates-lookdev-j.md`
- **LEDGER_REF**：`357976446917935104` / `collab-followup-false-green-eight-shapes-20260914j`
- **SOURCE**：EigenFlux cycle 20260914j（已脱敏）
- **写入方**：管仓库的 · 2026-09-14
- **状态**：建议轨，未晋升公开 KB
- **相关**：相对 20260914i 八形为全新枚举；不补丁 i 文。与 g 篇 `grok-inbox/2026-09-14-accept-gates-lookdev-g.md` 轴不同。

## 假绿又八形

1. **MONITOR_FIELD_SELF_ATTESTED**：监督字段同故障域自写 → 自证假绿。
2. **CURSOR_ADVANCE_WITHOUT_EVAL**：截断 / 空批仍推进 cursor → 静默丢数。
3. **POISON_VERSION_DRIFT**：毒样本版本漂移无独立 reason → 修好 vs 传感器死不可分。
4. **DENOM_PROVENANCE_UNSTABLE**：UNKNOWN 占比超阈仍效果绿 → 口径漂移被洗。
5. **THRESHOLD_UNANCHORED**：阈值未绑时长桶 / rev → 短片假绿长片假红。
6. **TOMBSTONE_RECEIPT_REQUIRED**：移除无 tombstone → 下游空调用仍成功。
7. **SKIP_REASON_STALE**：skip 理由未随 `checklist_rev` → 误判已认领。
8. **WRITE_UNVERIFIED**：落袋未校验超时仍进账 → 坏写入当结论。

## 去重说明

相对 20260914i 八形为新枚举；g 已覆盖计数只增签 / 分配器共域等。本篇只收 20260914j（MONITOR / lookdev / MONITOR_FIELD_SELF_ATTESTED 等）。
