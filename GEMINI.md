# LLM Wiki · 个人知识库维护规范（Schema）

> 本文件是本知识库的「宪法」，面向 **Gemini CLI**。
>
> **在读写本仓库任何文件之前，先完整读完本文件，并严格按其中的约定操作。**
>
> 核心分工：**人负责选材与提问，AI 负责其余全部维护工作**（摘要、交叉引用、建页、记日志、标矛盾）。
>
> 用 Claude Code 时以 `CLAUDE.md` 为准、用 Codex 时以 `AGENTS.md` 为准——三者内容等价，只是入口不同。

---

## 0. 这是什么

- **名称**：个人知识库（仓库 `statistics-data-analysis`）
- **覆盖主题**：AI 概念（Agent / 上下文 / Skill 等）+ 统计与数据分析
- **语言**：正文简体中文；关键术语保留英文原名（首次出现用「中文（English）」）
- **范式**：LLM Wiki —— 原始资料先被「编译」成结构化 wiki，之后所有问答都基于 wiki，而不是每次重新检索原文

### 三层架构（不可越界）

| 层 | 目录 | 谁维护 | 规则 |
|---|---|---|---|
| 原始资料 | `raw/` | **只由人放入** | 不可变；AI 只读，永不修改、永不删除 |
| 结构化 wiki | `wiki/` | **AI 全权维护** | AI 建页、改页、维护交叉引用与索引 |
| 规范 | `GEMINI.md`（本文件） | 人与 AI 共同迭代 | 约定目录、页面格式、工作流 |

---

## 1. 触发方式

| 意图 | 说法示例 |
|---|---|
| **ingest** 吸收新资料 | `ingest raw/ai-concepts/skill.md` |
| **query** 提问 | `query：Agent 和 Skill 有什么区别？` |
| **health** 结构体检 | `health`、`检查知识库结构` |
| **lint** 内容体检 | `lint 知识库` |
| **graph** 建图谱 | `build graph` |
| **graph report** 图谱体检 | `graph report` |

---

## 2. 目录结构

```
raw/                     # 不可变原始资料
  ai-concepts/           #   AI 概念相关原始文档
  statistics/            #   统计与数据分析原始文档
wiki/                    # AI 维护的结构化知识层
  index.md               #   全部页面的目录（每次 ingest 后更新）
  log.md                 #   只追加的时间线记录
  overview.md            #   跨全部资料的「活的综述」
  sources/               #   一篇来源文档 = 一个摘要页（kebab-case.md）
  entities/              #   人物 / 公司 / 产品 / 项目（TitleCase.md）
  concepts/              #   概念 / 框架 / 方法（TitleCase.md）
  syntheses/             #   问答沉淀页、横向对比
graph/                   # 知识图谱产物（graph.json / graph.html）
tools/                   # 独立 Python 脚本（纯标准库，无需 API Key）
  health.py              #   结构完整性检查（零 LLM 调用）
  lint.py                #   结构 + 图谱质量检查（确定性部分）
  build_graph.py         #   从 [[wikilinks]] 构建知识图谱
  check_graph_html.js    #   可选：深度校验 graph.html（需 Node.js）
```

---

## 3. 页面格式

```yaml
---
title: "页面标题"
type: source | entity | concept | synthesis
tags: []
sources: []          # 支撑本页的来源页 slug 列表
last_updated: YYYY-MM-DD
---
```

正文用 `[[页面名]]` 做 wikilink。**务必保证 wikilink 指向真实存在的页面。**

---

## 4. Ingest 工作流

触发：*"ingest &lt;文件&gt;"*

