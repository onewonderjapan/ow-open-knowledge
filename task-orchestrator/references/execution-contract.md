# Execution Contract

## Lifecycle

Advance through these states in order:

1. `intake`: parse the request.
2. `scan`: refresh the complete skill inventory.
3. `clarify`: resolve material gaps one question at a time.
4. `route`: select and explain the smallest sufficient skill set.
5. `plan-review`: present the execution plan and wait.
6. `executing`: perform the approved work and persist state.
7. `verifying`: run only authorized verification.
8. `delivering`: present outputs, evidence, and limitations.
9. `learning`: route durable rules by scope.
10. `complete`: record the final status.

## Plan Contract

Present these sections in this order:

1. **Outcome** — the concrete result to deliver.
2. **Selected skills** — each skill and why it is required.
3. **Execution steps** — ordered, observable work.
4. **Files and deliverables** — expected creations or modifications.
5. **Verification** — the check for each material output.
6. **Risks, permissions, and dependencies** — known boundaries or external needs.
7. **Assumptions** — reversible decisions made for non-material gaps.
8. **Approval request** — ask for an unambiguous decision on this plan.

Permit read-only inspection before approval. Do not create requested deliverables, change project files, mutate external systems, or create the task run record before approval.

Treat “同意”, “批准”, “开始执行”, and unambiguous equivalents as approval only when they clearly refer to the current displayed plan. Approval never expands the plan or authorizes unrelated, destructive, credentialed, or high-risk action.

## Approved Execution

After approval:

1. Create the task record.
2. Hash the approved plan and record the checksum.
3. Mark the first step in progress.
4. Execute ordinary in-scope decisions without additional approval.
5. Update step, artifact, verification, and state fields as work advances.
6. Pause only when the scope must materially expand, an irreversible or high-risk action is required, authority or a business choice is missing, the approved plan is invalidated, or safe in-scope alternatives are exhausted.

## Task Record

Use the Git root containing the primary output as the task directory. Outside Git, use the user-provided target directory, then the current working directory. When no local target exists, use `$HOME/.task-workflow/runs`.

Create:

```text
<task-directory>/.task-workflow/runs/<YYYYMMDD-HHMMSS>-<task-slug>/
├── request.md
├── plan.md
├── status.yaml
├── result.md
└── learning.md
```

Write `status.yaml` with this schema:

```yaml
task_id: "20260801-120000-example"
state: "executing"
approved_plan_sha256: "64-lowercase-hex-characters"
steps:
  - id: "step-1"
    status: "completed"
artifacts: []
verification: []
blocking_reason: null
```

Use only these step statuses: `pending`, `in_progress`, `completed`, and `blocked`. Keep at most one step `in_progress`.

## Resume Contract

On resume, read `request.md`, `plan.md`, and `status.yaml`. Compare the approved-plan checksum and relevant input hashes with the recorded values.

- When unchanged, reuse completed steps and passing checks, then continue at the first incomplete step.
- When a relevant input changed but the plan remains sound, update only affected pending work and state the change.
- When the plan changed materially, return to `plan-review` and obtain renewed approval.
- When an expected artifact is missing or corrupt, treat it as a concrete error and diagnose only that affected output.

## Error Handling and QC Budget

Recoverable errors are recorded and handled within the approved scope. A concrete error is a non-zero command, traceback, OOM, non-finite result, missing or corrupt expected artifact, input or artifact hash drift, explicit threshold failure, or required GPU safety-precheck failure.

After a concrete error, diagnosis remains limited to the affected component. Do not expand a local failure into a full-project, full-dataset, or repeated review. Reuse passing checks when their inputs, outputs, and verification contract have not changed.

Run only plan-specified verification during normal execution. Do not add an independent reviewer, extra contact sheet, duplicate gate, or unrelated audit unless the user or approved plan explicitly requires it.

## Delivery

Deliver the result before proposing personal learning. Report:

- the produced outcome;
- absolute paths or external locations for material outputs;
- verification commands and actual outcomes;
- known limitations or unresolved blockers;
- the final task-record location.
