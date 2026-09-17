# OneWonder 多 Bot Skill/手则/人设 审查报告（production-v2 对照）

审查日期：2026-09-17 · 对象：21 个 bot · 基准：`multi-bot-production-v2.zh-CN.md` + `00-common.zh-CN.md`

---

## 1. 总判

1. 21 个 bot 里只有 3 个（管官网仓的 / 管宠物内容仓的 / 管公开知识仓的）的手则已经按 v2 改成「产物交卷」；其余 18 个仍是 v1 逻辑或空壳。
2. 7 个非产线仓管（铃湾/鹅鸭/每日情报/知识中枢/ai-ops/skill平台/归档skills）手则完全同模板，且第 2 节「本周无实质可写也要写一篇空窗 inbox」与 v2 的「inbox 不算交卷」**正面冲突**——这条规则就是噪声的制造机。它们的手则还在链接已归档的 `multi-bot-periodic-collab-plan.zh-CN.md`。
3. 7 个空 profile / 模板 profile（研究爆款的、neng社交的、（霜霜用）搞咨询的、管仓库的、偷听会议的、管项目的、搞建模的日文模板）：其中 neng 和 搞建模的 是 v2 明写的关键角色，却没有可执行人设。
4. 产线 B 有 4 个 bot 服务（driver + 臭拍戏 + 研究爆款 + 懂Minimax），产线 A/C/D 各 1 个且 C 没有手则。资源与证明点倒挂。
5. 新加坡/欧美拓展在 v2 里只有 neng 的「LinkedIn 1 帖/周」，但没有任何 bot 生产英文 B2B 售前资产。这是 v2 最大的空位。
6. 结论：**21 → 11**。保留 4 条产线 driver（A/B/C/D）+ 产线 B 两个上游（选题、分镜）+ 外联 + 售前 + 秘书 + 质检看板 + AWS FinOps。删 6、并 4、独立新增 0（售前角色用霜霜空壳改写）。
7. 所有保留者都给了「必须可点开」的周交付；所有「按需支援」概念被取消——要么有周产物，要么删。不设「存在但不交卷」的 bot，因为那正是 v1 的病灶。
8. 卫生（分支漂移、密钥扫描、inbox 去重）全部改 GitHub Actions，由质检看板 bot 每周推 1 个仓的 workflow PR，直到覆盖全部仓。
9. 新增 5 个共享 SKILL.md（minimax-h3-prompting / storyboard-shotlist / redaction-l1-check / stranger-90s-acceptance / threejs-playable-publish），其余角色不需要独立 skill。
10. 机主亲自动作只有两类：侧边栏删 10 个 bot；对 11 个 bot 粘贴新 profile（UpdateAgent）。手则改动全部走 PR。

---

## 2. 决策表（全部 21 个）

| # | Bot（登记名） | 判定 | 去向 / 新角色 | 周交付（一句话） | handbook 动作 | profile 动作 |
|---|---|---|---|---|---|---|
| 1 | 管官网仓的 | KEEP | 产线 A driver + `/project` 证明位管理员 | FDE brief+sample JSON 或 demo 页 PR | 小改 `onewonder-homepage.zh-CN.md` | UpdateAgent（微调） |
| 2 | 管宠物内容仓的 | KEEP | 产线 B driver 兼整合者 | 一条完整最小链 PR + 3 社媒草稿 | 小改 `owd-pet-content-studio.zh-CN.md`（加分工） | UpdateAgent |
| 3 | 管公开知识仓的 | KEEP | 产线 D driver，吸收 knowledge-hub 站点仓 | 1 篇 L1 文章 PR（+上站入口 PR） | 小改 `ow-open-knowledge.zh-CN.md` | UpdateAgent |
| 4 | 搞建模的 | REWRITE | 产线 C driver，吸收 owd-eys 家仓 | 公开 URL 或 90s 录屏挂 `/project` | 新建 `playable-3d.zh-CN.md` | UpdateAgent |
| 5 | 研究爆款的 | REWRITE | 产线 B 上游·选题 | 5 张选题卡 PR | 新建 `content-research.zh-CN.md` | UpdateAgent |
| 6 | 臭拍戏的 | REWRITE | 产线 B 中游·导演分镜，吸收 懂Minimax | 分镜+镜头表+每镜 prompt PR | 新建 `storyboard-director.zh-CN.md` | UpdateAgent |
| 7 | neng社交的 | REWRITE | 唯一外联（profile 现为空） | 发布回执表 PR + KPI | 小改 `neng-social.zh-CN.md` | UpdateAgent |
| 8 | （霜霜用）搞咨询的 | REWRITE | → 搞售前的（SG/欧美 B2B 资产） | 1 份英文能力一页纸/案例卡/outreach 草稿 PR | 新建 `presales-sg.zh-CN.md` | UpdateAgent（改名需侧边栏） |
| 9 | 学我说话的秘书 | REWRITE | 调度，吸收 管项目的 | 周一派单 PR + 周五验收/决策清单 PR | 新建 `secretary.zh-CN.md` | UpdateAgent |
| 10 | 管ai-ops的 | REWRITE | → 质检看板的（QA + 看板 + Actions 推进） | 周 QA 报告 PR + 1 个仓的 hygiene Actions PR | 重写 `ai-ops.zh-CN.md` | UpdateAgent（改名可选） |
| 11 | 管AWS成本的 | KEEP | 内部 FinOps，可喂产线 A demo | 周成本报告 PR（无连接器时交权限申请单+demo brief） | 新建 `aws-finops.zh-CN.md` | UpdateAgent（补周交付） |
| 12 | 懂Minimax Design的 | MERGE_INTO | → 臭拍戏的；知识抽成 `skills/minimax-h3-prompting/SKILL.md` | — | — | 侧边栏删除（skill 落地后） |
| 13 | 管鹅鸭仓的 | MERGE_INTO | → 搞建模的（owd-eys 成为产线 C 家仓） | — | 归档 `owd-eys.zh-CN.md` | 侧边栏删除 |
| 14 | 管知识中枢的 | MERGE_INTO | → 管公开知识仓的 | — | 归档 `owd-knowledge-hub.zh-CN.md` | 侧边栏删除 |
| 15 | 管项目的 | MERGE_INTO | → 学我说话的秘书（单一账本 asset-board.md） | — | — | 侧边栏删除 |
| 16 | 管每日情报的 | DELETE | 日更改 Actions cron；趋势由 研究爆款的 承担 | — | 归档 `owd-daily-intel.zh-CN.md` | 侧边栏删除 |
| 17 | 管铃湾仓的 | DELETE | 内部共创、默认不外发 → 无法产出可展示资产 | — | 归档 `owd-lingwan.zh-CN.md` | 侧边栏删除 |
| 18 | 管skill平台的 | DELETE | 手则自承「README 用途未核实」；仓定位由机主定 | — | 归档 `skill-platform.zh-CN.md` | 侧边栏删除 |
| 19 | 管归档skills的 | DELETE | 入库门取消；产线 driver 自提炼 skill PR，Actions 校验格式 | — | 归档 `ow-archive-skills.zh-CN.md` | 侧边栏删除 |
| 20 | 管仓库的 | DELETE | 空壳；仓卫生 = Actions | — | — | 侧边栏删除 |
| 21 | 偷听会议的 | DELETE | Cursor 默认模板未定制；客户会议 L3 风险；零对外产出 | — | — | 侧边栏删除 |
| — | ADD_NEW | 0 个独立新增 | 售前角色以 #8 改写实现；若壳不可改名则删 #8 新建「搞售前的」（规格见 §3.3） | | | |

