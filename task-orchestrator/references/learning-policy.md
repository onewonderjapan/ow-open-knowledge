# Learning Policy

## Qualifying Learning

Create a learning candidate only from:

- an explicit user statement framed as a recurring preference or rule;
- a correction the user asked to preserve;
- a workflow or verification practice that succeeded in the completed task and is clearly reusable.

Reject credentials, customer secrets, personal data, temporary paths, one-off values, unverified guesses, incidental failures, task history, and facts that merely describe the completed output.

Write concise instructions in imperative form. Deduplicate equivalent rules. Surface a contradiction instead of silently replacing either rule.

## Scope Decision

Choose the narrowest durable scope:

- **Project:** the rule depends on the current repository, customer, codebase, workbook schema, deployment environment, or local acceptance convention.
- **Personal:** the rule expresses the user's reusable preference across unrelated projects.
- **No learning:** the candidate is temporary, sensitive, uncertain, or unlikely to be useful again.

Use the selected task category. Propose a new category only when the candidate and available skills do not fit an existing category and the distinction is likely to recur.

## Project Skill Update

After task delivery, automatically merge a qualified project rule into:

```text
<project-root>/.agents/skills/project-<category>-rules/SKILL.md
```

For a new frontend rule skill, use:

```yaml
---
name: project-frontend-rules
description: Use when performing frontend work in this project and project-specific conventions or acceptance rules apply.
---

# Project Frontend Rules

- Preserve the verified project-specific instruction in imperative form.
```

Replace `frontend` with the selected lowercase category and describe that category's project work. Merge into the most focused existing project rule skill when one already owns the rule. Do not create duplicate instructions or a chronological log.

## Personal Skill Proposal

Do not change a personal rule skill during the initial task approval. After delivery, show exactly:

```text
Personal Skill learning proposal
Target: <absolute SKILL.md path>
Category: <category>
Additions: <exact proposed instructions>
Changes: <exact before and after text, or none>
Removals: <exact text, or none>
Reason: <why this is durable across projects>
Approval required: yes
```

Wait for a separate unambiguous approval. On approval, create or update:

```text
$HOME/.agents/skills/personal-<category>-rules/SKILL.md
```

Use valid frontmatter, a trigger description limited to that category, and concise durable instructions. If the user rejects or edits the proposal, preserve the delivered task result and apply only the approved learning text.

## Protected Sources

Treat `system`, `admin`, and `plugin` catalog entries as read-only even when file permissions allow writes. Do not reuse the same skill name as a protected source. Store any qualified overlay in the focused project or personal rule skill instead.

Record accepted, rejected, and pending candidates in the task run's `learning.md`; keep the Skill itself free of provenance logs.
