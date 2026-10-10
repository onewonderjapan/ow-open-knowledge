# 知识笔记索引 / Index

共 4 篇。由 `kb export-public` 生成，请勿手改。

| id | title | summary | lang | updated | path |
|---|---|---|---|---|---|
| `20260925-codegen-2d-landscape` | 代码生成 2D：高星 repo 与官方 skill 方法论 | 代码生成 2D 五层盘点（as-of 2026-09-25）：最高星的是「AI 可靠生成的目标格式」库（mermaid 90.4k / excalidraw 132.9k / manim 94.2k）；官方 skill 方法论样本 anthropics/skills（178.1k）是先写美学宣言再用 canvas/p5.js 表达的两段式，强调不锁创意、craftsmanship、原创避版权。 | zh | 2026-09-25 | [gh-research/codegen-2d-landscape.md](gh-research/codegen-2d-landscape.md) |
| `20260925-gh-research-framework` | GitHub 高星 repo 定期调查框架（3D 渲染与代码生成 2D） | 本主题的调查规程：对象是 AI 做视觉产出（3D 渲染 / 代码生成 2D）的高星 repo；口径用 GitHub API 当日实测星数；知识按「引擎层→神经渲染→生成式→接口层（skill/MCP）」分类轴归类，每轮刷新盘点笔记而非新建。 | zh | 2026-09-25 | [gh-research/gh-research-framework.md](gh-research/gh-research-framework.md) |
| `20260925-render-3d-landscape` | 3D 画面渲染：高星 repo 路线图与方法论 | 3D 渲染高星 repo 四层盘点（as-of 2026-09-25，GitHub API 实测）：实时引擎 three.js 115.9k 一枝独秀且日更；神经渲染主线已收敛到 3DGS 工具链；生成式 3D 研究 repo 普遍「发论文即冻结」；AI×3D 的增量在 MCP/skill 接口层而非新算法库。 | zh | 2026-09-25 | [gh-research/render-3d-landscape.md](gh-research/render-3d-landscape.md) |
| `20260906-model-blindtest-quadrant` | 自有任务多模型盲测与价格×能力象限 | 12 道自有任务（代码/剧本/日文邮件）× 5 模型三盲盲测（GLM-5.3 主评+Flash 副评，绝对分天花板后补强制排名 24 对）：Borda 排名 opus-5 68 > gpt-6-astra 53 > GLM-5.3 43 > GLM-5.3-Flash 40 > gpt-5.6-luna 36；预注册「位次互换」假设因榜单可比对不足（仅 2 模型有榜）不可判定；定性：榜单「GLM≈Opus」口径在本团队任务未复现，代码题 20/20 全过无区分。 | zh | 2026-09-06 | [lab/model-blindtest-quadrant.md](lab/model-blindtest-quadrant.md) |
