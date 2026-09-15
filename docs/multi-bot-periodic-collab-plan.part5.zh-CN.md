# 多 Bot 定期协作计划 · 第 5 分册（附录与 §8/§9）

## 附录 D · 脱敏清单与三件套

抽查时逐项打勾。任一项未处理且目标为外发/公开 → 退回。

- [ ] 客户公司法定名、可反查的项目暗号 → 代号或删除
- [ ] 人名、电话、邮箱、账号、工号、住址
- [ ] 密钥、token、口令、cookie、内网 URL、机器名、IP
- [ ] 合同金额、未公开报价、未发表 IP / 未上线产品名
- [ ] L3 原文句子不得出现在 `-out.md`、open-knowledge、daily-intel、就绪外发稿
- [ ] `-map.md` 只写「字段类型 → 策略」，不写可复制明文秘密
- [ ] 对照 `ow-open-knowledge/agent-cultivation/data-classification.md`
- [ ] 头字段含：RED-ID、源 path、分级、执行者、抽查者、抽查结果

`-src.md` 不得进入 outbound-queue 或公开仓。

## 附录 E · 晋升申请格式

```markdown
# 晋升申请 · PRM-YYYYMMDD-NN

- 源 AN：AN-…
- 源整理/INV：
- 分级：L1 / L2 / L3
- 脱敏 RED：RED-…（L1 公开或外发必填；抽查=通过）
- 目标仓/path：（必须是已核实允许清单）
- 申请 Bot：
- 审批人：（拍板 #4 未决则填「未指定」并停止 merge）
- 是否触及附录 B 确认门：是/否 → 若是，机主批示：

## 拟写入摘要
## 仍需人工确认
## 审批
- 结果：待批 | 通过 | 拒绝
- 日期：
- 合入引用：（通过后填；拒绝则写回待验证/丢弃）
```

## 附录 F · 排程登记与告警格式

**排程登记一行一例**（与 §3 对齐，改表须改此登记草稿）：

```text
研究爆款的 | 热点速报 | 08:30 | 工作日 | investigations/YYYY-MM-DD-hotspot-*.md 或空窗 | 有 INV 或空窗 | 30min | 允许空窗（无热点）
neng社交的 | 外发窗2 | 16:00 | 工作日 | outbound-queue 就绪发出 或 空窗 | 有发出记录或空窗 | 30min | 允许空窗（无就绪队列）
管仓库的 | 孤儿审计 | 11:00 | 周日 | audits/YYYY-MM-DD-repo-orphan.md | 非空报告 | 30min | 不允许空窗
```

**告警文件**：

```markdown
# ALT-YYYYMMDD-NN

- 时间（意图时刻 + 宽限后）：
- Bot / 任务：
- 失败类型：未交卷 | 缺必填 | 禁止路径 | 脱敏退回 | 未授权 live | 日向未扫失败 | 其他
- 已影响 path：
- 是否触及确认门：是/否
- 建议动作：
- 状态：open | closed
- 补交 path / 关闭原因：
```

---

## 8. 仓专管 Bot · Grok 专用分支（机主新增硬规则 · 2026-09-11）

> 本条为机主新增运营硬规则。落实细节（哪些仓算「进行中」、分支名、节奏、谁建 Bot）进「需要拍板」；**不**静默替机主选定。

### 8.1 规则原文精神

1. **每一个正在进行中的仓库**，必须有一个**专门的 Bot** 管理该仓。
2. 该专管 Bot **都能**调取本地 Grok Build CLI 的 **`grok-4.6` / effort `xhigh`**，定期为该仓**输送知识与建议**。
3. 知识与建议只落到该仓的 **Grok 专用分支**（不得默认直推 `main`）。
4. **负责开发的 agent** 定期阅读该 Grok 分支上由 Grok 推送的知识与建议，再决定是否吸收进开发分支 / `main`（吸收须走既有确认门与晋升门，见 §4.7 / 附录 B）。

