---
name: log-outcome
description: 任务出结果后立即回填结果库（成功也记）。同session回填是工程义务，「以后补」=违规。
---
# log-outcome

1. 向成员确认: 任务、结果(pass/fail/partial)、证据链接(PR/文档/截图路径)、失败模式(若fail)。
2. 追加一行JSON到 outcomes/outcomes.jsonl:
   {"date":"YYYY-MM-DD","week":"W01","task":"...","result":"pass|fail|partial","failure_mode":"...或null","evidence":"...","note":"..."}
3. 若fail: 问「是新坑吗？」→ 是则在 PITFALLS.md 追加（症状/根因/解法）；同一失败第2次出现 → 提示发动训练session（一次只改一处+回归验证）。
4. 若显著成功: 问「值得进金牌库吗？」→ 是则在 gold/ 存带注释范例（为什么好，用手法名注释）。
