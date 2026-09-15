# 验收门增量（2026-09-13l）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-l.md`
- **LEDGER_REF**：`357676289471021056` / `collab-followup-accept-gates-lookdev-20260913l` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260913l（已脱敏）
- **写入方**：管仓库的 · 2026-09-14
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 k 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-k.md`；本篇只收相对 k 的新增量。注意：另有 2026-09-12 的 `lookdev-l` 旧篇，本文件名带日期 `2026-09-13` 区分。

## 1. NEGATIVE_CONTROL_INEFFECTIVE

形态合法但未拒闸或缺 `error_origin`。

## 2. ESCALATION_EXHAUSTED

升级超时拒同因重试。

## 3. POLICY_REV_DRIFT

digest 变、`rev` 未 bump → 拒载。

## 4. SIDE_PROBE_SCORE_MUTATION=forbid

旁路探头不改分。

## 5. STALLED_AFTER_ACK

ack 后无 stage completion。

## 6. AUDIT_PATH_DEGRADED

与 DETECTOR_DEGRADED 分码。

## 7. PLATFORM_CHECK_TIMEOUT

PENDING 超时不自动绿。

## 8. RISK_EXPIRED / risk_source=unsupported

风险过期；不支持来源。

## 9. BASELINE_STALE

baseline 超 30d 未再验证。

## 10. FAULT_DOMAIN_INDEPENDENCE

独立性锚故障域。

## 11. DIGEST_ALGO_VERSION

短哈希算法版本。

## 12. DIAG_VS_CAPACITY_DENOM

诊断分母 ≠ 容量分母。

## 13. STICKY_NEAR_POLICY_SUSPECT

sticky 系数进 `policy_rev`。

## 14. HOMOLOGOUS_BUCKET

同骨架不同音色分桶。

## 去重说明

k 已覆盖 NEGATIVE_CONTROL_DULLED、SAMPLE_PADDED、LOG_COMPLETENESS_UNKNOWN、NOISE_SATURATED 等。本篇只收 20260913l 新码（无效负控、升级耗尽、灰度退出相关）。
