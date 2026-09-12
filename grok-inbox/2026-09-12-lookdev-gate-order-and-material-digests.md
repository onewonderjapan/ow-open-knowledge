# Lookdev 门禁顺序与材质 digest

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video / 视频生产 · 本地LLM
- **建议文件名**：`video/lookdev-gate-order-and-material-digests.md`（inbox：`grok-inbox/2026-09-12-lookdev-gate-order-and-material-digests.md`）
- **LEDGER_REF**：`357069884238069760` / `collab-followup-accept-gates-lookdev-20260912d` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 2026-09-12T07:43Z（已脱敏）
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB
- **相关**：短毛五硬点见 `grok-inbox/2026-09-12-accept-gates-independence-lookdev.md`；本篇补门序、材质三层 digest、freshness/降级、story_beat_digest

## 门禁顺序（硬）

1. scale / transform / UV·normal 通过后才允许毛发  
2. 材质 SSS/roughness 通过后才允许灯光调参  
3. 灯光与毛发不得替几何/材质错误背锅；缺前序 → HOLD

## 材质三层（Blender）

- `base_skin`：Principled BSDF + 轻 SSS（鼻头/耳缘/眼周）
- `fur`：Principled Hair BSDF，melanin/tint 分区，不与皮肤共用 SSS
- `wet/detail`：鼻头高光 / 眼周湿润 / 胡须根 AO
- 输出 `skin_digest` / `fur_digest` / `detail_digest`；灯光变化不得改材质 digest

## children 分档（短毛起步）

- 近景脸 20–50 / 身体 12–30 / 远景 6–12；viewport ≈ render/4
- 先 clump/roughness/length variance，最后 density；发黏优先降 children 或抬 roughness

## Freshness / 降级纪律（验收）

- stale → 重取证；不可得才作废并留 tombstone（不物理删）
- 降级 ≠ 放行；`typed_reason` 仅受控枚举；降级事件进分母

## Schema 指纹两层

- 字段集指纹：名/类型/必填/枚举
- 语义指纹 `field_def_digest`：同名改义必变

## 跨集第三锚

- `story_beat_digest`：结构节拍差分，不依赖全文重放

## 去重说明

新建；与既有 identity_anchor≠styling_anchor 互补（第三锚）。不与空窗原稿整篇入库。
