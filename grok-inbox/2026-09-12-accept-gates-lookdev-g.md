# 验收门增量（2026-09-12g）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / business · 视频生产 · 本地LLM
- **建议文件名**：多路径合并落 inbox：`grok-inbox/2026-09-12-accept-gates-lookdev-g.md`
- **LEDGER_REF**：`357160557024903168` / `collab-followup-accept-gates-lookdev-20260912g` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 2026-09-12g（已脱敏）
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 f 篇 `grok-inbox/2026-09-12-accept-gates-lookdev-f.md`；本篇只收相对 f 的新增量

## 1. cost_capped_chain_depth + nearest_anchor_segment_proof

链深按回放成本封顶；回放用最近锚 + 段证明，不做全链 expand；缺 `segment_proof_rev` → UNREPLAYABLE；`resolved_rev` 硬门。

## 2. declare_set_digest_in_beat

共享轴静态声明 + 现场闭包；declare_set 进 `beat_digest`；闭包漂移 = 新故障域，不扩 expand-freeze；回执字段 `declared_set_digest`。

## 3. consume_freshness_triple

消费点 freshness 绑定 `export_digest` + `render_runtime` + `review_time` + 双回执；playback-path 是否独立 oracle 待对拍。

## 4. billing_eligibility_vs_usable_clip

订阅费（eligibility）与计件（usable_clip）双层；客户可见发票不得泄露内部 gate 错误码。

## 5. controlled_empty_reopen

空 changed 仅允许 POLICY_CHANGE / CORRUPTION / WITNESS_REVOKED / UPSTREAM_EPOCH_SUPERSEDED；附 `policy_or_witness_delta_digest`。

## 6. usable_clip_24h_same_cause_recall

usable = 可入队 ∧ 24h 同因无召回 ∧ root_cause 分轴回写；超 24h 召回是否回冲计件待定。

## 7. batch_intent_drift_8pct + LOW_N_UNCERTAIN

8% 按批不按条；n&lt;30 → LOW_N_UNCERTAIN；`intent_drift_rate` hard_cap 公式待收口。

## 8. WINDOW_REV_PENDING bilateral

`window_spec_rev` 随调度 epoch 升；双边接受 WINDOW_REV_PENDING；PENDING 回滚时钟上界待定。

## 9. ATTEMPT_SIDE_PARTIAL sidecar

迁移过渡仅记录型 sidecar；钩子仍唯一源时不得宣称独立。

## 10. population_zero_delta_UNVERIFIABLE

caller-side population 独立故障域；零差额 → UNVERIFIABLE 审阅桶，不自动绿。

## 11. ROLLBACK_RESTORE ≠ silent un-supersede

须 `rollback_epoch` + `prior_freeze_digest` + typed reason；`patcher_id` ≠ `approver_id`。

## 12. revoke_reason_code_enum_rev

枚举版本化（`enum_rev` + retired_codes 注册表）；落回执 vs policy bundle 待定。

## 13. wall_clock_independent_liveness

探针 tombstone 墙钟 N + 双探针 AND-红；须 NTP-attested / 外部 tick，防 SUT 拖业务钟。

## 14. as_of_clock_independence

网段源 as_of 实时禁缓存；时钟锚独立于 SUT。

## 15. receipt_append_only + tombstone

`failed_prior_receipt` 仅追加；`receipt_tombstone` 禁静默删。

## 16. lease_fence_pending_deadletter

lease expiry fence → pending + backoff → dead-letter；幂等键字段名待对拍。

## 17. golden_kms_split + independent_observed_count=0

golden 签钥与产线 KMS 分域；count=0 → NOT_EVALUATED / COVERAGE_UNVERIFIED，不进分母。

## 18. layered_attribution_windows

24h / 72h / 7d；早窗仅信号；弱归因不得进版本 credit / usable_clip 成本。

## 去重说明

f 已覆盖双指纹 / 僵尸消费者 / canary / PATCH_EPOCH / witness liveness / population mismatch / blast-radius / SELF_ATTESTED 等。本篇只收 g 增量。社交与发布统计不入库。
