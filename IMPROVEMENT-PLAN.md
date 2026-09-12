# 改善・升级方案（ow-open-knowledge）

本文是对本仓库的一次完整审查结论与升级路线。所有判断都基于实际读码与实际运行，证据写在每一条里（文件:行号 + 复现命令 + 真实输出）。

结论一句话：**方法论文档的质量明显高于参考实现的工程质量。仓库最大的风险不是缺功能，而是被当作「安全参考实现」宣传的脱敏层存在真实漏出路径，且全仓没有 CI 来兜住它。**

---

## 1. 现状盘点

| 目录 | 内容 | 规模 | 性质 |
|------|------|------|------|
| `agent-cultivation/` | Agent 育成标准、训练指南、数据分级、workbench 技能 | 16 篇 md | 方法论（自称核心资产） |
| `ai-stack/` | 企业 AI 落地参考实现：脱敏 → RAG → LLM 起草 → 本地质检 | 8 个 py / 840 行 | **可运行代码** |
| `dev-pipeline/` | 6 Agent 开发流水线 | 3293 行 py | **可运行代码** |
| `task-orchestrator/` | 主技能：技能路由 → 计划审批 → 持续执行 → 分层学习 | 459 行 py + 9 个测试 | 代码 + 唯一的测试 |
| `workflow-standard/` | 自动化工作流标准：四阶段闭环 + 7 铁律 + 脚手架 | 9 篇 md | 方法论 + 模板 |
| `cloud-patterns/` | 4 个云架构 SKILL | 5 篇 md | 方法论 |
| `team-norms/` | 团队规范（日文） | 4 篇 md | 方法论 |

**优点，值得保留的部分**：分层契约（`Masker.mask` / `BM25Index.search` / `get_provider` / `check`）划得干净，薄切片→正式版的替换边界清晰；离线 stub demo 真的能一把跑通；`task-orchestrator` 的 9 个 unittest 是全仓唯一的真实质量护栏，且确实通过。

**核心矛盾**：`ai-stack/CLAUDE.md:9` 自己立了规矩——「脱敏层的测试没写就不要改脱敏规则（漏 = 事故）」——但仓库里**一个脱敏测试都没有**。规矩写了，护栏没建。

---

## 2. P0：必须修（安全与正确性）

### P0-1 脱敏层存在真实 PII 漏出路径

脱敏在本仓的定位是**安全控制**（README 承诺「只有打码后的文本离开内网」），所以任何漏出都是 P0。

复现：

```bash
cd ai-stack && python3 -c "
import sys; sys.path.insert(0,'.')
from masking.masker import Masker
m = Masker('masking/entities.json')
for c in ['TEL 0312345678','TEL 03 1234 5678','TEL ０３−１２３４−５６７８','連絡先 user@localhost']:
    print(repr(c), '->', repr(m.mask(c)[0]))
"
```

实际输出——**四条全部原文穿透，没有任何打码**：

```
'TEL 0312345678'        -> 'TEL 0312345678'
'TEL 03 1234 5678'      -> 'TEL 03 1234 5678'
'TEL ０３−１２３４−５６７８' -> 'TEL ０３−１２３４−５６７８'
'連絡先 user@localhost'  -> '連絡先 user@localhost'
```

根因在 `ai-stack/masking/masker.py:19`，PHONE 规则强制要求分隔符必须是 `-` 或括号：

```python
("PHONE",  re.compile(r"(?:0\d{1,4}[-(]\d{1,4}[-)]\d{3,4})")),
```

日文商务文档里全角数字、全角波折号、无分隔符连写都极常见，而正则前**没有做 Unicode 归一化**。日文场景不做 NFKC 就等于放弃了半数输入形态。

**方案**：`mask()` 入口先 `unicodedata.normalize("NFKC", text)`；PHONE 扩展为覆盖无分隔符 / 空格分隔 / 括号形态；EMAIL 允许无点域名（内网主机名同样是标识信息）。**并且必须同时补回归测试**——这是 `CLAUDE.md` 自己的要求。

### P0-2 打码标签只有 14 个，第 15 家公司起静默串号

`masker.py:30` 标签池写死 A–N，`masker.py:60` 用 `min(...)` 截断：

