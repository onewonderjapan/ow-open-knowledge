# 验收门增量（2026-09-13j）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-j.md`
- **LEDGER_REF**：`357613750947151872` / `collab-followup-accept-gates-lookdev-20260913j`
- **SOURCE**：EigenFlux cycle 20260913j（已脱敏）
- **写入方**：管仓库的 · 2026-09-13
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 i 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-i.md`；本篇只收相对 i 的新增量

## 1. PROBE_ROTATION / PROBE_ROTATION_FAIL

验证器身份稳定；探针源按 `fence_epoch` 轮换；轮换 ledger 签名。

## 2. WEAK_INDEPENDENCE

经由共享 substrate 集（process / cred / clock-domain）；钟域必须加入故障域声明。

## 3. evidence_epoch

按证据诞生时间（非重判次数）；重判窗要求新鲜负控。

## 4. EVIDENCE_POST_HOC

决策后可见证据不得为该决策背书。

## 5. DEGRADED_UNDECLARED

`CLOCK_DOMAIN_DEGRADED` 必须声明式（谁 / issuer domain / expiry）。

## 6. EMPTY_UNATTESTED

EMPTY 要求 ≥1 次成功探活。

## 7. AUDIT_TTL_BY_SCOPE

死授权审计保留按 scope。

## 8. rule_content_epoch ⊥ rule_rev

hotfix 正交版本。

## 9. retry_exhausted

进成本 / SLA 看板（queue / 429 / OOM 分桶）。

## 10. STORYBOARD_SLOT_MISS

slot 序列作强骨架 hash。

## 11. PATH_PLATFORM_REJECT + O_NOFOLLOW

字符串层路径检查。

## 12. ANCHOR_DRIFT

`v_n-1` 外部锚漂移时冻结变更集。

## 去重说明

i 已覆盖 CLOCK_DOMAIN_*、制品四态、REBASE_NONDETERMINISTIC、DELEGATED_EXPIRED_USED、COLOR_TAG_* 等。g 已有 EMPTY 需探活。本篇收 20260913j 增量（探针轮换、弱独立、事后证据、lookdev 分母切片相关）。
