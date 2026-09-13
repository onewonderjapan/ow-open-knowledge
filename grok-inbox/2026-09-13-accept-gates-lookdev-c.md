# 验收门增量（2026-09-13c）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / economic · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-c.md`
- **LEDGER_REF**：T2 `357402918430703616` / T3B `357403035028160512` / `collab-followup-accept-gates-lookdev-20260913c` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260913c（已脱敏）
- **写入方**：管仓库的 · 2026-09-13
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 b 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-b.md`；本篇只收相对 b 的新增量

## 1. CLOCK_DOMAIN_COLOCATED

出证钟与业务钟分域；同宿主 NTP 恒 0 偏差 = 无效证据。

## 2. ROUTE_ATTEMPT_CAP

`(request_id, route_attempt_n)` + `policy_rev` 上限。

## 3. SEAM_PROBE_DOWN

接缝检测 liveness；`NOT_RUN` 不得标续跑成功。

## 4. CLASS_MISLABEL

跨域副作用标签错分，不进主结论。

## 5. parse_layer fault_domain

`parse_status` / `error_origin` 闭集；EMPTY ≠ CANNOT_CONFIRM。

## 6. roster_effective_span / ROSTER_EXPIRED

签名花名册有效期窗口。

## 7. path_escape_class

dotdot / symlink / absolute 分类进 `typed_reason`。

## 8. FRAMEWORK_DRIFT

框架升级输出变 ≠ identity 变更；CLIP + phash 双锚。

## 9. window_policy_rev

归因窗按类别中位；`credit_event_class` 分列。

## 10. N_ESTIMATE_LOW_SAMPLE

+ 自适应解冻 N（`persistent_risk`）。

## 11. INFRA_OPAQUE.infra_signal

分维计数。

## 12. SNAPSHOT_INVALIDATED + subscriber_lag ack

下游广播需订阅者滞后确认。

## 去重说明

b 已覆盖 AV_SYNC_SEGMENT_HARD_GATE、LOOKDEV_IDENTITY_BEFORE_MATERIAL、RENDER_RESUME_*、NEGCTL_THREE_STATE、PROBE_DOMAIN_COLOCATED、SNAPSHOT_INVALIDATED 广播等。本篇只收 20260913c 增量。
