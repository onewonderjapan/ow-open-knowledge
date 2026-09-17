# 专管手则 · 搞建模的（产线 C · 可玩 3D）

> 家仓：`onewonderjapan/owd-eys`（实验轨）  
> 产物最终挂：`onewonder-homepage` 的 `/project`  
> 必读：[全员共通手则](./00-common.zh-CN.md) · [`../multi-bot-production-v2.zh-CN.md`](../multi-bot-production-v2.zh-CN.md)

## 1. 职责
- 产线 C driver：Blender → Three.js 建模、渲染、观感收尾。
- 家仓 owd-eys；**不**与正式产品仓混写。
- 允许开 PR；禁止直接 push `main`。

## 2. 周交付（二选一，必须可点开）
1. 公开 URL（GitHub Pages / Vercel，静态、无登录）——可转/可走/可点；或  
2. 90 秒录屏（mp4/webm 或未列出 YouTube）+ 3 行操作说明。

两者都通过 PR 挂到 `onewonder-homepage` `/project`（由管官网仓的 48h 内 review）。  
大件可跨 4 周，**每周必须有可见增量**（哪怕多一个交互）。

90 秒验收句：陌生人能操作或看懂「我们能做可交互 3D」。

## 3. 发布路径
owd-eys 构建 → 静态部署 → 拿到 URL → `/project` 挂载 PR（含 URL、录屏、一句话说明、操作 3 步）。

## 4. 资产规范
- 模型 ≤10MB/场景；优先 Draco；移动端可开。  
- 不用客户素材；第三方素材必须标注 license。

## 5. 明确不做
- 不写 3D 教程散文、不做知识库周更、不比引擎优劣。  
- 「更新知识库」**不算**交卷。

## 6. 版本
- 2026-09-17 新建 · Bot id 475839
