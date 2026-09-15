# 验收门增量（2026-09-14a）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-14-accept-gates-lookdev-a.md`
- **LEDGER_REF**：`357703837110239232` / `collab-followup-accept-gates-lookdev-20260914a` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260914a（已脱敏）
- **写入方**：管仓库的 · 2026-09-14
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 20260913l 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-l.md`；本篇只收相对 l 的新增量

## 证据时序

1. **EVIDENCE_POST_HOC**：`verdict_made_at` < `evidence_visible_at` → 禁补证维持原绿
2. **ADJUSTMENT_RECEIPT_EPOCH**：新证据必须新 epoch；金额 / 计价只追加

## 签方与故障域

3. **QUOTA_POOL_COLLISION**：双签共池探针失败降单签
4. **CA_FINGERPRINT_SPLIT**：主机 + 密钥托管 + 签发 CA 三件全要
5. **ROOT_ROTATION_RECEIPT**：换根留痕；伪造 CA 风险保持 EDGE_ROTATE_STORM
6. **OWNER_UNREACHABLE_ESCALATION**：钝化 owner 失联升 oncall

## sticky / 默认 / 人审

7. **STICKY_ROLLBACK**：嫌疑系数拒载后回落上一签版 + HOLD
8. **DEFAULT_FIELD_FAIL_CLOSED**：无源默认字段级拒生效
9. **HUMAN_VERDICT_REV**：人审后强制重判，不当放行开关

## 视频 / 声纹 / 基线

10. **VOICE_EMBEDDING_MODEL_VERSION**：`voice_hash` 带模型版本
11. **DUAL_TRACK_OLD_OFFICIAL** + `downgrade_reason`
12. **CONTENT_FIX_DIFF_GATE**：`content_fix_only` 必带 `fix_diff`
13. **ANCHOR_SYNC_LAG** vs **ANCHOR_DRIFT**
14. **BASELINE_SAMPLE_REVERIFY**（抽 10%）
15. `skeleton_hash` 排除镜头时长
16. **PLATFORM_INTEGRATION_ALERT**（超时连续 ≥3）

## 恢复与探针

17. **RESUME_AT_FORK** / **NOISE_BUDGET_FLOOR** / **PROBE_EXIT_QUEUED_DROPPED**
18. **SEAM_NOT_RUN_BUCKET**；时钟域按校时作证源切
19. **TEST_BASIS_TRIPLE**：脚本 / 清单 / 工况三件同签

## 本轮补充

20. **negctl_judge_source**=同源|异源：负控判定器相对被测链须独立；同源只进诊断
21. **ESCALATION_REMEDY_AVAILABLE**：与 ESCALATION_EXHAUSTED 分终态（仍有可解除动作未执行）

## 去重说明

20260913l 已覆盖 NEGATIVE_CONTROL_INEFFECTIVE、ESCALATION_EXHAUSTED、POLICY_REV_DRIFT 等 14 条。j 已有 EVIDENCE_POST_HOC 初版。本篇收 20260914a 细化（证据时序、签方故障域、决策卡独立性分母相关）。
