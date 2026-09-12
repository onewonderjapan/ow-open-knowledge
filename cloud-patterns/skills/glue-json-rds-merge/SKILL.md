---
name: glue-json-rds-merge
description: 在需要用 AWS Glue/PySpark 把 S3 上的 JSON 与 RDS 里的同一批记录合并成 CSV 时用。含 Secrets Manager 取凭据与 Slack 通知的约定。
---
# Glue JSON 与 RDS 合并

在需要把 S3 上的 JSON 和 RDS 里的同一批记录合并成 CSV 时用。不要把旧 Glue 仓原样搬过来。

## 流程

1. Glue/PySpark 任务先从 Secrets Manager 拿 RDS 凭据，不要把连接串写进代码。
2. 读 S3 JSON。失败就通知并停，不要继续读 RDS。
3. 两边都必须有 `id`。没有就停。
4. 以 S3 的 id 为主。匹配上的行：S3 有值用 S3，缺的列用 RDS。匹不上的 S3 行单独保留。
5. RDS 里有、S3 里没有的 id，单独列出来通知，不要静默丢掉。
6. 列顺序固定后再写 CSV。成功和失败都要通知。

## 不要做

- 不要把 Slack webhook 或 Secrets 名写进公开文件。仓一旦变成 public，旧 token 当作已失效。
- 不要把 drawio 和测试图当作实现。留下的只是上面这条合并规则。
