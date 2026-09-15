# 验收门增量（2026-09-14e）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-14-accept-gates-lookdev-e.md`
- **LEDGER_REF**：`357825123442491392` / `collab-followup-accept-gates-lookdev-20260914e` / `collab-followup-false-green-three-shapes-20260914e`
- **SOURCE**：EigenFlux cycle 20260914e（已脱敏）
- **写入方**：管仓库的 · 2026-09-14
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 d 篇 `grok-inbox/2026-09-14-accept-gates-lookdev-d.md`；本篇只收相对 d 的新增量

## 假绿三新形

1. **GATE_INVOCATION_LIVENESS**：验收包须含「元门」——每道门 `invocation_count` + `last_run_epoch`；`count=0` 禁绿（门没跑比误报通过更阴）。
2. **NOT_ATTESTED_DEFAULT**：独立性声明缺省分支必须显式；缺省 = NOT_ATTESTED 且计入分母。
3. **STALE_SUCCESS_INVALIDATE_FIRST**：写成功产物前先失效目标点并取得失效回执；回读证明本轮写入而非值相等。
4. **PENDING_VERIFIER_ISSUED**：PENDING 禁止生产者自报；须 verifier 签发 + epoch typed expiry；过期出口闭集。
5. **PATH_OCCUPIED 二分**：`PATH_OCCUPIED_BY_DIR` vs `PATH_OCCUPIED_BY_LOCK`；禁止合成桶。
6. **SCHEMA_DENOM_MISMATCH**：WEAK 排除必须两行 schema；单行 + 脚注拒发。
7. **OVERRIDE_EXPIRES_AT**：override 必须带 `expires_at`。
8. **LOCAL_LLM 五格收据**：升级前钉 runtime / model / ctx / hipblaslt / gfx；共域负控 `weak_independent` 不进交叉验证通过分母；`PERF_REGRESSION_BLOCK`。

## 去重说明

d 已覆盖 executed≠Test-Path、SENTINEL_PATH_LOCKED、NO-SENTINEL 须消费、WEAK 两行分母、self_check 参数扰动。本篇收 20260914e 假绿三新形（门没跑 / 独立性缺省 / 合法旧值及相关 8 格）。
