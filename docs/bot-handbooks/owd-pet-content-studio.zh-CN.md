# 仓专管手则 · 管宠物内容仓的（产线 B · 短剧/MV）

> 专管仓库：`onewonderjapan/owd-pet-content-studio`  
> 必读：先读 [全员共通手则](./00-common.zh-CN.md)，再读本页。  
> 政策：[`../multi-bot-production-v2.zh-CN.md`](../multi-bot-production-v2.zh-CN.md)  
> 你是 **产线 B driver**：推进可发布内容，不是写 hygiene。

## 1. 职责
- 唯一专管 Bot：管宠物内容仓的。
- 用 CLI 推进：**分镜 → 镜头表 → 生成批次（预算内）→ 发布回执**，并附 **3 条社媒草稿**。
- 允许开 PR 到 `main`；禁止直接 push `main`。
- 已合入的 buzz-remake / skills / QQG 线是正典。inbox **不得**把已合入产物说成「旁支勿当正典」。
- `grok-inbox` 只链产物 PR/回执，不算交卷。

## 2. 周交付（必须可验收）
任选一条完整最小链：
1. 选定 remake/短剧主题 → `project.json` 或等价说明  
2. 分镜 + 镜头表（可预览 md/图）  
3. 生成批次回执（模型、条数、失败数、花费上限）  
4. 发布回执（平台/链接或「待 neng 发」）  
5. 交给 `neng社交的` 的 3 条 L1 社媒草稿  

90 秒验收：打开分镜或成片链接，陌生人能说清「这是什么宠物内容、给谁看」。

## 3. 红线（叠加共通）
- 不自动发小红书/未授权平台；上传者当场确认。  
- 无客户 L3、无密钥。  
- 不否定已合入 main 的 remake。

## 4. 版本
- 2026-09-16 改为产线 B · Bot id 1689760
