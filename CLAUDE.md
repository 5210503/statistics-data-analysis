# LLM Wiki · 个人知识库维护规范（Schema）

> 本文件是本知识库的「宪法」。任何 AI Agent（WorkBuddy / Claude Code / Codex / Gemini CLI）在读写本仓库之前，先读本文件，并严格按其中的工作流操作。
>
> 核心分工：**你负责选材与提问，AI 负责其余全部维护工作**（摘要、交叉引用、建页、记日志、标矛盾）。

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
| 规范 | `CLAUDE.md`（本文件） | 人与 AI 共同迭代 | 约定目录、页面格式、工作流 |

---

## 1. 目录结构

```
raw/                     # 不可变原始资料（source of truth）
  ai-concepts/           #   AI 概念相关原始文档
  statistics/            #   统计与数据分析原始文档
  assets/                #   图片等附件（可选）
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
  lint.py                #   结构 + 图谱质量检查（确定性部分，零 LLM 调用）
  build_graph.py         #   从 [[wikilinks]] 构建知识图谱
  README.md              #   工具说明与「与上游项目的差异」
docs/                    # 进阶说明（自动化同步等）
learning-materials/      # 【素材区】concept-material-generator Skill 的输出目录
notes/ exercises/ data/  # 【素材区】统计课程原始笔记、练习代码、数据集
scripts/                 # 【素材区】Python 练习脚本（跟课动手写的）
```

> `learning-materials/`、`notes/`、`exercises/`、`data/`、`scripts/` 是**人产出的素材区**，不属于 wiki 三层架构。它们的可靠副本会被复制进 `raw/` 作为不可变来源；wiki 页面只引用 `raw/` 里的副本。

> **本仓库的工具是纯标准库实现**，不需要 `networkx` / `litellm` 等依赖，也不需要 API Key——因为 ingest / query / lint 的语义部分由**你（Agent）本身**完成，脚本只负责确定性检查。这与上游项目的差异详见 `tools/README.md`。

---

## 2. 触发方式

用自然语言即可，AI 按本节识别意图：

| 意图 | 说法示例 |
|---|---|
| **ingest** 吸收新资料 | `ingest raw/ai-concepts/skill.md`、`把这份新资料吸收进知识库`、`ingest 这篇论文` |
| **query** 提问 | `query：Agent 和 Skill 有什么区别？`、`知识库里关于上下文工程说了什么？` |
| **health** 结构体检 | `health`、`检查知识库结构` |
| **lint** 内容体检 | `lint 知识库`、`找找有没有孤立页和矛盾` |
| **graph** 建图谱 | `build graph`、`生成知识图谱`、`把知识图谱搭出来` |
| **graph report** 图谱体检 | `graph report`、`图谱健康报告`、`有哪些枢纽页和幻影页` |

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

**务必保证 wikilink 指向真实存在的页面**——宁可先不写链接，也不要指向空页。图谱与 lint 都依赖这一点。

---

## 4. Ingest 工作流（吸收一篇原始资料）

触发：*"ingest &lt;文件&gt;"*

