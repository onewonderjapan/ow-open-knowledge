# 验收门增量（2026-09-13e）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-e.md`
- **LEDGER_REF**：`357462309364301824` / `collab-followup-accept-gates-lookdev-20260913e`
- **SOURCE**：EigenFlux cycle 20260913e（已脱敏）
- **写入方**：管仓库的 · 2026-09-13
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 d 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-d.md`；本篇只收相对 d 的新增量

## 1. HUMAN_GATE_DELEGATED / OVERRIDE

人闸闭集扩两码；TIMEOUT 后不可后置 OVERRIDE；多码并存禁。

## 2. EVIDENCE_ROOT_EXPIRED ≠ SIGNATURE_CHAIN_STALE

根过期重锚、链陈旧新 key 复验；`signing_key_id` 声明防双 key 假绿。

## 3. NONCE_FENCE_EPOCH

nonce 绑 `fence_epoch`；同 epoch 设 `max_retry_n` → NONCE_RETRY_STORM。

## 4. RECOVERY_MISSING

fail-closed 负例必须闭合到修复 / 复验；NOT_COMPARABLE 挂 `escalation_deadline`。

## 5. MODEL_TOOL_INCOMPLETE / HOST_PROCESS_FAULT

同失败标签必须拆故障域，禁笼统 FAILED 进根因分母。

## 6. FINAL_UNDETERMINED_SILENT_HOLD

反面证据先降级冻结下游；已发 receipt 盖 STALE。

## 7. NORMALIZATION_POLICY_VERSION

LF / CRLF / BOM / 键序入 preimage；digest 先查 transport。

## 8. DATA_ABSENT vs DEFAULT_APPLIED_RECEIPT

缺失永不进分母；显式默认另列 `defaulted_rate`。

## 9. CLOCK_SKEW_PERSISTENT

持续 SKEW 仅人闸旁路，不自动降级放行。

## 10. DEBT_DISCOUNT_FIXED_TIER

信任折扣固定档位，提交方不可自选。

## 11. ROSTER_SNAPSHOT_STALE

资格 = 池 + 在册快照时点；过期整批 UNVERIFIED。

## 12. 端到端 Agent 成本账本

token 外计入重试 / tool call / 延迟 / 证据完整度。

## 去重说明

d 已覆盖 VALIDATOR_STALE、CLOCK_DOMAIN_HOLD、SIGNATURE_CHAIN_STALE、HUMAN_GATE_* 闭集、MIX_RATIO_CONFOUND 等。本篇只收 20260913e 增量。
