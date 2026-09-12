# CHANGELOG

本仓库的变更历史。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

`agent-cultivation/AGENT育成標準.md` 要求「標準の変更は CHANGELOG 付きで版数を上げる」——
本文件是该要求在仓库自身层面的落地。

## [Unreleased]

### Security

- **脱敏层的 PII 漏出路径**（`ai-stack/masking/masker.py`）。修复前，以下四种日文商务文档中的常见写法全部原文穿透，未被打码：
  `0312345678`（无分隔符）、`03 1234 5678`（空格分隔）、`０３−１２３４−５６７８`（全角 + U+2212）、
  `user@localhost`（无点域名）。根因是 PHONE 正则强制要求分隔符为 `-` 或括号，且入口缺少 Unicode 归一化。
  现在 `mask()` 入口做 NFKC 归一化，电话覆盖无分隔符/空格/括号三种形态，邮箱接受无点域名。
- **RAG 召回的先例文档未脱敏就送入云端 LLM**（`ai-stack/pipeline/run.py`、`ai-stack/ui/app.py`）。
  此前只有需求书经过 `Masker.mask()`，拼进 prompt 的过往设计书是磁盘原文。demo 语料已预先匿名故无法察觉，
  但一旦投入真实历史设计书（这正是该组件的用途），客户名会随 prompt 直接出境。
  新增 `ai-stack/pipeline/drafting.py` 收敛 prompt 组装，使出境文本必经一处；先例正文与标题（文件名可能含客户名）
  一并脱敏；先脱敏后截断，避免边界切断实体留下残片。
- **模型输出驱动的任意文件读写**（`dev-pipeline/agents/developer.py`、`agents/tester.py`）。
  LLM 返回的 `file_path` 被直接拼到 workspace 上写入/删除/读取，`../../etc/passwd` 会解析到 workspace 之外。
  新增 `dev-pipeline/core/paths.py::resolve_in_workspace()`，拒绝父级引用、绝对路径、符号链接逃逸与前缀相同的兄弟目录。
- `ClaudeCLIProvider` 移除不必要的 `subprocess(shell=True)`，改为 `shutil.which()` 解析可执行文件后以 `shell=False` 启动（Windows 的 `claude.cmd` 同样可解析）。
- Web UI 输入校验：请求体上限 2MB，校验 `Content-Length`/JSON/必需键并返回 4xx，异常详情只进服务端日志（避免泄漏路径与环境信息）。
- 审计报告 `out/*_report.json` 不再写入实名逆查表。公开产物只保留件数与伏字标签；逆查表单独落在 `*_mapping.json`（`out/` 已被 gitignore）。
- 新增 [SECURITY.md](SECURITY.md)：漏洞私下上报流程，明确脱敏绕过为最高深刻度，并区分「设计上的已知限制」与真正的漏洞。

### Fixed

- 打码标签池从固定 14 个（`A社`..`N社`）改为算法生成（`A社`..`Z社`、`AA社`..），撤销上限。
  此前第 15 家公司起被 `min()` 静默压成 `N社`，破坏 mapping 的 1:1 审计对应——审计报告会声称多家不同客户是同一家。
  前 14 个标签顺序保持不变以兼容既有输出。
- 役职名不再被误判为人名。`人事部長の承認フロー` 曾变成 `担当者01部長の承認フロー`，并在审计表注入不存在的人 `{"人事": "担当者01"}`，同时破坏文意与审计记录。
- 辞典与 custom 替换合并为单一正则的最长匹配优先单趟替换，消除顺序依赖：此前短的 custom 条目（如「田中」）会先吃掉长公司名（「田中商事」）的内部，使后者再也无法匹配。
- 法人格与实体一体消化，不再产出 `株式会社A社` 这类损坏输出。
- `mask()` 新增可选 `mapping` 参数（向后兼容），跨文档继承编号。此前每篇文档从 `A社` 重新编号，导致不同文档的不同公司共用同一标签。
- `REQUIRED_SECTIONS` 收敛到 `evalkit` 单一真实源，prompt 章节由其生成。此前 prompt 要求 8 章而 QC 只查 6 章，`外部連携` 与 `移行・運用` 从未被检查。漏出正则也改为与 masking 层共享并在归一化后判定——检查者比生成者宽松则检查无意义。
- `BM25Index.add_dir` 只对本次新增文档累加 df。此前每次调用都重算全部文档，第二次调用会二重计上已有文档，IDF 失真。
- `get_provider` 的 if/elif 改为注册表，新增 `register_provider()`，外部可在不改动核心分支的前提下添加 provider。
- `claude` CLI 缺失时给出可操作的错误提示，而非 `FileNotFoundError` 回溯。
- 要件文件解析器（`dev-pipeline/core/requirement_parser.py`）：无分隔线时 `branch:` 行会残留在正文并原样传给 Agent；正文中的 Markdown 水平线会被误认为分隔线而丢弃其前的正文。改为只将「开头连续的 header 行」视为 header，并支持 YAML frontmatter 形式。
- `dev-pipeline` 的 JSON/Markdown 读写补上 `encoding="utf-8"`（Windows cp932 下写日文会炸）。Claude CLI 的 cwd 从硬编码 `/tmp` 改为 `tempfile.gettempdir()`。
- `--memory` / `--consolidate` / `--optimize` 纳入 Reviewer（它会写 memory，此前被漏掉）。
- Tester 文档不再写成“执行功能测试”；实际是 LLM 评审，不跑项目测试套件。
- 结构检查会对已知全名留下的姓氏断片报警。Demo UI 默认 stub，高亮 `担当者NN`。

