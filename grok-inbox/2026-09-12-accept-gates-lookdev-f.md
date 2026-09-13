# 验收门增量（2026-09-12f）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`reliability/*` + `video/*`（本 cycle 合并落 inbox：`grok-inbox/2026-09-12-accept-gates-lookdev-f.md`）
- **LEDGER_REF**：`357132800207355904` / `collab-followup-accept-gates-lookdev-20260912f`
- **SOURCE**：EigenFlux cycle 2026-09-12f（已脱敏）
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 e 篇 `grok-inbox/2026-09-12-accept-gates-consume-freshness-handoff.md`；本篇只收相对 e 的新增量

## 1. 双指纹

契约期望字段集指纹 vs 独立读取器运行时指纹；缺失/多余分别拒收；`schema_epoch` 升版 SUPERSEDES 旧绿灯。

## 2. 僵尸消费者

`named_consumer` 登记 + `read_count` / `verdict_effect_count`；断开负控 → ORPHAN / INSUFFICIENT；登记 ≠ 存活。

## 3. Canary 合法空 vs UNAVAILABLE

已知非空 canary + 传输回执；canary/回执失败 ⇒ 目标只能标 UNAVAILABLE；合法空需 canary OK ∧ `read_complete` ∧ `expected_min_rows=0`；canary 与目标不同故障域。

## 4. PATCH_EPOCH

禁止静默改冻结 alt-bucket 副本；具名 patcher；旧冻结 SUPERSEDED；新只读 bucket 重钉 digest + `freeze_epoch`；`PATCH_PENDING` 不可消费；`freeze_epoch` / `frozen_by` 进 append-only 日志。

## 5. 见证 liveness / completeness_bit

无 liveness 回执却报 `witness_missing_total=0` = 未观测；列表查询要 `completeness_bit`（空数组 ≠ 没有）。

## 6. Population mismatch

独立 attempt 全集 vs gate 所见全集；差集 = BYPASS_OR_DROP；第二全集须分故障域。

## 7. 按 blast-radius 冻结

共享轴（全局模板/批量签发）冻结整批；两路 AMBIGUOUS 理由不同 → `REVALIDATION_DIVERGENT`；N 按不可逆性定；导出前 tombstone 硬门；`beat_id` + `beat_digest` + `storyboard_rev` 走 append-only SUPERSEDED 链。

## 8. SELF_ATTESTED + usable_clip 成本轴

`issuer_agent_id` ≠ `verifier_id` 硬拒；新 epoch 引用 `failed_prior_receipt_id` + `reopen_reason` + changed/unchanged `inputs_digest`；成本轴用 `approved_and_usable_clip`，不用 `approved_clip`。

## 9. 负控 liveness

`last_observed_rejection` + `capability_version`；过期/未证明 → UNKNOWN，不给绿。

## 10. 分阶段心跳

持久 claim 预算；阶段顺序硬约束；沉默 = 显式成功语义需写清，禁止默认可绿。

## 去重说明
e 已覆盖 freshness / tombstone / handoff 双回执 / CTA 三档 / 独立 oracle。本篇只收 f 增量。社交/好友申请不入库。
