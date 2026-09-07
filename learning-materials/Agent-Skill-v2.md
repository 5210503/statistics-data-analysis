# Agent Skill（v2 · 深入版）

> 概念学习资料 · 生成日期：2026-09-06 · 生成工具：concept-material-generator
> v1 讲"是什么"（见 [Agent-Skill.md](Agent-Skill.md)）；本版讲"怎么写好"。

## 1. 概念个人解释

写 skill 不是编程，是给智能体写一份**能被正确发现的 SOP**。一个 skill 的命运系于两处文字：description 决定它会不会被用，正文决定它做得对不对。

description 是唯一的"广告位"——agent 平时只看得见这一句，写模糊的结局不是"偶尔用错"，而是**永远不会被用**。

一句话本质：**description 是触发条件，正文是说明书，附件是弹药库。**

## 2. 核心机制或组成

作者视角下，你能控制的只有三层，每层写差都有明确后果：

```mermaid
flowchart LR
    A["① description<br/>做什么 + 何时用"] --> B["② 正文<br/>单一工作流 + 示例"] --> C["③ 附件<br/>细节按需加载"]
```

- ① 写模糊 → 永不触发；② 写臃肿 → 拖累上下文；③ 全堆进正文 → 违背渐进披露

frontmatter 硬性规则（官方）：

- `name`：小写连字符，≤ 64 字符，不得含 "claude" / "anthropic"
- `description`：写清"做什么 + 何时用"；上传校验上限 1,024 字符

官方定义的"好 skill"五个特征：特定可重复的任务、清晰指令、含示例、明确何时使用、**聚焦单一工作流**。

## 3. 具体应用场景

1. **skill-creator 创建 skill**：官方内置技能，对话式引导生成文件夹结构与 SKILL.md，无需手写。
2. **评测驱动开发**：官方建议先跑任务找能力缺口再写 skill；上线后若 Claude 不在预期时机触发，**迭代 description**。
3. **企业知识固化**：品牌规范打包成 skill 的官方案例——颜色、字体、logo 用法一次成型，文档生成自动遵循。
4. **官方示例库取经**：[anthropics/skills](https://github.com/anthropics/skills) 中的 docx/pdf/pptx/xlsx 是生产级参考，可读源码学习拆分模式。

## 4. 容易混淆的问题或使用边界

| 维度 | 好 skill | 差 skill |
|---|---|---|
| 触发 | description 写明"当…时使用" | 只描述功能，不含时机 |
| 范围 | 单一工作流 | 一个 skill 包揽一切 |
| 示例 | 少量典型输入输出 | 穷举规则的"洗衣单" |

**Skill vs 系统提示词**：全局常驻（任何任务都要遵守的规范）放系统提示；按需加载（特定任务才用的知识）放 skill——判断标准是"是否每次都需要"。

**使用边界**：一次性任务不值得建 skill；多个聚焦的小 skill 组合优于一个臃肿的大 skill（组合性与触发精度都更好）；API 场景下依赖须预装，不能运行时装包。

## 5. 可核查资料来源链接

1. [How to create custom skills — Anthropic 帮助中心](https://support.claude.com/en/articles/12512198-creating-custom-skills)：官方创建指南，name/description 规则、"聚焦单一工作流"等最佳实践的一手出处。
2. [anthropics/skills — GitHub 官方仓库](https://github.com/anthropics/skills)：官方示例库（含生产级文档技能、规范与模板），学拆分模式的原始材料。
3. [Equipping agents for the real world with Agent Skills — Anthropic 工程博客](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)：评测驱动开发、渐进式披露设计的工程深潜。

## 6. 自测题

**Q1（识别）** `name` 和 `description` 各有哪些硬性规则？请各说至少两条。

<details><summary>答案</summary>

name：小写连字符、≤64 字符、不得含 "claude"/"anthropic"。description：写清做什么+何时用、上传校验上限 1,024 字符。
</details>

**Q2（理解）** 为什么官方强调"多个聚焦的小 skill 优于一个全能大 skill"？给出两个理由。

<details><summary>答案</summary>

① 触发精度：description 范围越窄，agent 判断越准；② 组合性：小 skill 可按需叠加，渐进披露让每个只在该用时加载——大 skill 一触发就把无关工作流全灌进上下文。
</details>

**Q3（应用）** 把这条模糊的 description 改成带触发条件的版本："处理公司的文档。"

<details><summary>答案</summary>

示例："当用户要求创建或修改公司文档（周报、公告、对外函件）时使用：套用公司品牌规范（字体、配色、logo），遵循 data/templates/ 中的最新模板。"要点：写明何时用、覆盖哪些任务、指向资源。
</details>

**Q4（辨析）** "回复必须始终用简体中文"和"填写 PDF 表单的流程"——分别该放系统提示词还是 skill？为什么？

<details><summary>答案</summary>

前者放系统提示词：全局生效、每次都需要、内容极短，做成 skill 反而多一层触发风险。后者放 skill：特定任务才用、内容较多、按需加载正合适。判断标准是"是否每次都需要 + 内容体量"。
</details>