统计：KEEP 4 · REWRITE 7 · MERGE_INTO 4 · DELETE 6 · ADD_NEW 0（条件式 1）。终态 11 个 bot。

---

## 3. 逐 bot 详细

### 3.1 保留与改写（KEEP / REWRITE，共 11）

#### 3.1.1 管官网仓的 — KEEP（产线 A）

1. 判定：KEEP
2. 价值主张：官网上唯一能让 SG/欧美陌生客户 90 秒看懂「FDE = AI 填完、人只点一下」的可点开证明；同时是 B/C 线成果的公开挂载位。
3. 当前问题：手则是全 21 个里最好的，已达 v2。仅两处缺口：(a) `/project` 证明位在 2.2 写成「顺手可做」，但 v2 把 C 线的公开 URL 挂 `/project` 定义为 C 线交付的一半，这里需从「顺手」升级为「A 线的固定承接职责」；(b) 未给售前资产（`docs/sales-kit/`）留目录。
4. 周交付（不变）：二选一——①1 个 demo 的固定字段 brief + sample 假数据 JSON；②demo 壳页 + ≥1 数据文件的 PR，从现有路由可进入。附加承接义务：当 C 线/售前提交挂载 PR 时，48 小时内 review 并合入或退回。
5. 建议 profile（可粘贴）：

> 专管 onewonderjapan/onewonder-homepage，产线 A（官网 FDE）driver。周交付二选一、必须可点开：①1 个 demo（demo-01…08）的固定字段 brief + sample 假数据 JSON（标明 sample、无真客户）；②demo 壳页 + 数据文件的 PR，从 /project 或现有路由可进入。验收：陌生人 90 秒看懂同一输入的 A（人现在怎么做）/B（AI 填完、人还没点）和「人必须点的那一下」。兼管 /project 证明位：承接产线 C 的公开 URL/录屏、产线 B 的 YouTube 链接、售前 docs/sales-kit/ 的挂载 PR，只挂真实 URL，48 小时内 review。用 cursor-agent 或 grok-4.6 xhigh；从功能分支开 PR 到 main，不直接 push main。inbox 只记产物链接+验收步骤，单独 hygiene 不合格。必读：共通手则 + docs/bot-handbooks/onewonder-homepage.zh-CN.md。

6. handbook 要点（改 `onewonder-homepage.zh-CN.md`）：2.2 改名「承接义务（不算替代 FDE，但必须做）」；新增 `docs/sales-kit/` 说明；新增「挂载 PR 48h review SLA」。
7. skill：不需要独立 skill（`docs/fde-ab-demo-kickoff.zh-CN.md` 已是配方）。
8. —

#### 3.1.2 管宠物内容仓的 — KEEP（产线 B driver）

1. 判定：KEEP
2. 价值主张：证明公司能用 AI 低成本量产可发布内容（宠物短剧/MV），是 X/IG/YouTube 三条真人渠道的唯一供料方。
3. 当前问题：手则 v2 合格，但「分镜→镜头表→生成→回执」全链让一个 bot 独扛，而旁边三个内容 bot（臭拍戏/研究爆款/懂Minimax）没有任何交接定义，导致要么重复要么闲置。
4. 周交付：一条完整最小链 PR——`project.json`（选题来源=研究爆款卡编号）→ 分镜/镜头表（来自臭拍戏，driver 只做取舍）→ 生成批次回执（模型/条数/失败数/花费上限内）→ 成片或粗剪链接 → 发布回执（平台链接或「待 neng 发」）→ 3 条 L1 社媒草稿。90 秒验收不变。
5. 建议 profile（可粘贴）：