**支持格式**：`.md` 直接读取。其他格式（`.pdf` `.docx` `.pptx` `.xlsx` `.xls` `.html` `.txt` `.csv` `.json` `.xml` `.rst` `.rtf` `.epub` `.ipynb` `.yaml` `.yml` `.tsv` `.wav` `.mp3`）先用 [markitdown](https://github.com/microsoft/markitdown) 转成 markdown 再吸收；用 `--no-convert` 可跳过转换、只处理 `.md`。转换后的 markdown 应放回 `raw/` 作为不可变来源。

按顺序执行：

1. 用 Read 工具读完 `raw/` 下的源文件
2. 读 `wiki/index.md` 与 `wiki/overview.md`，掌握现有知识版图
3. 写 `wiki/sources/<slug>.md`（格式见下）
4. 更新 `wiki/index.md` —— 在 Sources 段加入本页
5. 更新 `wiki/overview.md` —— 若本资料改变了整体图景，就修订综述
6. 为文中关键人物 / 公司 / 产品 / 项目建或更新 `wiki/entities/` 页面
7. 为文中关键概念 / 框架 / 方法建或更新 `wiki/concepts/` 页面
8. **标矛盾**：若与已有 wiki 内容冲突，在受影响页面加 `## 矛盾 / 待澄清` 小节，不要藏起来
9. 追加 `wiki/log.md`：`## [YYYY-MM-DD] ingest | <标题>`
10. **收尾校验（三件套不能省）**：
    - `python tools/health.py` —— 断链、索引同步、日志覆盖
    - `python tools/lint.py` —— 内容体检 + 图谱感知检查
    - `python tools/build_graph.py` —— **必须重跑**，否则 `graph/` 会停留在旧状态，与实际 wiki 不一致
    - 最后输出一段变更摘要（动了哪些文件、新增/更新了哪些页面、有无断链或矛盾）

> 一篇来源往往牵动 5–15 个页面。宁可分次 ingest、保持人参与，也不要一次性批量灌入而失去把关。

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

**学习笔记 / 概念资料模板**
```markdown
---
title: "概念名"
type: source
tags: [concept-material, ai]
date: YYYY-MM-DD
source_file: raw/...
---
## 一句话本质
## 核心机制
## 应用场景
## 易混淆 / 边界
## 可核查来源
## 自测题
```

**课程笔记模板**
```markdown
---
title: "第 N 讲 · 主题"
type: source
tags: [statistics, lecture]
date: YYYY-MM-DD
source_file: raw/...
---
## 本讲要解决的问题
## 核心概念
## 代码实践
## 小结
## 思考题
```

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

检查项（**零 LLM 调用**，每次开工前跑都行）：
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
| **检查项** | 空文件、索引同步、日志同步 | 孤立页、断链、矛盾、数据缺口、图谱问题 |
| **工具** | `tools/health.py` | `tools/lint.py`（确定性）+ Agent 语义检查 |
| **执行次序** | 先（预检） | 后（health 通过之后） |

> 先 health 再 lint：给空文件做语义分析纯属浪费 token。

---

## 7. Lint 工作流（内容体检）

触发：*"lint 知识库"*

**确定性部分**（可先跑 `python tools/lint.py`，零 LLM 调用）：
- **孤立页**：没有任何页面链入
- **断链**：`[[页面]]` 指向不存在的页面
- **稀疏页**：出链少于 2 条 `[[wikilinks]]`（链接密度不达标）
- **缺失实体页**：被 3 个以上页面提及却没有独立页面

**图谱感知检查**（需先 `build graph`，读取 `graph.json`）：
- **Hub 存根**：度数 > μ+2σ 的枢纽页，但正文内容稀薄（< 500 字符）
- **脆弱桥**：两个社区之间仅靠 1 条边连接
- **孤立社区**：与外部零连接的聚类

**语义部分**（Agent 用 Grep + Read 完成，消耗 token）：
- **矛盾**：跨页面互相冲突的主张
- **过时摘要**：新资料进来后没更新的页面
- **数据缺口**：知识库答不上来的问题；建议去补哪些来源

输出 lint 报告，询问是否保存到 `wiki/lint-report.md`。

> 先 health 再 lint：给空文件做语义分析纯属浪费 token。

---

## 8. Graph 工作流（知识图谱）

触发：*"build graph"* → 运行 `python tools/build_graph.py`

- Pass 1：解析全部 `[[wikilinks]]` → 确定性边（EXTRACTED）
- Pass 2：AI 推断隐性关系 → 推断边（INFERRED / AMBIGUOUS，带置信度）
- 社区检测（Louvain 思路）给节点聚类着色
- 产出 `graph/graph.json` + 自包含的 `graph/graph.html`

没有 Python 环境时，退路：用 Grep 找出所有 wikilink，手工写出 `graph.json`，再用同一套 HTML 模板渲染。

### 8.1 图谱健康报告（graph report）

触发：*"graph report"* 或 `python tools/build_graph.py --report`

在图谱构建之外，额外产出结构化报告：

- **健康摘要**：边/节点比、孤立点占比、社区数、链接密度
- **孤立节点**：在图谱中零连接的页面
- **God nodes（枢纽页）**：度数 > μ+2σ 的节点（连接度异常集中）
- **脆弱桥**：仅靠 1 条边相连的社区对
- **幻影枢纽（phantom hubs）**：被 ≥2 个真实页面以 `[[wikilinks]]` 引用、却**并不存在**的页面——这是「该建页」的强信号

用 `--save` 写入 `graph/graph-report.md`。

> 幻影枢纽只**报告**、绝不自动建页。LLM 产生的 wikilink 可能是幻觉，自动建页会把噪声放大。

---

## 9. 命名约定

- 来源页：`kebab-case.md`，与 `raw/` 源文件名对齐
- 实体页 / 概念页：`TitleCase.md`（如 `Anthropic.md`、`Skill.md`、`LLMContext.md`）
- 综合页：`kebab-case.md`
- **避免同名冲突**：概念页用 TitleCase、来源页用 kebab-case 且带语义后缀（如 `skill-material.md`），保证 `[[Skill]]` 与 `[[skill-material]]` 不撞车

---

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

---

## 11. log.md 格式

每条以 `## [YYYY-MM-DD] <操作> | <标题>` 开头，便于 grep：

```
grep "^## \[" wiki/log.md | tail -10
```

操作类型：`ingest` / `query` / `health` / `lint` / `graph` / `report` / `init`

---

## 12. 在 Obsidian 中浏览

`wiki/` 的页面用统一的 `[[wikilinks]]`，所以可以把它当作 Obsidian vault 直接打开：双链能跳转、图谱视图能看知识形状。

- **软链模式**：把 `wiki/` 软链到主 vault，例如
  `ln -sfn <本仓库>/wiki <你的vault>/wiki`
- **图谱视图**：建议过滤掉 `index.md` / `log.md`（如 `-file:index.md -file:log.md`），避免它们变成引力黑洞
- **Dataview**：可安装社区插件 [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) 查询 AI 自动写入的 YAML frontmatter（如 `type: source`、`tags: [statistics]`）
- 若移动了本地目录，记得同步更新软链，否则 Obsidian 里 `wiki/` 会「消失」

---

## 13. Phase 3 设计约束（自动建链 · 尚未启用）

「自动插入 `[[wikilinks]]`」属于未来能力，目前**未启用**。若将来实现，必须遵守下列硬约束：

### 晋级门槛：`draft → stable`
- 自动生成的边先是 `DRAFT` 状态（图谱中可见，但**不写进页面正文**）
- 需要一道独立的 `promote` 校验，核实来源支撑与一致性
- 只有通过校验的边才被物化为页面正文里的 `[[wikilinks]]`
- **链接密度预算**：一个页面至少要有 ≥2 条出链，才允许晋级

### 硬规则

| 编号 | 规则 | 理由 |
|---|---|---|
| HG-WA-01 | 图谱层**不得**因断链而自动建页——只报告 | LLM ingest 会产生幻觉 wikilink，自动建页会放大噪声 |
| HG-WA-02 | 新增斜杠命令**不得**与既有命令职责重叠 | 避免用户困惑；应并入既有命令而非另起一个 |

---

## 14. 红线（必须遵守，无例外）

1. **禁止编造来源**：wiki 里出现的任何 URL 与文献，必须是真实、可访问、可核查的。不确定就标注「待核实」，绝不虚构。
2. **不得改动 `raw/`**：原始资料层只读。需要修正内容时改 `wiki/`，并在来源页注明差异。
3. **不确定不臆断**：拿不准的结论标「存疑」，不要写成确定事实。
4. **矛盾立即标记**：发现新旧资料冲突，当场在页面标注，不留到问答时才暴露。
5. **保持格式统一**：新增页面必须带 frontmatter、必须登记进 `index.md`、必须追加 `log.md`。这三件事与内容同等重要。
