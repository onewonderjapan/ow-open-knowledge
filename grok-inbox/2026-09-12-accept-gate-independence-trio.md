# 验收门独立性三问（短视频/本地LLM）

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-acceptance / 视频生产 · 本地LLM
- **建议文件名**：`video-acceptance/accept-gate-independence-trio.md`（按 inbox 约定落为 `grok-inbox/2026-09-12-accept-gate-independence-trio.md`）
- **LEDGER_REF**：`collab-20260912-b-accept-gates` / `357009508439949312`
- **SOURCE**：EigenFlux collab 2026-09-12 + T3B（已脱敏）
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB

## 三问

1. **签发权**：负例/期望由人审 authority 签发，bot 只托管；失陷时 VALID_FROZEN 部分幸存，新签发通道关闭。
2. **故障域**：成功判定与转换/被测同分故障域则不可证伪；交付门只认旁路探针；oracle 基准样本需签名 + `corpus_rev`。
3. **使用身份**：缓存/探针/归一器必须带 `judge_rev` 或 `canon_rev` 或 `rule_content_digest`；消费时与当前门不一致则 STALE/重判。

## 附加

预算耗尽用 `PAUSED_BUDGET_EXHAUSTED` + `fallback_event`，禁止静默降配冒充规格。

## 去重说明

相对已有 fixture-dual-track / keyframe_histogram_gate：本篇收的是「独立性元规则」，不是具体探针步骤。
