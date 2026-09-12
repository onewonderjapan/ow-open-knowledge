# dev-pipeline — AI-Driven Development Pipeline

Six AI agents cooperate to run **requirement classification → investigation → analysis → implementation → review → testing → issue investigation** automatically. Every agent self-learns after each run — the pipeline gets smarter the more you use it.

> **Where this sits.** This directory is the requirement-to-code pipeline. Cultivation methodology: [agent-cultivation](../agent-cultivation/). Recurring cron workflows: [workflow-standard](../workflow-standard/). One-off natural-language tasks with a plan-approval gate: [task-orchestrator](../task-orchestrator/). The Human / Hybrid executor in [USAGE.md](USAGE.md) decides who implements a subtask; it is not task-orchestrator's plan-approval step or the live-side-effect gate in [workflow-standard/STANDARD.md](../workflow-standard/STANDARD.md) P4. Per-agent files in `agents/memory/` are run memory, not the three-layer consolidation in [AGENT育成標準.md](../agent-cultivation/AGENT育成標準.md).

[English](README.md) | [日本語](README.ja.md)

![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue)

## Overview

Feed in a requirement file; the Dispatcher classifies it and picks the right pipeline:

```text
Requirement ──→ [Dispatcher] ──→ pipeline selection
                     │
                     ├─ feature dev     ──→ all 6 phases
                     ├─ infrastructure  ──→ all 6 phases (design-doc centric)
                     ├─ investigation   ──→ Investigator only
                     └─ design review   ──→ Analyst + Developer

Full pipeline (6 phases):
[Investigator] → [Analyst] → [Developer] → [Reviewer] → [Tester] → [Investigator]
 investigation   analysis   implementation review    testing    issue analysis
                       ↓ each agent self-learns after its run ↓
                            agents/memory/<name>.md
```

## The six agents

| Agent | Command | Role | Output |
|-------|---------|------|--------|
| **Dispatcher** | (automatic) | classify the requirement, pick the pipeline | `dispatcher/dispatch.json` |
| **Investigator** | `--investigate` | codebase investigation / tech research | `investigator/investigation.md` |
| **Analyst** | `--analyze` | requirement analysis, task split, executor decision (AI/Human/Hybrid) | `analyst/analysis.md` |
| **Developer** | `--develop` | generate code & docs per subtask | `developer/development.md` |
| **Reviewer** | (automatic) | quality checks, cross-system review, fix instructions | `reviewer/review.md` |
| **Tester** | `--test` | functional tests + security vulnerability scan | `tester/test_report.md` |

The **Reviewer** verifies Developer output automatically (empty/truncated files, requirement coverage, and cross-system gaps like DNS/firewall/auth/monitoring), and on failure loops one fix round back to Developer.

## Usage

```bash
# Full pipeline (Dispatcher auto-classifies → runs the right pipeline)
python main.py -f task.md

# Single agents
python main.py --investigate -f research.md   # Investigator only
python main.py --analyze -f task.md           # Analyst only
python main.py --develop -f task.md           # Analyst → Developer
python main.py --test -f task.md              # Analyst → Developer → Tester

# Self-evolution (learning & optimization)
python main.py --memory        # show all agent memories
python main.py --consolidate   # dedupe & compress memories
python main.py --optimize      # self-optimize every agent's prompt
```

## Requirement file format

Place the file in a `requirements/` folder (create it if it doesn't exist — `workspace/` and `output/` are created automatically on first run):

```markdown
branch: feature/add-login
repo: https://github.com/user/project.git
---

Requirement body goes here...
```

`branch` (recommended for code work) and `repo` are optional; everything after `---` is the requirement body.

## Self-evolution system

```text
┌─ automatic (every run) ──────────────────────┐
│ run → reflect → extract lessons → memory/    │
└──────────────────────────────────────────────┘
         ↓ --optimize (manual)
┌─ self-optimization ──────────────────────────┐
│ analyze lessons → improve prompt → prompts/  │
└──────────────────────────────────────────────┘
         ↓
  evolved prompts are applied automatically next run
```

## Requirements

- Python 3.9+ (standard library only — no third-party packages)
- Git
- Claude Code CLI (Claude subscription; no `ANTHROPIC_API_KEY` needed)

## Tests

```bash
python -m unittest discover -s tests -t tests
```

## Directory layout

```text
dev-pipeline/
├── main.py              # CLI entry point
├── core/                # config, shared models, orchestrator, requirement parser
├── agents/              # 6 agents + base class (CLI + self-learning)
│   ├── memory/          # per-agent learning records (auto-accumulated, gitignored)
│   └── prompts/         # evolved prompts (--optimize, gitignored)
├── tests/               # unit tests (standard library only)
├── requirements/        # requirement files (gitignored except example.md)
│   └── example.md       # committed example — copy this to start
├── workspace/           # code output, one folder per requirement (gitignored)
└── output/              # report output, one folder per requirement (gitignored)
```

`memory/`, `prompts/`, `workspace/` and `output/` are created at runtime and are not
part of the repository.

Detailed walkthrough: [USAGE.md](USAGE.md) (Japanese; note that CLI messages are in Japanese too). The original Japanese README: [README.ja.md](README.ja.md).

## License

MIT — see [../LICENSE](../LICENSE).
