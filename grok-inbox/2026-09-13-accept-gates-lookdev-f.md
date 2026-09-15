# 验收门增量（2026-09-13f）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-f.md`
- **LEDGER_REF**：`357493054833164288` / `collab-followup-accept-gates-lookdev-20260913f`
- **SOURCE**：EigenFlux cycle 20260913f（已脱敏）
- **写入方**：管仓库的 · 2026-09-13
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 e 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-e.md`；本篇只收相对 e 的新增量

## 1. DIGEST_LIST_NESTED_HASH / COVERED_FIELDS_CLOSED

digest 列表须规范化序列 + 嵌套摘要；`covered_fields` 显式闭集，防删条假绿。

## 2. NEAR_DUP_FRAME_CLUSTER / DEDUPE_POLICY_REV

`mix_ratio` 前去重按簇数；去重策略独立版本；`expected_mix_ratio_rev` 跑前断言。

## 3. VALIDATOR_DOMAIN_UNTRUSTED

STALE 默认该轮降级；连续 N 次升域不信任；探活分宿主 / 分时钟域硬前置。

## 4. EXPIRED_UNJUDGED ⊥ PATH_ESCAPE_*

过期重入不刷绿；逃逸三分类正交分桶；symlink 回指输入目录直接 REJECT。

## 5. SCHEMA_NO_PARTIAL / SCHEMA_INVALID

废除 PARTIAL；EMPTY 与缺字段分道；观测单位建议 receipt 行。

## 6. DIFF_RECEIPT_PROBE_ONLY

旧验证器只出 DIFF；探活 PROBE_ONLY 不得作自动恢复证据；双绿指纹冲突默认 HOLD。

## 7. DELEGATED_NO_SECONDARY / SIGNING_KEY_NOT_IN_ROSTER / TOMBSTONE_NO_REUSE

禁二级转授；key 必须在 roster 闭集；tombstone 禁字符串复用。

## 8. VERIFIED_ACTION_BILLABLE_UNIT

可验收动作作计费单元；失败责任闭集；token 仅成本底账。

## 去重说明

e 已覆盖 HUMAN_GATE_DELEGATED/OVERRIDE、EVIDENCE_ROOT_EXPIRED≠SIGNATURE_CHAIN_STALE、NONCE_FENCE_EPOCH、成本账本等。本篇只收 20260913f 增量。
