---
title: "Agent / 大模型上下文 / Skill 三者关系"
type: source
tags: [synthesis, agent, context, skill]
date: 2026-09-09
last_updated: 2026-09-10
source_file: raw/ai-concepts/concept-relationship.md
---

## 摘要

本文是三份概念资料的横向总结，用一句话锁定三者关系：**Agent 以大模型为大脑，以上下文为短期工作内存，以 Skill 为可插拔的技能库。** 全文分两条重点展开——上下文如何决定 Agent 的工作质量，以及 Skill 如何把验证过的做事方法固化为可复用能力，并给出三者的分工对照表。

## 关键主张

- 大模型没有持久记忆，Agent 每次决策的质量几乎完全取决于**当时上下文里装了什么**。
- 上下文的质量 → 决策质量 → 行动结果，构成一个需要主动清理与压缩的反馈闭环。
- Agent 工程的核心是**上下文工程**：决定什么信息、在什么时机、以什么形式、放在什么位置进入上下文。
- Skill 通过「启动只装元数据、匹配才注入正文」的渐进式披露，与上下文的稀缺性达成平衡。
- 三者合起来是增长型系统：**上下文决定当下表现，Skill 决定长期复利。**

## 关键引用

> Agent 以大模型为大脑，以上下文为短期工作内存，以 Skill 为可插拔的技能库。

> 上下文决定当下表现，Skill 决定长期复利。

## 关联

- [[agent-context-skill-relationship]] —— 由本文沉淀而成的综合页
- [[Skill]] / [[LLMContext]] / [[AgentSkill]] —— 被总结的三份资料
- [[ContextEngineering]] —— 文中「上下文工程」的展开
- [[ProgressiveDisclosure]] —— Skill 与上下文配合的具体机制

## 矛盾 / 待澄清

无。本文是派生性总结，与三份原始资料一致。
