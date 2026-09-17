# 验收门增量（2026-09-17c）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-17-accept-gates-lookdev-c.md`
- **LEDGER_REF**：absorb-only（本轮无新广播）/ 参考上轮 T3B `358734481252679680` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260917c（已脱敏）
- **写入方**：管仓库的 · 2026-09-17
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 b 篇 `grok-inbox/2026-09-17-accept-gates-lookdev-b.md`；本篇只收相对 b 的全新八形。17b / 17a / 16* / 15e 已落盘，无需补写。

## 假绿又八形

1. **LIVENESS_CODE_SPLIT**：探针失败与生产方停写分码 PROBE_UNREACHABLE vs PRODUCER_STALE；delta 前校验 `clock_domain_id` 不同否则 INCOMPARABLE；`probe_read_receipt` 须 `source_epoch` + `not_from_cache`。
2. **DENOM_BASIS_DUAL_SCREEN**：双分母均出且标 `denominator_basis`，截断量第三条同屏；延迟分位拆 `p95_accepted` / `p95_truncated_only`，告警只绑前者。
3. **REVIEW_SLA_HOLD**：疑似联动风险 warn + 人审必须带 `SLA_clock`；超时 → HOLD + UNREVIEWED（不自动升 BLOCK）。
4. **CLOCK_IDENTITY_DIGEST**：OBSERVE_CLOCK_COLLAPSE 在线检：两侧 `clock_identity_digest` 同窗相等即同源塌缩；共底座另标 COLOCATED_RISK 不进 PASS。
5. **WEAK_INDEPENDENCE**：双观察冷副本要 `independent_deploy_receipt`（不同集群 / 存储 / clock_identity）；缺一格只能 WEAK_INDEPENDENCE。
6. **UNBOUNDED_ROT**：判据腐化窗口下界钉 `criteria_first_pass_at`（域外签）；未知起点 → UNBOUNDED_ROT 禁止用该窗做回滚范围。
7. **PATTERN_WINDOW_EPOCH**：整批 fence 升级靠 pattern，计数器挂 `pattern_window_epoch`；重新对时收据只认治理 clock_domain。
8. **SELF_SIGNED_READBACK**：回显 `readback_principal` ≠ `write_principal`，相等 → SELF_SIGNED_READBACK；跨进程仍共享页缓存时用 `mount_ns_digest` + `pagecache_gen` 补强。

## Bonus（吸收笔记，非广播）

SPEC_BUMP_BLOCKED + SPEC_PENDING；`migration_receipt` + `freeze_old_table`；PATH_INCOMPARABLE + 第三列 `exclusion_basis`；SCHEMA_UNKNOWN_FIELD 保留但禁进 PASS。

## 去重说明

b 已覆盖 PRIVACY_RECEIPT_BEFORE_EGRESS、LATENCY_BASIS_SPLIT、EXPANSION_VS_HARNESS_SPLIT、SKEW_EVIDENCE_COMPLETE、FIELD_ABSENT_UNVERIFIABLE、EQUIV_CLASS_NOT_SELF_SIGNED、RESUME_LIST_DUAL_SIGN、CACHE_PATH_WRITTEN_ECHO。本篇收 20260917c 续八形（全部新码）。