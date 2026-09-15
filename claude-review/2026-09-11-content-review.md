# Claude 内容 review · 2026-09-11 · ow-open-knowledge

- 条目 ID：CR-OPENKB-20260911-01
- 仓：onewonderjapan/ow-open-knowledge
- 分支：claude/review
- 写入方：Claude（开发侧 review）
- 机密分级：L1（本仓公开）
- 状态：待机主阅读

## 仓定位
公开知识库，main 分支单次 squash 提交（858d06e，2026-09-11），97 个跟踪文件、7 个主题目录。定位为内部方法卡「晋升」后的公开终点：方法论（agent-cultivation / workflow-standard / team-norms）+ 可运行参考实现（ai-stack / dev-pipeline / task-orchestrator）+ 云模式 skill（cloud-patterns）。MIT 许可。

## 发现
1. **实测通过**：README 快速开始（stub provider）跑通，QC PASS，脱敏输出中 demo 实体残留 0；task-orchestrator 9 测试全过；三目录 compileall 无错。「verified end-to-end」声明属实。
2. **无硬泄漏**：全仓 grep 未发现内网 IP、密钥样式串、真实本机路径、外部 webhook；83 条仓内相对链接 0 死链；git 历史仅 1 次 squash 提交，无历史泄漏面。
3. **内部项目代号成片出现**（违反 CONTRIBUTING.md:8 自定禁则）：agent-cultivation 下 4 份文档引用内部业务线代号（图像生产 PJ / MV 制作 PJ）及内部 skill/agent 名与目录（含不宜出现在公司公开仓的产线命名），详见机密扫描表。
4. **真实客户案件元信息**：agent-cultivation/PHASE0-RESULTS.md:5-25 记录「実顧客案件の提案資料 PPTX」的主题（仮想化基盤検討）、页数、实体数（人名 37）、AI 发现的资料内部矛盾。无客户名，但与 README.md:13「No client information」自相矛盾。
5. **CONTRIBUTING 未描述目录结构与晋升流程**：CONTRIBUTING.md 全文 26 行，只有收录边界与 PR 约定；「方法卡如何从内部仓晋升到本仓」「目录如何组织」零描述。下方两张表只能以各 README 的自述为基准。
6. **草稿状态文档被当成品发布**：agent-cultivation/data-classification.md:1 标题自称「v0.9（初稿・待经营者批准后 W1 发布）」，:31-35 三项待批未勾；而 agent-cultivation/README.md:30 称其「ready-to-adopt template」。
7. **换行符全仓 CRLF**：97/97 文件 CRLF，无 .gitattributes，无 BOM，UTF-8 正常。对 Linux/macOS 贡献者会产生整文件 diff 噪音。
8. **dev-pipeline 英日 README 内容不对等**：日文版（原版）多出 Dispatcher 分类表、Reviewer 细节、実行フロー/進捗表示 三节（README.ja.md:41-59, 99-116），英文版无对应；README.ja.md:139 目录树根名与目录实名不一致。

## 机密扫描结果
| 类型 | 路径:行 | 处置建议 |
|---|---|---|
| 内部项目代号（业务线 PJ 名） | agent-cultivation/AGENT育成標準.md:5,68-71,101-108；agent-cultivation/FLOW.md:92；agent-cultivation/PITFALLS.md:14；agent-cultivation/既存AGENT訓練ガイド.md:5,52,100 | P1：改为中性描述（image line / MV line），或在 README 声明为公开代号 |
| 内部 skill/agent 名（含不宜公开的产线命名） | agent-cultivation/FLOW.md:80,96-97；agent-cultivation/AGENT育成標準.md:105,108；agent-cultivation/既存AGENT訓練ガイド.md:6；ai-stack/templates/project-skeleton/CLAUDE.md:11 | P1：删除或泛化；不宜公开的产线命名建议直接移除（公司公开仓声誉面） |
| 客户案件元信息 | agent-cultivation/PHASE0-RESULTS.md:7,12,17-21,24-25 | P1：保留数字、删除案件主题与「AI 发现的资料矛盾」细节，或整文件下线 |
| 内部硬件采购信息 | agent-cultivation/AI研究会-学習と業務適用の基礎.md:2,5 | P2：「購入済み」改为中性前提 |
| 内部销售话术 | agent-cultivation/FLOW.md:101 | P2：属 L2 内部策略表述，建议删 |
| 本机环境细节（OS/Python 版本/用户名类型） | ai-stack/CLAUDE.md:15；agent-cultivation/PITFALLS.md:15 | P2：无真实用户名（为占位符），仅建议泛化 |
| 演示邮箱使用疑似真实 .co.jp 域名 | ai-stack/demo_data/incoming/new_rfp.md:4；ai-stack/masking/masker.py:103 | P2：改用 .example / .test 域；域名是否真实注册未核实 |
| IP / 密钥样式 / 本机绝对路径 / 内网共享路径 | — | 未发现 |
| 关联仓链接使用内部仓前缀命名 | README.md:59；README.ja.md:59；README.zh-CN.md:59 | 已核实该仓为 public（HTTP 200 / visibility public），非泄漏；确认命名为有意即可 |

## CONTRIBUTING vs 实际目录
CONTRIBUTING.md 本身不含目录结构与晋升流程描述，以下以各 README / 文档自述为基准。

