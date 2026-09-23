---
title: "Agent Skill"
type: concept
tags: [agent, skill, anthropic, standard]
sources: [agent-skill-material, skill-material, concept-relationship-summary]
last_updated: 2026-09-10
---

## 定义

Anthropic 提出的智能体扩展格式：一个文件夹，唯一必需的文件是 `SKILL.md`。`SKILL.md` 的 YAML frontmatter 必填 `name` 与 `description`，正文写指令与工作流，文件夹里可捆绑脚本和资源。它是 [[Skill]] 这个通用概念在 Anthropic 体系下的具体规范。

## 为什么需要它

通用模型懂原理，却不懂你的流程——品牌规范、代码审查清单、PDF 表单填写步骤。过去每次对话都要重新解释，现在打包一次、处处复用。一句话：**用文件夹而非代码，把专业知识「挂」到智能体身上。**

## 核心机制

**[[ProgressiveDisclosure|渐进式披露]]**：系统提示词只常驻每个 Skill 的 name + description（约 100 tokens/个）→ 任务匹配才读取正文 → 正文引用的捆绑文件再按需读取；捆绑脚本直接执行，不进上下文。

官方四特性：**可组合**（多 Skill 自动叠加）、**可移植**（跨 Claude 应用 / Claude Code / API，2025-12 起为开放标准，30+ 工具通用）、**高效**（按需加载）、**强大**（可含可执行代码）。

## 边界与易混淆

- 与 [[MCP]] 的区别：Skill 是**静态文件**，解决「怎么做」；MCP 是**运行时协议**，解决「连什么」。
- 与微调 / RAG 的区别：不改权重、不建向量库，零训练成本换取「知道流程」，而非「学会新知识」。
- 触发由 `description` 决定——描述含糊则永不触发；执行捆绑脚本需要代码执行环境。

## 相关来源

- [[agent-skill-material]] —— 格式规范的一手整理
- [[skill-material]] —— Skill 的通用概念
- [[concept-relationship-summary]] —— 在整体关系中的位置

## 相关页面

[[Skill]] · [[ProgressiveDisclosure]] · [[LLMContext]] · [[MCP]] · [[Anthropic]] · [[WorkBuddy]]
