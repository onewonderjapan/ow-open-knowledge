# 协作吸收：压制 schema 独立版本 · presence 资产计价 · fixture 未核验降级 · not_evaluated 原因码

- **轨**：`grok/knowledge` 建议（非 main 事实）
- **逻辑域**：video-llm / 视频生产 · 本地LLM · 商业建议
- **建议文件名**：`video-llm/suppress-schema-and-presence-asset-pricing.md`（按 inbox 约定落为 `grok-inbox/2026-09-12-suppress-schema-and-presence-asset-pricing.md`）
- **LEDGER_REF**：`mid-tier-collab-recruit`
- **SOURCE**：EigenFlux DM 汇总（已脱敏）；非 feed 原文入库
- **写入方**：管仓库的 · 2026-09-12
- **状态**：建议轨，未晋升公开 KB

## 1) suppress 三字段（执行真伪 / 人审边界）

当 `suppressed` 只记录 `rule_set_epoch` 时，无法审计「按哪一版压制规则压住」。最小可交换字段：

| 字段 | 语义 | 缺失行为 | 签名域 |
|---|---|---|---|
| `suppress_schema_version` | 压制规则 schema 独立版本，与 `rule_set_epoch` 解耦 | FAIL_CLOSED，禁止记 suppressed | 是 |
| `last_meaningful_progress_at` | 有效前进时间戳；dwell 只从此起算（重试/心跳不算） | 按任务类默认 → DWELL_STALL，不给绿 | 是 |
| `next_due_max_span` | next_due 可推上界，防无限延期 | 用任务类默认上界；超上界 → STALE_PROMISE | 是 |

失效条件：若压制规则无独立 schema、或 dwell 从「任意动作」起算，本条不适用。

## 2) presence 按素材资产计价（非按秒）

- `presence_layer`：真人/真宠镜头带 `visual_anchor` 入库；通过门人审不可跳过；按可复用素材资产计费。
- `execution_layer`：可自动化部分仍按 receipt 计费；两层分列核算。
- 禁止：用秒数或自动化完成度冒充在场；presence 不进无限重试池。

## 3) fixture 正控：契约轨 vs 内容轨 + UNVERIFIED

- `contract_fixtures/`：协议形状永久冻结；改动 = PROTOCOL_DRIFT 事件。
- `content_fixtures/`：随 `model_epoch` 重冻；旧 epoch 只读归档。
- 签名对象含「选择规则」，不只是文件摘要；禁止通配扫盘长大正控集。
- 宣称门可用必须写出 `contract_fixture_rev` + `content_fixture_epoch`；写不出 → 结论降级 **UNVERIFIED**（`verified=false`），不得 PASS。

## 4) not_evaluated 原因码（禁折 not_applicable）

- `not_evaluated` 为硬枚举，原因至少区分：未启动 / 超时 / 依赖缺失 / 执行失败。
- `not_applicable` 必须带规则版本 + 理由码。
- 规则升级：保留旧 receipt，用新 epoch 复审；禁止改写历史结论。
- 负样本覆盖：「误跳过」与「理由码缺失」。

## 去重说明

与已入账 empty-output / identity-vs-styling / fixture-contract-vs-content / mid-tier 招募正文不重复：本文件只收**协作回复沉淀的字段级结论**。若已有 fixture 双轨文，对本文件 §3 做补丁锚到「UNVERIFIED 降级」与「选择规则进签名」两段。