**支持格式**：`.md` 直接读取；其他格式（`.pdf` `.docx` `.pptx` `.xlsx` `.html` `.txt` `.csv` `.json` `.xml` `.epub` 等）先用 [markitdown](https://github.com/microsoft/markitdown) 转成 markdown。

1. 读完源文件（非 markdown 先转换）
2. 读 `wiki/index.md` 与 `wiki/overview.md`
3. 写 `wiki/sources/<slug>.md`
4. 更新 `wiki/index.md`（Sources 段）
5. 更新 `wiki/overview.md`（如整体图景有变）
6. 建或更新相关 `entities/` 与 `concepts/` 页面
7. **标矛盾**：冲突处加 `## 矛盾 / 待澄清`
8. 追加 `wiki/log.md`：`## [YYYY-MM-DD] ingest | <标题>`
9. **收尾校验（三件套不能省）**：依次跑 `python tools/health.py`（断链/索引/日志）→ `python tools/lint.py`（内容 + 图谱感知）→ `python tools/build_graph.py`（**必须重跑，否则图谱停留在旧状态**），最后输出变更摘要

### 来源页格式

```markdown
---
title: "来源标题"
type: source
tags: []
date: YYYY-MM-DD
source_file: raw/...
---

## 摘要
2–4 句话。

## 关键主张
- 主张 1

## 关键引用
> "原文引用" —— 语境

## 关联
- [[ConceptName]] —— 如何相关

## 矛盾 / 待澄清
- 与 [[OtherPage]] 冲突之处：……
```

**领域模板**：学习笔记 → `一句话本质 / 核心机制 / 应用场景 / 易混淆 · 边界 / 可核查来源 / 自测题`；课程笔记 → `本讲要解决的问题 / 核心概念 / 代码实践 / 小结 / 思考题`。

---

## 5. Query 工作流

触发：*"query: &lt;问题&gt;"*

1. 读 `wiki/index.md` 定位相关页面 → 2. 读这些页面 → 3. 综合答案并用 `[[页面名]]` 标注出处 → 4. 询问是否沉淀为 `wiki/syntheses/<slug>.md`

---

## 6. Health 工作流（零成本）

触发：*"health"* → `python tools/health.py`（`--json` 取机器可读结果）

检查项（**零 LLM 调用**）：空文件 / 存根、索引同步、日志覆盖。`--save` 写入 `wiki/health-report.md`。

| 维度 | `health` | `lint` |
|---|---|---|
| 关注点 | 结构完整性 | 内容质量 |
| LLM 调用 | 零 | 有 |
| 频率 | 每次开工前 | 每 10–15 次 ingest 后 |
| 工具 | `tools/health.py` | `tools/lint.py` + Agent |

> 先 health 再 lint：给空文件做语义分析纯属浪费 token。

---

## 7. Lint 工作流

触发：*"lint 知识库"*

- **确定性部分**（`python tools/lint.py`）：孤立页、断链、稀疏页（出链 < 2）、缺失实体页
- **图谱感知**：Hub 存根、脆弱桥、孤立社区
- **语义部分**（Agent 完成）：矛盾、过时摘要、数据缺口

输出报告，询问是否保存到 `wiki/lint-report.md`。

---

## 8. Graph 工作流

触发：*"build graph"* → `python tools/build_graph.py`

- Pass 1：解析全部 `[[wikilinks]]` → EXTRACTED 边
- Pass 2：推断隐性关系 → INFERRED / AMBIGUOUS 边（带置信度）
- 社区检测聚类着色 → 产出 `graph/graph.json` + 自包含 `graph/graph.html`

**图谱健康报告**（*"graph report"* / `--report`）：健康摘要、孤立节点、God nodes、脆弱桥、幻影枢纽（被 ≥2 页引用却不存在 —— 「该建页」信号）。

> 幻影枢纽只报告、绝不自动建页。

---

## 9. 命名约定

来源页 `kebab-case.md`；实体页 / 概念页 `TitleCase.md`；综合页 `kebab-case.md`。

## 10. index.md / log.md 格式

index 分 Overview / Sources / Entities / Concepts / Syntheses 五段。

log 每条为 `## [YYYY-MM-DD] <操作> | <标题>`；操作类型：`ingest` / `query` / `health` / `lint` / `graph` / `report` / `init`。

---

## 11. Phase 3 设计约束（自动建链 · 尚未启用）

- 自动边先为 `DRAFT`，经 `promote` 校验后才物化为 `[[wikilinks]]`
- 链接密度预算：页面 ≥2 条出链才允许晋级
- **HG-WA-01**：图谱层不得因断链自动建页——只报告
- **HG-WA-02**：新增命令不得与既有命令职责重叠

---

## 12. 红线（必须遵守，无例外）

1. **禁止编造来源**：任何 URL 与文献必须真实、可访问、可核查。不确定就标「待核实」。
2. **不得改动 `raw/`**：原始资料层只读。
3. **不确定不臆断**：拿不准的结论标「存疑」。
4. **矛盾立即标记**。
5. **保持格式统一**：新页面必须带 frontmatter、登记 `index.md`、追加 `log.md`。
