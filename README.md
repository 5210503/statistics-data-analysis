# 统计与数据分析 · 学习仓库

一个双用途的个人学习仓库：**统计与数据分析课程**的笔记、代码与练习，以及借助 **concept-material-generator Skill** 自动生成的 **AI 概念学习资料**。

## 1. 仓库用途

- **统计学习主线**：从零基础到能独立完成一份数据分析报告（描述统计 → 概率 → 推断 → 回归 → 实战）。
- **AI 概念学习支线**：输入任意 AI 概念名词（不限于 Agent、上下文、Skill，覆盖机器学习、NLP、CV、强化学习、MLOps 等），由 Skill 自动生成结构统一、来源可核查的概念学习资料，沉淀到 `learning-materials/`，逐步构建个人 AI 概念知识库。
- 附带概念关系类总结文档（如根目录的 `concept-relationship.md`，说明 Agent、大模型上下文、Skill 三者关系）。

## 2. Skill 存放路径

| 项目 | 路径 |
|------|------|
| Skill 定义文件 | `.workbuddy/skills/concept-material-generator/SKILL.md` |
| Skill 输出目录 | `learning-materials/` |
| 输出索引文件 | `learning-materials/index.md` |

## 3. WorkBuddy 如何调用该 Skill

1. **触发**：在 WorkBuddy 对话中直接给出一个 AI 概念名词并表达"生成学习资料"的意图，例如"帮我生成 LoRA 的学习资料"、"给我做一份 RAG 的学习笔记"。Skill 的 `description` 字段声明了适用场景，WorkBuddy 据此自动匹配并加载 SKILL.md。
2. **加载**：SKILL.md 的完整指令（含 allowed-tools: Read、Write、WebSearch、WebFetch）被注入当次对话上下文，Agent 按 Skill 中定义的固定流程执行——这正是"Skill 把做事方法沉淀为可按需注入的知识单元"的实例。
3. **执行流程**（Skill 内固定八步）：解析概念 → 读索引查重（同名概念另存 `-v2.md`）→ WebSearch/WebFetch 去原始出处查证一手资料 → 筛选 2-5 条核实过的链接 → 按固定六部分模板撰写 → 保存到 `learning-materials/<概念名>.md` → 更新索引 → 逐项自检后汇报。
4. **输出结构**：固定六部分——概念个人解释 / 核心机制或组成（含 1-3 张 Mermaid 图）/ 具体应用场景 / 易混淆问题或使用边界 / 可核查资料来源链接 / 难度递进自测题（答案折叠）。

## 4. 已经生成的学习资料

详见 `learning-materials/index.md`（新资料生成后由 Skill 自动同步更新）。目前已生成：

| 概念 | 文件 | 生成日期 | 一句话简介 |
|------|------|----------|------------|
| Agent Skill | `learning-materials/Agent-Skill.md` | 2026-09-06 | Anthropic 的智能体扩展格式：文件夹 + SKILL.md，渐进式披露按需加载 |
| 大模型上下文 | `learning-materials/大模型上下文.md` | 2026-09-06 | 模型生成时可见的全部内容：有限、共享、位置敏感的"工作记忆" |
| Skill | `learning-materials/Skill.md` | 2026-09-09 | 为 Agent 封装的可复用任务能力模板：元数据 + 规则 + 流程 + 自检，按需注入上下文 |

另有概念关系总结文档（非 Skill 生成）：根目录 `concept-relationship.md`（Agent、大模型上下文、Skill 三者关系，2026-09-09 更新，与三份学习资料交叉引用）。

## 5. 人工核查与修改说明

AI 生成的资料**必须人工核查后才能当作可靠学习依据**，每次收到新生成的文档后，按以下三项核对：

### 核对链接（最优先）
- 逐条检查三份笔记「可核查资料来源链接」，删除AI生成的虚构链接，替换为WorkBuddy、Anthropic官方真实可访问网页链接，保证链接可正常打开。

### 修正概念错误
- 通读三份文档，修正部分概念描述模糊的地方；区分Agent与Skill的边界，补充二者的对比辨析，避免概念混淆。

### 补充个人理解
- 在每篇笔记的概念个人解释部分，用自己的话改写总结，加入自己对概念本质的理解；
- 完善Skill文档的自测题、应用场景，结合本次项目作业案例，保持文档六段结构完整不变。

>修订记录：2026‑09‑07，完善Agent、大模型的上下文、Skill三份学习笔记，替换真实参考链接，补充个人理解与概念辨析。
#加实际案例。
- 人工修改后无需改动索引，但建议保持文档的六部分结构不变，便于跨概念横向对比。

## 附：仓库结构

```
statistics-data-analysis/
├── README.md                        # 本文件
├── progress.md                      # 统计学习进度打卡
├── concept-relationship.md          # Agent / 上下文 / Skill 三者关系总结
├── notes/                           # 章节笔记（Markdown）
├── data/                            # 练习用的数据集
├── exercises/                       # 课后练习代码（Python）
├── learning-materials/              # Skill 生成的 AI 概念学习资料
│   └── index.md                     # 学习资料索引（查重 + 目录）
└── .workbuddy/
    └── skills/
        └── concept-material-generator/
            └── SKILL.md             # 概念学习资料生成器 Skill
```
