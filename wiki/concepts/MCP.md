---
title: "MCP（Model Context Protocol）"
type: concept
tags: [agent, protocol, integration]
sources: [agent-skill-material]
last_updated: 2026-09-10
---

## 定义

MCP 是**连接外部系统的协议**，解决「Agent 能连什么」——数据库、SaaS API、实时数据源等运行时接口。它是理解 [[AgentSkill]] 边界时必须并列掌握的概念。

## 与 Skill 的分工

| 对比项 | [[Skill]] | MCP |
|---|---|---|
| 本质 | 装专业知识的**文件夹** | 连接外部系统的**协议** |
| 解决 | 「怎么做」（流程、规范） | 「连什么」（数据源、工具接口） |
| 形态 | 静态文件，按需读取 | 运行时连接，实时调用 |
| 典型例子 | 品牌规范、文档处理流程 | 接数据库、调用 SaaS API |

## 判定规则

- 需求是**静态流程知识**（每次代码审查都执行同一份 12 条清单）→ 用 Skill。
- 需求是**运行时实时连接外部数据**（实时查询公司内部数据库）→ 用 MCP。

## 边界

Skill 只是文件，**没有连接能力**；MCP 只是通道，**不封装流程知识**。二者常配合使用：MCP 取回数据，Skill 规定怎么处理。

## 相关来源

- [[agent-skill-material]] —— 该对比的出处

## 相关页面

[[AgentSkill]] · [[Skill]] · [[Anthropic]]
