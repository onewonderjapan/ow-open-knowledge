# 验收门增量（2026-09-12i）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：多路径合并落 inbox：`grok-inbox/2026-09-12-accept-gates-lookdev-i.md`
- **LEDGER_REF**：`357222406919553024` / `collab-followup-accept-gates-lookdev-20260912i` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 2026-09-12i（已脱敏）
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 h 篇 `grok-inbox/2026-09-12-accept-gates-lookdev-h.md`；本篇只收相对 h 的新增量

## 1. dictionary_rev_pinned / schema_drift|dict_drift

读通路三回执；在途禁切口径。

## 2. STALE_REJECT + replay_of_receipt_id

门拒重放重算指纹；旧拒只追加；`GATE_UNRESPONSIVE` 审计分域。

## 3. PROBE_COLLECTOR_COLOCATED

探活采集方与 SUT 共因整段作废。

## 4. QUIESCE_POLICY_DRIFT

cutover N tick 为常量；改 N 必抬 `policy_rev`。

## 5. retired_inherit_digest

跨 policy bundle retired 只追加继承。

## 6. AS_OF_ISSUER_UNVERIFIED

issuer `principal_set` ∩ DNS 空则 freshness 作废。

## 7. credit 弱归因负表

`credit_event_class` + `attribution_window` + `unique_user_key` + `content_version_digest`。

## 8. NOT_COMPARABLE 面板

禁进主趋势；晋升须新 receipt。

## 9. DEGRADED_COMPENSATION_PENDING / COMPLETION_UNPROVEN

对外禁 success / 空结果。

## 10. REKEY_EXPIRED + grace 死日期

旧 key 只验 cutover 前在途；`drill=true` 演练。

## 11. lease 三字段 + return_evidence digest

校验方与签发方分域。

## 12. ASSERT_FAIL vs HOLD_UNDECIDABLE

分桶进分母，禁混记。

## 13. authority_batch_id → DRIFT_COUPLED

缺 batch 同变分别 FAIL。

## 14. 登记 schema_rev 第三方签 → UNPROVEN

## 15. SAME_SOURCE 精化

同宿主 / 同时钟锚 / 同母机算交集非空。

## 16. VERSION_SKEW → RECALIBRATING

独立 trust domain `recalibration_receipt` 才解除。

## 17. provenance ∈ {writer_attested, reconstructed, unknown}

另：`SPEC_UNANCHORED`。

## 18. SELFTEST_INSENSITIVE

正控必红自检报不出 = 哨兵钝。

## 去重说明

h 已覆盖 AS_OF_COLOCATED / CLOCK_ANCHOR_STALE / ENUM_REV_MISMATCH / SAME_SOURCE 分桶 / fingerprint_spec 等。本篇只收 i 增量（门拒重放 STALE_REJECT、探活共因、口径钉死等）。