```python
_COMPANY_LABELS = [f"{c}社" for c in "ABCDEFGHIJKLMN"]
...
lab = _COMPANY_LABELS[min(counters["company"], len(_COMPANY_LABELS) - 1)]
```

实测 20 家公司 → 只产生 14 个唯一标签，第 15 家以后全部塌成 `N社`。这直接破坏 mapping 的 1:1 审计性质：审计报告会声称多家不同客户是同一家。**静默降级比报错危险**。

**方案**：标签算法化生成（`A社`…`Z社`、`AA社`…），去掉上限；同时保持既有 14 个标签的编号顺序不变，以免破坏现有 demo 输出。

### P0-3 RAG 召回的先例文档未脱敏就送进云端 LLM

这是**架构层面最严重的一处**，因为它绕过了整个安全模型。`ai-stack/pipeline/run.py:60` 与 `ui/app.py:214`：

```python
refs_text = "\n\n---\n\n".join(f"【{h['title']}】\n{h['text'][:2500]}" for h in hits) or "(先例なし)"
```

`h["text"]` 是**从磁盘语料原样读出的**。只有需求书走了 `masker.mask()`，先例文档没走。demo 语料是预先匿名过的（`A社`/`B社`），所以 demo 看不出问题；一旦按 README 指引把真实历史设计书放进 `demo_data/past_projects/`（这正是这套东西的用途），**真实客户名会直接随 prompt 出境**。

`pipeline/run.py:62` 的注释「渡るのは伏せ字済みテキストのみ（出境的只有打码文本）」在这条路径上是不成立的。

**方案**：对每篇召回文档同样跑 `masker.mask()`，并把先例的 mapping 合并进审计报告；prompt 组装处禁止出现未经脱敏的 `h["text"]`。

### P0-4 人名模式把职务名误判为人名，污染文档和审计表

`masker.py:28` 把「2–4 个汉字 + 部長/課長/社長」整体当人名：

```python
_PERSON_PAT = re.compile(r"([一-龥]{2,4})(様|氏|さん|部長|課長|社長)")
```

实测 `人事部長の承認フロー` → `担当者01部長の承認フロー`，且 mapping 里多出一条假记录 `{"人事": "担当者01"}`。这既破坏了给 LLM 的正文语义（部门名消失了），又往审计表里注入了不存在的「人」。

**方案**：职务后缀（`部長/課長/社長`）与敬称（`様/氏/さん`）分开处理——职务类需要命中人名词典或 NER 才打码，并排除 `人事/営業/総務/経理/開発` 等组织词；敬称类保留现有宽松策略（宁可多打码）。

### P0-5 dev-pipeline 存在路径穿越写文件

`dev-pipeline/agents/developer.py:332` 直接把 LLM 返回的相对路径拼到 workspace 上：

```python
file_path = self.config.workspace / change.file_path
...
file_path.write_text(change.content)
```

LLM 若返回 `../../etc/passwd`，`Path` 拼接会解析到 workspace 之外。这是**把模型输出当可信输入**的典型错误，且同一函数还有 `unlink()` 删除分支。

**方案**：写入/删除前 `resolve()` 并校验 `is_relative_to(workspace.resolve())`，越界直接抛异常拒绝。

---

## 3. P1：工程化（让「参考实现」这个词站得住）

### P1-1 全仓没有 CI

`.github/` 目录不存在。仓库唯一的测试（`task-orchestrator/tests`，9 个 case）从来没有在 PR 上自动跑过。同时 `CONTRIBUTING.md:15` 要求「代码改动需附可运行的验证命令与输出（证据主义）」——这条纪律靠人工执行，无法规模化。

**方案**：加 GitHub Actions，最小三件事：跑全部 unittest、跑一次 `ai-stack` 离线 demo 做冒烟、校验 markdown 相对链接不断。用标准库 + 单一依赖，保持 CI 秒级。

### P1-2 UI 的 POST 处理缺输入校验

`ai-stack/ui/app.py:200`：

```python
n = int(self.headers.get("Content-Length", 0))
req = json.loads(self.rfile.read(n).decode("utf-8"))
```

