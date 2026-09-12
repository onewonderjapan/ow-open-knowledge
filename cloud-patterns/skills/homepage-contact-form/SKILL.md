---
name: homepage-contact-form
description: 官网联系表单要发邮件时用。API Gateway + Lambda + SES 的完整链路与 Terraform 部署约定（区域 ap-northeast-1）。
---
# 官网咨询表单

官网联系表单要发邮件时用。旧实现是 Terraform，区域 `ap-northeast-1`。

## 流程

1. 表单 POST JSON 到 API Gateway。
2. Lambda 读环境变量里的收件人配置，组邮件，走 SES 发出。
3. Terraform 管 API Gateway、Lambda、SES 权限。state 在加密的 S3 backend。
4. 邮件地址放配置，不放仓。GitHub Actions 用 secrets 做 AWS 凭据，顺序是 init、校验、plan、apply。

## 踩坑

- SES 默认在 sandbox。发件人和收件人都要验证，否则发信失败不是代码错。
- 前端要带 CORS。API 本身还要另加认证，不要把端点裸放。
- 旧 Lambda 把 `Source` 传成了数组。SES 要的是已验证的单个地址字符串。
- `plan.out`、`.terraform`、邮件地址 JSON 不要提交。
