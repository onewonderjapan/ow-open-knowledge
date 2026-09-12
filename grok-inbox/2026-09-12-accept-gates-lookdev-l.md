# 验收门增量（2026-09-12l）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：多路径合并落 inbox：`grok-inbox/2026-09-12-accept-gates-lookdev-l.md`
- **LEDGER_REF**：`357311821121585152` / `collab-followup-accept-gates-lookdev-20260912l` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 2026-09-12l（已脱敏）
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 k 篇 `grok-inbox/2026-09-12-accept-gates-lookdev-k.md`；本篇只收相对 k 的新增量

## 1. POOL_SUT_VISIBLE_OBSERVED vs POOL_SUT_UNREACHABLE

观测层 redact vs 拓扑层重声明 `pool_network_domain_id`；禁止把拓扑问题修成观测问题。

## 2. review_pending_ttl

外部 verifier 标记 `pending_review` 时 reset TTL；review 出口优先于自然 `divergence_entry_ttl`；到期无人 → ESCALATED_NO_OWNER。

## 3. ANCHOR_UNAVAILABLE（合并 FRESHNESS_ANCHOR_UNREADABLE）

单枚举；锚带 `clock_domain_id`；与产物域相同进锚域共模独立桶。

## 4. disposition_receipt

`DIVERGENCE_TTL_EXPIRED` 移除开放列表前必须有 owner + action。

## 5. EDGE_COVERAGE_STARVED

物理指纹覆盖率低于 `coverage_floor` 时告警；边集合缩空 ≠ 冷却生效。

## 6. EMPTY ≠ CANNOT_CONFIRM

空结果须 `re_read_attempt_n` + `last_error_class` + `reader_fault_domain_id`。

## 7. k-of-n 锚见证

高风险默认 2-of-3；单锚仅 `EXPLICIT_LOW_RISK` + 短 TTL。

## 8. SELF_ATTESTED

消费者心跳不得证明读正确性；自证从 accept-gate 证据集剥离。

## 9. INVALID_STALE_ROOT + ARCHIVE_LEGACY

新旧根并存窗口旧根重放；归档只读不生效。

## 10. vendor_control_plane_id / policy_rev 新裁决收据

共享 admin/recovery 根即 CONTROL_PLANE_COLOCATED；抬升 cap 禁止静默复活耗尽探针。

## 11. HOLD_PENDING_REAPPROVAL

`approval_receipt` 过期倾向此态而非笼统 INVALID。

## 12. 分层工时双条件

净工时硬降幅 + 任一失效切片返工不升；防挑软样本假绿。

## 去重说明

k 已覆盖 POOL_SUT_VISIBLE / FRESHNESS_ANCHOR_UNREADABLE / CLOCK_SKEW_BOUND_REVIEW / EDGE_IDENTITY_WEAK / DIVERGENCE_TTL_EXPIRED / ANNOTATED_PASS_UNVERIFIABLE / CONTROL_PLANE_COLOCATED 等。本篇只收 l 增量（双出口、EMPTY≠CANNOT_CONFIRM、SELF_ATTESTED 剥离等）。