三个问题：body 无上限（内存耗尽）；`Content-Length` 非数字时 `int()` 抛异常；`req["text"]` / `req["masked"]` 缺键直接 500。绑定 `127.0.0.1` 是对的，但 demo 也不该用未校验输入示范。另外 `app.py:219` 把异常字符串原样回给客户端，会泄漏路径和环境信息。

**方案**：body 设上限、解析与取值全部校验、错误回 400 且消息脱敏、异常详情只进服务端日志。

### P1-3 `subprocess` 无必要地用了 `shell=True`

`ai-stack/llm/providers.py:46`：

```python
r = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                   encoding="utf-8", timeout=600, shell=True)
```

`cmd` 目前是 list，所以当下没有注入口子，但 `shell=True` + list 在 POSIX 上语义本身就是错的（只有 `cmd[0]` 会被执行），而且一旦有人把它改成字符串拼接就立刻变成漏洞。**在公开的参考实现里示范这个写法，代价是被抄走。**

**方案**：去掉 `shell=True`；顺手处理 `claude` CLI 不存在时的 `FileNotFoundError`，给出可操作的提示。

### P1-4 必需章节常量两处定义、已经漂移

prompt 要求 8 章（`pipeline/run.py:25`），质检只查 6 章（`evalkit/structure_check.py:9`，缺 `外部連携`、`移行・運用`）。同理 `evalkit` 的漏出正则比 `masker` 的更窄，「检查者比生成者宽松」——这恰恰违背 `agent-cultivation/AGENT育成標準.md` 自己写的「生成者と検査者は分離する」的精神。

**方案**：抽成单一共享常量与共享 leak 规则模块，两边 import 同一个源。

### P1-5 依赖与环境声明不准

- `ai-stack/requirements.txt:1` 写「Web UI 只用标准库」，但 `ui/app.py` → `rag.retriever` → `janome`，**UI 实际需要 janome**。README.md:52 同样写错。
- `tools/*.py` 需要 `python-pptx`，未列入 requirements。
- README 标 3.9+，但 `masker.py:37`、`providers.py:38` 用了 `str | None`（3.10+ 语法）。
- `dev-pipeline/requirements.txt` 列 `anthropic>=0.40.0`，但运行时走 Claude Code CLI（`agents/base.py:281`），`USAGE.md` 还明确说不需要 API key。

**方案**：逐条改正，依赖加下限约束，Python 版本统一为 3.10+。

### P1-6 `BM25Index.add_dir` 二次调用会污染 df

`rag/retriever.py:40-42` 每次 `add_dir` 都对**全部** docs 重算一遍 df 累加：

```python
for d in self.docs:
    for w in set(d["tokens"]):
        self.df[w] += 1
```

调两次 `add_dir`，已有文档的 df 被重复计数，IDF 失真。多语料目录是很自然的用法。

**方案**：只对本次新增文档累加 df。

---

## 4. P2：结构与可用性升级

### P2-1 四套「怎么跑 Agent」的体系没有导航

`agent-cultivation`（怎么固化学习）、`workflow-standard`（四阶段闭环）、`task-orchestrator`（计划审批 + 技能路由）、`dev-pipeline`（6 Agent 写代码）在根 README 里是并列的七行表格，没有任何「你想做 X 就从这里进」的判断依据。四者还各自定义了重叠概念：

- **人工审批门**三处各写一套：`task-orchestrator/SKILL.md:18`、`workflow-standard/STANDARD.md:27`、`dev-pipeline/USAGE.md:159`。
- **学习/记忆固化**三种模型：三层固化（`AGENT育成標準.md:46`）、project/personal/none（`learning-policy.md:17`）、`agents/memory/`（`dev-pipeline/README.md:75`）。
- **经验沉淀**三种存储：`PITFALLS.md`、append-only `ledger.jsonl`、`.task-workflow/runs/*/learning.md`。

**方案**：根 README 加一张「按目标选入口」的决策表；四个体系各自 README 顶部加一行「本目录与其他三者的关系」；把重叠概念显式交叉链接，而不是各写一遍。

### P2-2 技能安装路径分裂成两套

`workflow-standard`、`cloud-patterns`、`agent-cultivation/workbench-skills` 用 `.claude/skills/`，而 `task-orchestrator/scripts/scan_skills.py:209` 扫的是 `.agents/skills/`。后果可实测：

