---
title: "大模型上下文（LLM Context）"
type: concept
tags: [llm, context, attention]
sources: [llm-context-material, concept-relationship-summary]
last_updated: 2026-09-10
---

## 定义

上下文（context）是模型生成每一个字时**能「看见」的全部内容**；上下文窗口（context window）是这块「工作记忆」的大小上限，以 token 计。模型不查数据库、不翻笔记，每一步只依据窗口里的内容作答。

一句话本质：**一块有限的、所有信息共享的「桌面空间」**——系统提示、对话历史、检索文档、工具结果全都要挤在桌上竞争。

## 三条关键性质

- **有限**：超限必须截断、压缩或外存，没有例外。
- **共享**：四类内容竞争同一空间，多塞一段文档就多挤占一分注意力。
- **位置敏感**：开头与结尾记得牢，中间易被忽略（Lost in the Middle 实证结论）。

根源在注意力机制：每个 token 与它之前所有 token 建立注意力关系，计算量随长度平方增长 → 窗口越长注意力越薄（context rot，上下文腐烂）。

## 窗口 ≠ 记忆

| | 上下文窗口 | 参数化知识（训练数据） |
|---|---|---|
| 类比 | 桌上摊开的资料（看见） | 脑子里的记忆（记住） |
| 生效期 | 单次请求，结束即消失 | 永久固化在权重里 |
| 改动成本 | 每次请求都能换 | 必须重新训练 |

跨会话不保留任何内容，长期记忆要靠外部存储主动写回窗口。

## 边界

窗口更长 ≠ 效果更好：信息淹没在中间时召回反降，且推理成本随长度增长。正确姿势是**用最小的、高信号的 token 集合达成目标**。

## 相关来源

- [[llm-context-material]] —— 机制与应用整理
- [[concept-relationship-summary]] —— 上下文如何决定 Agent 决策质量

## 相关页面

[[ContextEngineering]] · [[ProgressiveDisclosure]] · [[Skill]] · [[AgentSkill]] · [[WorkBuddy]]
