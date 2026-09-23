---
title: "渐进式披露（Progressive Disclosure）"
type: concept
tags: [context, skill, loading-strategy]
sources: [agent-skill-material, skill-material, llm-context-material]
last_updated: 2026-09-10
---

## 定义

一种**按需加载**的信息组织策略：启动时只装入极小的高信号元数据，只有当任务真正匹配时，才把完整正文与捆绑资源读进上下文。它是 [[AgentSkill]] 与 [[Skill]] 得以低成本常驻的底层机制，本质是一套 [[ContextEngineering|上下文工程]] 策略。

## 加载阶梯

1. 启动：每个 Skill 只装 `name` + `description`（约 100 tokens/个）
2. 任务匹配某个 `description` → 读取 `SKILL.md` 正文
3. 正文引用了捆绑文件 → 再按需读取 `references/` 或执行 `scripts/`（脚本执行，不进上下文）

## 为什么有效

直接回应了 [[LLMContext]] 的稀缺性：几十个能力包常驻的成本被压到每条约 100 tokens。未匹配的能力**零成本**，匹配的能力才付出 token 代价。

## 边界

渐进式披露把「何时加载」优化到极致，但不能替代「加载什么」的判断——注入正文若本身冗长低质，同样会稀释注意力。**元数据（description）的质量决定触发的准确性**：描述含糊则关键能力永不被加载。

## 相关来源

- [[agent-skill-material]] —— 三层加载机制的原始整理
- [[skill-material]] —— Skill 生命周期中的加载环节
- [[llm-context-material]] —— 所服务的上下文约束

## 相关页面

[[AgentSkill]] · [[Skill]] · [[LLMContext]] · [[ContextEngineering]]
