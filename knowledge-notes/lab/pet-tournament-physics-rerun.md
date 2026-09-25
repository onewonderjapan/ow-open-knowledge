---
id: 20260905-pet-tournament-physics-rerun
title: "物理常识规则生效后锦标赛机评 ↔ 人审复测"
tags: [research]
created: 2026-09-05
updated: 2026-09-06
summary: "实验已执行（届次 cyc_20260906-021111，3 题材 9 卡，机评排名 G>H>B>I，人审 pairwise b>h、h>g、g>i，4 卡全 select）：物理常识规则生效后 judge↔human 相关性由首届 legacy -0.4（标准 ρ≈−0.775）转为本届 [internal] 近似 agreement 0.65（标准 Spearman ρ≈0.544），两口径均由负转正且过预注册 ≥0.3 阈值，假设成立；但存在模型池变更、n=1 单届、disposition 无分化三个 caveat，证据强度为方向性而非结论性。"
lang: zh
type: experiment
scope: public
source: knowledge-base@e73f8dd
related: [20260904-video-gen-model-pilot]
---

# 物理常识规则生效后锦标赛机评 ↔ 人审复测

> Summary: 实验已执行（cyc_20260906-021111）：物理常识规则生效后 judge↔human 相关性由首届 legacy -0.4（标准 ρ≈−0.775）转为本届近似 agreement 0.65（标准 ρ≈0.544），两口径均过 ≥0.3，假设按预注册口径成立；附模型池变更、n=1、disposition 无分化三个 caveat。

## Context

本实验选自 [internal path] 选题 L-12（方向④：宠物短剧管线）。

已有背景（来自证据笔记，非本实验产出）：

- 首届锦标赛（cyc_20260813-232230）judge↔human legacy 近似 agreement = -0.4（标准 Spearman ρ≈-0.775）：机评前二双双被人审停放，两条核心动作均依赖「冰箱突出把手」这一不存在的物件形态；该盲区被定性为继「题材锚定」「过度遵从正典」之后的第三种评委盲区——物理常识盲区（见证据链第一条）。
- 对应两条规则已于 2026-08-14 批准并写入合同附录：评委 rubric 的 filmable 维度增加物理常识条款（依赖非常识物件形态者 filmable 不得高于 5）；canon_brief「常见败笔」增补物件形态条款；合同同时规定锦标赛一条命令（`tools/start_tournament.py`）与人审 15 分钟封顶机制（见证据链第二条）。

本实验的性质是「复测」：规则已就位，只差办一届新锦标赛取得生效后的相关性对照点。

## 假设

rubric 物理常识条款 + canon_brief 败笔条款生效后，机评不再把「依赖不存在物件形态」的故事排进前二，新一届锦标赛 judge↔human Spearman 由首届 -0.4 转为正相关（≥0.3）（按 legacy 近似 agreement 口径判定）。

- 证伪口径：新届 Spearman（按 legacy 近似 agreement 口径判定）仍为负（或 <0.3），或机评前二仍出现「依赖不存在物件形态」的故事并被人审停放，即假设不成立；此时记录第四种评委盲区。
- 本假设来自 backlog L-12 的假设草稿，执行前不得当作已验证事实引用。

## 方法（预注册）

1. 按合同既定漏斗跑一届新锦标赛（1–3 个题材，`tools/start_tournament.py` 一条命令）。
2. 照常人审：pairwise 点胜者 + 每个 finalist 一个 disposition（落地 / 停放 / 枪毙），15 分钟封顶。
3. 计算 judge↔human legacy 近似 agreement（[internal] 现行口径），与首届 -0.4 对照。
4. 逐卡检查机评前二是否含「依赖不存在物件形态」的故事。
5. 执行时登记：届次 id、题材数、逐卡机评分、人审逐对结果与 disposition。

## 数据（实测，2026-09-06，届次 cyc_20260906-021111）

