# 服务方案漏斗（正本）

节拍：**双周一轮（JST）**。一轮只押 **1 个 top1** 到人审；S4 同时最多 1 个方案在做。

命题范围：IT 网站、app、内部工具、FDE 导入、FinOps 看板等可卖服务。

## 阶段

| 阶段 | 截止 | 负责 | 交卷（可点开） | 验收句 | 人审 |
|------|------|------|----------------|--------|------|
| S0 命题 | W1 周一 | 学我说话的秘书 | `ai-ops/boards/funnel/YYYY-WW-brief.md` + asset-board 各 1 行 | 一句话说清本轮找什么 | 否 |
| S1 脑暴 | W1 周三 | 服务孵化的 | `boards/funnel/YYYY-WW-ideas.md`：5 张方案卡 | 每张说清卖给谁、交付什么 | 否 |
| S2 评分 | W1 周五 | 质检看板的（独立）+ 服务孵化的（自评） | 同文件评分表；分差≥2 写分歧；标 top1 | 「为什么是这张」有数 | 否 |
| S3 投入 | W2 周一 | 服务孵化的；涉云则管AWS成本的 24h 供成本行 | `boards/funnel/YYYY-WW-cost.md` | 大概花多少、几周出 demo | **仅超常设预算上限** |
| S4 demo | W2 周五 | 管官网仓的 | homepage 可点壳页 + sample JSON | 陌生人 90 秒懂服务干啥 | 否 |
| S5 人审 | W2 周五 | 秘书打包 | `boards/decisions/YYYY-WW.md` | 机主点开 demo 能拍板 | **是（72h 按默认）** |
| S6 售前/外联 | 下轮 W1 | 搞售前的 → neng社交的 | sales-kit + 发布回执 | 带询盘路径 | **仅新服务首次对外** |

## 红线

1. 没有可点开 demo / 可核对链接，不算交卷、不进 S5。**文章不算 demo。**
2. 人审只三处：S3 超常设上限、S5 选方案、S6 首次对外。其余默认推进。
3. 一轮只押 top1；并列第二进 `boards/funnel/backlog.md`。
4. 已退役产线（宠物短剧 / 3D 生成）不得借漏斗复活，除非机主书面重启。
5. 方案卡链接必须可核对；找不到就少写；不写「未核实」对冲句。
6. 客户法定名/合同号/人名/电话邮箱/密钥/内网 URL/未公开报价永不进仓。

## 仓库落点

- SSOT：`onewonderjapan/ai-ops` → `boards/asset-board.md` + `boards/funnel/` + `boards/decisions/`
- demo：`onewonderjapan/onewonder-homepage`（含 `/project`）
- 公开文章：`ow-open-knowledge` / knowledge-hub（归 neng社交的）