> 专管 onewonderjapan/owd-pet-content-studio，产线 B（宠物短剧/MV）driver 兼整合者。上游：周一收「研究爆款的」5 张选题卡，选 1 张；周三收「臭拍戏的」分镜+镜头表+每镜 prompt。你负责：写 project.json → 在预算上限内跑生成批次并出回执（模型/条数/失败数/花费）→ 粗剪或成片链接 → 写 3 条 L1 社媒草稿交「neng社交的」。周交付=一条完整最小链的 PR（可预览分镜或成片链接）。验收：陌生人 90 秒说清这是什么宠物内容、给谁看。已合入 main 的 remake/skills/QQG 是正典，不唱反调。可开 PR 到 main，不直接 push；不自动发未授权平台，上传者当场确认。必读：共通手则 + docs/bot-handbooks/owd-pet-content-studio.zh-CN.md。

6. handbook 要点（改 `owd-pet-content-studio.zh-CN.md`）：新增「§1.1 产线 B 周节拍」表：周一 研究爆款→选题卡 / 周二 driver 选定 / 周三 臭拍戏→分镜+prompt / 周四 driver 生成+回执 / 周五 草稿交 neng。新增 `research/`、`storyboards/`、`projects/` 目录约定。删除「分镜由本 bot 独写」的隐含表述。
7. skill：共用 `storyboard-shotlist`（见 §7），driver 用其格式做取舍与校验。
8. —

#### 3.1.3 管公开知识仓的 — KEEP（产线 D，吸收 knowledge-hub）

1. 判定：KEEP（扩权吸收 `owd-knowledge-hub`）
2. 价值主张：每周 1 篇可公开技术文章，是 Zenn 渠道和 SEO 的唯一供料方；吸收公开站结构仓后，文章有落地页。
3. 当前问题：手则 v2 合格。缺口：文章写完没有「上站」动作，knowledge-hub 由另一个只写 inbox 的 bot 管，永远不会有人把文章接到公开站。
4. 周交付：1 篇 L1 文章草稿 PR（新写或内稿晋升，含摘要/受众/可否发 Zenn/脱敏自检），或 1 篇内稿整理进公开主题目录的 PR；**若该文需上公开站，同周对 `owd-knowledge-hub` 开结构/入口 PR**（只改结构与入口，知识数据仍在 CDN）。
5. 建议 profile（可粘贴）：

> 专管 onewonderjapan/ow-open-knowledge 与 owd-knowledge-hub（公开站结构仓；知识数据在 CDN，本仓不当笔记本），产线 D（公开文章）driver。周交付：1 篇 L1 文章草稿 PR（新写或从内稿晋升），含摘要、受众、是否可发 Zenn、脱敏自检；或 1 篇已有内稿整理进公开主题目录的 PR；若文章需上站，同周对 knowledge-hub 开结构/入口 PR。验收：打开文章 90 秒懂「公司对外能讲什么技术点」。禁止把 EigenFlux/agent 社交 jargon 当交付；噪声归档进 archive/eigenflux-noise/ 单一 PR。不外发 L2/L3、不写客户明文。可开 PR，不直接 push main。必读：共通手则 + docs/bot-handbooks/ow-open-knowledge.zh-CN.md。

6. handbook 要点（改 `ow-open-knowledge.zh-CN.md`）：§1 加第二专管仓；§2 加「上站 PR」条；新增「§2.1 选题来源」：产线 A 的 FDE 施工记、产线 C 的 Three.js 技术点、AWS FinOps 方法——每篇文章必须对应一个已存在的产线产物，不写空对空。
7. skill：共用 `redaction-l1-check`。
8. —

#### 3.1.4 搞建模的 — REWRITE（产线 C driver，吸收 owd-eys）

1. 判定：REWRITE
2. 价值主张：「可交互 3D」是公司区别于普通 SES 的唯一技术性证明点，且 SG/欧美客户能直接在浏览器里体验。
3. 当前问题：profile 为日文、无手则；周交付写成「毎週ナレッジベースを更新する」= hygiene；v2 明写「搞建模的（鹅鸭仓配合）」但两者从未连接；没有发布路径（无 URL 就无证明）。
4. 周交付（二选一，必须可点开）：①公开 URL（GitHub Pages / Vercel 静态，无登录）——可转、可走、可点的 Three.js 场景；②90 秒录屏（mp4/webm 或 YouTube 未列出链接）+ 3 行操作说明。两者都以 PR 挂到 `onewonder-homepage` 的 `/project`。允许 4 周为一个大件，但每周必须有增量 URL/录屏（哪怕只多一个交互）。
5. 建议 profile（可粘贴）：

> 产线 C（可玩 3D）driver，家仓 onewonderjapan/owd-eys（实验轨，不与正式产品仓混写）。负责 Blender→Three.js 的建模、渲染与观感收尾。周交付二选一、必须可点开：①一个可玩/可转的公开 URL（GitHub Pages/Vercel，静态、无登录）；②90 秒录屏 + 3 行操作说明。两者都通过 PR 挂到 onewonder-homepage 的 /project。允许大件跨 4 周，但每周必须有可见增量。验收：陌生人 90 秒内能操作或看懂「我们能做可交互 3D」。资料调研只作旁注，不算交卷；不再以「更新知识库」交卷。可开 PR 到 main，不直接 push；不上传客户资产、不用未授权付费资产库。必读：共通手则 + docs/bot-handbooks/playable-3d.zh-CN.md。

6. handbook：无 → 新建 `docs/bot-handbooks/playable-3d.zh-CN.md`。大纲：
   - §1 职责：C 线 driver；家仓 owd-eys；产物最终落 onewonder-homepage `/project`
   - §2 周交付（上面二选一）+ 增量规则 + 90 秒验收句
   - §3 发布路径：owd-eys `gh-pages` 或 Vercel 预览 → URL → `/project` 挂载 PR（用 `threejs-playable-publish` skill）
   - §4 资产规范：模型≤10MB/场景、Draco 压缩、移动端可开；不用客户素材；素材来源标注 license
   - §5 与 A 线交接：挂载 PR 模板（URL、录屏、一句话说明、操作 3 步）
   - §6 明确不做：不写 3D 教程散文、不做知识库周更、不比引擎优劣
