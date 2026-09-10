---
name: daily-start
description: 每日开工。生成今日计划（学习≤3条+产出步骤+验收标准），并在logs/daily.md追加一行日志。
---
# daily-start

以 coach agent 的规则执行（.claude/agents/coach.md）:
1. 先读 tasks/ 下当前周任务卡 与 logs/daily.md 最后3行（昨日衔接）。
2. 向成员确认（最多5问）: 今天可投入时间、当前任务进度、阻塞项。
3. 输出Markdown表: 学习(≤3条)｜确认｜执行步骤｜检查｜风险｜验收标准/证据形式，外加「明日衔接动作」。
4. 在 logs/daily.md 追加一行: `YYYY-MM-DD | 任务 | 今日计划要点 | 阻塞(无则-)`。
5. 缺数据权限/代码权限/Owner/验收标准 → 列为Blocker并提示升级Team Lead。
