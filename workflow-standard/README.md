# workflow-standard — Automation Workflow Building Standard

What does a production-worthy automation workflow look like, where does it live, how does it run, and how does it improve itself? This standard answers that: workflows run as **Skill + scheduled task (cron)**, follow a **four-phase loop** (ingest → decide → evaluate → improve), and persist all learning as state files in the repo.

> **Where this sits.** This directory is the recurring-job standard (cron + skill + append-only state). Cultivation methodology: [agent-cultivation](../agent-cultivation/). One-off natural-language tasks with a plan-approval gate: [task-orchestrator](../task-orchestrator/). Requirement-to-code automation: [dev-pipeline](../dev-pipeline/). The human confirmation gate in [STANDARD.md](STANDARD.md) P4 is about irreversible / external side effects; it is not task-orchestrator's plan-approval step or the Human/Hybrid executor in [dev-pipeline/USAGE.md](../dev-pipeline/USAGE.md).

It applies to any recurring, automated, feedback-looped job: financial analysis & paper trading, routine content generation, data inspections, report aggregation, and so on.

## Contents

| Path | What it is |
|------|------------|
| [STANDARD.md](STANDARD.md) | **The core standard (read first).** 7 iron rules, the four-phase lifecycle, directory conventions, and a launch checklist |
| [template/](template/) | Scaffold for a new workflow (SKILL.md + config.yml + steps/ + state/) |

## Create a workflow

```bash
cp -r template workflows/<name>
ln -s ../../workflows/<name> .claude/skills/<name>   # Claude Code
# ln -s ../../workflows/<name> .agents/skills/<name>  # Codex-style
# edit workflows/<name>/SKILL.md and state/, then dry-run it: /<name>
```

The template's `SKILL.md` ships with placeholder frontmatter (`CHANGE-ME-workflow-name`). Fill `name` and `description` before using it — loaders ignore a skill that has no YAML frontmatter.

See STANDARD.md §11 for the launch checklist.

## Directory layout

```text
workflow-standard/
├── STANDARD.md        # the core standard
├── README.md
└── template/          # scaffold for new workflows
    ├── SKILL.md
    ├── config.yml
    ├── steps/         # 1-ingest → 2-decide → 3-evaluate → 4-improve
    └── state/         # externalized state: ledger / scorecard / strategy
```

## The 7 iron rules at a glance

Idempotent & replayable · externalized state · append-only ledgers · human confirmation gates · observable runs · small self-improvements · simulation first (details in [STANDARD.md](STANDARD.md) §1)
