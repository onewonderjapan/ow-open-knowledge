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
5. **改脱敏层必须补回归测试**。`ai-stack/masking/` 决定什么可以离开内网，属于安全控制；
   规则改了没测试就是漏出事故（见 `ai-stack/CLAUDE.md`）。测试加在
   `ai-stack/tests/test_masker.py`，并确认改动前失败、改动后通过。
6. 踩到的坑追记到 `agent-cultivation/PITFALLS.md`——这本身就是仓库的资产。

## 本地验证

```bash
python -m pip install janome                                                  # ai-stack RAG 层
python -m unittest discover -s ai-stack/tests -t ai-stack/tests
python -m unittest discover -s dev-pipeline/tests -t dev-pipeline/tests
python -m unittest discover -s task-orchestrator/tests -t task-orchestrator/tests
python -m unittest discover -s workflow-standard/tests -t workflow-standard/tests
python scripts/check_links.py
python scripts/check_skills.py
python -m unittest discover -s scripts -t scripts -p "test_*.py"

# 离线端到端 demo（无需 API key）
cd ai-stack && python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub
```

CI 在每个 PR 上跑同样的检查。

## 安全问题不要开公开 issue

脱敏绕过、未脱敏数据进入 LLM、模型输出驱动的任意文件读写——请按 [SECURITY.md](SECURITY.md)
私下上报。

## 文档约定

- 每份文档一个 H1 标题，开头一行说明「这是什么」。
- 代码块标注语言；表格保证列数对齐。
- 引用仓内文件用相对链接。

## License

提交即表示你同意以 [MIT](LICENSE) 许可证发布你的贡献。