### 8.2 操作化（逻辑约定；物理细节待拍板）

| 项 | 约定 |
|---|---|
| 专管关系 | 1 进行中仓 → 1 专管 Bot（可与 §3 角色表中的现有 Bot **兼任**，但兼任须在登记表写明；新建 Bot 名须拍板） |
| 模型 | 本地 CLI：`grok`，`-m grok-4.6 --reasoning-effort xhigh` |
| 写入分支 | Grok 专用分支（建议名见拍板 #14，例如 `grok/knowledge`）；**禁止**专管 Bot 因本规则直接 push `main` |
| 写入内容 | 仅「知识 / 建议」类 markdown（或仓内既有 docs 约定下的等价物）；默认路径建议：`grok-inbox/YYYY-MM-DD-<slug>.md`（相对仓库根；若仓已有 docs 习惯则对齐，拍板 #15） |
| 开发 agent 读法 | 定期 `fetch` 该 Grok 分支；只把 inbox 中条目当作**建议输入**，不视为已合并事实 |
| 与共通规则关系 | 仓专管产出若含外部/未验证知识 → 仍须走分析门（§4.4）与脱敏（§4.6）后，才能谈晋升；社交外发仍仅 neng社交的 |

**建议文件头（Grok inbox 条目）**：

```markdown
# Grok 建议 · YYYY-MM-DD · <标题>

- 条目 ID：GK-YYYYMMDD-<序号>
- 仓：<owner/repo>
- 分支：<grok-dedicated-branch>
- 模型：grok-4.6 / xhigh
- 专管 Bot：<名称>
- 类：知识 | 建议 | 风险提醒
- 机密分级：L1 / L2 / L3
- 状态：待开发阅读 | 已采纳 | 已拒绝 | 待验证

## 摘要
## 依据（可核对引用 / 未核实假设须标明）
## 建议开发 agent 采取的下一步
## 明确不要做什么
```

### 8.3 「进行中」仓库候选（来自 §2 活跃/半活跃轨；最终名单拍板 #16）

**默认纳入候选（须拍板确认）**：`ow-open-knowledge`、`owd-knowledge-hub`、`owd-daily-intel`、`owd-pet-content-studio`、`owd-lingwan`、`owd-eys`、`onewonder-homepage`、`ow-archive-skills`、`skill-platform`、`ai-ops`、`ow-ai-hq`、`ow-ai-stack`、`ai-knowledge-local`、`ai-workflow-hub`、`build-workflow`、`wonder4ge-flow`、`pet-universe`、`pet-drama-studio`、`ark-harness`、`task-orchestrator`、`lora-demo-suite`。

**默认不纳入（除非拍板拉入）**：§2.4 低活跃/演示、已归档仓、纯救援冻结仓。

### 8.4 节奏建议（意图；Owner 仍拍板 #9）

- 专管 Bot：每个进行中仓 **每周至少 1 次** Grok 输送（可错开星期，避免全仓同日打满）。
- 开发 agent：对应仓 **每周至少 1 次** 阅读该仓 Grok 分支 inbox，并回写条目状态（已采纳 / 已拒绝 / 待验证）。

### 8.5 与现有 Bot 的关系（不改名；兼任须登记）

现有角色 Bot（秘书、管仓库的、研究爆款的等）**可以**兼任某一仓专管，但必须在「仓→专管 Bot」登记表写死；未登记的仓视为缺口（管理类周审计须报）。新建「一仓一 Bot」名字空间须机主拍板后才能批量创建。

---

## 9. 已锁定拍板（机主 · 2026-09-11）

| 编号 | 选择 | 含义 |
|---|---|---|
| 14 | **A** | Grok 专用分支统一为 `grok/knowledge` |
| 15 | **A** | 输送路径统一为 `grok-inbox/YYYY-MM-DD-<slug>.md`（另有 `grok-inbox/README.md`） |
| 16 | **B** | 本轮只覆盖 §2.1 近 1–2 周活跃轨 |
| 17 | **C** | 分支与专管 Bot 一起建 |

