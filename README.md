# ow-open-knowledge

OneWonder Japan's public knowledge base: battle-tested methodology for growing AI agents, a minimal viable architecture for enterprise AI adoption, automation workflow standards, a multi-agent development pipeline, cloud patterns, and team norms — all distilled from internal production work.

English | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

![License](https://img.shields.io/badge/license-MIT-blue)

## What this repo is / isn't

**Is:** a set of working methods validated on real business lines — how to cultivate AI agents, how to build closed-loop automation workflows, what a minimal enterprise-AI pipeline looks like. Reference code runs as-is.

**Isn't:** a client case study or a product codebase. No client information, internal strategy, or unpublished IP; all demo data is fictional.

**Languages:** READMEs are in English. The underlying documents keep their original wording — Japanese, Chinese, or a Japanese–Chinese mix — exactly as the team writes them (task-orchestrator is English). Translating the core methodology documents is welcome future work. The Contents table marks the language of each directory so you know before you click.

## Start here

This repo is a kit, not a single product. Four directories describe how to run agents; they overlap on purpose and are not interchangeable.

| If you want to… | Start here |
|-----------------|------------|
| Learn how the team grows an agent (principles, training, data classification) | [agent-cultivation/](agent-cultivation/) |
| Build a recurring cron workflow that improves itself | [workflow-standard/](workflow-standard/) |
| Route a one-off natural-language task: discover skills, approve a plan, then execute | [task-orchestrator/](task-orchestrator/) |
| Turn a written requirement into code with a 6-agent pipeline | [dev-pipeline/](dev-pipeline/) |
| Send a business document to an LLM without leaking names or phone numbers | [ai-stack/](ai-stack/) |
| Reuse a distilled AWS/cloud flow (or its don't-do list) | [cloud-patterns/](cloud-patterns/) |
| Look up Git / Teams / email conventions | [team-norms/](team-norms/) |

### The same idea, three places

These concepts appear in more than one system. Read the copy that matches the job you are doing; they are not one shared implementation.

| Concept | Where it is defined | What that copy is for |
|---------|---------------------|------------------------|
| Human approval gate | [task-orchestrator/SKILL.md](task-orchestrator/SKILL.md) (plan approval before any mutation); [workflow-standard/STANDARD.md](workflow-standard/STANDARD.md) P4 (irreversible / external side effects); [dev-pipeline/USAGE.md](dev-pipeline/USAGE.md) (Human / Hybrid executor) | Task start vs. live side effects vs. who implements a subtask |
| Learning consolidation | [AGENT育成標準.md](agent-cultivation/AGENT育成標準.md) three layers (code / skill / memory); [learning-policy.md](task-orchestrator/references/learning-policy.md) (project / personal / none); [dev-pipeline `agents/memory/`](dev-pipeline/README.md) | Cultivation standard vs. post-task rule routing vs. per-agent run memory |
| Experience log | [PITFALLS.md](agent-cultivation/PITFALLS.md); workflow `state/` append-only ledger; task-orchestrator run `learning.md` | Human-written pitfalls vs. workflow replay log vs. per-run learning notes |

### Skill install paths

Published skills in this repo live next to their docs (`cloud-patterns/skills/`, `agent-cultivation/workbench-skills/`, …). Agent runtimes look in **two** conventional trees:

| Runtime | Project skills | User skills |
|---------|----------------|-------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex-style | `.agents/skills/` | `~/.agents/skills/` |

`task-orchestrator` documents itself as usable in both, and `scripts/scan_skills.py` searches both. A default scan of *this* repository still finds nothing, because the published skills are source packages — they are not installed under `.claude/` or `.agents/`. To catalog them:

```bash
python3 task-orchestrator/scripts/scan_skills.py --cwd . --pretty \
  --root project=cloud-patterns/skills \
  --root project=agent-cultivation/workbench-skills \
  --root project=task-orchestrator \
  --root project=workflow-standard/template
```

Copy a skill folder into `.claude/skills/` or `.agents/skills/` in *your* project to install it. Every `SKILL.md` needs YAML frontmatter (`name` + `description`) or loaders ignore it — `scripts/check_skills.py` guards that.

## Contents

| Directory | What's inside | Language |
|-----------|---------------|----------|
| ⭐ [agent-cultivation/](agent-cultivation/) | **The core asset.** Agent Cultivation Standard (5 principles + three-layer consolidation), training guide for existing agents, new-project startup standard, data classification rules, and a personal workbench skill set | JA / ZH (mixed) |
| [ai-stack/](ai-stack/) | Enterprise AI adoption reference implementation: requirement doc → masking → in-house precedent search (RAG) → LLM drafting → local verification, end to end | JA (READMEs EN + JA) |
| [workflow-standard/](workflow-standard/) | Automation workflow building standard: four-phase loop + 7 iron rules + a scaffold for new workflows | ZH |
| [task-orchestrator/](task-orchestrator/) | A master skill for natural-language tasks: skill routing → plan approval → sustained execution → layered learning (standard library only) | EN |
| [dev-pipeline/](dev-pipeline/) | A 6-agent development pipeline: Dispatcher / Investigator / Analyst / Developer / Reviewer / Tester with self-learning | JA (READMEs EN + JA) |
| [cloud-patterns/](cloud-patterns/) | Cloud architecture skills: Glue×RDS merge, API Gateway + Lambda + SES contact form, Form→IAM, Terraform pitfalls | ZH |
| [team-norms/](team-norms/) | Team norms: Git conventions, Teams chat manners, business email basics | JA |

## Quick start

The fastest way to see the whole idea — ai-stack's offline demo (no API key needed; verified end-to-end):

```bash
cd ai-stack
python -m venv .venv
# Windows (Git Bash / PowerShell):
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub
# macOS / Linux:
# source .venv/bin/activate && pip install -r requirements.txt
# python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub
```

Output: the masked content actually sent out (`out/*_masked.md`), a design-doc draft (`out/*_draft.md`), and an audit report (`out/*_report.json`).

A demo web UI is also included:

```bash
python ui/app.py    # → http://127.0.0.1:7877
```

> Dependencies: the HTTP layer of the web UI is standard-library only, but it reuses the RAG layer, so it needs `janome` just like the pipeline — which needs it even in stub mode. `anthropic` is only required for the API provider, and `python-pptx` only for `tools/`. Python 3.10+.

## Related public repos

- [form2cloudbuilder](https://github.com/onewonderjapan/form2cloudbuilder) — create AWS/Azure resources from a Microsoft Form entry
- [wonder-contact-terraform](https://github.com/onewonderjapan/wonder-contact-terraform) — homepage contact form infrastructure (Terraform)
- [rds-glue-s3-etl-pipeline](https://github.com/onewonderjapan/rds-glue-s3-etl-pipeline) — AWS Glue (PySpark) ETL: merge S3 JSON with RDS, Secrets Manager credentials, Slack notifications
- [owd-knowledge-hub](https://github.com/onewonderjapan/owd-knowledge-hub) — organization knowledge portal

## Contributing

Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for the inclusion
boundary (what may and may not go into this repo), and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

Run the tests before opening a PR:

```bash
python -m pip install janome                                                  # ai-stack RAG layer
python -m unittest discover -s ai-stack/tests -t ai-stack/tests               # masking + prompt assembly
python -m unittest discover -s dev-pipeline/tests -t dev-pipeline/tests       # workspace boundary + parser
python -m unittest discover -s task-orchestrator/tests -t task-orchestrator/tests
python scripts/check_links.py                                                 # relative markdown links
python scripts/check_skills.py                                                # SKILL.md frontmatter
```

CI runs the same checks plus the offline demo on every PR.

**Masking is a security control.** `ai-stack/masking/` decides what is allowed to
leave the building, so a rule change without a regression test is how leaks ship —
see [ai-stack/CLAUDE.md](ai-stack/CLAUDE.md).

## Security

Found a masking bypass, unmasked data reaching an LLM, or arbitrary file access driven
by model output? Please report it privately — see [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
