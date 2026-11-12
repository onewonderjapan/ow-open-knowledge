# ROADMAP — ow-open-knowledge

> **定位**：OneWonder Japan 的对外开源知识仓（PUBLIC，MIT）——把内部实战蒸馏为公开资产：Agent 育成方法论（agent-cultivation）、企业 AI 导入参考实现（ai-stack）、工作流标准、多代理开发管线、云模式；`knowledge-notes/` 由私有 knowledge-base 经 `kb.py export-public` 脱敏导出。

## P0 对外一致性与对账（零成本）

- [ ] P0-1 源库对账：私有 knowledge-base 现 5 篇 `scope: public`，本仓 `knowledge-notes/manifest.json`（exported_at 2026-09-27）登记 7 篇 notes——逐篇核对哪些源笔记已撤下/改 internal（先例：2026-09-27 机主判定撤 4 篇），出差异清单并按导出协议（只撤 manifest 列过的文件）出再导出方案，PR 由机主决定——验收：差异清单写入 PR 描述，`python scripts/check_kb_export.py` exit 0
- [ ] P0-2 三语 README 同步核对：README.md / README.zh-CN.md / README.ja.md 的 Contents 表（含 kenzu-ai 行、语言列）逐行 diff，滞后语言在同 PR 补齐——验收：三份文件目录条目数一致，`python scripts/check_links.py` exit 0
- [ ] P0-3 仓库 description 更新建议：当前描述仍写「整理中,完成后转公开」而仓库已 PUBLIC 且 IMPROVEMENT-PLAN 阶段一~三已落地——起草新描述文案（≤120 字符，三语任一）提交机主一键更新（repo 设置需管理员）——验收：本 ROADMAP 附文案，机主确认后 GitHub 描述与新文案一致
- [ ] P0-4 打首个版本 tag：CHANGELOG.md 已按 Keep a Changelog 维护但 `git tag` 为 0 个——按 CHANGELOG 首个稳定点打 `v0.1.0` 并在 CHANGELOG 增加版本小节——验收：`git tag` 列出 v0.1.0，tag 指向的 CI 全绿 commit
- [ ] P0-5 验证快速开始命令可照抄：在干净 venv 按 README「Quick start」与 agent-cultivation/新プロジェクトSTARTUP標準.md 的命令逐条实跑（IMPROVEMENT-PLAN P2-3 曾修过一批路径，防回归）——验收：实跑记录（命令+exit code）附入 PR 或 docs/

## P1 阶段四「薄切片→正式版」第一步（零成本）

- [ ] P1-1 provider 注册表化：`ai-stack/llm/providers.py` 从硬编码 if/else 改为注册表/entry-points（IMPROVEMENT-PLAN 阶段四既定项，纯代码无新依赖）——验收：新增一个 stub provider 只需注册一行，`ai-stack/tests/` 用例通过且 CI 绿
- [ ] P1-2 masking 叠 GiNZA NER（可选依赖，pip 本地安装无 API 费用）：作为规则引擎之后的第二道，装不上时降级并记录——验收：`ai-stack/tests/test_masker.py` 新增 NER 开启/关闭双模式用例
- [ ] P1-3 `scripts/check_kb_export.py` 增强：校验 manifest 的 notes id 与源库导出清单一致、sha256 复算——验收：`scripts/test_check_kb_export.py` 用例 +2，篡改一个 sha 后检查 exit ≠ 0
- [ ] P1-4 `task-orchestrator` 与 `workflow-standard` 的重叠概念对照表链接回检：README「The same idea, three places」表中 12 个相对链接逐个可达——验收：`python scripts/check_links.py` exit 0 且人工抽查表内 3 处锚点定位正确

## P2 对外影响力与正式版（需机主授权 / 花钱项标注）

- [ ] P2-1 RAG 正式版：multilingual-e5 + Qdrant——本地部署可零费用，但 Qdrant Cloud / GPU 推理需机主批 API key / 算力授权
- [ ] P2-2 对外发布推广（Zenn / Qiita / HN 发文介绍 agent-cultivation）——对外发声需机主授权，AI 可先备三语文稿草稿
- [ ] P2-3 核心方法论文档翻译（README 明示 welcome future work：AGENT育成標準 等日中混排文档出 EN 版）——可零成本由 AI 译 + 机主审；外包审校则需预算
- [ ] P2-4 GitHub Releases 自动化（tag → release notes 从 CHANGELOG 生成）——零成本 CI 可做，但首次对外 release 公告需机主批准

## 冻结项（不做）

- `knowledge-notes/` 只由 `kb.py export-public` 生成，禁止手工复制任何笔记进本仓（沿 knowledge-base AGENTS.md §6 红线）；再导出只撤 manifest 列过的文件
- 不收客户案例、内部策略、未发布 IP；demo 数据必须虚构（README「Isn't」边界）
- 正文不做翻译式重写（CONTRIBUTING 纪律：保持团队原文措辞）
- 改脱敏规则必须同 PR 带回归测试（ai-stack/CLAUDE.md 硬约束——漏出=事故）；公开物推送与 PR 由机主决定

## 依据（2026-11-08 读仓）

- 无开放 issue；P1 素材取自 IMPROVEMENT-PLAN.md 阶段四既定项（provider 注册表、GiNZA NER、e5+Qdrant）——阶段一~三已落地（测试 0→99，CI ci.yml 已建）
- 对账素材：`knowledge-notes/manifest.json`（exported_at 2026-09-27、7 notes）vs 私有库 DIGEST（5 篇 public）；`git tag` 为 0；repo description 仍写「整理中」
- 红线来源：README「What this repo is/isn't」、CONTRIBUTING.md、knowledge-base AGENTS.md §6

<!-- draft by knowledge-ops expert agent, 待机主圈改 -->
