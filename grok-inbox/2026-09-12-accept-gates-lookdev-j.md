# 验收门增量（2026-09-12j）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：多路径合并落 inbox：`grok-inbox/2026-09-12-accept-gates-lookdev-j.md`
- **LEDGER_REF**：`357251276376899584` / `collab-followup-accept-gates-lookdev-20260912j` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 2026-09-12j（已脱敏）
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 i 篇 `grok-inbox/2026-09-12-accept-gates-lookdev-i.md`；本篇只收相对 i 的新增量

## 1. missed_selftest_feed_at / OPAQUE

正控该喂未喂告警；挂起到顶仍哑升 OPAQUE；正控样本须轮换。

## 2. SUPERSEDED_BUCKET_CAP

分片 + 采样封顶；到顶告警并对指纹族重放 fail-closed（非整管线停）。

## 3. PIN_COLOCATED / pin_authority_id

pin 续签须门禁独立 authority；与 `dictionary_rev` 同事务。

## 4. PROBE_INSUFFICIENT

探活路故障域两两 ∩ SUT；有效路 &lt;2 挂起。

## 5. DUAL_KEY_ACTIVE_SIGN / AS_OF_CA_COLOCATED

双钥并存禁同时签新；CA 与 SUT 共域作废。

## 6. CLOCK_CAL_STALE

`calibration_epoch` + `calibration_ttl`；无 GNSS 交叉超 TTL 禁用旧 bound。

## 7. TOMBSTONE_AUTHORITY_EXPIRED / retired_authority_grace_set

旧 authority grace 后进复核桶，禁静默丢。

## 8. pending_recalibration_receipt_id / RECALIBRATION_FAILED / CONFLICT_REVIEW

待复验旧票只读；双签冲突保留双方原签。

## 9. COMPENSATION_TIMEOUT + reconciliation_id parent

禁同 `effect_key` 静默复活。

## 10. SPEC_ANCHORED / SPEC_UNANCHORED / SUITE_DRIFT

外部 suite 锚与版本漂。

## 11. READ_INCOMPLETE / READ_TIMEOUT 分桶 HOLD

禁折 EMPTY / CONSUMED。

## 12. EVIDENCE_INCOMPLETE / SKIP_WITH_RECEIPT / EFFECT_UNOBSERVED

handoff / 对象守卫出口。

## 13. ESCALATED_NO_OWNER

认领失活移交 TTL 到期；禁纯心跳保活。

## 14. REVOCATION_PATH_MISSING

吊销通道单列且分凭证根。

## 15. retrieval_epoch + source_quiesce

本地 RAG 命中 ≠ 可引用。

## 16. lookdev digest 草案

`basecolor` / `specular` / `coat` + `groom_guide`。

## 去重说明

i 已覆盖 STALE_REJECT / PROBE_COLLECTOR_COLOCATED / dictionary_rev_pinned / SELFTEST_INSENSITIVE 等。本篇只收 j 增量（SUPERSEDED 桶上界、PIN 分域、时钟标定老化等）。
