---
title: "大模型上下文（Context）"
type: source
tags: [ai-concept, llm, context]
date: 2026-09-06
last_updated: 2026-09-10
source_file: raw/ai-concepts/llm-context.md
---

## 摘要

上下文（context）是模型生成每一个字时**能「看见」的全部内容**；上下文窗口（context window）是这块「工作记忆」的大小上限，以 token 计。模型不查数据库、不翻笔记，每一步只依据窗口里的内容作答，因此同一模型在窗口内容丰富或空白时表现判若两人。三条关键性质——**有限、共享、位置敏感**——直接决定了 Agent 的失效模式。

## 关键主张

- **有限**：超限必须截断、压缩或外存，没有例外。
- **共享**：系统提示、对话历史、检索文档/工具结果竞争同一空间，多塞一段文档就多挤占一分注意力。
- **位置敏感**：开头与结尾记得牢，中间易被忽略（Lost in the Middle 的实证结论）。
- 根源在注意力机制：每个 token 与它之前所有 token 建立注意力关系，计算量随长度平方增长 → 窗口越长，注意力被摊得越薄（context rot）。
- **窗口 ≠ 记忆**：跨会话不保留任何内容，长期记忆要靠外部存储主动写回窗口。

## 关键引用

> 一块有限的、所有信息共享的「桌面空间」。

> 用最小的、高信号的 token 集合达成目标，而非拼命塞满。

## 关联

- [[LLMContext]] —— 本页对应的核心概念页
- [[ContextEngineering]] —— 由「有限/共享/位置敏感」推演出的工程实践
- [[ProgressiveDisclosure]] —— 一套应对上下文成本的加载策略
- [[Skill]] —— Skill 的触发机制本质是上下文管理
- [[AgentSkill]] —— 渐进式披露的具体落地格式
- [[concept-relationship-summary]] —— 把上下文放进「Agent / 上下文 / Skill」整体关系里看

## 矛盾 / 待澄清

无。
