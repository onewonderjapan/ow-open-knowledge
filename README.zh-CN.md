# ow-open-knowledge

OneWonder Japan 的公开知识库：把内部实战中蒸馏出来的 AI Agent 育成方法论、企业 AI 导入最小可行架构、自动化工作流标准、多代理开发管线、云架构模式与团队协作规范汇总开源。

[English](README.md) | 简体中文 | [日本語](README.ja.md)

![License](https://img.shields.io/badge/license-MIT-blue) ![CI](https://github.com/onewonderjapan/ow-open-knowledge/actions/workflows/ci.yml/badge.svg)

## 这个仓库是什么 / 不是什么

**是**：一套在真实业务线上反复验证过的工作方法——AI agent 怎么养、闭环自动化工作流怎么建、企业 AI 导入的最小管线长什么样。参考代码可直接运行。

**不是**：客户案例集或产品代码库。不含客户信息、内部战略与未发表 IP；演示数据均为虚构。

**语言**：README 以英文为主。底层文档保留原文——日文、中文或日中混写，与团队实际写作一致（task-orchestrator 为英文）。核心方法论文档的翻译欢迎贡献。

## 目录导航

| 目录 | 内容 |
|------|------|
| ⭐ [agent-cultivation/](agent-cultivation/) | **核心资产**。Agent 育成标准（五条原则 + 三层固化）、既存 agent 训练指南、新项目 STARTUP 标准、数据安全分级规则、个人工作台 skill 组 |
| [ai-stack/](ai-stack/) | 企业 AI 导入参考实现：需求书→脱敏→社内先例检索（RAG）→LLM 起草→质检 的端到端薄切片 |
| [workflow-standard/](workflow-standard/) | 自动化工作流构建标准：四阶段闭环 + 7 条铁则 + 新工作流脚手架 |
| [task-orchestrator/](task-orchestrator/) | 自然语言任务总控 skill：技能路由→计划审批→持续执行→分层学习（纯标准库） |
| [dev-pipeline/](dev-pipeline/) | 6-agent 开发管线：Dispatcher/Investigator/Analyst/Developer/Reviewer/Tester + 自我学习 |
| [cloud-patterns/](cloud-patterns/) | 云架构模式 skill：Glue×RDS 合并、API Gateway+Lambda+SES 表单、Form→IAM、Terraform 踩坑 |
| [team-norms/](team-norms/) | 团队协作规范（日语）：Git 使用规范、Teams 聊天礼仪、商务邮件基础 |
| [ROADMAP.zh-CN.md](ROADMAP.zh-CN.md) | 改善与升级方案（[English](ROADMAP.md)） |

## 快速开始

最快的体验路径——ai-stack 的离线 demo（无需 API key）：

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r ai-stack/requirements.txt
python scripts/verify.py           # 测试 + stub 管线
# 只跑演示：
python ai-stack/pipeline/run.py ai-stack/demo_data/incoming/new_rfp.md --provider stub --out ai-stack/out
```

输出三件套：脱敏后的发送内容（`ai-stack/out/*_masked.md`）、设计书草稿（`*_draft.md`）、审计报告（`*_report.json`）。

另附标准库演示 Web UI（janome 可选；没有时 RAG 回退到 CJK 二元语法）：

```bash
python ai-stack/ui/app.py    # → http://127.0.0.1:7877
```

> `janome` 能提高 RAG 质量。`anthropic` 仅 `--provider anthropic-api` 需要（`pip install -r ai-stack/requirements-llm.txt`）。

分阶段升级见 [ROADMAP.zh-CN.md](ROADMAP.zh-CN.md)。

## 关联公开仓库

- [form2cloudbuilder](https://github.com/onewonderjapan/form2cloudbuilder) — Microsoft Form 填资源名即可创建 AWS/Azure 资源
- [wonder-contact-terraform](https://github.com/onewonderjapan/wonder-contact-terraform) — 官网问询表单基础设施（Terraform）
- [rds-glue-s3-etl-pipeline](https://github.com/onewonderjapan/rds-glue-s3-etl-pipeline) — AWS Glue (PySpark) ETL：S3 JSON 与 RDS 合并、Secrets Manager 凭据管理、Slack 通知
- [owd-knowledge-hub](https://github.com/onewonderjapan/owd-knowledge-hub) — 组织知识门户

## 贡献

欢迎 issue 与 PR，见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License

[MIT](LICENSE)
