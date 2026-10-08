# 多 Bot 生产性大改审查（Fable 5.1 结论整理）

> 来源：Cursor `claude-fable-5-1` 对计划/手则 + 10 仓 `grok-inbox` 抽样审查。  
> 写稿阶段 CLI 多次挂起，本文件由秘书按 Fable 会话结论定稿（2026-09-16）。机主已授权**可以大改**。

---

## 1. 诊断：为什么现在不生产（机制层）

### 1.1 验收标准错了
- 当前「交卷」= 在 `grok/knowledge` 写一篇 hygiene / 空窗 / 分支状态说明。
- 对公司拿单无直接贡献：没有可点开的 demo、没有可发的帖、没有可给客户的 brief。

### 1.2 激励与真实生产脱节
- **真实产出在别处发生**：`owd-pet-content-studio` 已有 ~19 skills、连续 buzz-remake PR 合入；官网有 FDE kickoff / 站点企划 / Next 应用。
- **仓管 inbox 却在唱反调**：把已合入的 remake 说成「旁支别当正典」、对 FDE 连续四篇「没产品决策就别做」——bot 在挡路，不是在推进。

### 1.3 噪声淹没信号
- `ow-open-knowledge` 出现大量近乎同质的 `accept-gates-lookdev-*`（EigenFlux/agent 社交 jargon 倾倒），与 SES 获客无关。
- 周更文件充满「未核实 / 不要…」对冲；`grok-feedback` 设计不错但一轮后死亡，闭环从未形成。

### 1.4 门太多、拍板悬空
- 计划 ~40KB、17 项拍板未收口；分析门/晋升门/脱敏门/确认门全等拍板 → 默认动作变成「写文档等」。
- 「禁止 push main」+「只写 inbox」把 LLM 锁在元评论循环；token 烧在散文而不是草稿/代码/分镜。

### 1.5 「外联」名不副实
- `neng社交的` / EigenFlux 主要是 **agent↔agent** 网络，不是新加坡/西方 B2B 客户会去的渠道。
- 已有但未跑起来的真人渠道：Zenn（技术博客计划已写、drafts 空）、X/IG（宠物）、YouTube（MV）、公开 GitHub；**LinkedIn（SG/西方）缺席**。

---

## 2. 大改建议（原则）

1. **默认可交付**：除 5 条硬红线外，默认开 PR / 出可预览产物；inbox 散文不算交卷。  
2. **四条产品线**（对齐机主证明点），每条有周配额 + 90 秒陌生人可懂验收：  
   - **A 官网 FDE**：A/B demo 壳 + 数据文件（可讲解）  
   - **B 宠物短剧/MV**：分镜→镜头表→生成批次→发布回执 + 3 条社媒草稿  
   - **C 可玩 3D 证明**：Three.js / 机器人地图类 → 公开 URL 或 90s 录屏挂 `/project`  
   - **D 公开技术文章**：每周 1 篇 L1 文章进 Zenn/公开仓（从内稿晋升）  
3. **角色压缩**：10 仓专管 → **4 条产线 driver** + 秘书调度 + 外联 + 质检；仓卫生改 GitHub Actions，不再用 LLM 做 orphan 扫描。  
4. **外联改真人渠道**：Zenn / X·IG / YouTube / LinkedIn；EigenFlux 降级为只读情报。  
5. **一次拍板表**：17 项悬空决策给默认推荐，机主可覆写；不再用「等拍板」当空窗借口。

### 硬红线（仅此停下请示）
1. 删库/删生产数据  
2. 外发客户 L3 / 密钥 / 未脱敏  
3. 未授权的付费开通  
4. 直接 force-push / 绕过保护改 main（改走 PR）  
5. 对外冒充真人客户承诺  

其余：**开 PR、写草稿、生成资产、挂预览** 都算推进。

---

## 3. P0 / P1 落地清单

### P0（本周）
| 项 | 路径/动作 |
|---|---|
| 重写共通手则 | `docs/bot-handbooks/00-common.zh-CN.md`：五红线 + 默认出货 + 周交付定义（产物≠散文） |
| 官网产线手则 | `docs/bot-handbooks/onewonder-homepage.zh-CN.md`：周交付 = FDE brief+data 或 demo 页 PR |
| 宠物产线手则 | `docs/bot-handbooks/owd-pet-content-studio.zh-CN.md`：周交付 = 分镜/镜头/生成回执+3 社媒草稿 |
| 公开知识产线 | `docs/bot-handbooks/ow-open-knowledge.zh-CN.md`：禁 EF 倾倒；周交付 = 1 篇可公开文章 PR |
| neng 外联手则 | `docs/bot-handbooks/neng-social.zh-CN.md`（新建）：渠道矩阵、周配额、脱敏清单、KPI |
| 资产看板 | `ai-ops`：`boards/asset-board.md`（或 `grok-inbox` 改名为产线看板）四线状态 |
| 拍板默认表 | `docs/multi-bot-decisions-defaults.zh-CN.md`：17 项给推荐值 |
| 归档噪声 | 将 `accept-gates-lookdev-*` 归档进单一目录/PR（推荐合，等机主最终点头可并行） |

