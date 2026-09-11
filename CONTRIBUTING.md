# 贡献指南

欢迎 issue 与 PR。本仓收录的是 OneWonder 从内部实战中蒸馏出来的方法论、标准与参考实现，贡献前请先了解收录边界。

## 收录边界（先读这个）

- 只收**可公开**的知识：方法论、标准文档、可运行参考实现、模板。
- **禁止**进入本仓的内容：客户名/真实人名/内部项目代号、密钥与凭据、内部经营战略、未发表的 IP 设定、运行数据。
- 判断不了按更高一级处理：先脱敏再提交，或开 issue 讨论。

## 怎么贡献

1. 大改动先开 issue 对齐方向，小改动可直接 PR。
2. 保持各文档原有语言：日文文档用日文修改，中文文档用中文修改，不做翻译式重写。
3. 代码改动需附可运行的验证命令与输出（证据主义）。
4. 每个 PR 聚焦一件事，保持最小可审。

## 文档约定

- 每份文档一个 H1 标题，开头一行说明「这是什么」。
- 代码块标注语言；表格保证列数对齐。
- 引用仓内文件用相对链接。

## License

提交即表示你同意以 [MIT](LICENSE) 许可证发布你的贡献。


## Bot 协作轨（2026-09-11 起）

本仓有三条协作分支。它们都**不是仓库正本**，不合并进 `main`，只作为建议与反馈的输送通道：

| 分支 | 目录 | 写入方 | 读取方 | 用途 |
|---|---|---|---|---|
| `grok/knowledge` | `grok-inbox/` | 专管 Grok Bot | 开发 agent | Bot 定期推送的知识 / 建议 / 风险提醒（条目 `GK-<仓>-YYYYMMDD-NN`） |
| `grok/feedback` | `grok-feedback/` | 开发 agent / 机主 | 专管 Grok Bot | 对 GK 条目的采纳 / 拒绝 / 修正要求（条目 `GF-<仓>-YYYYMMDD-NN`） |
| `claude/review` | `claude-review/` | Claude（开发侧 review） | 开发 agent / 机主 | 对仓内容本身的 review 建议（条目 `CR-<仓>-YYYYMMDD-NN`） |

开发 agent 每次会话开始：

```bash
git fetch origin grok/knowledge grok/feedback claude/review
git show origin/grok/knowledge --stat --oneline   # 看最新 GK 条目
```

- 读 `grok-inbox/` 最新条目当**建议输入**，不当已生效规则。
- 对 GK 的裁定写进 `grok/feedback`，**不直接写 `grok/knowledge`**（那是 Bot 专属写入分支）。
- 要落地的改动走正常 PR → `main`，PR 描述引用对应 GK / CR 条目 ID。
- 专管 Bot 只写 `grok/knowledge`，运行前读 `grok/feedback`；禁止 push `main`。
