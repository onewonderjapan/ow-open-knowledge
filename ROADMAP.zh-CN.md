# 改善・升级方案

[English](ROADMAP.md) | 简体中文

本仓**不是**一个可 pip 安装的单库，而是公开知识库：Agent 育成方法论、企业 AI 导入薄切片、工作流标准、多代理管线、云模式 skill、团队规范。

升级保持这个形态。`ai-stack` 已对外承诺的接口不变：

`Masker.mask` · `BM25Index.search` · `get_provider` · `evalkit.check`

## 现状判断

| 模块 | 已经成立的部分 | 缺口 |
|------|----------------|------|
| 方法论 (`agent-cultivation/`) | 真实业务线上的育成闭环，踩坑即产品 | 核心文档日中混写，无英文原文 |
| 薄切片 (`ai-stack/`) | 端到端可跑，层可替换 | 脱敏无测试；UI 宣称零依赖却 import janome；`claude-cli` 使用 `shell=True`（Linux 上是坏的） |
| 总控 (`task-orchestrator/`) | 纯标准库扫描器 + 测试 | 未接入 CI |
| 开发管线 | 6-agent 设计 + 自我学习 | CLI 仍写「4 Agent」；Dispatcher 提示词漏了 Reviewer；无解析测试 |
| 工作流 / 云 / 团队规范 | 标准与 skill 清晰 | 除 markdown 脚手架外无可执行夹具 |
| 开源卫生 | MIT、CONTRIBUTING、三语 README | 无 CI、无 SECURITY.md、无 issue/PR 模板 |

既有 PR #1 / #2 是 Bot 协作文档轨，与本方案独立。

## Phase 0 — 本变更已落地

育成标准自己要求的卫生（PITFALLS：「脱敏はテストケース必須」）。

- 脱敏 / 质检 / RAG / stub 管线测试；`scripts/verify.py` + GitHub Actions（Python 3.9 / 3.12）
- 公司标签超过 `A社`–`N社` 不再碰撞；BM25 `add_dir` 重算 df；质检 8 章与起草提示词对齐
- 演示 UI 默认 stub，高亮 `担当者01` / `会社15`，无 janome 也能跑（CJK 二元语法回退）
- `claude-cli` 改为 `shell=False`；anthropic 拆到 `requirements-llm.txt`
- Dispatcher / `--memory` / `--optimize` 覆盖全部 6 个 agent；默认开发管线含 Reviewer
- SECURITY.md、issue/PR 模板；仓库根目录忽略 `entities.local.json`

验证：

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r ai-stack/requirements.txt
python scripts/verify.py
```

## Phase 1 — 让薄切片变得可信任

不改架构，每项一个小 PR。

1. **脱敏泄漏语料**：20–50 篇虚构日文商务文档（无敬称人名、株式会社/製作所、全角空格）。电话/邮件/已知实名残留则失败。
2. **可选 GiNZA NER**：同一 `Masker.mask` 契约下的 extra（`ai-stack/masking/ner.py`）。默认仍是正则+词典，演示保持轻。
3. **Evalkit judge**：按现有草图做 `evalkit/judge.py`；用冻结的 stub 夹具，CI 不打 API。
4. **Provider 矩阵**：OpenAI 兼容 + 本地 Ollama/llama.cpp；统一环境变量 `AI_STACK_PROVIDER`。消掉模型名漂移（`claude-sonnet-5` vs `claude-sonnet-4-6`）。
5. **演示 UI**：监听地址参数（默认仍 localhost）、POST 体积上限、JSON 错误处理；继续零第三方框架。
6. **dev-pipeline dry-run**：`--provider stub` 写同样的报告路径、不调用 Claude CLI，让 6-agent 环可进 CI。

## Phase 2 — 生产级替换（接口不变）

把 `ai-stack/README.md` 里那张表变成工作包：

| 层 | 替换为 | 约束 |
|----|--------|------|
| `masking/` | GiNZA + 法务审过的规则 + `entities.local.json` 流程 | 对应表只留在进程内，永不上传 |
| `rag/` | multilingual-e5 + Qdrant（或 pgvector）+ ACL | `search(query, k)` 签名不变 |
| `llm/` | LiteLLM / AI 网关，按租户给密钥 | `complete(prompt) -> str` 不变 |
| `evalkit/` | LLM-as-judge + 回归金样 | `check()` 仍是决定论闸门 |
| `pipeline/` | 任务队列 + 需登录的 UI | CLI 一发仍留给演示 |

不要一次加厚所有层。一层一个 PR，附 `scripts/verify.py` 前后对比 + 一份虚构 RFP。

## Phase 3 — 知识产品，而不只是代码

1. **翻译核心四件**（保留原文）：`AGENT育成標準.md`、`既存AGENT訓練ガイド.md`、`新プロジェクトSTARTUP標準.md`、`workflow-standard/STANDARD.md` → `*.en.md`，日/中为源。
2. **阅读路径**：根 README 加一页「我是 PM / SE / agent 搭建者」索引。
3. **Skill 包安装**：`make install-skills DEST=~/.claude/skills`，复制 `task-orchestrator`、`cloud-patterns/skills/*`、`agent-cultivation/workbench-skills/*`。
4. **标准版本化**：育成标准 / STANDARD.md 用 SemVer（v1.1 只增不改；v2 才破规则），旁边放 Changelog。
5. **社区**：CODE_OF_CONDUCT、Discussions 分类 “pitfalls”、GitHub topics（`ai-agents`、`rag`、`pii-masking`）。

## Phase 4 — 明确不做

- 不合并客户案例或真名。CONTRIBUTING.md 的收录边界是承重墙。
- 不把本仓做成产品单仓。配套仓（`form2cloudbuilder` 等）保持独立；这里只留蒸馏后的 skill + 可跑的薄切片。
- 在 Phase 2 的任务队列出现之前，不给 `ui/app.py` 上重型 Web 框架。
- 不用「统一成一种语言」原地重写方法论文档。

## Phase 0 之后建议的 PR 顺序

1. 脱敏泄漏语料 + 必要的规则修补
2. `evalkit/judge.py` + stub 夹具
3. `dev-pipeline --provider stub`
4. Skill 包安装器
5. 核心四件英文翻译
