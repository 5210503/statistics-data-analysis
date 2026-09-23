---
title: "Agent Skill（Anthropic Agent Skills 格式）"
type: source
tags: [ai-concept, agent, skill]
date: 2026-09-06
last_updated: 2026-09-10
source_file: raw/ai-concepts/agent-skill.md
---

## 摘要

Agent Skill 是 Anthropic 提出的智能体扩展格式：一个文件夹，唯一必需的文件是 `SKILL.md`，用 YAML frontmatter 的 `name` 与 `description` 声明身份和触发条件。核心机制是**渐进式披露（progressive disclosure）**——启动时系统提示词只装入每个 Skill 的 name + description（约 100 tokens/个），任务匹配后才读取正文，正文引用的捆绑文件再按需读取。它把「通用模型懂原理、不懂你的流程」这件事，用文件夹而非代码的方式解决。

## 关键主张

- 本质是**用文件夹而非代码，把专业知识「挂」到智能体身上**。
- 渐进式披露让几十个 Skill 常驻的成本压到极低，正文与脚本只在需要时才进入上下文。
- 官方四特性：可组合、可移植（2025-12 起为开放标准，30+ 工具通用）、高效、强大（可含可执行代码）。
- **Skill ≠ 微调 / RAG**：不改模型权重、不建向量库，只是智能体按需读取的文件。
- 触发完全依赖 `description`——描述含糊，Skill 就永远不会被用上。

## 关键引用

> 用文件夹而非代码，把专业知识「挂」到智能体身上。

> 脚本直接执行，不占上下文。

## 关联

- [[AgentSkill]] —— 本页对应的核心概念页
- [[ProgressiveDisclosure]] —— 支撑该格式的核心加载机制
- [[MCP]] —— 常与 Skill 混淆：Skill 管「怎么做」，MCP 管「连什么」
- [[Anthropic]] —— 该格式的提出方
- [[skill-material]] —— 姊妹资料，讲 Skill 的通用含义与四层结构

## 矛盾 / 待澄清

无。与 [[skill-material]] 的差异是视角而非冲突：本页聚焦 Anthropic 的具体格式规范，姊妹页聚焦 Skill 的通用概念。
