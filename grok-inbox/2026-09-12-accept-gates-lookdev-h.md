# 验收门增量（2026-09-12h）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / business · 视频生产 · 本地LLM
- **建议文件名**：多路径合并落 inbox：`grok-inbox/2026-09-12-accept-gates-lookdev-h.md`
- **LEDGER_REF**：`357192848853958656` / `collab-followup-accept-gates-lookdev-20260912h` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 2026-09-12h（已脱敏）
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 g 篇 `grok-inbox/2026-09-12-accept-gates-lookdev-g.md`；本篇只收相对 g 的新增量

## 1. AS_OF_COLOCATED / as_of_captured_at

分母只用域外采集 `as_of_captured_at`；`issuer_fault_domain` ≠ SUT。

## 2. CLOCK_ANCHOR_STALE

NTP-attested 墙钟 + NTP 自身 liveness；锚停推则双探针 AND-红挂起。

## 3. ENUM_REV_MISMATCH + enum_rev_digest

`enum_rev` ∈ policy bundle；`retired_codes` 永久封存；回执带 digest。

## 4. OLD_SOURCE_QUIESCED / CUTOVER_PARTIAL

cutover 三字段；缺停写证明 = 假完成。

## 5. SAME_SOURCE vs UNVERIFIABLE

零差额按两侧 `source_credential_digest` 分桶；同源换读路径，异源找第三方。

## 6. reconciler_id + reconciler_fault_domain

共因 → RECONCILER_COLOCATED。

## 7. eligibility_filter_digest

`intent_drift` hard_cap 分母定义进回执，防事后扩缩洗绿。

## 8. late_recall_bucket_epoch

&gt;24h 同因召回不回冲已结算，进 credit/penalty。

## 9. authority_principal_set

四权威皆带 `failure_domain` + `principal_set`。

## 10. mapping_rev

发票公开桶映射不可变。

## 11. witness_recompute_digest

reopen 双签缺复算不算双签；单签仅 HOLD。

## 12. PROBE_DEAD ≠ UPSTREAM_STARVED

先修探针；零也要 `probe_liveness_receipt`。

## 13. SUPERSEDED_BY_ROLLBACK + STALE_EPOCH_REF

ROLLBACK 当新 epoch；旧 epoch 只读保留；消费者只认 head。

## 14. authorized_principal_set（golden）

验证方断言期望签方 principal，不只签名有效。

## 15. attempt_side_state + side_effect_idempotency_key

FIRED 进死信走和解。

## 16. fingerprint_spec + CORPUS_UNPINNED

冻字节 ≠ 冻可复算规格；通配正控集禁。

## 去重说明

g 已覆盖 chain_depth / declare_set / consume_freshness / billing 分层 / empty reopen / 24h recall / intent drift / WINDOW_REV_PENDING / population zero-delta / ROLLBACK_RESTORE / revoke enum / wall-clock liveness 等。本篇只收 h 增量。
