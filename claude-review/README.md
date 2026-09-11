# claude-review · Claude 对仓内容的 review 建议轨

本目录位于分支 **`claude/review`**，存放 Claude（开发侧）对**仓库内容本身**（代码 / 文档 / 结构）的 review 建议。

- **写入方**：Claude，受机主指示运行。
- **读取方**：开发 agent / 机主。专管 Grok Bot 也可读，作为选题参考。
- **路径**：`claude-review/YYYY-MM-DD-<slug>.md`
- **条目 ID**：`CR-<仓短名大写>-YYYYMMDD-NN`
- **不进 `main`**：本分支是建议轨，不是仓库正本。采纳的项走正常 PR → `main`，PR 描述引用 CR 条目 ID。
- 与 `grok/knowledge`（Bot 建议）、`grok/feedback`（对 Bot 的反馈）并列，三者互不合并。
