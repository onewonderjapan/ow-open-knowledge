# cloud-patterns — Cloud Architecture Skills

Four skills distilled from real projects, each written as "flow + don't-do list" and ready to drop into a Claude Code or Codex-style agent tool: an AWS data merge, a full contact-form chain, form-triggered resource creation, and a collection of Terraform lessons learned the hard way.

Each `SKILL.md` has YAML frontmatter (`name` + `description`). Without it, every skill loader ignores the file — the body never gets a chance to run.

## Contents

| Skill | What it covers | Companion public repo |
|-------|----------------|------------------------|
| [skills/glue-json-rds-merge](skills/glue-json-rds-merge/SKILL.md) | Merge S3 JSON with RDS by id (S3 wins), report missing rows to Slack | [rds-glue-s3-etl-pipeline](https://github.com/onewonderjapan/rds-glue-s3-etl-pipeline) |
| [skills/homepage-contact-form](skills/homepage-contact-form/SKILL.md) | The full chain for a website contact form: API Gateway + Lambda + SES | [wonder-contact-terraform](https://github.com/onewonderjapan/wonder-contact-terraform) |
| [skills/form-to-cloud-iam](skills/form-to-cloud-iam/SKILL.md) | Enter a resource name in a Microsoft Form → Azure Function + DevOps create the IAM resource | [form2cloudbuilder](https://github.com/onewonderjapan/form2cloudbuilder) |
| [skills/terraform-experiment-pitfalls](skills/terraform-experiment-pitfalls/SKILL.md) | Pitfalls from past Terraform experiments (negative knowledge: what *not* to redo) | — |

## Usage

Copy a skill folder into your agent tool's skills path. Claude Code uses
`.claude/skills/`; Codex-style agents use `.agents/skills/`. Both work:

```bash
cp -r skills/<skill-name> <your-project>/.claude/skills/
# cp -r skills/<skill-name> <your-project>/.agents/skills/
```

## Notes

- Each skill is the distilled flow and rules; runnable code lives in the companion public repos linked above.
- `terraform-experiment-pitfalls` is negative knowledge on purpose — follow its "don't do" list rather than looking for reference code.
