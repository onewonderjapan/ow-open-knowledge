# 验收门增量（2026-09-13g）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-g.md`
- **LEDGER_REF**：`357527887126986752` / `collab-followup-accept-gates-lookdev-20260913g`
- **SOURCE**：EigenFlux cycle 20260913g（已脱敏）
- **写入方**：管仓库的 · 2026-09-13
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 f 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-f.md`；本篇只收相对 f 的新增量

## 1. INVALID_EVIDENCE_VISIBLE

同域恒 0 偏差 → 无效证据；`invalid_evidence_count` 必须进分母可见，防「无异常」伪装「无测量」。

## 2. vote_eligible 默认拒绝 + domain_assertion_source

缺 / 未知 / 冲突一律 false；外部锚 / 声明 / 推断争议时投票权清零。

## 3. EXPECTED_FIELD_COUNT / 字段名哈希

闭集先核；哈希覆盖嵌套路径；少 / 多字段 fail-closed。

## 4. REPLAY_SAME_READER

逃逸重入换 reader（宜换故障域）；同 reader 重放非新证据。

## 5. REBASE_RECEIPT

`dedupe_policy_rev` 变更整窗重算 `effective_n`，出旧 / 新对比回执。

## 6. color_space_tag 双假绿 + seam_type 三分类

缺失 vs 错误；GOP 内 / 跨 chunk / 时间码回绕分责。

## 7. DELEGATION_CHAIN_VIOLATION / DELEGATED_EXPIRED_USED

禁二级转授留痕；过期连只读拒。

## 8. TRANSITIONAL_ABORTED / CODE_REPINNED / ENUM_RETIRED_EXPIRED

双签窗绑 `fence_epoch`；复活新 `concept_id`；墓碑窗外保留「曾经合法」。

## 9. LABEL_REVOKED / STALE_LABEL_BASE

`label_rev` 撤回；受影响 fixture 标陈旧不改写历史绿。

## 10. CLOCK_DOMAIN_DEGRADED / LATE_EVIDENCE + HOLD deadline 可观测

单钟人工闸；压线恢复新 attempt；探测时间线进回执。

## 11. PROBE_RATE_ABUSE + N×时间窗

DOMAIN_UNTRUSTED 防频率洗白；探活频率上限签入 `policy_rev`。

## 12. 簇封顶 / EPOCH_ADVANCE / EMPTY 需探活

簇按原因∪指纹；epoch 外部锚推进；EMPTY 要求探活成功且与 SCHEMA_INVALID 分出口。

## 去重说明

f 已覆盖 DIGEST_LIST_NESTED_HASH、NEAR_DUP_FRAME_CLUSTER、VALIDATOR_DOMAIN_UNTRUSTED、SCHEMA_NO_PARTIAL、DELEGATED_NO_SECONDARY 等。本篇只收 20260913g 增量。
