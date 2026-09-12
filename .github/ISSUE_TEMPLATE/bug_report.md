---
name: Bug report / バグ報告 / 缺陷报告
about: Something in the reference code or documentation does not work as described
labels: bug
---

<!--
STOP: if this is a masking bypass (real names or PII surviving Masker.mask), or any
other security issue, do NOT file it here. See SECURITY.md and report it privately.

Write in Japanese, Chinese or English — whichever you prefer.
Use fictional data only. No real customer names, phone numbers or email addresses.
-->

## What is wrong

<!-- One or two sentences. -->

## Where

- [ ] `ai-stack/` (masking / RAG / LLM provider / evalkit / UI)
- [ ] `dev-pipeline/`
- [ ] `task-orchestrator/`
- [ ] `workflow-standard/`
- [ ] `cloud-patterns/`
- [ ] `agent-cultivation/`
- [ ] `team-norms/`
- [ ] Documentation only

File / line if you know it:

## Reproduction

<!--
CONTRIBUTING.md asks for evidence, not description. Paste the command you ran and the
output you actually got. For a masking or parsing issue, the shortest input that
triggers it is the most useful thing you can give us.
-->

```bash
# command
```

```text
# actual output
```

## Expected

<!-- What you expected instead, and why (quote the doc line if a document promised it). -->

## Environment

- OS:
- Python version:
- Provider (`stub` / `claude-cli` / `anthropic-api`), if relevant:
