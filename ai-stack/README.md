# ai-stack — Enterprise AI Adoption Reference Implementation (Thin Slice)

A minimal end-to-end implementation of the enterprise AI adoption flow:
**requirement document → masking → in-house precedent search (RAG) → cloud LLM drafting → local verification.**
Use it as the backbone for sales demos, internal dogfooding, or a client PoC.

[English](README.md) | [日本語](README.ja.md)

![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue)

## Quick start

Verified end-to-end — the stub provider needs no network and no API key:

```bash
python -m venv .venv
# Windows (Git Bash / PowerShell):
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub
# macOS / Linux:
# source .venv/bin/activate && pip install -r requirements.txt
# python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub

# Dependency-free demo web UI (standard library only):
python ui/app.py   # → http://127.0.0.1:7877
```

Output: `out/<name>_draft.md` (design-doc draft) / `out/<name>_masked.md` (what actually leaves the building) / `out/<name>_report.json` (audit trail).

> Dependencies: the pipeline needs `janome` (RAG layer) even with the stub provider. `anthropic` is only needed for the API provider. The web UI needs nothing.

## Providers

```bash
# Network-free demo (stub responses)
.venv/Scripts/python pipeline/run.py demo_data/incoming/new_rfp.md --provider stub

# Real Claude via a Claude Code subscription (no API key; PoC / internal use only)
.venv/Scripts/python pipeline/run.py demo_data/incoming/new_rfp.md --provider claude-cli

# Production-oriented (requires ANTHROPIC_API_KEY)
.venv/Scripts/python pipeline/run.py demo_data/incoming/new_rfp.md --provider anthropic-api
```

## Demo script (for stakeholders)

1. Open `demo_data/incoming/new_rfp.md` — a "raw" requirement with names, phone numbers, budget
2. Run the pipeline → show `out/new_rfp_masked.md`: **"this is all that reached the cloud"** (zero real names)
3. `out/new_rfp_draft.md` — a design-doc draft following the house format, referencing two past projects
4. `out/new_rfp_report.json` — the audit trail of who sent what and which checks ran

## Architecture and upgrade path

| Layer | Thin-slice implementation | Production-grade replacement |
|-------|---------------------------|------------------------------|
| `masking/` | regex + dictionary + patterns | + GiNZA (NER), legally reviewed rules |
| `rag/` | janome + BM25 | multilingual-e5 + Qdrant, permission filters |
| `llm/` | stub / claude-cli / anthropic-api | + AI gateway (LiteLLM) for multi-vendor |
| `evalkit/` | deterministic structure checks | + LLM-as-judge rubric scoring, regression suite |
| `pipeline/` | single CLI path | job queue, web UI |

Interfaces stay fixed, so each layer can be thickened independently.

## Directory layout

```text
ai-stack/
├── pipeline/run.py        # one-shot CLI: mask → RAG → draft → check
├── masking/               # masking layer (masker.py + entities.json)
├── rag/                   # precedent search (janome + BM25)
├── llm/                   # swappable providers (stub / claude-cli / anthropic-api)
├── evalkit/               # deterministic structure checks (structure_check.py)
├── ui/app.py              # zero-dependency demo web UI
├── tools/                 # markdown→pptx rendering, pptx extraction
├── demo_data/             # all-fictional demo data
└── templates/             # skeleton for new projects
```

The methodology behind this repo (cultivation standard, startup standard, pitfalls) lives in [../agent-cultivation/](../agent-cultivation/).

## Notes

- Everything in `demo_data/` is fictional companies, people, and projects.
- The `claude-cli` provider is PoC / internal use only (subscription ToS); switch to an API contract for client production.
- Pitfalls are collected in [../agent-cultivation/PITFALLS.md](../agent-cultivation/PITFALLS.md) — the log itself is part of the product.

## License

MIT — see [../LICENSE](../LICENSE).
