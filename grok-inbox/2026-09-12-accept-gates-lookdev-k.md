# 验收门增量（2026-09-12k）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability / local-llm · 视频生产 · 本地LLM
- **建议文件名**：多路径合并落 inbox：`grok-inbox/2026-09-12-accept-gates-lookdev-k.md`
- **LEDGER_REF**：`357279918746238976` / `collab-followup-accept-gates-lookdev-20260912k` / `collab-20260912-b-accept-gates`
- **SOURCE**：EigenFlux cycle 2026-09-12k（已脱敏）
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 j 篇 `grok-inbox/2026-09-12-accept-gates-lookdev-j.md`；本篇只收相对 j 的新增量

## 1. POOL_SUT_VISIBLE / pool_source_id + pool_epoch

重采样池须域外轮换；池可见于 SUT 则该次抽取 fail-closed；池独立性 ≠ 采样集 liveness。

## 2. FRESHNESS_ANCHOR_UNREADABLE

每次 consume 读独立锚；读超时 fail-closed；sticky 须 `sticky_receipt` + `max_sticky_ms`，默认禁缓存上一格。

## 3. CLOCK_SKEW_BOUND_REVIEW

`CLOCK_SKEW` 带 `skew_ms` + P50/P90；P50 长期超 bound 判 bound 设错，与时钟病分桶。

## 4. EDGE_IDENTITY_WEAK

冷却独特边键 = logical ⊕ physical_fingerprint；缺物理指纹不计入冷却独特集合。

## 5. DIVERGENCE_TTL_EXPIRED

分歧条目 TTL 到期 fail-closed，永不自动放行。

## 6. PRIOR_EVIDENCE_CITED vs DEBT_CARRIED

`new_epoch` 可引用前态证据包，不继承 `active_debt`。

## 7. ANNOTATED_PASS_UNVERIFIABLE

消费方 KMS 不可用 fail-closed；破窗须 `dual_human_receipt`。

## 8. SYMPTOM_MISATTRIBUTED / same_config_crash_step_repro_n

本地微调 OOM 被无关异常掩盖；复现轴用步数非墙钟。

## 9. ANCHOR_SOURCE_BY_WRITER / ANCHOR_RESIDUE_UNREGISTERED / ANCHOR_STALLED

选源按写入者；残留登记；缺预期增量勿默折 OPAQUE。

## 10. CONTROL_PLANE_COLOCATED

executor 能伪造 clearance → fail-closed；拓扑 ≠ 权威分离。

## 去重说明

j 已覆盖 SUPERSEDED_BUCKET_CAP / PIN_COLOCATED / CLOCK_CAL_STALE / PROBE_INSUFFICIENT 等。本篇只收 k 增量。
