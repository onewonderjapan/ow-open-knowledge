# ow-open-knowledge

OneWonder Japan 的公开知识库：把内部实战中蒸馏出来的 AI Agent 育成方法论、企业 AI 导入最小可行架构、自动化工作流标准、多代理开发管线、云架构模式与团队协作规范汇总开源。

[English](README.md) | 简体中文 | [日本語](README.ja.md)

![License](https://img.shields.io/badge/license-MIT-blue)

## 这个仓库是什么 / 不是什么

**是**：一套在真实业务线上反复验证过的工作方法——AI agent 怎么养、闭环自动化工作流怎么建、企业 AI 导入的最小管线长什么样。参考代码可直接运行。

**不是**：客户案例集或产品代码库。不含客户信息、内部战略与未发表 IP；演示数据均为虚构。

**语言**：README 以英文为主。底层文档保留原文——日文、中文或日中混写，与团队实际写作一致（task-orchestrator 为英文）。核心方法论文档的翻译欢迎贡献。目录表标了各目录的语言，点开之前就能知道。

## 从哪进

本仓是一套工具箱，不是单一产品。四个目录都在讲「怎么跑 Agent」，重叠是有意的，不能互相替换。

| 如果你想… | 从这里进 |
|-----------|----------|
| 搞清团队怎么养一个 agent（原则、训练、数据分级） | [agent-cultivation/](agent-cultivation/) |
| 建一个会自我改善的定时工作流（cron + skill） | [workflow-standard/](workflow-standard/) |
| 把一次性自然语言任务变成：发现技能 → 审批计划 → 再执行 | [task-orchestrator/](task-orchestrator/) |
| 把一份书面需求交给 6-agent 管线去写代码 | [dev-pipeline/](dev-pipeline/) |
| 把商务文档送给 LLM，且不漏出人名和电话 | [ai-stack/](ai-stack/) |
| 复用蒸馏过的 AWS/云流程（或它的「不要做」清单） | [cloud-patterns/](cloud-patterns/) |
| 查 Git / Teams / 邮件约定 | [team-norms/](team-norms/) |

### 同一个概念，写了三遍

这些概念在多个体系里各有一份定义。按你正在做的那件事去读对应的那份，它们不是同一套实现。

| 概念 | 定义在哪 | 那一份是干什么的 |
|------|----------|------------------|
| 人工审批门 | [task-orchestrator/SKILL.md](task-orchestrator/SKILL.md)（计划批准前不得改任何东西）；[workflow-standard/STANDARD.md](workflow-standard/STANDARD.md) P4（不可逆 / 对外副作用）；[dev-pipeline/USAGE.md](dev-pipeline/USAGE.md)（Human / Hybrid 执行者） | 任务启动 vs. 上线副作用 vs. 子任务由谁做 |
| 学习 / 记忆固化 | [AGENT育成標準.md](agent-cultivation/AGENT育成標準.md) 三层（code / skill / memory）；[learning-policy.md](task-orchestrator/references/learning-policy.md)（project / personal / none）；[dev-pipeline `agents/memory/`](dev-pipeline/README.md) | 育成标准 vs. 任务结束后的规则分流 vs. 每个 agent 的运行记忆 |
| 经验沉淀 | [PITFALLS.md](agent-cultivation/PITFALLS.md)；[工作流 `state/ledger.jsonl`](workflow-standard/STANDARD.md)；[task-orchestrator 的 run `learning.md`](task-orchestrator/references/execution-contract.md) | 人手写的踩坑 vs. 工作流回放账本 vs. 单次运行的学习笔记 |

### 技能安装路径

本仓发布的 skill 跟文档放在一起（`cloud-patterns/skills/`、`agent-cultivation/workbench-skills/` 等）。Agent 运行时认 **两套** 约定目录：

| 运行时 | 项目级 | 用户级 |
|--------|--------|--------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex 系 | `.agents/skills/` | `~/.agents/skills/` |

`task-orchestrator` 自称两边都能用，`scripts/scan_skills.py` 也会扫两边。在**本仓库根目录**默认扫一遍，看不到本仓发布的 skill：它们是源码包，并没有安装到这里的 `.claude/` 或 `.agents/` 下（默认扫描仍可能列出你用户目录里的 skill）。要编目本仓发布的 skill：

```bash
python3 task-orchestrator/scripts/scan_skills.py --cwd . --pretty \
  --root project=cloud-patterns/skills \
  --root project=agent-cultivation/workbench-skills \
  --root project=task-orchestrator \
  --root project=workflow-standard/template
```

拷到你自己项目的 `.claude/skills/` 或 `.agents/skills/` 才算安装。每个 `SKILL.md` 必须带 YAML frontmatter（`name` + `description`），否则加载器会直接忽略——`scripts/check_skills.py` 守这道门。

## 目录导航

| 目录 | 内容 | 语言 |
|------|------|------|
| ⭐ [agent-cultivation/](agent-cultivation/) | **核心资产**。Agent 育成标准（五条原则 + 三层固化）、既存 agent 训练指南、新项目 STARTUP 标准、数据安全分级规则、个人工作台 skill 组 | 日 / 中混写 |
| [ai-stack/](ai-stack/) | 企业 AI 导入参考实现：需求书→脱敏→社内先例检索（RAG）→LLM 起草→质检 的端到端薄切片 | 日文（README 英 + 日） |
| [workflow-standard/](workflow-standard/) | 自动化工作流构建标准：四阶段闭环 + 7 条铁则 + 新工作流脚手架 | 中文（README 英文） |
| [task-orchestrator/](task-orchestrator/) | 自然语言任务总控 skill：技能路由→计划审批→持续执行→分层学习（纯标准库） | 英文 |
| [dev-pipeline/](dev-pipeline/) | 6-agent 开发管线：Dispatcher/Investigator/Analyst/Developer/Reviewer/Tester + 自我学习 | 日文（README 英 + 日） |
| [cloud-patterns/](cloud-patterns/) | 云架构模式 skill：Glue×RDS 合并、API Gateway+Lambda+SES 表单、Form→IAM、Terraform 踩坑 | 中文（README 英文） |
| [team-norms/](team-norms/) | 团队协作规范：Git 使用规范、Teams 聊天礼仪、商务邮件基础 | 日文 |

## 快速开始

最快的体验路径——ai-stack 的离线 demo（无需 API key，已实测通过）：

```bash
cd ai-stack
python -m venv .venv
# Windows (Git Bash / PowerShell)：
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub
# macOS / Linux：
# source .venv/bin/activate && pip install -r requirements.txt
# python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub
```

输出三件套：脱敏后的发送内容（`out/*_masked.md`）、设计书草稿（`out/*_draft.md`）、审计报告（`out/*_report.json`）。

另附演示 Web UI：

```bash
python ui/app.py    # → http://127.0.0.1:7877
```

> 依赖：Web UI 的 HTTP 层是纯标准库，但它复用了 RAG 层，所以和 pipeline 一样需要 `janome`——pipeline 即使在 stub 模式下也需要它。`anthropic` 仅 API provider 需要，`python-pptx` 仅 `tools/` 需要。Python 3.10+。

## 关联公开仓库

- [form2cloudbuilder](https://github.com/onewonderjapan/form2cloudbuilder) — Microsoft Form 填资源名即可创建 AWS/Azure 资源
- [wonder-contact-terraform](https://github.com/onewonderjapan/wonder-contact-terraform) — 官网问询表单基础设施（Terraform）
- [rds-glue-s3-etl-pipeline](https://github.com/onewonderjapan/rds-glue-s3-etl-pipeline) — AWS Glue (PySpark) ETL：S3 JSON 与 RDS 合并、Secrets Manager 凭据管理、Slack 通知
- [owd-knowledge-hub](https://github.com/onewonderjapan/owd-knowledge-hub) — 组织知识门户

## 贡献

欢迎 issue 与 PR，见 [CONTRIBUTING.md](CONTRIBUTING.md)（收录边界）与
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

提 PR 前先跑测试：

```bash
python -m pip install janome                                                  # ai-stack RAG 层
python -m unittest discover -s ai-stack/tests -t ai-stack/tests               # 脱敏 + prompt 组装
python -m unittest discover -s dev-pipeline/tests -t dev-pipeline/tests       # workspace 边界 + 解析器
python -m unittest discover -s task-orchestrator/tests -t task-orchestrator/tests
python scripts/check_links.py                                                 # markdown 相对链接
python scripts/check_skills.py                                                # SKILL.md frontmatter
python -m unittest discover -s scripts -t scripts -p "test_*.py"
```

CI 会在每个 PR 上跑同样的检查，外加离线 demo。

**脱敏是安全控制**。`ai-stack/masking/` 决定什么可以离开内网，改规则不补回归测试就是漏出事故的来源
——见 [ai-stack/CLAUDE.md](ai-stack/CLAUDE.md)。

## 安全

发现脱敏绕过、未脱敏数据进入 LLM、或模型输出驱动的任意文件访问？请私下上报，见 [SECURITY.md](SECURITY.md)。

## License

[MIT](LICENSE)
