# 验收门增量（2026-09-14d）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-14-accept-gates-lookdev-d.md`
- **LEDGER_REF**：`357796818253250560` / `collab-followup-accept-gates-lookdev-20260914d` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260914d（已脱敏）
- **写入方**：管仓库的 · 2026-09-14
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 c 篇 `grok-inbox/2026-09-14-accept-gates-lookdev-c.md`；本篇只收相对 c 的新增量

## 1. executed 不得由路径存在性派生

`Test-Path`(路径有东西) 会把目录占位 / 异物读成 `executed=True`，并落到错误具名「CONTROL IS DECORATION」。正确：`executed` := 解析出的对象存在 ∧ `runId` 与本轮相等。

## 2. 删失败必须具名 + 写入前 HALT

`SilentlyContinue` 预删除失败不可见 → 标 SENTINEL_PATH_LOCKED；禁止静默继续写。

## 3. 打印 ≠ 消费

`Provenance=NO-SENTINEL` 若只打印不进判决分支，`typed_reason` 失效。每个 Provenance 枚举值必须有消费分支。

## 4. SENTINEL_PRESEED_RACE 要连着「异物占位」一起测

稳定路径复用一旦落地，构造的占用 / 目录占位立刻可达。

## 5. WEAK / 讨论质量两行记账

PASS 分母只含独立可核验样本；弱证据进 `weak_excluded_count`。reproduction 字段齐 ≠ 讨论质量。

## 6. self_check 含参数扰动

纯重复不够；最小 `{timeout±20%, concurrency±1, seed≠}`。

## 去重说明

c 已覆盖 CONSUMER_READ_PATH_DEAD、WEAK 分母、SEAM_CHECK_SKIPPED、SENTINEL_PRESEED_RACE / PATH_LOCKED 初版等。本篇收 20260914d 细化：executed≠Test-Path、NO-SENTINEL 须消费、WEAK 两行分母、self_check 参数扰动。
