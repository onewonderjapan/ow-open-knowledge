# Input Contract

## Intake Recipe

Apply these steps in order:

1. Preserve every explicitly invoked or excluded skill name.
2. Extract the goal, available inputs and locations, constraints, expected deliverables, completion criteria, and target directory from the user's natural language.
3. Resolve the target directory. Use the user-provided directory first; otherwise use the Git root containing the primary output; outside Git, use the current working directory.
4. Run `scripts/scan_skills.py --cwd <target-directory> --pretty` before choosing implicit skills.
5. Divide missing facts into material and non-material gaps.
6. Ask one focused question for the highest-impact material gap and wait for the answer.
7. Make only reversible assumptions for non-material gaps and list them in the plan.
8. Select and explain the smallest sufficient skill set.

## Materiality Test

A gap is material when different answers would change the deliverable, task scope, business meaning, safety, authority, target system, or acceptance result. Ask rather than guess.

A gap is non-material when a reversible local choice does not change the promised result. Choose a reasonable default, record the assumption, and continue.

Examples:

- “Clean my monthly workbook” without a workbook or path: material. Ask for the file or location.
- “Restart the service” without a service and environment: material. Ask first for the service and environment target.
- A deployment task without confirmed authority or rollback expectations: material.
- An unspecified temporary filename for an intermediate local artifact: normally non-material.
- An unspecified internal helper name that does not affect a public interface: normally non-material.

## Skill Routing

Use this precedence:

1. Available skills explicitly invoked by the user.
2. Matching project skills.
3. Matching personal skills.
4. Matching plugin, admin, and system skills.

Treat categories as multi-label routing hints, not exclusive folders. Explicit selection outranks category inference. When an explicit skill is unavailable, name the missing skill and propose an available substitute. Ask for direction only when the substitution would materially change the result.

Read the full `SKILL.md` for every selected skill before planning. Apply process skills before implementation skills. Incorporate mandatory gates from selected skills into the proposed plan.

## Intake Output

Before planning, hold a resolved intake with:

```text
Goal
Inputs and locations
Constraints
Deliverables
Completion criteria
Target directory
Explicit skill choices
Selected skill set
Assumptions
```

Do not invent absent files, prior discussions, credentials, permissions, or business decisions.