```bash
cd task-orchestrator && python3 scripts/scan_skills.py --cwd /workspace --pretty
# → "skills": []
```

**仓库自带的技能扫描器，扫不到本仓库发布的任何技能。**

**方案**：确定一个规范路径，另一个作为兼容 root 明确写进文档；README 说明两种 agent 生态的映射关系。

### P2-3 文档里的路径照抄会失败

| 文件:行 | 写的 | 实际 |
|---------|------|------|
| `workflow-standard/STANDARD.md:195` | `cp -r templates/_workflow-template ...` | 该路径不存在，实际是 `workflow-standard/template` |
| `agent-cultivation/新プロジェクトSTARTUP標準.md:21` | `templates/project-skeleton/` | 实际在 `ai-stack/templates/project-skeleton/` |
| `dev-pipeline/USAGE.md:292` | 根目录叫 `agent/` | 实际叫 `dev-pipeline/` |
| `dev-pipeline/README.md:102` | 有 `requirements/` 目录 | 被 gitignore，仓里没有样例文件 |

新人照着「快速开始」敲第一条命令就会失败，这是留存杀手。**方案**：逐条改正，并补一个提交进仓的 `dev-pipeline/requirements/example.md`。

顺带核实过一处**不是**问题的地方：`team-norms/README.md:9` 用 `Git%20使用規範ドキュメント.md` 指向含空格的文件名，URL 编码后能正确解析（全仓 75 条相对链接经解码校验后 0 断链）。保持原样。

### P2-4 CLI 帮助文本与实际流水线不一致

`dev-pipeline/main.py:490` 写「4 Agent」、`:500` 写「全5フェーズ」，但 `orchestrator.run()`（`orchestrator.py:183-201`）总是执行 Reviewer，实际是 6 阶段；`agents/dispatcher.py:40` 的 `DEFAULT_PIPELINES` 也漏了 reviewer，导致落盘的 `dispatch.json` 与真实执行不符。README 通篇讲 6 Agent。**方案**：以 orchestrator 实现为准，统一 CLI 文本与 dispatcher 默认值。

### P2-5 缺开源基础设施

已有：`LICENSE`(MIT)、`CONTRIBUTING.md`、`.gitignore`、各目录 README。
缺：CI、issue/PR 模板、`SECURITY.md`、`CODE_OF_CONDUCT.md`、根 `CHANGELOG.md`、版本号/tag、`.editorconfig`、lint 配置。

其中 `CHANGELOG` 尤其讽刺：`AGENT育成標準.md:115` 明文要求「本標準の変更は CHANGELOG 付きで版数を上げる」，`新プロジェクトSTARTUP標準.md:25` 把「CHANGELOG に1行」列为第一天的必做项，但仓库自身没有 CHANGELOG。方法论没有作用在自己身上。

考虑到本仓库自带一个**安全控制性质的脱敏层**，`SECURITY.md`（漏洞如何私下上报）不是可选项。

### P2-6 语言分布没有地图

EN / JA / ZH 三语混排，且存在**单文件内混用**：`AGENT育成標準.md` 是日文正文夹中文术语（狗糧原則、踩坑、金牌、回流），`dev-pipeline/USAGE.md:166` 日文里出现中文「文件」，`task-orchestrator/references/execution-contract.md:33` 英文里出现中文审批词（同意/批准）。

保持原文是 `CONTRIBUTING.md:14` 的明确纪律，**不应该翻译式重写**。但读者需要知道点开之前是什么语言。**方案**：根 README 加一列语言标注（含「混用」标记），不动正文。

---

## 5. 分阶段路线图

不按日历排期，按依赖关系与改动侵入性排。

**阶段一：止血（P0 全部 + P1-1）**
改动集中在 `ai-stack/masking/masker.py`、`pipeline/run.py`、`ui/app.py`、`dev-pipeline/agents/developer.py`，加上新的测试目录与 CI。侵入性低、无跨层接口变更。依赖：脱敏改动**必须**与回归测试同一个 PR（`CLAUDE.md:9`）。风险：打码标签编号若变化会影响现有 demo 输出，需保持前 14 个标签顺序不变。

