---
id: 20260906-maturity-quiz-v1
title: "三级成熟度自评问卷 v1"
tags: [research, japan-enterprise-ai]
created: 2026-09-06
updated: 2026-09-06
summary: "以 82.1% 生成 AI 使用 vs 13.3% 跨业务正式 Agent 断层为标尺的 3 题日文自评问卷 v1（L1 個人/L2 部門/L3 横断）+ 3 个反例校验问（個人利用混同/固定マクロ混同/成果物だけ AI）已产出；一致率 ≥70% 假设需 ≥3 次真实客户对话先测后讲，未执行；customer-demo-web 集成为待批项。"
lang: zh
type: experiment
scope: public
source: knowledge-base@e73f8dd
---

# 三级成熟度自评问卷 v1

> Summary: 3 题 + 3 反例校验的日文自评问卷 v1 已产出，挂钩 82.1%/13.3% 基线；一致率验证需真实客户对话，未执行。

## Context

选题来自 [internal path] L-16（方向⑤）：用日本本土调查基线让客户「定位自己」，为八道门第 0 道（現状確認）提供开场工具。

## 产出与使用

- 问卷：[internal path]（含记录欄：セルフ判定/検証後補正/一致・不一致）
- 反例校验防虚报：①個人利用≠会社利用 ②固定マクロ/RPA 不算 L3 ③只生成成果物不算 L2 工程組込み
- 使用口径：先自评→后讲解→对照补正→记录一致率；累计 ≥3 例后回填本页。

## 待办（人类环节 + 待批项）

1. ≥3 次客户/准客户对话实测一致率（人类执行）→ 回填 result 判定 ≥70% 假设。
2. 挂进 customer-demo-web 费用与导入页：代码改动超出施工白名单，报总控派任务。

## Related

- 日本企业 AI 导入 · 情报速览 — supports: 基线数字与三级标签建议来源。
- 客户 AI Demo 操作与讲解指南（内部笔记 20260721-customer-ai-demo-guide，未公开） — supports: adoption 页边界与八道门衔接。
- [「规则标准化型 Agent」案例卡→日文客户可读方案模板 v1](case-template-jp.md) — see-also: 问卷与案例卡在 demo 流程中配套使用。
