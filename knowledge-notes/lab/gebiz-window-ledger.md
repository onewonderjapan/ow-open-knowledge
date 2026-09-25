---
id: 20260906-gebiz-window-ledger
title: "新加坡 GeBIZ 投标窗口分布实测（8 周观察，L-20）"
tags: [research, singapore-it]
created: 2026-09-06
updated: 2026-09-06
summary: "8 周窗口观察第 1 周：台账已建（[internal path]），首批 4 个 IT 类机会窗口 12.85/24.91/≈9(粗)/12.99 天，中位数初值 ≈12.9 天、≤14 天占比 3/4，与假设方向一致但 n=4 不足以判定；每周由轮询会话从 digest 追加，8 周后出分布报告。"
lang: zh
type: experiment
scope: public
source: knowledge-base@e73f8dd
---

# 新加坡 GeBIZ 投标窗口分布实测（8 周观察，L-20）

> Summary: 台账已建并录入首批 4 点（中位初值 ≈12.9 天）；假设两项一符一未达；8 周观察期内不作结论。

## Context

选题来自 [internal path] L-20：digest 已可算 4 条机会窗口但无时效统计；本实验以 8 周滚动台账补齐分布与响应时效依据。

## 台账与 SOP

- 台账：[internal path]（周例行 SOP 内置：每周从 digest 追加、首响只记真实事件、每 4 周复算、第 8 周出报告回填本页）。
- 数据源：自动入库的 `topics/singapore-it/singapore-it-digest.md`，不新增检索。

## 局限

- 窗口时长 ≠ 可响应窗口（文件获取/澄清问询另计）。
- digest 只覆盖进入情报频道的机会，存在遗漏概率；口径以 digest 为准。
- MFA 条目发布时刻缺失，窗口为粗口径。

## Related

- 新加坡 IT 机会 · 情报速览 — supports: 数据源。
- [三级成熟度自评问卷 v1](maturity-quiz-v1.md) — see-also: 同批（2026-09-06）lab 实验。
