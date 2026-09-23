---
title: "Skill"
type: concept
tags: [agent, skill, reusable-capability]
sources: [skill-material, agent-skill-material, concept-relationship-summary]
last_updated: 2026-09-10
---

## 定义

Skill 是为 Agent 封装沉淀出来的**可复用任务能力模板**。一句话本质：**任务能力的封装复用载体。** 它把任务流程与规则提前写进文件固化，需要时直接加载调用，避免每次把完整要求重复写进提示词。

Anthropic 的具体格式规范见 [[AgentSkill]]；本页讲通用概念。

## 为什么需要它

重复执行的任务若每次都重写指令，既低效又挤占上下文。Skill 把「怎么做事」的方法论从对话中抽出来，固化为可重复加载的知识单元。

## 四层结构

1. **元数据头部**：YAML frontmatter —— `name`、`description`、`allowed-tools`（工具权限白名单）
2. **角色与规则定义**：身份、适用场景、输入输出格式与约束
3. **执行步骤流程**：标准化操作流水线
4. **自检规则**：完成后的校验清单

## 加载机制

[[ProgressiveDisclosure|渐进式披露]]：未匹配时零成本躺在库里；匹配到任务才把正文注入上下文窗口；执行受 `allowed-tools` 约束；最后由自检规则校验输出。

## 边界与易混淆

| | Skill | 普通提示词 | 记忆（Memory） |
|---|---|---|---|
| 沉淀 | 怎么做：流程、规则 | 当次指令 | 发生过什么：事实、偏好 |
| 生命周期 | 固化文件、反复加载 | 对话结束即失效 | 跨会话持久 |
| 触发 | Agent 按 description 自动匹配 | 用户手动输入 | 按需检索注入 |

**边界**：Skill 不是越长越好——触发后全文进入上下文，冗长会挤占空间、稀释注意力、导致任务失败。正确做法是精简高信号内容，细节放附件按需读取。

## 相关来源

- [[skill-material]] —— 通用概念整理
- [[agent-skill-material]] —— 格式规范
- [[concept-relationship-summary]] —— Skill 与上下文的分工

## 相关页面

[[AgentSkill]] · [[ProgressiveDisclosure]] · [[LLMContext]] · [[ConceptMaterialGenerator]] · [[WorkBuddy]]
