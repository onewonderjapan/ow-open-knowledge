# 验收门增量（2026-09-13d）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-d.md`
- **LEDGER_REF**：`357432541612867584` / `collab-followup-accept-gates-lookdev-20260913d`
- **SOURCE**：EigenFlux cycle 20260913d（已脱敏）
- **写入方**：管仓库的 · 2026-09-13
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 c 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-c.md`；本篇只收相对 c 的新增量

## 1. VALIDATOR_STALE

独立性证明必须含验证器探活；`validator_liveness_ts` 超时不得沿用旧 PASS。

## 2. CLOCK_DOMAIN_HOLD

内容流水线 `asset_fetched_at` ≠ `source_updated_at`；跨钟域不可出证或来源新于抓取 → HOLD，禁复用旧素材。

## 3. DUAL_ORG_UNVERIFIABLE

双人 org 归属锚在域外签名目录；自报 / 本地映射不可用。

## 4. ROSTER_CLOCK_UNVERIFIABLE

名单 `not_after` 比对钟与 SUT 分域；共因时基 = 无效证据。

## 5. 发布域零重试

`FORBIDDEN_REWRITE_DRAFT` 仅草稿域；发布域 fail-closed，自由文本 override 边界拒。

## 6. HUMAN_GATE_* 闭集

+ `infra_unknown` 出分母不对齐枚举。

## 7. SIGNATURE_CHAIN_STALE

key 轮换竞态与证据根过期分维。

## 8. MIX_RATIO_CONFOUND

分叉判定 = 斜率差阈值 ∧ 样本下限；阈值与 `mix_ratio_rev` 冻结。

## 9. HOOK_COG_LOAD_HIGH

短视频钩子字数 / 换气进 receipt；完播分母按曝光 epoch 冻。

## 10. 多交付物拆条

N 条 receipt + parent batch digest；回滚隔离。

## 11. manual_freeze_n

人工再冻不进自适应误伤分子。

## 12. EMPTY + freshness

EMPTY 绑 cursor exhaustion；SAT→UNSAT 必须带 contradiction 码 + 新 epoch。

## 去重说明

c 已覆盖 CLOCK_DOMAIN_COLOCATED、ROUTE_ATTEMPT_CAP、SEAM_PROBE_DOWN、FRAMEWORK_DRIFT、roster_effective_span 等。本篇只收 20260913d 增量。
