# Upgrade plan

English | [简体中文](ROADMAP.zh-CN.md)

This repository is **not** a single installable library. It is a public knowledge base: cultivation methodology, a runnable enterprise-AI thin slice, workflow standards, a multi-agent pipeline, cloud skills, and team norms.

The upgrade path below keeps that shape. Interfaces already advertised in `ai-stack` stay stable:

`Masker.mask` · `BM25Index.search` · `get_provider` · `evalkit.check`

## Current state

| Area | Strength | Gap |
|------|----------|-----|
| Methodology (`agent-cultivation/`) | Real-loop standard, pitfalls-as-product | Core docs still mixed JP/CN; no English originals |
| Thin slice (`ai-stack/`) | End-to-end demo, swappable layers | Masking had no tests; UI claimed zero-deps while importing janome; `claude-cli` used `shell=True` (broken on Linux) |
| Orchestrator (`task-orchestrator/`) | Stdlib-only scanner + tests | Not wired into CI |
| Dev pipeline | 6-agent design + self-learning | CLI still said “4 agents”; Dispatcher prompt omitted Reviewer; no parser tests |
| Workflow / cloud / team-norms | Clear standards and skills | No executable fixture beyond the markdown scaffold |
| Open-source hygiene | MIT, CONTRIBUTING, trilingual READMEs | No CI, no SECURITY.md, no issue/PR templates |

Existing PRs #1 / #2 are Bot-collaboration docs. This plan is independent engineering work.

## Phase 0 — done in this change

Hygiene the cultivation standard itself demands (PITFALLS: “脱敏はテストケース必須”).

- Masking / QC / RAG / stub-pipeline tests; `scripts/verify.py` + GitHub Actions on Python 3.9 and 3.12
- Company labels no longer collide after `A社`–`N社`; BM25 `add_dir` rebuilds df; QC sections match the 8-chapter prompt
- Demo UI defaults to stub, highlights `担当者01` / `会社15`, and runs without janome (bigram fallback)
- `claude-cli` uses `shell=False`; anthropic is an extra (`requirements-llm.txt`)
- Dispatcher / `--memory` / `--optimize` cover all six agents; Reviewer is in the default development pipeline
- SECURITY.md, issue & PR templates, `entities.local.json` gitignored at repo root

Verify:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r ai-stack/requirements.txt
python scripts/verify.py
```

## Phase 1 — make the thin slice trustworthy

Still no architecture change. Each item is a small PR.

1. **Masking leak corpus** — 20–50 fictional JP business docs (honorific-less names, 株式会社 vs 製作所, fullwidth spaces). Fail the suite on any leftover phone/email/known name.
2. **Optional GiNZA NER** behind the same `Masker.mask` contract (`ai-stack/masking/ner.py`, extra extra). Keep regex+dict as the default so the demo stays light.
3. **Evalkit judge** — `evalkit/judge.py` as already sketched: rubric scores + a frozen stub fixture so CI does not call an API.
4. **Provider matrix** — OpenAI-compatible + a local llama.cpp/Ollama provider; route through one env (`AI_STACK_PROVIDER`). Fix the model-name drift (`claude-sonnet-5` vs `claude-sonnet-4-6`).
5. **Demo UI** — bind-address flag (still default localhost), POST size limit, JSON error handling; keep stdlib-only.
6. **dev-pipeline dry-run** — `--provider stub` that writes the same report paths without Claude CLI, so the 6-agent loop can be CI-tested.

## Phase 2 — production replacements (interfaces unchanged)

This is the table already in `ai-stack/README.md`, turned into work packages:

| Layer | Replace with | Constraint |
|-------|----------------|------------|
| `masking/` | GiNZA + legally reviewed rules + `entities.local.json` workflow | Mapping stays in-process; never uploaded |
| `rag/` | multilingual-e5 + Qdrant (or pgvector) + ACL filter | `search(query, k)` signature stays |
| `llm/` | LiteLLM / AI gateway, per-tenant keys | `complete(prompt) -> str` stays |
| `evalkit/` | LLM-as-judge + regression goldens | `check()` remains the deterministic gate |
| `pipeline/` | job queue + auth’d UI | CLI one-shot remains for demos |

Do **not** thicken all layers at once. One layer per PR, with a before/after report from `scripts/verify.py` plus one real (fictional) RFP.

## Phase 3 — knowledge product, not just code

1. **Translate the core four** (keep originals): `AGENT育成標準.md`, `既存AGENT訓練ガイド.md`, `新プロジェクトSTARTUP標準.md`, `workflow-standard/STANDARD.md` → `*.en.md` / keep JP/CN as source.
2. **Reading paths** — a one-page “I am a PM / SE / agent-builder” index in the root README.
3. **Skill pack install** — `make install-skills DEST=~/.claude/skills` that copies `task-orchestrator`, `cloud-patterns/skills/*`, `agent-cultivation/workbench-skills/*`.
4. **Version the standards** — SemVer on STANDARD.md / 育成標準 (v1.1 = additive; v2 = breaking rule). Changelog next to each.
5. **Community** — CODE_OF_CONDUCT, discussion category “pitfalls”, GitHub topics (`ai-agents`, `rag`, `pii-masking`).

## Phase 4 — what not to do

- Do not merge client case studies or real names. The inclusion boundary in CONTRIBUTING.md is load-bearing.
- Do not turn this repo into a monorepo product. Companion repos (`form2cloudbuilder`, `wonder-contact-terraform`, …) stay separate; this repo keeps the distilled skill + a thin runnable slice.
- Do not add a heavy web framework to `ui/app.py` until Phase 2’s job queue exists.
- Do not “fix” mixed JP/CN in methodology docs by rewriting them into one language in place.

## Suggested PR order after Phase 0

1. Masking leak corpus + any rule fixes
2. `evalkit/judge.py` with stub fixtures
3. `dev-pipeline --provider stub`
4. Skill-pack installer
5. English translations of the four core standards
