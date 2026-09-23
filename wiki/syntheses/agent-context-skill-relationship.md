---
title: "Agent、上下文与 Skill 的三层关系"
type: synthesis
tags: [agent, context, skill, synthesis]
sources: [concept-relationship-summary, skill-material, llm-context-material, agent-skill-material]
last_updated: 2026-09-10
---

> 本页是知识库的第一份综合页：由 [[concept-relationship-summary]] 沉淀而来，回答「Agent、大模型上下文、Skill 三者到底怎么配合」。详细机制的展开见对应概念页。

## 一句话结论

**Agent 以大模型为大脑，以上下文为短期工作内存，以 Skill 为可插拔的技能库；上下文决定当下表现，Skill 决定长期复利。**

## 三者定位

| 角色 | 是什么 | 关键性质 |
|---|---|---|
| 大模型 LLM | 推理引擎，负责理解、决策、生成 | 每次醒来都是失忆的 |
| [[LLMContext]]（上下文） | 生成每个字时能「看见」的全部内容 | 有限、共享、位置敏感 |
| [[Skill]] | 可复用的任务能力模板 | 按需注入，用到才翻开 |

## 两条主线

**一、上下文决定 Agent 的工作质量。** Agent 的每一次决策几乎完全取决于当时窗口里装了什么——没读进来、没写进提示词的信息，对 Agent 而言等于不存在。因此 [[ContextEngineering|上下文工程]] 才是 Agent 工程的核心：决定什么信息、在什么时机、以什么形式、放在什么位置进入上下文。

**二、Skill 沉淀可复用的任务知识。** 上下文是单次请求的工作内存，跨会话不留痕；若「怎么做事」只存在于某次对话里，下次就得从零摸索。Skill 用四层结构（元数据 / 规则 / 流程 / 自检）把方法论固化，并以 [[ProgressiveDisclosure|渐进式披露]] 与上下文的稀缺性达成平衡。

## 闭环

```
接到任务 → 组装上下文（系统提示 + 工具 + 历史 + Skill 正文）
        → 模型推理 → 调用工具 → 结果写回上下文
        → 清理污染 / 压缩历史 → 继续
任务完成后 → 新经验沉淀回 Skill（长期复利）
```

## 本仓库的实例

[[ConceptMaterialGenerator]] 是 [[Skill]] 的活样本；它生成的三份资料被 ingest 为 [[Skill]]、[[AgentSkill]]、[[LLMContext]] 三个概念页，共同构成本综合页的证据基础——**这套「上下文 + Skill」的关系，本知识库本身就是它的一个完整实例。**

## 相关页面

[[Skill]] · [[LLMContext]] · [[AgentSkill]] · [[ContextEngineering]] · [[ProgressiveDisclosure]] · [[concept-relationship-summary]]