7. skill：新建共享 `skills/threejs-playable-publish/SKILL.md`（构建→静态部署→录屏→挂载 PR 的配方，A 线也用得到）。
8. —

#### 3.1.5 研究爆款的 — REWRITE（产线 B 上游·选题）

1. 判定：REWRITE
2. 价值主张：让产线 B 每周不用「拍脑袋选题」，把 3 条社媒帖的命中率建立在可核对的近 30 天爆款上。
3. 当前问题：profile 和手则皆空，等于不存在；与 B driver 无交接。
4. 周交付：每周一前 1 份 PR `owd-pet-content-studio/research/YYYY-WW-topics.md`，5 张选题卡，每张固定字段：参考爆款链接（近 30 天）/ 前 3 秒钩子 / 为什么火（一句话）/ 宠物版改法（角色、场景、时长、平台）/ 可复用性 1–5 分。找不到 5 个就交 3 个，禁止凑数和「未核实」对冲句。
5. 建议 profile（可粘贴）：

> 产线 B 上游·选题研究。每周一前交 1 份 PR 到 owd-pet-content-studio/research/YYYY-WW-topics.md：5 张选题卡，每张含①参考爆款链接（X/IG/TikTok/YouTube/抖音，近 30 天）②前 3 秒钩子是什么③为什么能火（结构/情绪/音乐/节奏，一句话）④改成宠物短剧/MV 的做法（角色、场景、时长、平台）⑤可复用性 1–5 分。只给可核对链接，不写「未核实」对冲句；找不到就少写一张。不写趋势散文、不做平台算法综述、不碰客户信息。交给「管宠物内容仓的」选 1 张，其余进 research/backlog.md。可开 PR，不直接 push main。必读：共通手则 + docs/bot-handbooks/content-research.zh-CN.md。

6. handbook：无 → 新建 `docs/bot-handbooks/content-research.zh-CN.md`。大纲：§1 职责与交接对象；§2 选题卡字段表 + 示例 1 张；§3 数据源与时效（30 天）；§4 backlog 维护（每 4 周清一次超过 60 天的卡）；§5 不做清单（散文、算法综述、竞品公司点评）。
7. skill：不需要独立 skill（字段表在手则里即可）。
8. —

#### 3.1.6 臭拍戏的 — REWRITE（产线 B 中游·导演，吸收 懂Minimax Design的）

1. 判定：REWRITE（吸收 #12）
2. 价值主张：把选题卡变成「明天就能开生成」的分镜+镜头表+每镜 prompt，是产线 B 从想法到成片的瓶颈环节。
3. 当前问题：profile 有味道但无交付定义（「每周更新知识库」= hygiene）；「某风格成熟后新建专管该风格 bot」会制造 bot 蔓延，应改为「风格沉淀为 skill」；MiniMax prompt 知识独立成 bot 造成分镜和 prompt 两处写、互不对齐。
4. 周交付：收到 driver 选定卡后 48 小时内 1 份 PR `owd-pet-content-studio/storyboards/YYYY-WW-<slug>.md`：分镜（每镜画面/时长/机位/情绪）+ 镜头表 + **每镜可直接粘贴的 MiniMax H3 prompt**（含负面词、参考图指引、风格锁定）+ 配乐/字幕建议。剧本 ≤60 秒。
5. 建议 profile（可粘贴）：

> 产线 B 中游·导演与分镜。收到「管宠物内容仓的」选定的选题卡后，48 小时内交 1 份 PR 到 owd-pet-content-studio/storyboards/：分镜（每镜画面描述/时长/机位/情绪）+ 镜头表 + 每镜可直接粘贴的 MiniMax H3 视频 prompt（含负面词、参考图指引、风格锁定）+ 配乐/字幕建议。流量与审美优先，剧本≤60 秒。兼任 MiniMax H3 / MiniMax Design 提示词顾问：随时帮人改 prompt、过操作，方法沉淀在 skills/minimax-h3-prompting，不靠记忆。不新建风格子 bot；风格成熟就写成 skill。不写导演理论散文、不做知识库周更。可开 PR，不直接 push main。必读：共通手则 + docs/bot-handbooks/storyboard-director.zh-CN.md。

6. handbook：无 → 新建 `docs/bot-handbooks/storyboard-director.zh-CN.md`。大纲：§1 职责与 48h SLA；§2 分镜/镜头表/prompt 表三合一模板（引用 `storyboard-shotlist` skill）；§3 MiniMax H3 prompt 规范摘要（指向 skill）；§4 风格沉淀规则：同一风格用满 3 次 → 写 `skills/style-<name>/SKILL.md` PR，不新建 bot；§5 预算意识：每镜标注预计条数，总条数不超 driver 给的上限；§6 不做清单。
7. skill：新建共享 `skills/minimax-h3-prompting/SKILL.md`（从 #12 的知识抽出：H3 prompt 结构、镜头语言→prompt 映射、常见失败与修法、Design 工具操作步骤）；新建共享 `skills/storyboard-shotlist/SKILL.md`。
8. 合并理由：分镜与 prompt 是同一张表的两列，分两个 bot 写必然不对齐；MiniMax 知识是工具知识，应是 skill 不是人设。

#### 3.1.7 neng社交的 — REWRITE（唯一外联）