### Changed

- `dev-pipeline` CLI 与元数据与实际执行对齐：`4 Agent`/`全5フェーズ` → `6 Agent`/`全6フェーズ`（`orchestrator.run()` 始终在第 4 阶段执行 Reviewer），`DEFAULT_PIPELINES` 补入 `reviewer`。
- 修正依赖与环境声明：Web UI 并非零依赖（经 RAG 层需要 `janome`，已实测验证）；`ai-stack` 的 Python 要求 3.9+ → 3.10+（运行时求值 `str | None`，且 3.9 已 EOL）；补入 `python-pptx`；移除 `dev-pipeline` 中从未 import 的 `anthropic`。
- 修正照抄即失败的文档路径：`workflow-standard/STANDARD.md` 的 `templates/_workflow-template` → `template`；STARTUP 标准中的 skeleton 路径指向 `../ai-stack/templates/project-skeleton/`；`dev-pipeline` 结构图根目录名 `agent/` → `dev-pipeline/`。

### Added

- `workflow-standard/scripts/validate.py`：可机检的铁则子集（必备文件、`paper`/`live`、jsonl、`run_key` 唯一）。
- `pyproject.toml`：ruff 配置。
- [IMPROVEMENT-PLAN.md](IMPROVEMENT-PLAN.md)：全仓审查结论与分阶段升级路线，每条附证据（文件:行号 + 复现命令 + 实际输出）与验收标准。
- 测试从 0 增至 112 件：`ai-stack/tests/` 59、`dev-pipeline/tests/` 24、`task-orchestrator/tests/` 11、`scripts/test_check_skills.py` 15、`workflow-standard/tests/` 3。
- CI（[.github/workflows/ci.yml](.github/workflows/ci.yml)）：四套测试在 Python 3.10/3.12 上运行、离线 demo 冒烟（机械校验 masked 输出与 report.json 均无实名且 QC 通过）、Markdown 相对链接校验、SKILL.md frontmatter 校验、全量字节编译。
- `scripts/check_links.py`：Markdown 相对链接校验（对 `%20` 等百分号编码解码后判断，与 GitHub 渲染一致）。
- `scripts/check_skills.py`：公开 `SKILL.md` 必须带非空 `name` / `description` frontmatter，且 `name` 与目录名一致（`CHANGE-ME` 模板除外）。没有 frontmatter 的 skill 对任何加载器都是隐形的。
- OSS 基础设施：[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)、issue 模板（bug/proposal）与 `config.yml`、PR 模板（含改动脱敏层时的测试必须项）、`.editorconfig`、本 CHANGELOG。
- `dev-pipeline/requirements/example.md`：提交进仓的要件文件样例。此前 `requirements/` 被整目录 gitignore，新人无可复制的起点（目录形式的 ignore 会让 git 不再进入该目录，否定模式因此失效，已改为 `requirements/*`）。
- `agent-cultivation/PITFALLS.md` 追加第 12–20 条踩坑记录。12–19 是脱敏层；第 20 条是 `cloud-patterns` 四份 skill 缺 YAML frontmatter、被加载器整份忽略（README 还写着「可以直接放进 Claude Code」）。
- 根 README（英 / 日 / 中）增加「按目标选入口」决策表、三套重叠概念的对照表、两套 skill 安装路径说明，以及目录表的语言列（日/中混写、日文、中文、英文）。四个 Agent 体系的 README 顶部各加一行相互关系。
- `task-orchestrator/scripts/scan_skills.py` 同时发现 `.agents/skills`（Codex 系）与 `.claude/skills`（Claude Code）。只扫前者时，Claude Code 用户的 skill 对编目工具本身不可见。
- `cloud-patterns/skills/*/SKILL.md` 四份补上 `name` / `description` frontmatter。补之前扫描器报 6 skills / 4 warnings，补之后本仓 11 个 `SKILL.md` 全部可编目。

## [0.1.0] - 2026-09-11

### Added

- 首次公开发布：`agent-cultivation`（Agent 育成标准与方法论）、`ai-stack`（企业 AI 落地参考实现）、
  `workflow-standard`（自动化工作流标准）、`task-orchestrator`（任务总控 skill）、
  `dev-pipeline`（6 Agent 开发流水线）、`cloud-patterns`（云架构 skills）、`team-norms`（团队规范）。