### P1（两周内）
| 项 | 动作 |
|---|---|
| 计划瘦身 | 五分册压缩为 ≤300 行「生产版」；旧文归档 |
| Hygiene→Actions | 各仓加 bot-hygiene workflow（分支漂移、密钥扫描），停掉 LLM 日审 |
| 官网第一个 FDE PR | `src/app/...` demo 壳 + JSON；对接 kickoff 8+1 |
| 宠物一条完整发布链 | remake → project.json → storyboard PR → 发布回执 |
| `/project` 证明位 | 挂上已有 Three.js / YouTube 证明链接（先找公开 URL） |
| 路由规则 | 专管可开 PR 到 main，合并仍由人或指定门；废「只许 inbox」 |

---

## 4. neng社交的 → 定期外联生产机

### 渠道（真人）
| 渠道 | 内容 | 周配额（起步） |
|---|---|---|
| Zenn | 技术/FDE/本地 LLM | 1 篇 |
| X / Instagram | 宠物短剧/MV 切片 | 3 条 |
| YouTube | MV / 短剧合集 | 1 次更新或描述刷新 |
| LinkedIn | 公司能力/案例（SG/西方） | 1 帖 |
| EigenFlux | **只读情报**，不计入外联 KPI | 可选摘要进内网 |

### 流程
产线产出 → 脱敏清单（L1、无客户名/密钥）→ neng 排期发布 → KPI 表（发帖数、曝光、主页访问、询盘）  
无脱敏过的内容：**不许发**。

### KPI（周）
- 发帖达成率  
- 至少 1 条可带来询盘路径的帖（含联系方式/官网）  
- EigenFlux 不计入「外联完成」

---

## 5. 仓专管：从写 inbox → 推进可展示/可变现资产

| 旧 | 新 |
|---|---|
| 周更一篇 hygiene md | **打开/更新 1 个 PR 或可预览产物** |
| 「建议开发去看」 | 自己用 CLI 起草 demo/分镜/文章，PR 里给验收步骤 |
| 空窗说明 | 仅当产线阻塞且已 ALT；否则必须推进最小可交付 |
| 10 仓平行元评论 | 映射到四条产线；非产线仓降频或改 Actions |

**周验收一句话**：陌生人打开链接，90 秒内能懂你们会什么。

---

## 6. 给 Grok 4.6 的实施顺序（立刻执行）

在 `onewonderjapan/ow-open-knowledge` 的 `plan/multi-bot-periodic-collab`（或新分支 `grok/production-rework`）上：

1. **重写** `docs/bot-handbooks/00-common.zh-CN.md`（五红线、默认出货、周交付=产物、CLI 优先保留）。  
2. **改写** `onewonder-homepage` / `owd-pet-content-studio` / `ow-open-knowledge` 三份仓手则（按 §3 P0）。  
3. **新建** `docs/bot-handbooks/neng-social.zh-CN.md`。  
4. **新建** `docs/multi-bot-decisions-defaults.zh-CN.md`（拍板默认表）。  
5. **新建** `docs/multi-bot-production-v2.zh-CN.md`（≤300 行生产版总览；旧分册加「归档，以 v2 为准」头注）。  
6. **更新** `docs/bot-handbooks/README.md` 索引。  
7. 在 `onewonderjapan/ai-ops` 的 `grok/knowledge`：**新建** `boards/asset-board.md` 四线看板模板。  
8. **不要**本轮改业务代码（FDE 页/短剧生成留给下一轮产线 PR）；本轮只改规则/手则/看板，让下周例程按新标准交卷。  
9. 推送后给秘书一份变更文件列表 + 下一周各 bot 该交什么的一句话命令。

---

## 一句话结论

现在的多 bot 是 **文档剧场**：token 花在描述「没做/别做/分支状态」，真实生产在旁路发生甚至被 inbox 否定。  
大改核心：**交卷=可展示产物 + 四条产线 + 真人外联 + 卫生脚本化**。