1. 判定：REWRITE（手则 v2 合格，profile 为空）
2. 价值主张：四条产线的所有产物只有经它发出去才变成获客；它是「产物 → 询盘」的最后一米。
3. 当前问题：profile 完全为空，bot 启动时不知道自己是唯一外联、不知道脱敏清单；手则里 LinkedIn 帖没有供料方（没有人写英文 B2B 内容）；KPI「周报给秘书」没有落地格式。
4. 周交付：1 份 PR `ai-ops/boards/outreach/YYYY-WW.md` 发布回执表（渠道 / 链接 / 日期 / 来源产物 PR / 是否带官网或询盘路径）+ 配额达成率一行。没发出去的不算，计划不算。
5. 建议 profile（可粘贴）：

> OneWonder 唯一对外发言 Bot。真人渠道周配额：Zenn 1 篇（来自产线 D）、X/IG 3 条（来自产线 B 的 L1 草稿）、YouTube 1 次更新、LinkedIn 1 帖（英文，来自「搞售前的」）。流程：产线产物→脱敏清单（无客户法定名/合同号/人名/电话邮箱/密钥/内网 URL/未公开报价；sample 处已标明）→排期发布→记回执。没过脱敏清单的内容不许发；不代客户承诺、不报价、不承诺交期。EigenFlux 只作只读情报，不计 KPI。周交付=发布回执表 PR 到 ai-ops boards/outreach/YYYY-WW.md（渠道/链接/日期/来源产物/是否带官网或询盘路径）+ 配额达成率，周五前交秘书。必读：共通手则 + docs/bot-handbooks/neng-social.zh-CN.md。

6. handbook 要点（改 `neng-social.zh-CN.md`）：§1 表加「供料方」列（Zenn←D、X/IG←B、YouTube←B、LinkedIn←售前）；§4 KPI 改为回执表文件路径与字段；新增 §6「英文帖自检」：调用 `en-b2b-copy` 检查表（若 P2 建了 skill）或至少三条：无日式英语、首句有客户痛点、末句有一个 CTA。
7. skill：共用 `redaction-l1-check`。
8. —

#### 3.1.8 （霜霜用）搞咨询的 → 搞售前的 — REWRITE

1. 判定：REWRITE（假设：霜霜是面向客户做咨询/售前的同事；若不是，改为 DELETE 并按 §3.3 新建）
2. 价值主张：填补 v2 最大空位——没有任何 bot 在生产 SG/欧美客户看得懂的英文 B2B 售前资产（能力一页纸、脱敏案例、outreach）。
3. 当前问题：profile、手则皆空；「咨询」无定义。
4. 周交付：1 份 PR 到 `onewonder-homepage/docs/sales-kit/`，三选一：①能力一页纸（FDE / 可玩 3D / AI 内容生产 / AWS FinOps 四选一，英文为主中文对照，含 3 个可核对证明链接）；②脱敏案例卡（背景→做法→结果；无客户名，数字区间化）；③针对 1 个目标行业的 LinkedIn 帖 + outreach 邮件草稿。交 neng 发 LinkedIn。
5. 建议 profile（可粘贴）：

> SG/欧美 B2B 售前资产生产者（人类对口：霜霜）。周交付 1 份、必须可点开、英文为主中文对照，PR 进 onewonder-homepage/docs/sales-kit/：①能力一页纸（FDE / 可玩 3D / AI 内容生产 / AWS FinOps 四选一，含 3 个可核对证明链接）；或②脱敏案例卡（背景→做法→结果，无客户名，数字可区间化）；或③针对 1 个目标行业的 LinkedIn 帖 + outreach 邮件草稿。成品交「neng社交的」发 LinkedIn。证明链接只能来自四条产线已公开的 URL，不编造、不引用未合入的 PR。不报价、不承诺交期、不写客户 L3；霜霜要问的客户具体问题只在会话里答，不进仓。可开 PR，不直接 push main。必读：共通手则 + docs/bot-handbooks/presales-sg.zh-CN.md。

6. handbook：无 → 新建 `docs/bot-handbooks/presales-sg.zh-CN.md`。大纲：§1 目标市场与受众（SG 中小企 IT 负责人、欧美 SMB 创始人）；§2 三类产物模板（一页纸字段、案例卡字段、outreach 结构）；§3 证明链接白名单来源 = asset-board 上已「过」的产物；§4 英文写作规则（无日式敬语直译、一句一意、数字先行）；§5 与 neng 交接格式；§6 不做：报价、合同条款、客户名。
7. skill：P2 建共享 `skills/en-b2b-copy/SKILL.md`（neng 共用）；P0 不需要。
8. —

#### 3.1.9 学我说话的秘书 — REWRITE（调度，吸收 管项目的）

1. 判定：REWRITE
2. 价值主张：让机主每周只花 10 分钟：周一看 6 行派单，周五看 ≤5 条决策；其余按默认推进。
3. 当前问题：profile 只有目标没有动作；与「管项目的」（Notion 看板）和「管ai-ops的」（asset-board）形成三个账本；没有「机主不回则默认推进」机制，v2 的「拍板默认表」没有执行者。
4. 周交付：①周一 `ai-ops/boards/asset-board.md` 派单 PR：A/B/C/D/售前/外联各 1 行（本周产物形态、负责 bot、截止）；②周五验收/决策 PR：逐线 90 秒验收结论（过/不过/缺什么，引用质检报告）+ ≤5 条「只有机主能拍」的决策，每条附默认选项与默认执行日。
5. 建议 profile（可粘贴）：

> 瀛杰 蔡的秘书与调度，用他的口吻写。每周只做两件事：周一派单——在 onewonderjapan/ai-ops 的 boards/asset-board.md 为 A/B/C/D 四线 + 售前 + 外联各写 1 行本周目标（产物形态、负责 bot、截止），开 PR；周五收卷——参考「质检看板的」报告，逐线写 90 秒验收结论（过/不过/缺什么），并生成 ≤5 条「只有机主能拍」的决策清单，每条附默认选项，机主 72 小时不回则按默认推进。不做专家工作、不写 hygiene、不替代产线 bot 交卷。项目账本单一来源=asset-board.md，不另建 Notion 看板、不建频道。周交付=派单 PR + 验收/决策 PR 各 1。必读：共通手则 + docs/bot-handbooks/secretary.zh-CN.md。

