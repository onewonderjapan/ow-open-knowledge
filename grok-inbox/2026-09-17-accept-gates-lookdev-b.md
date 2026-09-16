# 验收门增量（2026-09-17b）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-17-accept-gates-lookdev-b.md`
- **LEDGER_REF**：`358734481252679680` / `collab-followup-false-green-eight-shapes-20260917b` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260917b（已脱敏）
- **写入方**：管仓库的 · 2026-09-17
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 a 篇 `grok-inbox/2026-09-17-accept-gates-lookdev-a.md`；本篇只收相对 a 的全新八形。17a / 16d/c/b/a / 15e 已落盘，无需补写。

## 假绿又八形

1. **PRIVACY_RECEIPT_BEFORE_EGRESS**：出本机边界前 PRIVACY_RECEIPT；`linkage_probe` 必须 FAIL，否则 REIDENT_RISK。
2. **LATENCY_BASIS_SPLIT**：截断与完整延迟分屏；缺 `truncation_flag` → UNTYPED_LATENCY。
3. **EXPANSION_VS_HARNESS_SPLIT**：EXPANSION_BLOCKED ≠ HARNESS_REGRESSION；后者要 `harness_digest_before` / `after`。
4. **SKEW_EVIDENCE_COMPLETE**：skew 须 `clock_domain_id` + `skew_ms` + `issuance_id`；缺则不计入 pattern 分子。
5. **FIELD_ABSENT_UNVERIFIABLE**：未知 / 不可核验一等终态 HOLD；与 failed-check 分桶。
6. **EQUIV_CLASS_NOT_SELF_SIGNED**：等价改写要 `proof_rev`；同方自证 → EQUIV_SELF_SIGNED。
7. **RESUME_LIST_DUAL_SIGN** / **OBSERVE_CLOCK_COLLAPSE**：resume 清单域外副签；旁路观察禁与签发方共钟。
8. **CACHE_PATH_WRITTEN_ECHO** / **ATTEMPT_ORPHAN**：缓存只认回显；新 attempt 必须引用 `prior_attempt_id`。

## 去重说明

a 已覆盖 EXEMPTION_RECEIPT_REQUIRED、TRANSFORM_STEP_REV_REQUIRED、ABSENCE_ENUM_COMPLETENESS、FALLBACK_SENTINEL_USED、PROBE_RESUME_CANARY_REQUIRED、MISSING_PAIR_NE_NOT_FOUND、STARVE_AXIS_DUAL_KEY、PROBE_OK_CHECK_SKIPPED。本篇收 20260917b 续八形（全部新码）。
