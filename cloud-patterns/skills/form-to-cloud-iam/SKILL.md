---
name: form-to-cloud-iam
description: 只有在要做「表单填资源名，自动创建 AWS IAM 用户和策略」时才用。旧仓只有流程说明，没有可跑的代码，不要当成可运行系统。
---
# 表单触发云资源

只有在还要做「表单填资源名，自动建 AWS IAM 用户和策略」时才用。旧仓只有流程说明，`main` 没有代码。不要把它当成可跑的系统。

## 流程

1. Microsoft Form 里填 IAM 用户名和策略名。
2. 答案落到 OneDrive Excel。
3. Azure Function 读 Excel，改成 JSON，覆盖 Azure DevOps 仓里的 json。
4. Pipeline 读那份 json，创建 AWS 资源。

## 重开时先做

- 先拿 refresh token，再让 Function 访问 Graph。
- Function 依赖里要有 Az、Microsoft.Graph.Users、Microsoft.Graph.Authentication、ImportExcel。
- 不要把 token、租户或客户名写进仓。
- 这条线是 2025-03 的草案。重做时用现在的身份体系，不要复刻旧 Azure Function。