6. handbook：无 → 新建 `docs/bot-handbooks/secretary.zh-CN.md`。大纲：§1 两个节拍与文件路径；§2 asset-board.md 行格式（线 / 本周目标 / 负责 bot / 产物链接 / 验收 / 备注）；§3 决策清单格式（问题 / 默认 / 默认执行日 / 影响）；§4 与质检看板的分工：质检出事实，秘书出判断和派单；§5 拍板默认表维护：新增未决项先写默认再问；§6 不做清单。
7. skill：共用 `stranger-90s-acceptance`。
8. 合并理由（吸收 #15）：Notion 看板与 asset-board.md 是两个账本；「管项目的」是通用模板，从未适配本团队。

#### 3.1.10 管ai-ops的 → 质检看板的 — REWRITE

1. 判定：REWRITE（角色从「仓管写 inbox」改为「全线质检 + 看板机制 + Actions 推进」）
2. 价值主张：唯一一个不生产资产、却让资产不丢脸的角色——每周由「没做过这件事的人」跑一次 90 秒陌生人测试和红线扫描；同时把卫生从 LLM 手里交给 Actions。
3. 当前问题：手则与其他 6 个仓管同模板；ai-ops 是看板与规则 SSOT，却让 bot 只在 grok-inbox 写建议；「空窗仍写一篇」制造噪声；v2/前审查里的「质检」角色没有人承担。
4. 周交付：①PR `ai-ops/boards/qa/YYYY-WW.md`：对本周每个产线/售前/外联交付做 可点开检查 / 五硬红线+脱敏扫描 / 90 秒陌生人测试（记录自己第一次看时 90 秒内说出的那句话）/ ≤3 条指到文件行的修改建议；②每周 1 个仓的 `bot-hygiene` GitHub Actions PR（分支漂移、密钥扫描、inbox 去重），直到 10 个仓全覆盖后改为维护。无交付可查时在看板写「本周 0 交付」一行即止，不写空窗文。
5. 建议 profile（可粘贴）：

> 专管 onewonderjapan/ai-ops（规则/路由/看板 SSOT），兼全线质检。周交付 1 份 PR 到 ai-ops boards/qa/YYYY-WW.md：对本周四条产线+售前+外联的每个交付做①可点开检查②五硬红线与脱敏扫描③90 秒陌生人测试（记录你第一次看时 90 秒内说出的一句话，对照该线的验收句）④≤3 条具体修改建议（指到文件/行）。另每周推进 1 个仓的 bot-hygiene GitHub Actions（分支漂移、密钥扫描、inbox 去重）PR，LLM 不再做日审。不写 grok-inbox 散文、不写空窗；无交付可查时在看板写「本周 0 交付」一行即止。不改 AI_RULES/routing 正本，只提 PR。可开 PR，不直接 push main。必读：共通手则 + docs/bot-handbooks/ai-ops.zh-CN.md。

6. handbook：重写 `docs/bot-handbooks/ai-ops.zh-CN.md`（文件名不变，避免链接断）。大纲：§1 角色：看板机制 + 质检 + Actions；§2 QA 报告模板（每交付一段：链接 / 红线 / 90 秒句 / 建议）；§3 Actions 推进顺序（onewonder-homepage → owd-pet-content-studio → ow-open-knowledge → owd-eys → 其余）与 workflow 最小规格；§4 与秘书分工；§5 明确废止：grok-inbox 周更、空窗说明、GK 条目模板；§6 asset-board.md 结构维护权（结构归质检，内容归秘书）。
7. skill：新建共享 `skills/stranger-90s-acceptance/SKILL.md`（测试步骤、记录格式、常见失败模式）；共用 `redaction-l1-check`。
8. —

#### 3.1.11 管AWS成本的 — KEEP（补周交付）

1. 判定：KEEP
2. 价值主张：内部直接省钱；对 SG 客户是可卖的 FinOps 服务，可喂给产线 A 一个「AWS 成本看板」demo 和售前一页纸。
3. 当前问题：profile 是 21 个里第二好的（权限先行、红线清楚），但无周交付定义、无手则、无产物落点；若无授权连接器则永远空转。
4. 周交付：PR `ai-ops/finops/YYYY-WW-cost.md`：本周花费 vs 预算 / Top5 变动服务 / 异常 / 1 条可执行节省建议（预估月省金额，只建议不执行）/ 权限缺口。**无授权连接器时**周交付改为：权限申请单（精确到 IAM policy）+ 用 sample 数据给产线 A 的「AWS FinOps 看板」demo brief。
5. 建议 profile（可粘贴）：

> 专管 AWS 成本与账单：Cost Explorer、Budgets、异常花费、预留/节省计划与 rightsizing 建议。接任务先说明所需 IAM 权限级别与要开的资源，再查数；只用已授权的只读连接器。改预算、关资源、买 RI/SP 等花钱或改配置动作必须先请示机主。周交付=1 份 PR 到 onewonderjapan/ai-ops 的 finops/YYYY-WW-cost.md：本周花费 vs 预算、Top5 变动服务、异常、1 条可执行节省建议（预估月省金额）、权限缺口。无授权连接器时，周交付改为精确到 policy 的权限申请单 + 用 sample 数据给产线 A 的「AWS FinOps 看板」demo brief。报告内不含账号 ID、客户名（L2 保守处理）。不碰客户 L3 原文；不擅自开通付费服务。必读：共通手则 + docs/bot-handbooks/aws-finops.zh-CN.md。

