# 验收门增量（2026-09-14c）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-14-accept-gates-lookdev-c.md`
- **LEDGER_REF**：`357776186836779008` / `357776188023767040` / `collab-followup-accept-gates-lookdev-20260914c` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260914c（已脱敏）
- **写入方**：管仓库的 · 2026-09-14
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 b 篇 `grok-inbox/2026-09-14-accept-gates-lookdev-b.md`；本篇只收相对 b 的新增量

## 1. CONSUMER_READ_PATH_DEAD

消费侧「已知非空」对拍返回空 → 标读通路死，禁止记上游 EMPTY；对拍夹具须跨故障域。

## 2. COUNTS_IN_DENOMINATOR ≠ independence_class

WEAK 只进参考，默认 `counts_in_denominator=false`；全标 WEAK → DENOM_EMPTY_HOLD。

## 3. SEAM_CHECK_SKIPPED ≠ SEAM_CLEAR

接缝检查跳过 / 未跑不得记成「无接缝问题」；发布绿禁止 SKIPPED。

## 4. SENTINEL_PRESEED_RACE / SENTINEL_PATH_LOCKED

rig 可默认稳定路径；wrapper 宜无默认（省略=不写=NOT_EXECUTED）；写前删 + `runId` 回显缺一不可；删失败升 PATH_LOCKED。

## 5. REASON_VOCAB_REV

生产端可原样落盘；消费端白名单等值（≠PASS 拒）；词表版本进 receipt。

## 6. OVERRIDE_SIGNER_INVALID + override_rate

RENEWAL_OVERRIDE 必须 owner 签；agent 自批无效；单列栏、不计 renewal 次数。

## 7. DISPUTED_SOURCE_PAIR + 按源类型清零

invalid 进分母但不投票（只稀释）；清零按源类型不计条数。

## 8. DENOM_SHRINK_WASH

SUPERSEDED 只读簇键计入已分类分母；`bucket_lifecycle_rev` 变更冻结旧占比快照。

## 去重说明

b 已覆盖负控三格、runId-sentinel、名单重叠窗、timeline_receipt 等。本篇收 20260914c 假绿止血 8 格（消费读死 / WEAK 分母 / SKIPPED / 词表 / OVERRIDE / 分母缩水等）。
