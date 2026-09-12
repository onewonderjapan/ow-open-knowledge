# Security policy

This repository contains a **thin-slice** PII masking layer (`ai-stack/masking/`) intended for demos and internal dogfooding. Treat masking failures as security incidents.

## Report a vulnerability

Please **do not** open a public issue for:

- masking leaks (names, phones, emails, amounts, internal hostnames left in outbound text)
- credential or secret exposure
- anything that would help bypass the local-before-cloud boundary

Use GitHub's [private vulnerability reporting](https://github.com/onewonderjapan/ow-open-knowledge/security/advisories/new) if it is enabled, or email the maintainers listed on the organization profile.

Include: the input snippet (fictionalize real names), the masked output, provider (`stub` / `claude-cli` / `anthropic-api`), and the `*_report.json` QC section.

## Rules for contributors

- Never commit `entities.local.json`, API keys, or real customer data.
- Do not change masking rules without adding a failing-then-passing test under `ai-stack/tests/test_masker.py`.
- The demo UI binds to `127.0.0.1` on purpose. Do not expose it on `0.0.0.0` without an auth layer.
- `claude-cli` is PoC / internal use only (subscription terms). Production workloads should use a contracted API.
