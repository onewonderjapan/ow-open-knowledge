# ow-open-knowledge

OneWonder Japan's public knowledge base: battle-tested methodology for growing AI agents, a minimal viable architecture for enterprise AI adoption, automation workflow standards, a multi-agent development pipeline, cloud patterns, and team norms — all distilled from internal production work.

English | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

![License](https://img.shields.io/badge/license-MIT-blue)

## What this repo is / isn't

**Is:** a set of working methods validated on real business lines — how to cultivate AI agents, how to build closed-loop automation workflows, what a minimal enterprise-AI pipeline looks like. Reference code runs as-is.

**Isn't:** a client case study or a product codebase. No client information, internal strategy, or unpublished IP; all demo data is fictional.

**Languages:** READMEs are in English. The underlying documents keep their original wording — Japanese, Chinese, or a Japanese–Chinese mix — exactly as the team writes them (task-orchestrator is English). Translating the core methodology documents is welcome future work.

## Contents

| Directory | What's inside |
|-----------|---------------|
| ⭐ [agent-cultivation/](agent-cultivation/) | **The core asset.** Agent Cultivation Standard (5 principles + three-layer consolidation), training guide for existing agents, new-project startup standard, data classification rules, and a personal workbench skill set |
| [ai-stack/](ai-stack/) | Enterprise AI adoption reference implementation: requirement doc → masking → in-house precedent search (RAG) → LLM drafting → local verification, end to end |
| [workflow-standard/](workflow-standard/) | Automation workflow building standard: four-phase loop + 7 iron rules + a scaffold for new workflows |
| [task-orchestrator/](task-orchestrator/) | A master skill for natural-language tasks: skill routing → plan approval → sustained execution → layered learning (standard library only) |
| [dev-pipeline/](dev-pipeline/) | A 6-agent development pipeline: Dispatcher / Investigator / Analyst / Developer / Reviewer / Tester with self-learning |
| [cloud-patterns/](cloud-patterns/) | Cloud architecture skills: Glue×RDS merge, API Gateway + Lambda + SES contact form, Form→IAM, Terraform pitfalls |
| [team-norms/](team-norms/) | Team norms (Japanese): Git conventions, Teams chat manners, business email basics |

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

Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