### 9.1 本轮活跃轨仓 ↔ 专管 Bot 登记

| 仓库 | 专管 Bot | 分支 | inbox |
|---|---|---|---|
| `ow-open-knowledge` | 管公开知识仓的 | `grok/knowledge` | `grok-inbox/` |
| `owd-knowledge-hub` | 管知识中枢的 | `grok/knowledge` | `grok-inbox/` |
| `owd-daily-intel` | 管每日情报的 | `grok/knowledge` | `grok-inbox/` |
| `owd-pet-content-studio` | 管宠物内容仓的 | `grok/knowledge` | `grok-inbox/` |
| `owd-lingwan` | 管铃湾仓的 | `grok/knowledge` | `grok-inbox/` |
| `owd-eys` | 管鹅鸭仓的 | `grok/knowledge` | `grok-inbox/` |
| `onewonder-homepage` | 管官网仓的 | `grok/knowledge` | `grok-inbox/` |
| `ow-archive-skills` | 管归档skills的 | `grok/knowledge` | `grok-inbox/` |
| `skill-platform` | 管skill平台的 | `grok/knowledge` | `grok-inbox/` |
| `ai-ops` | 管ai-ops的 | `grok/knowledge` | `grok-inbox/` |

> 半活跃/低活跃仓本轮不建。后续扩容须再拍板。

---

## 修订说明

本次（2026-09-11）对草案的完善，不重跑仓库调研、不改五条规则、不删拍板 1–10：

11. 新增 §8：每进行中仓专管 Bot + 本地 grok-4.6 xhigh 定期向 Grok 专用分支输送知识/建议；开发 agent 只定期阅读该分支。拍板追加 #14–#17。
1. 增加 §1.4 / §2.7：用 `{OPS_ROOT}` `{ISOLATION_ROOT}` 逻辑路径把「格式可执行」与「物理仓未拍板」拆开；未拍板前运行默认改为停写未定仓，而不是把建议 path 写死成已存在目录。
2. 去掉内矛盾：撤销「N 默认 14」（等于抢先选拍板 #5A）；撤销审计报告正文写死挂 `ai-ops`；调查正本与 `owd-daily-intel` 今日份改为「一行指针」，禁止全文冒充已入库。
3. 去掉时序重叠：周五爆款周复盘 16:00→15:00；分析窗改为 16:30–17:30；秘书周闭环改为周五 17:40；周日秘书抽查改为 12:00（晚于 11:00 审计）。并写明 16:00 第二外发窗空窗不算失败。
4. 补 §4.6 脱敏可操作步骤（打标 → 三件套 → 第二人抽查 → 通过/退回）及附录 D 清单；执行者仍拍板 #7，未决前停在待脱敏。
5. 补 §4.7 晋升门硬条件与附录 E 申请格式；审批人仍拍板 #4，未决前不得 merge；L3 禁止公开晋升。
6. 补 §4.8 排程值守与失败告警（30 分钟宽限、空窗规则、ALT 文件、升级时钟）；Owner 仍拍板 #9，外部通道仍拍板 #13。
7. 角色表落点全部改为逻辑路径；内容仓子目录标未核实；skill-platform 空描述、FDE 404、脱敏管线可用性保持未核实。
8. §5 区分「步骤已覆盖」与「政策未拍板」；周/日抽查清单补晋升、脱敏、ALT 项。
9. 拍板 1–10 与 A/B/C 原文保留，仅加「本修订注」；追加 #11 时区、#12 分析门发起 Bot、#13 告警通道。
10. §7 增补：不把逻辑路径当 Git 实目录、不把未决项写成已决默认、不自动补发对外内容。

---

*起草：多 Bot 协作调研执行 · 2026-09-11 · 分支 `plan/multi-bot-periodic-collab`*
*修订：同日完善操作化步骤与去矛盾 · 仍为草案 · 未合并*
