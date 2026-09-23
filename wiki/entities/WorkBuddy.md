---
title: "WorkBuddy"
type: entity
tags: [product, agent, environment]
sources: [skill-material]
last_updated: 2026-09-10
---

## 是什么

本仓库的运行环境——用户的 AI 助手工作台（基于 CodeBuddy Code）。它读取项目级 Skill 与配置文件，按描述自动匹配并加载能力。

## 在知识库中的位置

- 支持 Skills 功能：`SKILL.md` 的 frontmatter 定义 `name` / `description` / `allowed-tools`，可组织项目级与用户级 Skill。
- 本仓库的 [[ConceptMaterialGenerator]] 与 `llm-wiki` 两个 Skill 都在此环境下运行。
- 本知识库的 [[Skill]] / [[AgentSkill]] / [[LLMContext]] 三份资料，正是它在 [[ProgressiveDisclosure|渐进式披露]] 机制下按需加载 Skill 后生成的产物。

## 相关页面

[[Skill]] · [[AgentSkill]] · [[LLMContext]] · [[ConceptMaterialGenerator]]
