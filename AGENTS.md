# LLM Wiki · 个人知识库维护规范（Schema）

> 本文件是本知识库的「宪法」，面向 **Codex / OpenCode 及任何读取 `AGENTS.md` 的通用 Agent**。
>
> 读到这里就先停下：**在读写本仓库任何文件之前，先完整读完本文件，并严格按其中的约定操作。**
>
> 核心分工：**人负责选材与提问，AI 负责其余全部维护工作**（摘要、交叉引用、建页、记日志、标矛盾）。
>
> 用 Claude Code 时以 `CLAUDE.md` 为准、用 Gemini CLI 时以 `GEMINI.md` 为准——三者内容等价，只是入口不同。

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
| 规范 | `AGENTS.md`（本文件） | 人与 AI 共同迭代 | 约定目录、页面格式、工作流 |

---

## 1. 触发方式

用自然语言即可，AI 按本节识别意图：

| 意图 | 说法示例 |
|---|---|
| **ingest** 吸收新资料 | `ingest raw/ai-concepts/skill.md`、`把这份新资料吸收进知识库` |
| **query** 提问 | `query：Agent 和 Skill 有什么区别？`、`知识库里关于上下文工程说了什么？` |
| **health** 结构体检 | `health`、`检查知识库结构` |
| **lint** 内容体检 | `lint 知识库`、`找找有没有孤立页和矛盾` |
| **graph** 建图谱 | `build graph`、`生成知识图谱` |
| **graph report** 图谱体检 | `graph report`、`图谱健康报告` |

---

## 2. 目录结构

```
raw/                     # 不可变原始资料（source of truth）
  ai-concepts/           #   AI 概念相关原始文档
  statistics/            #   统计与数据分析原始文档
wiki/                    # AI 维护的结构化知识层
  index.md               #   全部页面的目录（每次 ingest 后更新）
  log.md                 #   只追加的时间线记录
  overview.md            #   跨全部资料的「活的综述」
  sources/               #   一篇来源文档 = 一个摘要页（kebab-case.md）
  entities/              #   人物 / 公司 / 产品 / 项目（TitleCase.md）
  concepts/              #   概念 / 框架 / 方法（TitleCase.md）
  syntheses/             #   问答沉淀页、横向对比、综合分析
graph/                   # 知识图谱产物
  graph.json             #   节点/边数据（由 tools/build_graph.py 生成）
  graph.html             #   自包含可视化，双击即可在浏览器打开
tools/                   # 独立 Python 脚本（纯标准库，无需 API Key）
  health.py              #   结构完整性检查（零 LLM 调用）
  lint.py                #   结构 + 图谱质量检查（确定性部分）
  build_graph.py         #   从 [[wikilinks]] 构建知识图谱
docs/                    # 进阶说明
```

---

## 3. 页面格式

每个 wiki 页面都必须带 YAML frontmatter：

```yaml
---
title: "页面标题"
type: source | entity | concept | synthesis
tags: []
sources: []          # 支撑本页的来源页 slug 列表
last_updated: YYYY-MM-DD
---
```

正文里用 `[[页面名]]` 做 wikilink（Obsidian 兼容，也是图谱连边的依据）。

**务必保证 wikilink 指向真实存在的页面**——宁可先不写链接，也不要指向空页。

---

## 4. Ingest 工作流（吸收一篇原始资料）

触发：*"ingest &lt;文件&gt;"*