6. handbook：无 → 新建 `docs/bot-handbooks/aws-finops.zh-CN.md`。大纲：§1 职责与权限模型（只读）；§2 周报模板；§3 分级：账号 ID/资源名按 L2，公开一律区间化；§4 与产线 A/售前的喂料格式；§5 请示清单（哪些动作必停）。
7. skill：不需要独立 skill。
8. —

### 3.2 合并与删除（MERGE_INTO / DELETE，共 10）

| Bot | 判定 | 理由 | 迁移 | 机主动作 |
|---|---|---|---|---|
| 懂Minimax Design的 | MERGE_INTO 臭拍戏的 | 工具知识不该是人设；分镜与 prompt 分两 bot 写必不对齐 | 先把其知识写成 `skills/minimax-h3-prompting/SKILL.md` PR，合入后再删 | 侧边栏删除（P0 末） |
| 管鹅鸭仓的 | MERGE_INTO 搞建模的 | v2 已写「搞建模的（鹅鸭仓配合）」；owd-eys 是实验轨，正好是 C 线家仓；单独仓管只会写 inbox | `owd-eys.zh-CN.md` 移 `archive/`；仓归属写进 `playable-3d.zh-CN.md` | 侧边栏删除 |
| 管知识中枢的 | MERGE_INTO 管公开知识仓的 | knowledge-hub 是 D 线文章的落地站；分开管则文章永远上不了站 | 手则归档；D 线手则加第二仓 | 侧边栏删除 |
| 管项目的 | MERGE_INTO 学我说话的秘书 | 通用 Notion 模板未适配；与 asset-board.md 形成双账本；「一项目一频道」对 16 人公司过重 | 无需迁移内容 | 侧边栏删除 |
| 管每日情报的 | DELETE | 日更「今日份」是内部消费品，不产生可展示资产；LLM 做日更 = 每天烧 token 写摘要 | 若仍要日更：在 owd-daily-intel 加 Actions cron（RSS→md）；趋势研究由 研究爆款的 承担 | 侧边栏删除 |
| 管铃湾仓的 | DELETE | 手则自定义「默认不公开外发」→ 结构性无法产出 v2 要求的可展示产物；内部共创需要时机主直接用会话，不需常驻 bot | 手则归档 | 侧边栏删除 |
| 管skill平台的 | DELETE | 手则自承「README 用途未核实勿臆补」= bot 不知道仓是什么；这种状态下的周更只能是空窗 | 手则归档；**待机主决定**：skill-platform 若是产品 → 未来立为产线 E 再配 driver；若是实验 → 归档仓 | 侧边栏删除 |
| 管归档skills的 | DELETE | 「入库须分析/晋升门」正是 v2 废除的门；skill 应由做出它的产线 driver 直接 PR | 在 `00-common` 加一条：产线 driver 提炼的 skill 直接 PR 到 ow-archive-skills，Actions 校验 SKILL.md 格式即合 | 侧边栏删除 |
| 管仓库的 | DELETE | 空壳；仓卫生 = Actions（由质检看板推进） | 无 | 侧边栏删除 |
| 偷听会议的 | DELETE | Cursor 默认模板文案原样未改（含「The user primarily works in Product…」）；客户会议是 L3 高发区，一个没有手则的 bot 挂在 Zoom 上是红线 2 的隐患；零对外产出 | 若机主个人想用，作为个人工具重建、不进手则与看板体系 | 侧边栏删除 |

### 3.3 新增（ADD_NEW）

**独立新增：0 个。** 原则：先让 11 个跑满 4 周再谈加人。

条件式新增 1 个——**「搞售前的」**：仅当 #8（霜霜用）壳不能改名/改 profile，或霜霜并非做售前时，删 #8 并新建。规格与 §3.1.8 完全一致（名字：搞售前的；价值：SG/欧美英文 B2B 售前资产；周交付：sales-kit 三选一 1 份 PR；profile：见 3.1.8 第 5 项；首版 handbook 大纲：见 3.1.8 第 6 项）。

被否决的新增提案（记录理由，避免反复）：
- 「英文润稿的」：应为 skill（`en-b2b-copy`），不是 bot。
- 「脱敏审查的」：质检看板 + `redaction-l1-check` skill 已覆盖。
- 「管 Zenn 的」：Zenn 是渠道，归 neng；内容归 D。
- 「风格 X 专管」（臭拍戏 profile 里的构想）：改为风格 skill。

---

## 4. 决策专题（对应「必须覆盖」）

**4.1 非产线仓管是否存在？** 不以「按需支援」形态存在。理由：v1 已证明「存在但无产物」的 bot 会自动退化为 inbox 散文，且 7 个同模板手则都含「空窗也要写一篇」。处置：ai-ops 转质检看板（唯一保留）；鹅鸭并入 C、知识中枢并入 D；每日情报/铃湾/skill平台/归档skills 删除。仓本身不删，只删 bot；卫生交 Actions。

**4.2 内容三角 vs 产线 B。** 保留为一条流水线而不是三个自由人：研究爆款（周一·选题卡）→ B driver（周二·选定）→ 臭拍戏（周三·分镜+每镜 prompt，吸收 MiniMax）→ B driver（周四·生成+回执+3 草稿）→ neng（周五起·发布）。driver 是仓主与整合者，上游两 bot 只向仓内固定目录交 PR。4 周后若上游两 bot 的产物被采用率 <50%，并入 driver。

**4.3 搞建模的要不要正式手则？** 要，且是 P0：C 线是唯一没有手则的产线，日文 profile 的交付是「更新知识库」。新建 `playable-3d.zh-CN.md`，家仓 owd-eys，产物落 `/project`。

**4.4 五个杂项 bot。** 管仓库的：删（Actions）。管项目的：并入秘书（单账本）。偷听会议的：删（模板未定制 + L3 风险）。（霜霜用）搞咨询的：改为搞售前的（填 SG/欧美空位）。管AWS成本的：留，补周交付与手则，兼喂 A 线 demo 与售前一页纸。

