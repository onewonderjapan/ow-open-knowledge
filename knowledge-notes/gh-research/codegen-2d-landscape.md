---
id: 20260925-codegen-2d-landscape
title: "代码生成 2D：高星 repo 与官方 skill 方法论"
tags: [research, tactics]
created: 2026-09-25
updated: 2026-09-25
summary: "代码生成 2D 五层盘点（as-of 2026-09-25）：最高星的是「AI 可靠生成的目标格式」库（mermaid 90.4k / excalidraw 132.9k / manim 94.2k）；官方 skill 方法论样本 anthropics/skills（178.1k）是先写美学宣言再用 canvas/p5.js 表达的两段式，强调不锁创意、craftsmanship、原创避版权。"
lang: zh
type: research
scope: public
source: knowledge-base@8256ce7
related: [20260925-gh-research-framework, 20260925-render-3d-landscape]
---

# 代码生成 2D：高星 repo 与官方 skill 方法论

> Summary: 按「图 DSL → 画布/矢量库 → 代码化动画 → 白板 → skill 方法论」五层归类；方法论重点是官方 skill 的两段式生成结构与可移植纪律。周期刷新。

## Context

首轮调查（2026-09-25），规程见 [调查框架](gh-research-framework.md)。星数为当日 GitHub API 实测；SKILL.md 内容读自 raw 原文。

## E skill 方法论层（先讲，因为这是「怎么教 AI 画 2D」的正典）

### 仓库面

