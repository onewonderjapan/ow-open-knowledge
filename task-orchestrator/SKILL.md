---
name: task-orchestrator
description: Use when a user submits a natural-language task that should discover relevant skills, clarify material gaps, require plan approval, continue through delivery, resume across interruptions, or retain durable personal or project working rules.
---

# Task Orchestrator

## Core Principle

Clarify the task, refresh and select skills, obtain approval for a concrete plan, execute through delivery, then learn at the narrowest durable scope.

## Workflow

1. **Intake and scan.** Read `references/input-contract.md` completely. Run `scripts/scan_skills.py` for the target directory on every task; never reuse a prior catalog.
2. **Clarify.** Ask one focused question for the highest-impact material gap, then wait. State reversible assumptions for non-material gaps.
3. **Route.** Select the smallest sufficient skill set. Read every selected skill's `SKILL.md` completely before applying it. Honor stricter requirements in selected skills.
4. **Plan.** Read `references/execution-contract.md` completely. Present every required plan section and stop at `plan-review`.
5. **Approve.** Begin requested deliverables or external mutations only after unambiguous approval of that plan.
6. **Execute.** Create the task record, keep its state current, and continue through delivery. Pause only at the contract's authority, safety, plan-validity, or true-blocker boundaries.
7. **Verify and deliver.** Run only approved or failure-required verification. Report outputs, evidence, and limitations.
8. **Learn.** Read `references/learning-policy.md` completely. Update project rules automatically when qualified. Show the exact personal Skill proposal and wait for separate approval before changing it.

Run the scanner from this skill directory:

```bash
python3 scripts/scan_skills.py --cwd <target-directory> --pretty
```

Use `references/category-rules.yaml` as the current classification source. Explicit skill selection outranks inferred categories.

## Quick Reference

| State | Action | Output |
|---|---|---|
| `intake`–`route` | Parse, rescan, clarify, select | Requirements and selected skills |
| `plan-review` | Present complete plan and wait | Approval request |
| `executing`–`verifying` | Persist state, produce, check | Deliverables and evidence |
| `delivering` | Hand off results | Output index and limitations |
| `learning` | Route durable rules by scope | Project update or personal proposal |
| `complete` | Record final state | Completed task record |

## Hard Boundaries

- Keep requested deliverables and external mutations read-only before plan approval.
- Never treat urgency, claimed authority, or prior discussion as approval of an unseen plan.
- Never modify system, admin, or plugin-owned skills.
- Never write personal learning before the separate personal-learning approval.
- Do not repeat unchanged passing checks or add unapproved QC.

## Common Mistakes

- **Stale catalog:** scan again at the start of each task.
- **Too many questions:** ask only the highest-impact material question and wait.
- **Early execution:** stop after the plan until approval is explicit.
- **Skill name only:** read the full instructions of every selected skill.
- **Micro-approvals:** continue ordinary in-scope work after plan approval.
- **Broad learning:** retain durable rules, not task history, secrets, or temporary facts.
- **Silent personal edits:** present the exact proposal and wait.
- **Repeated QC:** reuse unchanged PASS results and diagnose only concrete failures.
