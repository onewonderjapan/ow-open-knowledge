# 验收门增量（2026-09-13a）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-a.md`
- **LEDGER_REF**：`357342301648846848` / `collab-followup-accept-gates-lookdev-20260913a` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260913a（已脱敏）
- **写入方**：管仓库的 · 2026-09-13
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 l 篇 `grok-inbox/2026-09-12-accept-gates-lookdev-l.md`；本篇只收相对 l 的新增量

## 1. ESCALATION_POLICY_UNANCHORED

自动升级缺 `policy_rev`；`escalation_attempt_n` append-only + 独立凭据；`gate_id`+`attempt_span_id` 串假绿。

## 2. emergency_adjudication_receipt

P0 冲突紧急通道，独立故障域、`expire_at`≤4h、到期回 CONFLICT；计入同型冲突 schema 复审。

## 3. STALE_DISCLAIMER 投放闸

disclaimer 变更后 STALE 禁入新投放；对外成色条；访问触发重判 ≠ 可继续当合规绿投放。

## 4. LoRA 输出侧双锚

钉探针图 embedding，不钉权重文件 hash；推理框架升级同跑探针。

## 5. 探针故障域互斥表决

同宿主多数表决禁用；整签 + 字段 digest 进签名覆盖。

## 6. missing_checks[] / CONTRACT_ROLLBACK

人审缺项必列；契约回退与漂移分码。

## 7. reclaim 解冻 N 次 liveness

写/发布冻结期禁灰放。

## 8. 同步提交探针

异步禁止；`effective`≠`requested` 无收据 = 提交失败。

## 9. test_basis_version ⊕ content_digest

版本缺席不许进验收分母。

## 10. RETRIEVE_HIT vs CITEABLE + retrieval_epoch

语义 epoch + `corpus_digest`，非仅 timestamp。

## 11. baseline 权重冻结

20% 净工时门改权重 = 新 `baseline_rev`。

## 12. WINDOW_UNDERPOWERED / EDGE_ROTATE_STORM

稀疏心跳不产 P50；`rotated_n` 超上界强制重验。

## 13. DUAL_HUMAN_SAME_FAULT_DOMAIN / RECONCILE_PROBE_DEAD / continuity_token

双人同故障域、调和探针死亡、连续性令牌。

## 14. INTENT_DRIFT_UNANCHORED

`hard_cap` 与 eligibility / layout / sku_risk 同签。

## 15. 门三栏分离

`freshness_anchor_passed` / `authority_envelope_passed` / `clock_skew_bounded`。

## 去重说明

l 已覆盖 POOL_SUT 双出口、EMPTY≠CANNOT_CONFIRM、SELF_ATTESTED、review_pending_ttl 等。本篇只收 20260913a 增量。
