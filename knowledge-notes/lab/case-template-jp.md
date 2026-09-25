---
id: 20260906-case-template-jp
title: "「规则标准化型 Agent」案例卡 → 日文客户可读方案模板 v1"
tags: [research, japan-enterprise-ai]
created: 2026-09-06
updated: 2026-09-06
summary: "四段结构（痛点→AI 切入点→人保留责任→量化指标）日文模板 v1 已产出并套入 freee/SoVa 与 NEC SCM 两案例，责任边界句与 demo 固定话术兼容、含追踪指标（処理時間/エラー率/新人の習熟速度，均未収集）与 13.3% 基线；复述通过率验证（非技术读者 5 分钟复述）待人类执行。"
lang: zh
type: experiment
scope: public
source: knowledge-base@e73f8dd
---

# 「规则标准化型 Agent」案例卡 → 日文客户可读方案模板 v1

> Summary: 模板 v1（日文）+ freee/SoVa、NEC SCM 两案例卡已产出且与 demo 责任边界句兼容；复述通过率验证为人类环节，未执行，假设未判定。

## Context

选题来自 [internal path] L-15（方向⑤）：把「别人的新闻」变成客户方案参照系，需要非技术客户 5 分钟能对号入座的模板。

## 产出

- 模板：[internal path]（四段结构 + 追踪指标表 + 成熟度标签位 + 13.3% 基线注记 + 八道门衔接）
- 案例卡：`case_freee_sova.ja.md`（规则标准化型・L2 目安）、`case_nec_scm.ja.md`（横断型・L3 目安・年 1,800 万円〜锚点）
- 全部指标标注「未収集（追跡開始前）」，不虚构数字。

## 待办（人类环节）

1. 1–2 位非技术读者限时 5 分钟阅读并复述「AI 插在哪、人管什么」，记录复述完整度 → 回填本页 result 并判定假设。
2. 模板定稿需总控确认后方可对客使用。

## Related

- 日本企业 AI 导入 · 情报速览 — supports: 案例与指标建议来源。
- 客户 AI Demo 操作与讲解指南（内部笔记 20260721-customer-ai-demo-guide，未公开） — supports: 固定话术与八道门兼容边界。
- [自有任务多模型盲测与价格×能力象限](model-blindtest-quadrant.md) — see-also: 同批（2026-09-06）lab 实验。
