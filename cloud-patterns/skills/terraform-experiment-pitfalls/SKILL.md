# Terraform 实验仓踩坑

看到旧的 QuickSight、S3、RDS、IAM 实验仓时用。只留规矩，不留那些模块。

## 不要做

- 不要把 AWS 账号、桶名、客户名写进 tf。用变量和当前身份。
- 不要提交 `.terraform`、`plan.out`、lock 里外的本地状态。
- 不要用已弃用的 `template` provider 和 `aws_s3_bucket_object`。
- 不要用 `null_resource` + `local-exec` 去改权限。权限要进 state。
- 不要把 PR 指到一个个人实验分支。base 用默认分支。
- IAM 不要给 `s3:*` 或 `quicksight:*` 加 `Resource *`。旧仓这么写过，不要学。

## 可以留的分层

客户配置用 JSON，Terraform 只负责创建资源。客户数据本身不进仓。RDS 凭据走 Secrets Manager，按 master / developer / customer 分开，不要共用一个超级用户。
