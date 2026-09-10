# task-orchestrator

A single skill that turns a natural-language task into a disciplined execution loop:
**discover relevant skills → clarify material gaps → require plan approval → execute through delivery → learn at the narrowest durable scope.**

Works as a [Claude Code](https://claude.com/claude-code) skill or a Codex-style agent definition.

## Why

Ad-hoc agent sessions tend to skip clarification, act without an approved plan, and lose what was learned.
Task Orchestrator enforces the missing discipline: it never mutates anything before an explicit plan approval,
keeps task state persistent across interruptions, and routes durable rules to the right layer (project vs. personal).

## Usage

Scan the skills available in a target directory (run on every task, never reuse a prior catalog):

```bash
python3 scripts/scan_skills.py --cwd <target-directory> --pretty
```

Install as an agent skill by copying this directory into your skills path
(e.g. `.claude/skills/task-orchestrator/`), then invoke it whenever a user submits a
natural-language task that needs routing, approval, delivery, or scoped learning.
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
