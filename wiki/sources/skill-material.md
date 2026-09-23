---
title: "Skill（通用概念：可复用任务能力模板）"
type: source
tags: [ai-concept, agent, skill]
date: 2026-09-09
last_updated: 2026-09-10
source_file: raw/ai-concepts/skill.md
---

## 摘要

本文取 Skill 的通用含义——为 Agent 封装的可复用任务能力模板。很多任务会反复执行，若每次都把完整要求写进提示词，既麻烦又占上下文，于是把任务流程与规则提前封装成 Skill，需要时直接加载调用。其四层结构为：元数据头部、角色与规则定义、执行步骤流程、自检规则。与上下文的关系是「平时躺在库里不占空间，触发时才注入窗口」——用到才翻开的专业操作手册。

## 关键主张

- 一句话本质：**任务能力的封装复用载体**。
- 四层结构：元数据头部（name / description / allowed-tools）→ 角色与规则 → 执行流程 → 自检规则。
- 触发依赖 description 匹配；未匹配则零成本，匹配则全文注入上下文。
- **Skill 不是越长越好**：全部内容会加载进窗口，冗长会挤占空间、稀释注意力，反而导致任务出错。
- 与记忆的分工：Skill 沉淀「怎么做」，记忆沉淀「发生过什么」。

## 关键引用

> 用到才翻开的专业操作手册。

> Skill 触发后全部内容加载进上下文窗口，内容过长会挤占空间、稀释注意力。

## 关联

- [[Skill]] —— 本页对应的核心概念页
- [[AgentSkill]] —— Anthropic 对该概念的具体格式规范
- [[LLMContext]] —— Skill 的加载策略所服务的对象
- [[ConceptMaterialGenerator]] —— 本仓库中 Skill 的活样本
- [[WorkBuddy]] —— 本仓库 Skill 的运行环境

## 矛盾 / 待澄清

无。本页与 [[agent-skill-material]] 互为补充：一为通用概念，一为具体规范。
