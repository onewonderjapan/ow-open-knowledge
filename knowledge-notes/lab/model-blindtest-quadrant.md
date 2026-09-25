---
id: 20260906-model-blindtest-quadrant
title: "自有任务多模型盲测与价格×能力象限"
tags: [research, ai-intel]
created: 2026-09-06
updated: 2026-09-06
summary: "12 道自有任务（代码/剧本/日文邮件）× 5 模型三盲盲测（GLM-5.3 主评+Flash 副评，绝对分天花板后补强制排名 24 对）：Borda 排名 opus-5 68 > gpt-6-astra 53 > GLM-5.3 43 > GLM-5.3-Flash 40 > gpt-5.6-luna 36；预注册「位次互换」假设因榜单可比对不足（仅 2 模型有榜）不可判定；定性：榜单「GLM≈Opus」口径在本团队任务未复现，代码题 20/20 全过无区分。"
lang: zh
type: experiment
scope: public
source: knowledge-base@8256ce7
---

# 自有任务多模型盲测与价格×能力象限

> Summary: 12 自有任务 × 5 模型三盲盲测：Borda 排名 opus-5 明显第一；绝对分口径天花板失效应弃用；预注册位次互换假设因榜单覆盖不足不可判定；榜单「GLM≈Opus」口径未在本团队任务复现。

## Context

选题来自 [internal path] L-04：公开榜单的价格×能力散点只有 4 个点且能力全是第三方 SWE-bench（证据链第一条自注局限）。本实验补「自己的」象限点。

## 数据（实测 2026-09-06）

- 跑批 60 调用全成功；CLI 首轮 36 调用因 cmd.exe 转义截断 prompt 作废重跑（raw/ 留证）。
- 盲评 120 调用（逐响应独立）+ 强制排名 24 调用（逐题全序）；代码机械判分 20/20 PASS。
- 全部调用六要素落 [internal path]；汇总表 [internal path]。

## 结论与 caveat

1. 排名结论以 Borda 为准：opus-5 > gpt-6-astra > GLM-5.3 > GLM-5.3-Flash > gpt-5.6-luna。
2. 预注册假设不可判定 ≠ 不成立：需参赛集含 ≥3 个有榜单读数模型（如接入 DeepSeek V4 Pro）方可复跑。
3. 局限：codex/claude 为 agent 环境非裸 completion（无 temperature 控制）；主评 GLM-5.3 兼参赛者（三盲下不知情）；GLM-5.3-Flash/gpt-6-astra 价格 TBD、opus-5 为推算价，散点缺 2 点。
4. 方法论副产物：绝对分盲评存在「礼貌性高分」天花板，任务内强制排名是对冲手段，可复用于 L-03 系机评。

## 复现

任务集/跑批/评审/汇总脚本与原始响应全部在 [internal path]（tasks.jsonl → run_contestants.py → check_code.py / judge.py / judge_rank.py → aggregate.py），按序执行可复现三表。

## Related

- AI 会员与 API 价格指数 — supports: 价格轴来源。
- AI 模型情报与能力评分 — supports: 榜单名次轴来源。
- [新加坡 GeBIZ 投标窗口分布实测（8 周观察，L-20）](gebiz-window-ledger.md) — see-also: 同批（2026-09-06）lab 实验。
- [会员订阅 vs API 按量计费交叉点实测](subscription-vs-api-crossover.md) — see-also: 同批价格侧实验，计费口径互补。
