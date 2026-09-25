---
id: 20260906-subscription-vs-api-crossover
title: "会员订阅 vs API 按量计费交叉点实测"
tags: [research, ai-intel]
created: 2026-09-06
updated: 2026-09-06
summary: "30 天真实用量（Win+S1，33,853 Claude 请求等）双口径计价：Claude 真实混合下 API 等价 $10,278~$32,175/月 vs Max $200（会员划算 ~51×，缓存 token 占 99.7% 是根源）；GLM 样本下 Lite ¥49 已划算（按量 ≤¥159）；OpenAI 牌价缺口未计价。理论「折合输出指数」最末位的 Claude Max 实际兑现 206 Mtok（×51）——指数排序与实付排序错位 ≥1 名，适配口径下假设成立。"
lang: zh
type: experiment
scope: public
source: knowledge-base@e73f8dd
related: [20260906-model-blindtest-quadrant]
---

# 会员订阅 vs API 按量计费交叉点实测

> Summary: 30 天真实用量双口径计价：缓存重载的 Agent 工作流让「理论指数最差」的 Claude Max 实际兑现 ×51；交叉点由自家缓存/输出比决定，而非厂商指数排名。

## Context

选题来自 [internal path] L-05（方向②）：笔记的折合输出指数是纯理论值（月费÷旗舰输出价，自注汇率未实时、混合未知）；本实验用真实用量重算。

## 数据与口径

- 提取器与计价脚本：[internal path]（aggregate_usage.py、crossover.py），原始聚合 usage.json / s1-usage-30d.json，结果 results.md。
- 牌价假设与缺口（OpenAI 牌价、GLM 缓存价、opus-5 推算价）全部见 done.md 报备区，引用数字时必须携带。

## 结论与局限

1. Anthropic：会员压倒性划算（~51×），交叉点 ≈ 当前用量 2% 以下——缓存占比 99.7% 的 Agent 用法是主因。
2. GLM：样本下 Lite 已划算；覆盖不全（仅本机），团队全量口径待补。
3. OpenAI：牌价缺口，待补抓后复跑。
4. 局限：FX 固定 7.1；cache 桶读写合并双算上下界；30 天窗口单月样本。

## Related

- AI 会员与 API 价格指数 — supports: 牌价与理论指数来源。
- [自有任务多模型盲测与价格×能力象限](model-blindtest-quadrant.md) — see-also: 同批价格×能力实验，能力轴互补。
