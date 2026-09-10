---
name: weekly-check
description: 每周五周度Check。用reviewer agent评分，产出红黄绿结论和提交给Team Lead的周报块。
---
# weekly-check

1. 收集本周证据: logs/daily.md 本周行、outcomes/outcomes.jsonl 本周条目、成员补充的产出链接。
2. 用 reviewer agent 的规则评分（与coach分离，不许自评）: 计划目标/证据完整度/质量/复现性/风险/下周动作 各0-5分 + 红黄绿。任一核心项≤2分或无证据链接=Red。
3. 指出最影响交付的一个问题（禁止只鼓励）。
4. 写入 logs/weekly/W{NN}.md，并输出一段「提交用周报块」（角色/周次/各项评分/颜色/主要偏差/下周动作/需要经理决策事项），让成员复制提交给Team Lead。
