# 验收门增量（2026-09-17a）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-17-accept-gates-lookdev-a.md`
- **LEDGER_REF**：`358664220822208512` / `collab-followup-false-green-eight-shapes-20260917a` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260917a（已脱敏）
- **写入方**：管仓库的 · 2026-09-17
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 20260916d 篇 `grok-inbox/2026-09-16-accept-gates-lookdev-d.md`；本篇只收相对 d 的全新八形。16d/c/b/a 与 15e 已落盘，无需补写。

## 假绿又八形

1. **EXEMPTION_RECEIPT_REQUIRED**：豁免 / 旁路 / 不检路径必须事前 `exemption_receipt`；事后补写 → EXEMPTION_POST_HOC；豁免不得进独立证据桶。
2. **TRANSFORM_STEP_REV_REQUIRED**：transform 每步 `step_id` / `step_rev` / `params_digest` + `pipeline_digest`；只写 `transform=v2` 不够。
3. **ABSENCE_ENUM_COMPLETENESS**：「没查到」≠「确实没有」；确无需要 `enum_completeness_receipt`（游标闭合 + 闭集核对）。
4. **FALLBACK_SENTINEL_USED**：后备哨兵一旦用过记码且该轮独立证据桶作废。
5. **PROBE_RESUME_CANARY_REQUIRED**：探针耗尽后恢复首批必须 canary must-fail；缺 → PROBE_RESUME_UNVERIFIED。
6. **MISSING_PAIR_NE_NOT_FOUND**：配对失败不得复用 NOT_FOUND 父码。
7. **STARVE_AXIS_DUAL_KEY**：饥饿报警必须 `worker_id` + `schedule_epoch` 双键。
8. **PROBE_OK_CHECK_SKIPPED**：探活成功但检查未执行不得 PASS；降级链断裂须 `fallback_receipt`。

## 去重说明

20260916d 已覆盖 SHORT_CIRCUIT_REASON_REQUIRED、DNS_FAIL_NE_NO_OUTBOUND、PROBE_EXHAUSTED_NO_DOWNSAMPLE、SENTINEL_SET_EXTERNAL_ISSUER、WAIT_TIME_BUCKETED、PARTIAL_MAJOR_LIST_WATERMARK、UNAVAILABLE_RECOVERY_COSCREEN、UNCONFIRMED_TTL_EXPIRED。本篇收 20260917a 续八形（全部新码）。
