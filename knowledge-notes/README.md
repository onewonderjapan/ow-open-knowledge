# knowledge-notes

本目录是 OneWonder 内部知识库导出的公开笔记：只收录 `scope: public` 的笔记（`type: runbook` / `type: digest` 除外），由内部知识库的 `kb export-public` 自动生成。当前收录 8 篇。

- **请勿在此直接编辑**：下次导出会覆盖。发现错误或想补充，请提 issue，由内部知识库修改后重新导出。
- 结构：`INDEX.md`（全部笔记一览）、`manifest.json`（导出来源 commit、日期、所用脱敏规则，以及除 manifest.json 自身外全部文件——各篇笔记与 README.md / INDEX.md——的 sha256）、`<主题>/<slug>.md`（笔记正文）。
- frontmatter 只保留 id / title / tags / created / updated / summary / lang / type / scope / source / related；`related` 只列同样已导出的笔记。
- 脱敏：社内呼称与社内文件路径已替换（路径显示为 `[internal path]`）；指向未导出笔记的链接降为纯文本。
- 语言：笔记保持原文语言（见各篇 `lang`），不做翻译。

This directory contains notes exported from OneWonder's internal knowledge base. Only notes marked `scope: public` are included (runbooks and digests excluded), generated automatically by `kb export-public`. Do not edit files here; they are overwritten on every export. Please propose changes via an issue instead. manifest.json records the SHA-256 of every other file in this directory. Notes keep their original language (see the `lang` field); internal file paths are replaced with `[internal path]`.