**支持格式**：`.md` 直接读取。其他格式（`.pdf` `.docx` `.pptx` `.xlsx` `.html` `.txt` `.csv` `.json` `.xml` `.rst` `.rtf` `.epub` `.ipynb` `.yaml` `.yml` `.tsv`）先用 [markitdown](https://github.com/microsoft/markitdown) 转成 markdown 再吸收。

按顺序执行：

1. 读完 `raw/` 下的源文件（非 markdown 先转换）
2. 读 `wiki/index.md` 与 `wiki/overview.md`，掌握现有知识版图
3. 写 `wiki/sources/<slug>.md`（格式见下）
4. 更新 `wiki/index.md` —— 在 Sources 段加入本页
5. 更新 `wiki/overview.md` —— 若本资料改变了整体图景，就修订综述
6. 为关键人物 / 公司 / 产品 / 项目建或更新 `wiki/entities/` 页面
7. 为关键概念 / 框架 / 方法建或更新 `wiki/concepts/` 页面
8. **标矛盾**：与已有内容冲突时，在受影响页面加 `## 矛盾 / 待澄清` 小节
9. 追加 `wiki/log.md`：`## [YYYY-MM-DD] ingest | <标题>`
10. **收尾校验**：检查有无指向不存在页面的 `[[wikilinks]]`；确认所有新页都进了 `index.md`；输出变更摘要

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
- [[EntityName]] —— 如何相关

## 矛盾 / 待澄清
- 与 [[OtherPage]] 冲突之处：……
```

### 领域模板（按资料类型选用）

**学习笔记 / 概念资料模板**：`## 一句话本质` / `## 核心机制` / `## 应用场景` / `## 易混淆 · 边界` / `## 可核查来源` / `## 自测题`
**课程笔记模板**：`## 本讲要解决的问题` / `## 核心概念` / `## 代码实践` / `## 小结` / `## 思考题`

---

## 5. Query 工作流（提问）

触发：*"query: &lt;问题&gt;"*

1. 读 `wiki/index.md` 定位相关页面
2. 用 Read 读这些页面
3. 综合出答案，用 `[[页面名]]` 行内标注出处
4. **主动询问**：是否把这条答案沉淀为 `wiki/syntheses/<slug>.md`

> 好答案要回填进 wiki——你的探索和 ingest 的资料一样会「复利」。

---

## 6. Health 工作流（结构体检，零成本）

触发：*"health"* → 运行 `python tools/health.py`（或 `--json` 取机器可读结果）

检查项（**零 LLM 调用**）：
- **空文件 / 存根**：除 frontmatter 外没有内容的页面
- **索引同步**：`index.md` 条目 vs 磁盘真实文件
- **日志覆盖**：有来源页却缺对应 `ingest` 日志

`--save` 可写入 `wiki/health-report.md`。

### Health 与 Lint 的边界

| 维度 | `health` | `lint` |
|---|---|---|
| **关注点** | 结构完整性 | 内容质量 |
| **LLM 调用** | 零 | 有（语义分析） |
| **成本** | 免费 | 消耗 token |
| **频率** | 每次开工前 | 每 10–15 次 ingest 后 |
| **工具** | `tools/health.py` | `tools/lint.py` + Agent |

> 先 health 再 lint：给空文件做语义分析纯属浪费 token。

---

## 7. Lint 工作流（内容体检）

触发：*"lint 知识库"*

**确定性部分**（可先跑 `python tools/lint.py`）：孤立页、断链、稀疏页（出链 < 2）、缺失实体页（被 3+ 页提及却无独立页）。

**图谱感知检查**（需先 `build graph`）：Hub 存根（度数 > μ+2σ 却内容稀薄）、脆弱桥（社区间仅 1 条边）、孤立社区。

**语义部分**（Agent 用 Grep + Read 完成）：矛盾、过时摘要、数据缺口。

输出 lint 报告，询问是否保存到 `wiki/lint-report.md`。

---

## 8. Graph 工作流（知识图谱）

触发：*"build graph"* → 运行 `python tools/build_graph.py`

- Pass 1：解析全部 `[[wikilinks]]` → 确定性边（EXTRACTED）
- Pass 2：AI 推断隐性关系 → 推断边（INFERRED / AMBIGUOUS，带置信度）
- 社区检测给节点聚类着色
- 产出 `graph/graph.json` + 自包含的 `graph/graph.html`

### 8.1 图谱健康报告（graph report）

触发：*"graph report"* 或 `python tools/build_graph.py --report`

- **健康摘要**：边/节点比、孤立点占比、社区数、链接密度
- **孤立节点** / **God nodes（枢纽页）** / **脆弱桥**
- **幻影枢纽（phantom hubs）**：被 ≥2 个真实页面引用、却并不存在的页面——「该建页」的强信号

> 幻影枢纽只**报告**、绝不自动建页。LLM 产生的 wikilink 可能是幻觉，自动建页会放大噪声。

---

## 9. 命名约定

- 来源页：`kebab-case.md`，与 `raw/` 源文件名对齐
- 实体页 / 概念页：`TitleCase.md`（如 `Anthropic.md`、`Skill.md`、`LLMContext.md`）
- 综合页：`kebab-case.md`
- **避免同名冲突**：概念页用 TitleCase、来源页用 kebab-case 且带语义后缀（如 `skill-material.md`）

## 10. index.md 格式

```markdown
# 知识库索引

## Overview
- [综述](overview.md) — 活的整体图景

## Sources
- [来源标题](sources/slug.md) — 一句话摘要

## Entities
- [实体名](entities/EntityName.md) — 一句话说明

## Concepts
- [概念名](concepts/ConceptName.md) — 一句话说明

## Syntheses
- [综合标题](syntheses/slug.md) — 回答了什么问题
```

## 11. log.md 格式

每条以 `## [YYYY-MM-DD] <操作> | <标题>` 开头，便于 grep：

```
grep "^## \[" wiki/log.md | tail -10
```

操作类型：`ingest` / `query` / `health` / `lint` / `graph` / `report` / `init`

---

## 12. Phase 3 设计约束（自动建链 · 尚未启用）

- 自动生成的边先是 `DRAFT` 状态（图谱可见，但不写进页面正文）
- 需一道独立的 `promote` 校验，核实来源支撑与一致性后才物化为 `[[wikilinks]]`
- **链接密度预算**：页面至少 ≥2 条出链才允许晋级
- **HG-WA-01**：图谱层不得因断链自动建页——只报告
- **HG-WA-02**：新增命令不得与既有命令职责重叠

---

## 13. 红线（必须遵守，无例外）

1. **禁止编造来源**：任何 URL 与文献必须真实、可访问、可核查。不确定就标注「待核实」，绝不虚构。
2. **不得改动 `raw/`**：原始资料层只读。
3. **不确定不臆断**：拿不准的结论标「存疑」。
4. **矛盾立即标记**：发现冲突当场标注，不留到问答时才暴露。
5. **保持格式统一**：新增页面必须带 frontmatter、登记 `index.md`、追加 `log.md`。
