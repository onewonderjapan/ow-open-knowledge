# workflow-standard — Automation Workflow Building Standard

What does a production-worthy automation workflow look like, where does it live, how does it run, and how does it improve itself? This standard answers that: workflows run as **Skill + scheduled task (cron)**, follow a **four-phase loop** (ingest → decide → evaluate → improve), and persist all learning as state files in the repo.

It applies to any recurring, automated, feedback-looped job: financial analysis & paper trading, routine content generation, data inspections, report aggregation, and so on.

## Contents

| Path | What it is |
|------|------------|
| [STANDARD.md](STANDARD.md) | **The core standard (read first).** 7 iron rules, the four-phase lifecycle, directory conventions, and a launch checklist |
| [template/](template/) | Scaffold for a new workflow (SKILL.md + config.yml + steps/ + state/) |

## Create a workflow

```bash
cp -r template workflows/<name>
ln -s ../../workflows/<name> .claude/skills/<name>   # expose as a Skill
# edit workflows/<name>/SKILL.md and state/, then dry-run it: /<name>
```

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
