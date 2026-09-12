# Security Policy

## Why this file exists

This repository is not only documentation. It ships a **masking layer**
(`ai-stack/masking/`) that is used as a security control: it is what decides which
parts of a business document may be sent to a cloud LLM. It also ships agents that
write files to disk based on model output (`dev-pipeline/`). Bugs in either can have
real consequences, so please report them privately rather than in a public issue.

## Reporting a vulnerability

Please **do not open a public issue** for security problems.

Use GitHub's private reporting: go to the repository's **Security** tab →
**Report a vulnerability**. This creates a private advisory visible only to
maintainers.

Reports in Japanese, Chinese or English are all fine.

Helpful things to include:

- Which component (`ai-stack/masking`, `ai-stack/ui`, `dev-pipeline`, …)
- A minimal reproduction — for masking issues, the **shortest input string** that
  leaks, and what you expected to be masked
- Why it matters (what information escapes, or what an attacker gains)

Please use fictional data in the report itself. Do not paste real customer names,
real phone numbers, or real email addresses.

## Scope

In scope:

- **Masking bypasses** — any input where PII or a client identifier survives
  `Masker.mask()`. This is the highest-severity class in this repository.
- **Unmasked data reaching an LLM provider** — any code path that puts text into a
  prompt without passing it through the masking layer.
- **Path traversal or arbitrary file access** driven by model output in
  `dev-pipeline` agents.
- Command injection, unsafe deserialization, or secret leakage in any shipped code.

Out of scope:

- The demo web UI (`ai-stack/ui/app.py`) binds to `127.0.0.1` and has no
  authentication **by design**. It is a localhost demo, not a server. Reports that
  amount to "it has no login" are expected behaviour. Reports that it can be made to
  read or write files outside its intended scope, or that it leaks data to a third
  party, are in scope.
- Over-masking (masking more than necessary) is a quality issue, not a
  vulnerability — please open a normal issue for those.
- Third-party dependencies (`janome`, `anthropic`, `python-pptx`) — report those
  upstream.

## Known limitations (not vulnerabilities)

The masking layer is a documented thin slice, and its limits are deliberate:

- Person names outside the dictionary are only detected when followed by an
  honorific or title (`様` / `氏` / `さん` / `部長` …). Names with no such marker are
  **not** detected. Real deployments are expected to maintain
  `masking/entities.local.json` (gitignored) and to layer NER on top; see
  `agent-cultivation/PITFALLS.md`.
- `mapping` (real name → label) is written to `out/*_report.json` for audit purposes.
  Those files contain real names by design — treat `out/` as sensitive.

If you find a leak that the notes above do **not** already cover, it is a bug and we
want to hear about it.

## If you are changing the masking layer

`ai-stack/CLAUDE.md` requires it, so it is worth repeating here: **do not change
masking rules without adding regression tests.** Add cases to
`ai-stack/tests/test_masker.py` and make sure they fail before your fix and pass
after it.
