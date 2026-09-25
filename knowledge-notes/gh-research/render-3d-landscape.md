---
id: 20260925-render-3d-landscape
title: "3D 画面渲染：高星 repo 路线图与方法论"
tags: [research, tactics]
created: 2026-09-25
updated: 2026-09-25
summary: "3D 渲染高星 repo 四层盘点（as-of 2026-09-25，GitHub API 实测）：实时引擎 three.js 115.9k 一枝独秀且日更；神经渲染主线已收敛到 3DGS 工具链；生成式 3D 研究 repo 普遍「发论文即冻结」；AI×3D 的增量在 MCP/skill 接口层而非新算法库。"
lang: zh
type: research
scope: public
source: knowledge-base@8256ce7
related: [20260925-gh-research-framework, 20260925-codegen-2d-landscape]
---

# 3D 画面渲染：高星 repo 路线图与方法论

> Summary: 按「实时引擎 → 神经渲染 → 生成式 3D → AI 接口层」四层归类；每层给星数/健康度实测与方法论要点。周期刷新（下一轮 ≥2026-12 或提前触发）。

## Context

首轮调查（2026-09-25），规程见 [调查框架](gh-research-framework.md)。星数与 `pushed_at` 均为当日 GitHub API 实测。

## A 实时渲染引擎（全部活跃）

| repo | 星数 | 最近 push | 要点 |
|---|---|---|---|
| [mrdoob/three.js](https://github.com/mrdoob/three.js) | 115,879 | 2026-09-25 | WebGL/WebGPU 3D 事实标准，日更；AI 生成 3D 画面的默认靶场 |
| [pmndrs/react-three-fiber](https://github.com/pmndrs/react-three-fiber) | 32,484 | 2026-09-24 | three.js 的 React 声明式渲染器；组件树写法对 LLM 代码生成友好 |
| [BabylonJS/Babylon.js](https://github.com/BabylonJS/Babylon.js) | 26,109 | 2026-09-24 | 引擎+编辑器+工具链一体，游戏向 |
| [playcanvas/engine](https://github.com/playcanvas/engine) | 16,923 | 2026-09-25 | WebGL/WebGPU/WebXR 运行时，glTF 资产管线 |

## B 神经渲染（真实感重建）

| repo | 星数 | 最近 push | 状态 |
|---|---|---|---|
| [graphdeco-inria/gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting) | 23,970 | 2025-10-17 | 3DGS 原始参考实现；研究代码冻结（约 11 个月无 push） |
| [nerfstudio-project/nerfstudio](https://github.com/nerfstudio-project/nerfstudio) | 12,026 | 2025-07-29 | NeRF 工作室；引擎本体活跃度下降 |
| [playcanvas/supersplat](https://github.com/playcanvas/supersplat) | 10,260 | 2026-09-23 | 浏览器端 3DGS 编辑器，活跃——落地工具比论文代码活得好 |
| [nerfstudio-project/gsplat](https://github.com/nerfstudio-project/gsplat) | 5,728 | 2026-09-19 | 3DGS 的 CUDA 光栅化内核，活跃 |

## C 生成式 3D（文/图生 3D 资产）

| repo | 星数 | 最近 push | 状态 |
|---|---|---|---|
| [microsoft/TRELLIS](https://github.com/microsoft/TRELLIS) | 13,701 | 2026-06-26 | 图/文生 3D（CVPR'25 Spotlight），本层唯一尚在维护的高星项 |
| [openai/shap-e](https://github.com/openai/shap-e) | 12,263 | 2024-06-22 | 冻结两年多 |
| [threestudio-project/threestudio](https://github.com/threestudio-project/threestudio) | 7,066 | 2024-12-16 | 冻结 |
| [TencentARC/InstantMesh](https://github.com/TencentARC/InstantMesh) | 4,536 | 2025-01-03 | 观察名单（<5k）；单图生 mesh，冻结 |

## D AI 接口层（agent 产出/操控 3D）

- **官方 skill 无 3D 项**：[anthropics/skills](https://github.com/anthropics/skills)（178,096 星，2026-09-25 实测）19 个官方 skill 覆盖 canvas/算法艺术/前端，唯独没有 3D——3D 的官方位是空的。
- **MCP 实时操控路线**：threejs-devtools-mcp（[mcpmarket 条目](https://mcpmarket.com)）提供 59 个工具在浏览器里实时检视/修改 three.js 场景（对象/材质/着色器/动画）；three.js 官方 MCP Apps 示例提供托管式 3D Viewer（星数未核实）。
- **扩展/应用路线**：Hello3DMCP（[three.js Discourse, 2026-01](https://discourse.threejs.org)）以 Claude Desktop 扩展形式装出 AI 驱动的 3D 交互应用。
- **社区 skill 路线**：agenticskills.io 收录的 "Three.js Skills"（场景搭建/相机/渲染器配置；星数未核实）。

## 结论

1. **「发论文即冻结」是生成式 3D 的常态**：本层 4 个高星 repo 中 3 个已停更 9 个月以上（shap-e / threestudio / InstantMesh / graphdeco 原始实现同理）。吸收它们的方法论要一次抓全（论文+README+示例），不能依赖上游维护；活跃的是工具链与产品化层（gsplat、supersplat）。
2. **生产路径共识**：three.js（事实标准）+ 声明式封装（R3F 组件树对 LLM 生成更友好，错误更局部）+ glTF 资产管线（PlayCanvas 系工具链背书）。
3. **神经渲染落地收敛到 3DGS**：CUDA 内核（gsplat）与浏览器编辑器（supersplat）都活跃，而 NeRF 引擎本体趋缓。真实感重建需求走 3DGS，风格化/交互需求走实时引擎。
4. **AI×3D 的 2026 增量在接口层**：无官方 3D skill 的空位由社区以两条路线填补——「文本→three.js 代码直接生成」（轻量、一次性）与「MCP 闭环：生成→实时检视→修改」（可迭代）。给本库 AI 生成 3D 画面的默认建议：简单场景用 R3F 代码生成；需要反复调的场景用 MCP 闭环。
5. 待实证（本库假设）：声明式（R3F）比命令式（原生 three.js）更适合 LLM 一次生成成功——直觉来自组件树的结构约束，未做对照实验。

## 下一轮待办

- 核实 threejs-devtools-mcp / Hello3DMCP / Three.js Skills 各自星数与维护状态（本轮未核实）。
- 关注 tldraw 的 agent-ready 画布是否延伸出 3D 形态。

## 来源

- GitHub API 实测（as-of 2026-09-25）：上表各 repo `https://github.com/<owner>/<repo>`；anthropics/skills 目录列表 `https://api.github.com/repos/anthropics/skills/contents/skills`
- three.js MCP 生态：https://mcpmarket.com 、https://discourse.threejs.org 、https://agenticskills.io （2026-09-25 检索）
