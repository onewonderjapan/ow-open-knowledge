---
id: 20260925-gh-research-framework
title: "GitHub 高星 repo 定期调查框架（3D 渲染与代码生成 2D）"
tags: [research, methodology]
created: 2026-09-25
updated: 2026-09-25
summary: "本主题的调查规程：对象是 AI 做视觉产出（3D 渲染 / 代码生成 2D）的高星 repo；口径用 GitHub API 当日实测星数；知识按「引擎层→神经渲染→生成式→接口层（skill/MCP）」分类轴归类，每轮刷新盘点笔记而非新建。"
lang: zh
type: research
scope: public
source: knowledge-base@8256ce7
related: [20260925-render-3d-landscape, 20260925-codegen-2d-landscape]
---

# GitHub 高星 repo 定期调查框架（3D 渲染与代码生成 2D）

> Summary: 调查对象、数据口径、分类轴与刷新规则。凡是「AI 怎么做出 3D 画面 / 用代码画出 2D 图」的可复用方法论，都归入本主题两篇盘点笔记并持续刷新。

## Context

建题需求（2026-09-25）：定期调查 AI 相关高星 GitHub repo，吸收「如何做 3D 画面渲染」「如何用代码生成 2D 图形」的 skill 与方法论，归类入库。本篇定义规程；首轮成果见两篇盘点笔记。

## 调查口径（每轮必须遵守）

- **数值一律当日实测**：星数、最近 push、是否 archived 用 GitHub API（`GET /repos/{owner}/{repo}`，字段 `stargazers_count` / `pushed_at` / `archived`）当日拉取，笔记中标注 as-of 日期。遵守全库情报时效铁律：禁止沿用上轮名单里的旧数字。
- **入榜门槛**：核心盘点 ≥5k 星；<5k 但方法论有独特价值的（如官方示例、新出现的 MCP）可入「观察名单」，标星数与未核实项。
- **定性材料看原文**：skill 方法论必须读 repo 内 SKILL.md / README 原文（raw.githubusercontent.com），不引用二手转述。
- **健康度三看**：星数 × `pushed_at`（研究 repo 常见「发论文即冻结」）× archived 标记。

## 分类轴（知识归类）

**3D 画面渲染**（→ [render-3d-landscape](render-3d-landscape.md)）：
- A 实时渲染引擎（three.js / R3F / Babylon / PlayCanvas）
- B 神经渲染（3D Gaussian Splatting / NeRF 及其工具链）
- C 生成式 3D（文/图生 3D 资产：TRELLIS、shap-e、threestudio 等）
- D AI 接口层（让 agent 产出/操控 3D 的 skill 与 MCP）

**代码生成 2D**（→ [codegen-2d-landscape](codegen-2d-landscape.md)）：
- A 图 DSL（mermaid、vega-lite 等声明式语法）
- B 画布/矢量库（d3、fabric、konva、p5.js）
- C 代码化动画（manim）
- D 白板/无限画布（excalidraw、tldraw，agent-ready 方向）
- E skill 方法论（anthropics/skills 等官方与高星社区的「怎么写生成式绘图 skill」）

## 吸收方式

1. **每轮刷新盘点**：编辑两篇盘点笔记的表格与结论、bump `updated`，不新建笔记；跨期对比分析才另建。
2. **方法论提炼成模式条目**：如官方 skill 的「philosophy-first 两段式」（先宣言后表达）——提炼时附 SKILL.md 路径与要点，可直接移植到本库其他生成工作流。
3. **结论要分层**：事实（带 as-of）/ 社区共识（注明）/ 本库假设（标「待实证」）。

## 刷新节奏

`review_every: 90`；两篇盘点任一超过 90 天未更新即出现在公开站的 stale 列表，触发下一轮。每轮流程：GitHub API 拉数 → 读新出现的 skill/MCP 原文 → 更新表格与结论 → `make verify` → PR。

## 来源

- GitHub REST API（repo 元数据）：https://docs.github.com/rest/repos/repos#get-a-repository （as-of 2026-09-25 调用）