### 说有但没有
| 声明位置 | 声明内容 | 实际 |
|---|---|---|
| dev-pipeline/README.md:100-102；README.ja.md:154-156 | agents/memory/、agents/prompts/、requirements/ | 三者均被 dev-pipeline/.gitignore 排除，仓内不存在；仅 en:61 解释了 requirements/ 需自建 |
| workflow-standard/STANDARD.md:195 | `cp -r templates/_workflow-template …` | 实际目录为 workflow-standard/template/（README.md:17 用法正确） |
| agent-cultivation/新プロジェクトSTARTUP標準.md:5,21,72 | `templates/project-skeleton/`（相对本目录） | 实际在 ai-stack/templates/project-skeleton/ |
| agent-cultivation/新プロジェクトSTARTUP標準.md:72 | 文件名「AI研究会-学習と業適用の基礎.md」 | 少一字，实际文件名含「業務」 |
| agent-cultivation/AI研究会-学習と業務適用の基礎.md:147 | 两份提案侧资料 .md | 仓内无（ai-stack/CLAUDE.md:3 说明有意不含） |
| agent-cultivation/既存AGENT訓練ガイド.md:6,60,100-101；AGENT育成標準.md:69-71 | library/training_cases/、library/prompt_outcomes/、library/story_gold/ 等 | 内部项目产物，仓内无 |
| agent-cultivation/FLOW.md:95 | docs/PITFALLS.md | 实际 agent-cultivation/PITFALLS.md |
| ai-stack/masking/masker.py:6 | config/entities.json | 实际 masking/entities.json（:104 代码路径正确，仅 docstring 过时） |
| ai-stack/evalkit/structure_check.py:5 | evalkit/judge.py | 明示「今後追加」，可接受 |

### 有但未索引
| 文件 | 缺失的索引位置 |
|---|---|
| ai-stack/CLAUDE.md | ai-stack/README.md:66-77 目录树未列 |
| task-orchestrator/agents/openai.yaml | task-orchestrator/README.md:39-47 目录表未列（仅 :25 正文提及） |
| workflow-standard/template/runs/.gitkeep | workflow-standard/README.md:26-35 目录树未列（STANDARD.md:78 有） |
| workflow-standard/template/state/README.md、portfolio.json | workflow-standard/README.md:34 只列 ledger/scorecard/strategy |
| ai-stack/templates/project-skeleton/**（5 文件） | 仅目录级提及；agent-cultivation/README.md 未链接，但 STARTUP 标准依赖它 |
| dev-pipeline/agents/dispatcher.py、reviewer.py | dev-pipeline/agents/__init__.py:1-6 未导出（代码级索引不全） |

## 三语 README 同步状态
- 根目录三份 README **结构完全同步**：各 68 行、6 个 H2、16 条链接、9 行表格；章节一一对应。
- 微小落后：README.ja.md:15 缺少 en/zh 都有的「task-orchestrator 为英文」括注（已核实 task-orchestrator 全目录 0 个 CJK 字符，括注属实）。
- 子目录双语：ai-stack en/ja 内容等价（en 多拆一节 Providers）；dev-pipeline en 落后 ja 三节（见发现 8）。
- 语言声明与实际一致：CONTRIBUTING.md 为中文，README.md:15 未提及此点。

## 建议
### P0
- 无。未发现 IP / 密钥 / 真实人名 / 真实客户名 / 本机路径。
### P1
1. 清理内部项目代号与内部 skill 名（机密扫描表前两行），一次 PR 完成；不宜公开的产线命名优先移除。
2. PHASE0-RESULTS.md 删客户案件主题与 AI 发现细节，或整文件移回内部仓，仅在 AGENT育成標準.md 保留一行汇总数字。
3. CONTRIBUTING.md 补两节：目录结构（7 目录各放什么）与「内部方法卡 → 本仓」晋升清单（脱敏检查项 = 本文机密扫描类型列）。
### P2
1. 加 .gitattributes（`* text=auto eol=lf`）并一次性归一化为 LF。
2. 修正「说有但没有」表中 6 处路径/文件名错误（STANDARD.md:195、STARTUP標準:5,21,72、FLOW.md:95、masker.py:6）。
3. data-classification.md 去掉「初稿・待批准」标题与待批清单，改为模板口径，与 README:30 一致；或 README 改口。
4. dev-pipeline/README.md 补齐 ja 版多出的三节；README.ja.md:139 目录树根名改为实名。
5. 演示邮箱域改 .example；AI研究会:5 与 FLOW.md:101 去掉采购/话术表述。
6. 补 dev-pipeline/agents/__init__.py 导出；补各目录 README 缺漏索引项。

## 不建议做
- 不建议为统一语言而翻译各原文文档（README.md:15 与 CONTRIBUTING.md:14 已明确保留原文，这是有意设计）。
- 不建议给 .py 文件逐个加 SPDX/版权头：根 LICENSE + 各 README License 节已一致，无冲突，加头只增噪音。
- 不建议拆分或重命名 7 个主题目录：三语 README 与所有相对链接均以此为锚，0 死链是当前最大资产。

## 未核实
- 演示数据中两个 .co.jp 域名是否为真实注册域名（未做 DNS/WHOIS 查询）。
- 内部业务线代号（图像生产 PJ / MV 制作 PJ）是否已在公司其他公开渠道出现过；若已公开则 P1 第 1 项降为 P2。
- 4 个关联公开仓的内容本身未 review（本次仅核实可见性为 public）。
- README.md:31 所称「verified」仅在 Windows + Python 3.13 环境复现，未在 macOS/Linux 验证。