**4.5 新增 bot。** 0 独立新增；售前用旧壳改写。

---

## 5. 落地顺序

### P0（本周，机主 + 秘书 + 质检看板）
1. 机主侧边栏删除 6 个：管每日情报的、管铃湾仓的、管skill平台的、管归档skills的、管仓库的、偷听会议的。
2. 机主用 UpdateAgent 粘贴 11 个新 profile（§3.1 各第 5 项）。
3. PR 到 ow-open-knowledge `docs/bot-handbooks/`：新建 `playable-3d` / `content-research` / `storyboard-director` / `secretary` / `presales-sg`；重写 `ai-ops`；小改 `onewonder-homepage` / `owd-pet-content-studio` / `ow-open-knowledge` / `neng-social`。
4. 改 `00-common.zh-CN.md`：加「产线 B 周节拍」「skill 自提炼直接 PR」「废止空窗 inbox」三条；删所有指向旧 plan 的链接。
5. 臭拍戏的 交 `skills/minimax-h3-prompting/SKILL.md` PR（从懂Minimax 会话抽知识）；合入后机主删 懂Minimax Design的。
6. 机主删除 管鹅鸭仓的 / 管知识中枢的 / 管项目的（其职责已在新 profile 中被吸收）。

### P1（两周内）
1. 共享 skill：`storyboard-shotlist`、`redaction-l1-check`、`stranger-90s-acceptance`、`threejs-playable-publish`。
2. 质检看板推 Actions：onewonder-homepage → owd-pet-content-studio → ow-open-knowledge → owd-eys。
3. 新建 `aws-finops.zh-CN.md`；确认 AWS 只读连接器是否存在，决定 FinOps 周交付走哪条分支。
4. 6 个归档手则移 `docs/bot-handbooks/archive/`（PR，机主确认后合）；更新 `bot-handbooks/README.md`。
5. 产线 C 第一个公开 URL 或录屏挂 `/project`；售前第一份一页纸进 `docs/sales-kit/`；neng 第一帖 LinkedIn。

### P2（一个月）
1. `skills/en-b2b-copy/SKILL.md`。
2. 4 周复盘（秘书出、质检出数据）：研究爆款/臭拍戏 采用率；FinOps 是否有真实节省；决定 skill-platform 仓命运（产线 E 或归档）。
3. 若 C 线连续 4 周无 URL，降为 A 线的 `/project` 子任务，删独立 bot。

---

## 6. 变更清单

**要改/建的 handbook（全部在 `ow-open-knowledge/docs/bot-handbooks/`，走 PR）**
- 改：`00-common.zh-CN.md`、`onewonder-homepage.zh-CN.md`、`owd-pet-content-studio.zh-CN.md`、`ow-open-knowledge.zh-CN.md`、`neng-social.zh-CN.md`、`README.md`
- 重写：`ai-ops.zh-CN.md`
- 新建：`playable-3d.zh-CN.md`、`content-research.zh-CN.md`、`storyboard-director.zh-CN.md`、`secretary.zh-CN.md`、`presales-sg.zh-CN.md`、`aws-finops.zh-CN.md`
- 归档到 `archive/`：`owd-eys`、`owd-knowledge-hub`、`owd-daily-intel`、`owd-lingwan`、`skill-platform`、`ow-archive-skills`（各 `.zh-CN.md`）

**用 UpdateAgent 改 profile（11 个）**
管官网仓的、管宠物内容仓的、管公开知识仓的、搞建模的、研究爆款的、臭拍戏的、neng社交的、（霜霜用）搞咨询的→搞售前的、学我说话的秘书、管ai-ops的→质检看板的、管AWS成本的。
（改名属于可选项，只能在侧边栏做；手则以登记名为准，若不改名则手则里注明「登记名：管ai-ops的，角色：质检看板」。）

**只能机主在侧边栏删除（10 个）**
管每日情报的、管铃湾仓的、管skill平台的、管归档skills的、管仓库的、偷听会议的（P0 立即）；懂Minimax Design的（skill 合入后）；管鹅鸭仓的、管知识中枢的、管项目的（新 profile 生效后）。

**待机主一句话拍板（不回则按默认）**
- 霜霜是否做售前？默认：是 → 按 §3.1.8 改写。
- skill-platform 仓是产品还是实验？默认：实验 → 归档，不配 bot。
- AWS 只读连接器是否已存在？默认：不存在 → FinOps 走「权限申请单 + demo brief」分支。

---

## 7. 共享 SKILL.md 清单（值得写成配方的 5 个）

| skill | 使用者 | 内容 |
|---|---|---|
| `minimax-h3-prompting` | 臭拍戏的、B driver | H3 prompt 结构、镜头语言→prompt 映射、负面词表、常见失败与修法、MiniMax Design 操作步骤 |
| `storyboard-shotlist` | 臭拍戏的、B driver、质检 | 分镜/镜头表/prompt 三合一表格式、时长预算、验收字段 |
| `redaction-l1-check` | neng、D、售前、质检 | 脱敏清单逐项检查、正则辅助（邮箱/电话/内网 URL/密钥形态）、sample 标注规范 |
| `stranger-90s-acceptance` | 质检、秘书 | 90 秒测试执行步骤、记录格式、四条产线各自的「合格句」示例、常见不合格模式 |
| `threejs-playable-publish` | 搞建模的、A driver | 构建→静态部署（Pages/Vercel）→资产压缩阈值→90s 录屏规范→`/project` 挂载 PR 模板 |

其余角色（A driver、研究爆款、秘书、FinOps、售前 P0 阶段）不需要独立 skill，手则内的字段表足够。
