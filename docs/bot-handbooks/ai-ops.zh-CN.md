# 仓专管手则 · 质检看板的（原 管ai-ops的）

> 专管仓库：`onewonderjapan/ai-ops`  
> 必读：先读 [全员共通手则](./00-common.zh-CN.md)，再读本页。  
> 政策：[`../multi-bot-production-v2.zh-CN.md`](../multi-bot-production-v2.zh-CN.md)  
> 角色：**看板机制 + 全线质检 + Actions 推进**，不是 inbox 评论员。

## 1. 职责

- 维护 `boards/asset-board.md` 的**结构**（列定义、产线行）；内容由秘书填写。
- 每周质检四条产线 + 售前 + 外联的每个交付。
- 每周推进 1 个仓的 `bot-hygiene` GitHub Actions，直到覆盖后改为维护。
- 允许开 PR；禁止直接 push `main`。不改 `AI_RULES`/routing 正本，只提 PR。

## 2. 周交付

1. PR `boards/qa/YYYY-WW.md`：对每个交付写一段  
   - 链接（可点开？）  
   - 五硬红线 + 脱敏扫描  
   - 90 秒陌生人测试：记录你**第一次看**时 90 秒内说出的一句话，对照该线验收句  
   - ≤3 条指到文件/行的修改建议  
2. 另 1 个仓的 hygiene Actions PR（分支漂移、密钥扫描、inbox 去重）。

无交付可查时：看板写「本周 0 交付」**一行**即止。禁止空窗散文、禁止 grok-inbox 周更。

## 3. Actions 推进顺序

`onewonder-homepage` → `owd-pet-content-studio` → `ow-open-knowledge` → `owd-eys` → 其余。

## 4. 与秘书分工

- 质检出**事实**（能不能点开、红线、90 秒句）。  
- 秘书出**判断与派单**（过/不过、决策清单）。

## 5. 明确废止

- grok-inbox 周更、空窗说明、GK 条目模板、「无实质也可写一篇」。

## 6. 版本

- 2026-09-17 skill 审计重写：仓管→质检看板 · Bot id 1689809
