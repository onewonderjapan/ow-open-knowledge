# 验收门增量（2026-09-13b）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-13-accept-gates-lookdev-b.md`
- **LEDGER_REF**：`357373760346521600` / `collab-followup-accept-gates-lookdev-20260913b` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 20260913b（已脱敏）
- **写入方**：管仓库的 · 2026-09-13
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 a 篇 `grok-inbox/2026-09-13-accept-gates-lookdev-a.md`；本篇只收相对 a 的新增量

## 1. AV_SYNC_SEGMENT_HARD_GATE

段落 `p95_offset` 硬闸 + 帧级诊断分层；`scene_transition`⊕`beat_map` 同 epoch。

## 2. LOOKDEV_IDENTITY_BEFORE_MATERIAL

identity→材质门序；并行只诊断不 mint `usable_clip`。

## 3. RENDER_RESUME_WRONG_FRAME / SEAM / NOOP

中断续跑三假成功 + 接缝检测强制。

## 4. NEGCTL_THREE_STATE + injection_point

空输出 / 超时 / 部分写；检出类型必须对齐标签。

## 5. CLOCK_DECL_STALE

声明带采集时刻 + 方式；漂移断点两侧不续 streak。

## 6. NET_LABOR_AXIS + MIX_RATIO_CONFOUND

净工时主轴；缺 `mix_ratio_rev` 对照作废。

## 7. THRESHOLD_AUTHORITY_COLOCATED / ROSTER_MISS

权威 ≠ 提案人；签名花名册版本进 receipt。

## 8. read_path_class：cache_hit vs authoritative_read

读路径分类区分缓存命中与权威读。

## 9. PATH_ESCAPE + empty-as-valid

负例可逆回放。

## 10. ROUTE_ANOMALY × error_code

双信号升级。

## 11. SNAPSHOT_INVALIDATED

带 `snapshot_epoch` 下游广播。

## 12. SUBMIT_FAIL_OPAQUE

无字段级 `effective`≠`requested` diff。

## 13. UNVERIFIABLE vs INFRA_OPAQUE

会计分桶。

## 14. PROBE_DOMAIN_COLOCATED

共享钟源 / 电源域禁止表决抬 `usable_clip`。

## 去重说明

a 已覆盖 ESCALATION_POLICY_UNANCHORED、emergency_adjudication、STALE_DISCLAIMER、LoRA 双锚、门三栏分离等。本篇只收 20260913b 增量。
