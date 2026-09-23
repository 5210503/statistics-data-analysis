---
title: "concept-material-generator"
type: entity
tags: [project, skill]
sources: [skill-material, concept-relationship-summary]
last_updated: 2026-09-10
---

## 是什么

本仓库中的项目级 Skill（`.workbuddy/skills/concept-material-generator/SKILL.md`），把「生成 AI 概念学习资料」这件事固化为标准化流程，是 [[Skill]] 概念在本仓库中的活样本。

## 做了什么

- **输入**：任意 AI 概念名词（机器学习、NLP、CV、强化学习、MLOps 等）。
- **固定流程**：解析概念 → 索引查重 → 去原始出处查证一手资料 → 筛选 2–5 条核实链接 → 按六部分模板撰写 → 保存到 `learning-materials/<概念名>.md` → 更新索引 → 自检汇报。
- **输出结构**：概念个人解释 / 核心机制或组成 / 具体应用场景 / 易混淆问题或使用边界 / 可核查资料来源链接 / 难度递进自测题。
- **硬性红线**：禁止编造链接。

## 与知识库的关系

它产出的三份资料（`learning-materials/`）经复制进入 `raw/ai-concepts/`，被 ingest 成本知识库的概念页：[[Skill]]、[[AgentSkill]]、[[LLMContext]]。

## 相关页面

[[Skill]] · [[AgentSkill]] · [[WorkBuddy]] · [[ProgressiveDisclosure]]