| repo | 星数 | 最近 push | 定位 |
|---|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 291,447 | 2026-09-25 | agentic skills 框架 + 软件开发方法论，全 GitHub 梯队顶部 |
| [anthropics/skills](https://github.com/anthropics/skills) | 178,096 | 2026-09-24 | Anthropic 官方 Agent Skills 仓（19 个 skill，目录 2026-09-25 实测） |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 90,586 | 2026-09-22 | MCP 参考/社区服务器 |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | 15,171 | 2026-04-28 | skill 聚合清单 |

官方 19 个 skill 中与 2D 视觉直接相关：`canvas-design`、`algorithmic-art`、`frontend-design`、`web-artifacts-builder`、`theme-factory`、`slack-gif-creator`（另有品牌/文档向的 `brand-guidelines` 等）。

### 方法论提炼：philosophy-first 两段式（读自官方 SKILL.md 原文）

[canvas-design/SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/canvas-design/SKILL.md) 与 [algorithmic-art/SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/algorithmic-art/SKILL.md) 结构同构，是「AI 生成静态视觉/生成艺术」的可复制模式：

1. **第一段·宣言（.md）**：先命名一个 1–2 词的美学运动（如 "Brutalist Joy"、"Chromatic Silence"），写 4–6 段哲学，规定它如何经由——canvas 版：空间与形式/色彩与材质/尺度与节奏/构图与平衡/视觉层级；算法版：计算过程与涌现/噪声与种子随机/粒子与场/参数变化与受控混沌。
2. **第二段·表达（同会话）**：按宣言落地——canvas 版输出 .pdf/.png（成品 90% 视觉、10% 必要文字）；算法版输出 p5.js 的 .html+.js（带种子随机与可交互参数探索，可复现）。

**共同纪律（可移植到任何生成式视觉任务，含本库图像/视频工作流）**：
- 用户输入只作地基，不锁死创作自由；
- 宣言里反复强调 craftsmanship（"meticulously crafted"、"master-level execution"）——用措辞抬高生成质量下限；
- 原创性约束写进 description：不复制在世艺术家作品（版权）；
- 输出物类型白名单（只出声明的文件类型）。

### 聚合层启示

superpowers（291k）把「skill 即方法论」做成了独立赛道——skill 不只是提示词模板，而是带纪律的工序。值得单独一轮调查吸收其框架设计（列入下一轮待办）。

## A–D 目标格式层（AI 生成 2D 的「靶场」）

| 层 | repo | 星数 | 最近 push | 对 LLM 生成的意义 |
|---|---|---|---|---|
| A 图 DSL | [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) | 90,418 | 2026-09-21 | 文本→流程/时序图的事实标准，LLM 生态默认图输出 |
| A 图 DSL | [vega/vega-lite](https://github.com/vega/vega-lite) | 5,497 | 2026-09-24 | 纯声明式统计图语法，JSON 即图 |
| B 画布/矢量 | [d3/d3](https://github.com/d3/d3) | 113,762 | 2026-05-28 | 数据驱动 SVG/Canvas，命令式、表达力最强也最难生成 |
| B 画布/矢量 | [fabricjs/fabric.js](https://github.com/fabricjs/fabric.js) | 31,464 | 2026-09-25 | Canvas 编辑器内核（SVG↔Canvas 互转） |
| B 画布/矢量 | [konvajs/konva](https://github.com/konvajs/konva) | 14,825 | 2026-09-23 | 交互式 Canvas 框架，设计编辑器常用 |
| B 画布/矢量 | [processing/p5.js](https://github.com/processing/p5.js) | 24,041 | 2026-09-24 | 创意编码运行时——官方 algorithmic-art skill 的选型 |
| C 代码化动画 | [3b1b/manim](https://github.com/3b1b/manim) | 94,241 | 2026-09-09 | 数学解释动画引擎（原版） |
| C 代码化动画 | [ManimCommunity/manim](https://github.com/ManimCommunity/manim) | 41,049 | 2026-09-22 | 社区维护版，文档/安装对 LLM 更友好 |
| D 白板 | [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw) | 132,877 | 2026-09-24 | 手绘风白板，本层最高星 |
| D 白板 | [tldraw/tldraw](https://github.com/tldraw/tldraw) | 50,561 | 2026-09-25 | 无限画布 SDK，官方描述自称 agent-ready——白板正在变成 agent 的画布 |

## 结论

1. **本主题最高星的不是 AI repo，而是「AI 可靠生成的目标格式」**：excalidraw（132.9k）、d3（113.8k）、manim（94.2k）、mermaid（90.4k）。方法论第一问不是「用哪个模型」，而是「让模型往哪个受限格式里生成」——语法越受限、越声明式，一次生成成功率越高。
2. **官方 skill 方法论 = philosophy-first 两段式**（宣言 → 表达）+ 四条纪律（输入不锁创意 / craftsmanship 措辞 / 原创避版权 / 输出白名单）。这是本轮最值得吸收的模式，可直接移植。
3. **选型映射**（经验规则，供 agent 直接引用）：结构图/流程图→mermaid；统计图→vega-lite（声明式优先）或 d3（复杂交互）；海报/静态视觉→canvas-design 模式（HTML canvas→png/pdf）；生成艺术→algorithmic-art 模式（p5.js+种子随机）；教学动画→manim（社区版）；交互画布应用→tldraw/fabric。
4. **白板层是 agent 化最激进的一层**：tldraw 官方定位已写明 agent-ready（描述原文，2026-09-25 API 实测）；excalidraw 体量更大但 agent 叙事较弱——下轮对比两者 agent API。
5. 待实证（本库假设）：LLM 画图可靠性排序 文本 DSL（mermaid）> 声明式（vega-lite/SVG）> 命令式（d3/fabric）> 帧级动画（manim）。直觉来自约束强度，未做对照实验；可用 [20260904-video-gen-model-pilot] 的预注册横评协议改造成 2D 版验证。

## 下一轮待办

- superpowers 框架设计单轮调查（skill 工序化/方法论打包方式）。
- tldraw vs excalidraw 的 agent 接口对比；验证第 5 条可靠性排序假设。

## 来源

- GitHub API 实测（as-of 2026-09-25）：上表各 repo 与 anthropics/skills 目录（`https://api.github.com/repos/anthropics/skills/contents/skills`）
- 官方 skill 原文：https://raw.githubusercontent.com/anthropics/skills/main/skills/canvas-design/SKILL.md 、https://raw.githubusercontent.com/anthropics/skills/main/skills/algorithmic-art/SKILL.md （2026-09-25 读取）
