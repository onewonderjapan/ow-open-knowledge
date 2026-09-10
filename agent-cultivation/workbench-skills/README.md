# workbench-skills — Personal Workbench Skill Set

A set of skills for Claude Code-style tools that turn the daily rhythm of a "90-day personal agent training program" into fixed rituals: starting the day, logging outcomes, weekly reviews, and retrospectives — so the discipline doesn't depend on willpower.

## Contents

| Skill | Purpose |
|-------|---------|
| `daily-start` | Start of day: generate today's plan (≤3 learning items + delivery steps + acceptance criteria) and append a log line |
| `log-outcome` | Log a task outcome into the ledger in the same session ("later" counts as not done) |
| `pre-task` | Pre-flight check before risky tasks |
| `weekly-check` | Friday review: score the week on plan goals / evidence completeness / quality / reproducibility / risk, emit a weekly report block |
| `retro` | Gate-week retrospective: capture pitfalls and winning patterns for the phase |
| `_agents/coach.md` | The coach agent these skills rely on (breaks down tasks, ties advice to deliverables, never grades — grading belongs to a separate reviewer) |

## Usage

Copy the skill folders into your workbench's `.claude/skills/`, and the coach into `.claude/agents/`:

```bash
cp -r workbench-skills/<skill-name>            <your-workbench>/.claude/skills/
cp workbench-skills/_agents/coach.md  <your-workbench>/.claude/agents/coach.md
```

Then invoke them in a workbench session as `/daily-start`, `/weekly-check`, etc.

## Notes

- The skills enforce "evidence-first": a task without clickable/runnable evidence is not done.
- Sample task cards, logs, and outcome ledgers are personal working data and are not part of this public repo.
- The methodology behind them: [AGENT育成標準](../AGENT育成標準.md) and [data-classification](../data-classification.md).
