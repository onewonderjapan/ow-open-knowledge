# task-orchestrator

A single skill that turns a natural-language task into a disciplined execution loop:
**discover relevant skills → clarify material gaps → require plan approval → execute through delivery → learn at the narrowest durable scope.**

Works as a [Claude Code](https://claude.com/claude-code) skill or a Codex-style agent definition.

> **Where this sits.** This directory is the one-off natural-language loop (discover skills → approve a plan → execute → learn). Cultivation methodology: [agent-cultivation](../agent-cultivation/). Recurring cron workflows: [workflow-standard](../workflow-standard/). Requirement-to-code automation: [dev-pipeline](../dev-pipeline/). The plan-approval gate here is about not mutating anything before a plan is approved; it is not the live-side-effect gate in [workflow-standard/STANDARD.md](../workflow-standard/STANDARD.md) P4, nor the Human/Hybrid executor in [dev-pipeline/USAGE.md](../dev-pipeline/USAGE.md).

## Why

Ad-hoc agent sessions tend to skip clarification, act without an approved plan, and lose what was learned.
Task Orchestrator enforces the missing discipline: it never mutates anything before an explicit plan approval,
keeps task state persistent across interruptions, and routes durable rules to the right layer (project vs. personal).

## Usage

Scan the skills available in a target directory (run on every task, never reuse a prior catalog):

```bash
python3 scripts/scan_skills.py --cwd <target-directory> --pretty
```

Default discovery looks in **both** conventional trees, because this skill documents
itself as usable in both ecosystems:

| Runtime | Project skills | User skills |
|---------|----------------|-------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex-style | `.agents/skills/` | `~/.agents/skills/` |

Looking only in `.agents/skills` made a Claude Code user's skills invisible to the
very tool that is supposed to catalog them.

A default scan of *this* knowledge-base repository is empty on purpose: the
published skills (`cloud-patterns/skills/`, `agent-cultivation/workbench-skills/`,
this directory, `workflow-standard/template/`) are source packages, not an
installed `.claude/` or `.agents/` tree. Catalog them with `--root`:

```bash
python3 scripts/scan_skills.py --cwd .. --pretty \
  --root project=../cloud-patterns/skills \
  --root project=../agent-cultivation/workbench-skills \
  --root project=../task-orchestrator \
  --root project=../workflow-standard/template
```

Install as an agent skill by copying this directory into either skills path
(`.claude/skills/task-orchestrator/` or `.agents/skills/task-orchestrator/`),
then invoke it whenever a user submits a natural-language task that needs
routing, approval, delivery, or scoped learning.
`agents/openai.yaml` provides the equivalent interface metadata for OpenAI-style agent runtimes.

## Requirements

- Python 3.9+ (standard library only, no third-party dependencies)

## Tests

```bash
python3 tests/test_scan_skills.py
```

## Directory layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | The skill definition: workflow, state table, hard boundaries |
| `references/input-contract.md` | How to parse and clarify incoming tasks |
| `references/execution-contract.md` | Plan sections, authority and safety boundaries |
| `references/learning-policy.md` | How durable rules are routed by scope |
| `references/category-rules.yaml` | Current skill classification rules |
| `scripts/scan_skills.py` | Skill catalog scanner |
| `tests/test_scan_skills.py` | Scanner tests |

## License

MIT — see [LICENSE](../LICENSE) at the repository root.
