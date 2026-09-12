<!--
Write in Japanese, Chinese or English — whichever you prefer.
CONTRIBUTING.md: 每个 PR 聚焦一件事，保持最小可审 (one PR, one thing, minimal to review).
-->

## What this changes

<!-- One or two sentences. Lead with the outcome, not the process. -->

## Why

<!-- What was wrong before. Quote the file:line or the failing command if there is one. -->

## Evidence

<!--
CONTRIBUTING.md 要求：代码改动需附可运行的验证命令与输出（证据主义）。
For code changes, paste the command you ran and its real output. Not a description of
what should happen — the actual output.
-->

```bash
# command
```

```text
# output
```

## Checklist

- [ ] One logical change, minimal to review
- [ ] No customer names, real personal names, internal codenames, credentials, or
      operational data (see [CONTRIBUTING.md](https://github.com/onewonderjapan/ow-open-knowledge/blob/main/CONTRIBUTING.md))
- [ ] Affected documents keep their original language (no translation-style rewrites)
- [ ] Relative links to files inside the repo still resolve (`python3 scripts/check_links.py`)

### If you touched code

- [ ] Tests pass:
      `python3 -m unittest discover -s ai-stack/tests -t ai-stack/tests`,
      `python3 -m unittest discover -s dev-pipeline/tests -t dev-pipeline/tests`,
      `python3 -m unittest discover -s task-orchestrator/tests -t task-orchestrator/tests`

### If you touched the masking layer

`ai-stack/CLAUDE.md`: 脱敏層のテストを書かずに脱敏ルールを変更しない（漏れ=事故）.
Masking is a security control — a rule change without a test is how leaks ship.

- [ ] I added regression tests to `ai-stack/tests/test_masker.py`
- [ ] Those tests fail without my change and pass with it
- [ ] I recorded any trap I hit in `agent-cultivation/PITFALLS.md`
