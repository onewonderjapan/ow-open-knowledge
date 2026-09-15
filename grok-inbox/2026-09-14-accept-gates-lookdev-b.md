# 验收门增量（2026-09-14b）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-production / reliability · 视频生产 · 本地LLM
- **建议文件名**：`grok-inbox/2026-09-14-accept-gates-lookdev-b.md`
- **LEDGER_REF**：`357737953700610048` / `collab-followup-accept-gates-lookdev-20260914b`
- **SOURCE**：EigenFlux cycle 20260914b（已脱敏）
- **写入方**：管仓库的 · 2026-09-14
- **状态**：建议轨，未晋升公开 KB
- **相关**：不覆盖 a 篇 `grok-inbox/2026-09-14-accept-gates-lookdev-a.md`；本篇只收相对 a 的新增量（runner / roster / seam-time 轴）

## 1. 负控三格修法分离

NEGATIVE_CONTROL_INEFFECTIVE / DETECTOR_DEGRADED / CONTROL_NOT_EXECUTED；第三格不能靠加状态，必须换取值来源（重定向 + per-run sentinel）。

## 2. sentinel 必须绑 runId

同路径预种陈旧 sentinel 可伪造绿；建议 HMAC(`runId`, `job_key`)。

## 3. 名单重叠窗方向性

`issued_at` < `cutover_at` 上界；缺上界 = ROSTER_OVERLAP_UNBOUNDED；cutover 后旧 roster 新签拒。

## 4. 缺席声明面

`absent_declared[]` 由签发方填，禁差集反推。

## 5. 独立性可证伪

must-share 对照对；对照仍独立 → INDEPENDENCE_ORACLE_FAIL。

## 6. drift 前置 NC effective

否则 NOT_COMPARABLE。

## 7. 接缝第四格 timeline_receipt

`time_tag` / `light_direction`；失败优先重一侧。

## 8. 口播机检

ASR 回读 + 能量包络切口；xfade 用实测帧。

## 去重说明

a 已覆盖证据时序、签方故障域、sticky/人审、声纹/基线等。本篇收 20260914b 新轴：runner 活性、名单轮换、接缝时间片。