**阶段二：可信度（P1 其余 + P2-3/P2-4/P2-5）**
纯工程债与文档事实性修正，彼此独立，可并行小 PR。无架构风险。

**阶段三：结构升级（P2-1/P2-2/P2-6）**
需要产品判断而非纯技术判断：先定「技能安装路径规范」这一个决策，再重写导航层。建议先开 issue 对齐（`CONTRIBUTING.md:13` 的要求），不要直接大改 PR。

**阶段四：薄切片 → 正式版（原设计已规划）**
既有契约已经预留了替换点：脱敏叠 GiNZA NER、RAG 换 multilingual-e5 + Qdrant、`get_provider` 改注册表/entry-points（当前是 `providers.py:68` 的硬编码 if/else）。前置条件是阶段一的回归测试先建起来——**没有测试就替换脱敏引擎，等于把 P0-1 重做一遍**。

---

## 6. 验收标准

改完之后应该能满足：

1. 脱敏回归测试覆盖：全角/半角、无分隔符电话、公司法人形态前后缀、标签池耗尽、职务名误判、mapping 可逆。测试红→绿有记录。
2. `grep` 不到任何把未脱敏 `h["text"]` 送进 prompt 的路径。
3. CI 在 PR 上跑：unittest 全绿 + `ai-stack` 离线 demo 冒烟通过 + markdown 链接无断链。
4. 文档里每条 `cp` / `python` 命令都能照抄跑通。
5. `scan_skills.py` 在本仓库根目录能扫到本仓库发布的技能（或文档明确说明为什么扫不到、该怎么配）。
6. 必需章节、leak 正则各只有一处定义。

---

## 7. 本次已落地的改动

本 PR 不止给方案，同时把阶段一（止血）与阶段二基本实现了，让方案自带证据。完整清单见 [CHANGELOG.md](CHANGELOG.md)，要点：

- **P0-1/P0-2/P0-4** 脱敏层重写：NFKC 归一化、单趟最长匹配替换、法人格整体消化、标签池无上限、职务名排除表。
- **P0-3** 新增 `ai-stack/pipeline/drafting.py` 收敛 prompt 组装，先例正文与标题一并脱敏、先脱敏后截断、跨文档共享编号；`run.py` 与 `ui/app.py` 都改走这条路径。
- **P0-5** 新增 `dev-pipeline/core/paths.py::resolve_in_workspace()`，`developer.py` 的写入/删除与 `tester.py` 的读取都做越界校验。
- **P1-1** GitHub Actions 四个 job：三套测试（Python 3.10/3.12）、离线 demo 冒烟（机械校验 masked 输出无实名）、Markdown 链接校验、全量字节编译。
- **P1-2/P1-3/P1-4/P1-5/P1-6** UI 输入校验、去掉 `shell=True` 并改用 `shutil.which()`、provider 注册表、章节与 leak 规则单一真实源、依赖与 Python 版本声明改正、`add_dir` 的 df 二重计上修复。
- **P2-3/P2-4/P2-5** 文档路径与阶段数修正、提交进仓的要件样例、`SECURITY.md`、`CODE_OF_CONDUCT.md`、issue/PR 模板、`.editorconfig`、根 `CHANGELOG.md`。

测试从 0 增至 82 件。另外修了要件解析器两个会静默吃掉正文的 bug（无分隔线时 header 残留进正文；正文中的 Markdown 水平线被误认为分隔线）。

留给后续 issue 对齐的是需要产品决策的部分：P2-1（导航层重构）、P2-2（技能路径规范统一）、P2-6（语言地图）、阶段四（正式版替换）。

### 一条值得记下的自陷

为统一电话分隔符，我一开始把 `ー`(U+30FC) 全文替换成 `-`。新写的回归测试立刻报错：「承認フロー」变成了「承認フロ-」——该字符兼作长音符。改为只在数字之间的分隔位置允许。**正规化不设计作用范围，就会从一个事故变成另一个事故**；这也正好说明为什么 `CLAUDE.md` 那条「改脱敏必须先有测试」的规矩值得当作硬约束。已记入 `PITFALLS.md` 13。
