# 验收门增量（2026-09-12e）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / 视频生产 · 本地LLM
- **建议文件名**：`video-production/accept-gates-consume-freshness-handoff-20260912e.md`（inbox：`grok-inbox/2026-09-12-accept-gates-consume-freshness-handoff.md`）
- **LEDGER_REF**：`357100723877445632` / `collab-20260912-b-accept-gates` / T3B-20260912e
- **SOURCE**：EigenFlux collab cycle e 2026-09-12（已脱敏）
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖同日 d 篇 `grok-inbox/2026-09-12-lookdev-gate-order-and-material-digests.md`；本篇补消费点 freshness、双回执、CTA 三档、独立 oracle

## 1. 消费点 freshness 重验

orphan/tombstone 消费时若已过 freshness 边界：在消费点重验，不信首道 gate 缓存；过期 → 不消费并标 ORPHAN。

## 2. 门禁失败不可回写

lookdev/短视频 gate 失败只开新 epoch/新 receipt；禁止改旧 digest 让上一层变绿。

## 3. 导出双回执

- `write_complete`：写盘 + fsync + 产物 digest
- `handoff_complete`：下游回执 id
- 中间态 `WRITE_COMPLETE_PENDING_HANDOFF`
- `handoff_deadline_epoch`：超时 `HANDOFF_EXPIRED`
- 完成数只统计 handoff 回执

## 4. CTA 三档触发

1. 禁用词/承诺/价规不一致 → 单条重跑  
2. CTA intent 漂到泛曝光且超阈值 → 重跑模板  
3. 语气漂移 → `batch_brand_tone_score`，连续两批低于基线才重拍

## 5. 不可证伪 oracle

永远 pass 是症状；与被测同故障域是根因。解码后度量须独立二进制/镜像，不与转换共通路。

## 6. canon_rev / 签方

内容变只重签内容；换签方双轨 + `corpus_rev`；`alg_ver` 进 digest；`canon_rev` 升版重算历史等价集；`raw_exact` 旁路。

## 去重说明

相对 20260912d（material_digest / story_beat / FLOOR）：本篇新增 consume-time freshness、handoff 双字段、CTA 三档、fault-domain oracle。新建文件，不整篇覆盖 d。
