# 知识库索引

> 本文件由 AI 在每次 ingest 后维护。查询时先读这里定位页面，再深入具体页。
> 维护规范见 [CLAUDE.md](../CLAUDE.md)。

## Overview
- [综述](overview.md) — 跨全部资料的「活的整体图景」

## Sources
- [Agent Skill（Anthropic 格式）](sources/agent-skill-material.md) — 文件夹 + SKILL.md，渐进式披露的智能体能力包
- [大模型上下文](sources/llm-context-material.md) — 有限、共享、位置敏感的「工作记忆」
- [Skill（通用概念）](sources/skill-material.md) — 可复用任务能力模板的四层结构
- [Agent / 上下文 / Skill 三者关系](sources/concept-relationship-summary.md) — 横向总结：上下文决定当下表现，Skill 决定长期复利
- [第 01 讲 · 描述性统计](sources/descriptive-statistics-01.md) — 集中趋势、离散程度、分布形态与 Python 上手

## Entities
- [Anthropic](entities/Anthropic.md) — Agent Skills 格式与开放标准的提出方
- [WorkBuddy](entities/WorkBuddy.md) — 本仓库的 AI 助手运行环境，支持 Skills
- [concept-material-generator](entities/ConceptMaterialGenerator.md) — 本仓库生成 AI 概念资料的 Skill 项目

## Concepts
- [Agent Skill](concepts/AgentSkill.md) — Anthropic 的具体格式规范：文件夹 + SKILL.md
- [Skill](concepts/Skill.md) — 通用概念：为 Agent 封装的可复用任务能力模板
- [大模型上下文](concepts/LLMContext.md) — 模型生成时可见的全部内容与其三条性质
- [上下文工程](concepts/ContextEngineering.md) — 由上下文稀缺性推演出的工程实践
- [渐进式披露](concepts/ProgressiveDisclosure.md) — 按需加载：启动只装元数据
- [MCP](concepts/MCP.md) — 连接外部系统的协议，与 Skill 的分工辨析
- [描述性统计](concepts/DescriptiveStatistics.md) — 用少数几个数字概括一大堆数据

## Syntheses
- [Agent、上下文与 Skill 的三层关系](syntheses/agent-context-skill-relationship.md) — 回答三者如何配合，及其在本仓库中的实例
