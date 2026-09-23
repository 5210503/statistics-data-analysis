---
title: "上下文工程（Context Engineering）"
type: concept
tags: [llm, context, engineering, agent]
sources: [llm-context-material, concept-relationship-summary]
last_updated: 2026-09-10
---

## 定义

由 [[LLMContext]] 的三条性质（有限、共享、位置敏感）推演出的工程实践：**决定什么信息、在什么时机、以什么形式、放在什么位置进入上下文，以及何时清理过期内容。**

因为模型每一步只依据窗口内容作答，Agent 的决策质量几乎完全取决于当时上下文里装了什么——所以 **Agent 工程的核心就是上下文工程**。

## 四个作用层面

1. **视野边界**：没读进来、没写进提示词的历史等于不存在——能力上限不是「模型会不会」，而是「上下文里有没有」。
2. **组成决定稳定性**：系统提示定基调、工具定义定能力、对话历史定连贯、记忆/文档定项目规矩。
3. **失效模式**：有限 → 膨胀与遗忘；共享 → 污染（过期工具输出持续误导）；位置敏感 → 中段被忽略。
4. **反馈闭环**：上下文质量 → 决策质量 → 行动结果；需要主动压缩历史、清理失败尝试的痕迹。

## 常用手段

- **压缩（compaction）**：长对话逼近上限时把历史摘要化，丢掉冗余工具输出。
- **检索增强（RAG）**：窗口装不下整个文档库，就只把相关片段塞进去。
- **渐进式披露**：[[ProgressiveDisclosure]] —— 启动只装元数据，按需加载正文。
- **子智能体 / 外存**：把中间状态写进文件，需要时再读回，而不是无限依赖窗口。

## 相关来源

- [[llm-context-material]] —— 机制基础
- [[concept-relationship-summary]] —— 上下文工程的完整论述

## 相关页面

[[LLMContext]] · [[ProgressiveDisclosure]] · [[Skill]] · [[AgentSkill]]
