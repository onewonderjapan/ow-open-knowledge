# grok-feedback · 开发侧 → 专管 Bot 反馈轨

本目录位于分支 **`grok/feedback`**，是 `grok/knowledge` 的反向通道。

- **写入方**：开发 agent / 机主。专管 Bot **不写**本分支。
- **读取方**：专管 Bot。每次运行前 `git fetch origin grok/feedback`，读本目录全部条目，在下一条 GK 正文加 `## 对反馈的回应`，并按反馈更新旧 GK 条目的「状态」字段。
- **路径**：`grok-feedback/YYYY-MM-DD-<slug>.md`
- **条目 ID**：`GF-<仓短名大写>-YYYYMMDD-NN`
- **不进 `main`**：本分支与 `grok/knowledge` 一样，都是协作轨，不是仓库正本。

条目头字段：条目 ID / 仓 / 针对 GK / 写入方 / 状态裁定（对每条 GK：已采纳 | 已拒绝 | 部分采纳 | 待验证）。