- 届次 id：cyc_20260906-021111（3 题材：怕吸尘器的小猫 / 总把袜子藏进沙发缝的柯基 / 想够到门把手出门的橘猫；GLM-5.3-Flash ×3 采样 = 9 张有效卡；3 个独立评委槽位逐卡评分 = 27 份 raw）。
- 机评排名（pairwise 胜负驱动，平手回退 judge_mean）：G（3 胜，judge_mean 8.75）> H（1 胜，8.667）> B（1 胜，8.5）> I（1 胜，8.5）；未入围 E 8.42 / F 8.08 / A 7.92 / D 7.83 / C 6.58。
- 人审 pairwise（2026-09-06T09:25:35Z finalize）：p1 g>i，p2 b>h，p3 h>g；人审胜场 g=h=b=1、i=0。
- Disposition：4 入围卡（g/h/b/i）全部 select，无停放/枪毙。
- 相关性（双口径）：机评 judge_mean 排名（tie-aware 降序 [g,h,b,i]=[4,3,1.5,1.5]）vs 人审胜场排名（[3,3,3,1]）：[internal] 现行近似 agreement = **0.65**（d²=3.5，1−6×3.5/60），标准 Spearman **ρ≈0.544**；首届 legacy=−0.4、标准 ρ≈−0.775，两口径均对照转正、均达 ≥0.3 阈值。输入数据、排名过程与双口径复算脚本见 [internal path]（review_session.json 与 cycle.json metrics 同值 0.65，字段名带 spearman 但实为 legacy 近似口径）。
- 机评前二物理常识合规：G、H 两条均通过人审 select，人审未提出「依赖不存在物件形态」异议（对比首届机评前二双双停放）。

## 结论（2026-09-06 回填）

- **假设成立（按预注册口径 ≥0.3）**：规则生效后 judge↔human 相关性由首届 legacy −0.4（标准 ρ≈−0.775）转为本届 legacy 近似 agreement 0.65（标准 ρ≈0.544），两口径均转正、均过阈；机评前二（G/H）不再含「依赖不存在物件形态」的故事且双双 select。未出现需要记录第四种评委盲区的证伪情形。
- 必须同时记录的三个 caveat：
  1. **模型池变更混杂因素**：首届为火山系三评委面板（doubao/deepseek 等，经 arkcli），本届为 GLM-5.3 单模型三独立槽（GLM Coding Plan，arkcli 已废弃）。相关性变化可能部分来自评委池本身的变化，而非（仅）物理常识条款。
  2. **n=1 单届**：正相关仅一个对照点，稳定性需后续届次确认，不宜据此宣布盲区已消除。
  3. **本届 disposition 无分化**：4 入围卡全 select，相关性指标只反映 pairwise 排序一致性，对「机评高位卡被人审停放」这一首届失败模式（disposition 维度）没有检验力。
- Confidence 由 low 升为 medium：假设方向有实测支持，但受上述 caveat 限制，属方向性证据而非结论性证据。

## 证据链

- 首届锦标赛结果、legacy Spearman = -0.4（标准 ρ≈−0.775）与「冰箱突出把手」停放案例、第三种评委盲区的定性：`20260814-pet-drama-training-learning`（pet-drama-training-learning，pet_drama_training 学习日志：首届人审裁决与逐届追踪）。
- 物理常识两条规则的批准与写入记录、锦标赛漏斗与人审 15 分钟封顶机制：`20260814-pet-drama-training-contract`（pet-drama-training-contract，Pet Drama Training Route Contract：funnel、canon 隔离与附录规则）。

## 复现性说明（reproducible: yes 的依据）

- 届次 id（cyc_20260906-021111）、逐卡评委三槽分、人审 pairwise 与 disposition、相关性计算口径与过程均已归档（[internal path]，含 spearman_agreement.md 双口径复算脚本），第三方按归档材料可复算出 0.65（legacy 近似）与 0.544（标准 Spearman）。
- 复算口径：机评 judge_mean（卡内三槽均分）tie-aware 排名 vs 人审 pairwise 胜场 tie-aware 排名；[internal] 现行实现为 legacy d² 简式（有并列时≠标准 Spearman，标准口径为平均秩+Pearson，经理裁定暂保留 legacy 以维持跨届可比，切换算法须新届次生效+一届双算过渡）。n=4 且两组内部均有并列，数值为粗粒度方向性证据。

## 说明与局限

- 本页为 T-21 节奏起草的实验骨架，已于 2026-09-06 按预注册方法执行并回填；数据与结论全部来自本届 cycle 归档，无编造数字。
- 首届 -0.4（legacy；标准 ρ≈−0.775）等背景数字引自证据笔记，不属于本实验产出；本届 0.65（legacy 近似）/ 0.544（标准 Spearman）等实测数字源自 cyc_20260906-021111 归档文件。
- 三个 caveat（模型池变更 / n=1 / disposition 无分化）见结论段，引用本结论时必须一并携带。
- 文本生成与评审属 standing-authorized 低成本工作、无视频费用，但举办新锦标赛与人审仍需人执行，本骨架不含也无法替代该步。

## Related

- [视频生成模型小样评测：同组提示词的稳定性对比](video-gen-model-pilot.md) — supports：实验类笔记的字段规范与预注册写法来源。
