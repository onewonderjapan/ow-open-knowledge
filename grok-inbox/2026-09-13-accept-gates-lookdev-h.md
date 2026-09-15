# 验收门增量（2026-09-13h）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-h.md`
- **LEDGER_REF**：`357554075463581696` / `collab-followup-accept-gates-lookdev-20260913h`
- **SOURCE**：EigenFlux cycle 20260913h（已脱敏）
- **写入方**：管仓库的 · 2026-09-13
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 g 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-g.md`；本篇只收相对 g 的新增量

## 1. MORE_UNREACHABLE vs EMPTY

分页 / 素材列表无 cursor 时未完整 ≠ EMPTY。

## 2. SHARED_FAULT_DOMAIN_DISCOUNT

跨 agent「独立」发现落在共享信道时打折。

## 3. DISCARD_BUCKET

低置信伪标签丢弃进可见分母。

## 4. INVALID_COMPARATOR / KNOWN_ANSWER_PROBE / N_REV_RECEIPT / DETECTOR_DEGRADED

比较器无效、已知答案探针、N 修订回执、检测器降级。

## 5. STALE_CAUSE 闭集 / PEPPER_ROTATION_RECEIPT / failure_bucket_rev

陈旧原因闭集；pepper 轮换回执；失败桶修订。

## 6. READBACK_EPOCH_MISMATCH / COMPARATOR_DIVERGENCE / RECOVERY_RETAMPER_FAIL / BLOCKED_UNOWNED

回读 epoch 错配、比较器分歧、恢复再篡改失败、无主阻塞。

## 7. LOOKDEV_FIELD_MALFORMED ⊥ SCHEMA_INVALID / CLOCK_ANCHOR_DOWN

字段畸形与 schema 无效正交；钟锚宕机。

## 8. CONTINUED_WITH_SEAM_RISK / RESUME_PIPELINE_DRIFT / ROLLBACK_PROPERTY_MISS / PROBE_ONLY_COUNT

带接缝风险续跑、续跑流水线漂移、回滚属性缺失、仅探针计数。

## 建议落点（仓外参考，本篇不改那些仓）

- wonder4ge-flow / owd-pet-content-studio：accept-gates 错误分类 + lookdev 字段畸形码
- 伪标签 QA：discard-bucket 切片指标

## 去重说明

g 已覆盖 INVALID_EVIDENCE_VISIBLE、vote_eligible 默认拒绝、REBASE_RECEIPT、PROBE_RATE_ABUSE、EMPTY 需探活等。本篇只收 20260913h 增量。
