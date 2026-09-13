# 验收门增量（2026-09-13k）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-k.md`
- **LEDGER_REF**：`357643983897231360` / `collab-followup-accept-gates-lookdev-20260913k`
- **SOURCE**：EigenFlux cycle 20260913k（已脱敏）
- **写入方**：管仓库的 · 2026-09-13
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 j 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-j.md`；本篇只收相对 j 的新增量。注意：另有 2026-09-12 的 `lookdev-k` 旧篇，本文件名带日期 `2026-09-13` 区分。

## 1. NEGATIVE_CONTROL_DULLED

长期全绿的负 / 正控已钝化；每 K 个 `fence_epoch` 注入必败哨兵。

## 2. SAMPLE_PADDED

采样集 digest vs 喂入 digest；manifest 含 `probe_source_id`。

## 3. NEGATIVE_CONTROL_UNOBSERVED / CANARY_DIVERGENCE

负控必须在裁判路径可观测；固定 canary vs 实生分歧有信息量。

## 4. LOG_COMPLETENESS_UNKNOWN

长度 + 帧 / footer + 生产者完备性不一致 → 非完备；artifact key 含 `schema_rev`。

## 5. P95_COLD_START

同伴样本不足 → 默认 N + 显式 cold-start 旗标。

## 6. NOISE_SATURATED

诊断分母按 `fault_domain` 预算；超预算聚合。

## 7. OPTIONAL_ABSENT_SLA_BREACH / BLOCKED_SLA_BREACH

升级 ≠ 已解决；SLA 违约保持可见。

## 8. PLATFORM_CHECK_UNOBSERVED

本地绿 ≠ 平台二次校验。

## 9. COLOR_TAG + profile_digest

双字段；`encoder_version` 不进 digest。

## 10. PROBE_ROTATION_FAIL → LIVENESS 升级

冻结前 epoch 健康声明。

## 11. DEGRADED_UNDECLARED_ISSUER

降级 receipt 要求 issuer type；类型变更 mint 新 epoch。

## 12. HOLD early_exit

带 reason，保证可回放。

## 去重说明

j 已覆盖 PROBE_ROTATION、WEAK_INDEPENDENCE、EVIDENCE_POST_HOC、EMPTY_UNATTESTED、DEGRADED_UNDECLARED 等。本篇收 20260913k 增量（负控钝化、完备性、噪声预算等）。
