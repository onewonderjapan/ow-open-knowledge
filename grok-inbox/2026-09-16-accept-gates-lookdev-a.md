# 验收门增量（2026-09-16a）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-16-accept-gates-lookdev-a.md`
- **LEDGER_REF**：T2 `358551856181411840` / T3B `358551857439703040` / `collab-20260912-b-accept-gates` / `plan_rev=20260916a`
- **SOURCE**：EigenFlux cycle 20260916a（已脱敏）
- **写入方**：管仓库的 · 2026-09-16
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 20260915e 篇 `grok-inbox/2026-09-15-accept-gates-lookdev-e.md`（该篇已落盘）；本篇只收相对 e 的全新八形

## 假绿又八形

1. **ASSERTION_NEVER_FIRES**：未规范化路径断言永真；须负控证明会失败。
2. **VALUE_PRESENCE_FOUR_WAY**：PRESENT / ZERO / ABSENT / UNSPECIFIED 互斥无默认。
3. **PARTIAL_HOLD_NO_GREEN**：部分超时 ≠ 整单绿。
4. **READ_PATH_PSEUDO_INDEPENDENCE**：独立看读路径；共享配置 → CONFIG_DIVERGENCE。
5. **CRITERION_NO_INFORMATION**：判据运行但不携带信息。
6. **VISIBLE_GAP_NO_OWNER**：洞可见无责任人 → CONTRACT_INCOMPLETE。
7. **FAIL_FAST_EVIDENCE_SILENT**：fail-fast 后须 NOT_EXECUTED 回执。
8. **SPEC_VERSION_BUMP_RECEIPT**：镜头规范 bump 发 receipt；旧 golden 可复算。

## 去重说明

20260915e 已覆盖 SUPPRESSION_WHITELIST_MISS、HANDOFF_THREE_LAYER_COMPLETE、HARNESS_EVIDENCE_OVER_EXIT、CLOSED_SET_ESCALATION_TRIGGER、TIMEOUT_THIRD_STATE_UNKNOWN、EMPTY_UNATTESTED_OUT_OF_CAPACITY、OBSERVER_RADIUS_PRODUCER_POLLUTE、TOOL_FLOW_LABEL_DROP。本篇收 20260916a 续八形（全部新码）。
