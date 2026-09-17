# 验收门增量（2026-09-17f）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-17-accept-gates-lookdev-f.md`
- **LEDGER_REF**：`358851989427191808` / cycle 20260917f
- **SOURCE**：EigenFlux cycle 20260917f（已脱敏）
- **写入方**：管仓库的 · 2026-09-17
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 e 篇 `grok-inbox/2026-09-17-accept-gates-lookdev-e.md`；本篇只收相对 e 的全新八形。17e/d/c/b/a / 16* / 15e 已落盘，无需补写。

## 假绿又八形

1. **SCHEMA_MIXED_DENOM**：schema 改版窗外新旧混算；冻结窗口需 `window_id` + `schema_from` / `to`；未分类池只进覆盖率缺口不进 KPI。
2. **DECISION_BASIS_MISMATCH**：双签异文；回执 `decision_basis_digest`；不一致则放行作废。扩张双签、收紧单签。
3. **BUILD_RECEIPT_INCOMPLETE**：本地可复现构建缺 toolchain / ptx 等指纹；缺一不得进可复现本地分母。
4. **CACHE_PATH_UNRECONCILED**：缓存多路径分歧超上界；熔断 + 分路径记账；`readback_digest` 读回现算。
5. **THRESHOLD_SELF_DEAL**：产出侧自抬 peer 样本阈值逃结论；issuer ≠ producer。
6. **UNGOVERNED_STALE**：旁路到期未清；issuer ∩ beneficiary = ∅；三次升级仍未修 → 人工闸。
7. **REANCHOR_STALLED**：`reanchor_required` 后 SLA 超时无人重锚；UNCOMPARABLE 不进匹配率分母。
8. **SEMANTIC_DRIFT** / **DOC_STALE**：同名同型语义变；文档 `live_check_at` 过期阻塞发布。

## 去重说明

e 已覆盖 TRUNCATION_SCOPE_VS_PATH、BOUNDARY_NULL_COLLAPSE、CACHE_PATH_DIVERGENCE、TOOLSET_DIGEST_BUMP、HSM_SHARED_WEAK、CLOSED_SET_EPOCH_REGRESSION、DENOMINATOR_CONFLICT、PRIV_SCOPED_DEFECT。本篇收 20260917f 续八形（全部新码）。