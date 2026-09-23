# 统计与数据分析 · 个人知识库

> 一个 **LLM Wiki** 范式的个人知识库：你负责选材与提问，AI 负责把资料「编译」成结构化、互相链接的 wiki 页面并长期维护。

## 这是什么

传统的文件问答（RAG）每次提问都要重新从原文里检索碎片；LLM Wiki 反过来——**先把资料编译成一套结构化 wiki，之后所有问答都基于这套 wiki**。

| RAG | LLM Wiki（本仓库） |
|---|---|
| 每次查询都重新推导知识 | 编译一次，持续维护 |
| 以原文碎片为检索单位 | 以结构化 wiki 页面为单位 |
| 没有交叉引用 | 交叉引用在 ingest 时建好 |
| 矛盾往往到查询时才暴露（也可能永远不暴露） | 在 ingest 时当场标注 |
| 不积累 | 每加一份资料，wiki 更丰富一层 |

三层架构，互不越界：

| 层 | 目录 | 谁维护 | 规则 |
|---|---|---|---|
| 原始资料 | `raw/` | **人** | 不可变，AI 只读 |
| 结构化 wiki | `wiki/` | **AI** | 建页、改页、维护索引与交叉引用 |
| 规范 | `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` | 人 + AI | 目录约定、页面格式、工作流、红线 |

> 三份 schema 内容等价，只是入口不同：Claude Code 读 `CLAUDE.md`，Codex / OpenCode 读 `AGENTS.md`，Gemini CLI 读 `GEMINI.md`。

## 快速开始

直接用自然语言对 AI 说：

| 想做什么 | 说什么 | 背后发生什么 |
|---|---|---|
| 吸收新资料 | `ingest raw/ai-concepts/新文件.md` | 读原文 → 建来源页/概念页/实体页 → 更新索引与综述 → 记日志 |
| 提问 | `query：Agent 和 Skill 有什么区别？` | 读索引定位 → 读相关页 → 综合答案（可沉淀为综合页） |
| 结构体检 | `health` | 跑 `python tools/health.py`，零成本，检查空文件/索引/日志 |
| 内容体检 | `lint 知识库` | 跑 `python tools/lint.py`，找孤立页、断链、稀疏页、图谱问题 |
| 建知识图谱 | `build graph` | 跑 `python tools/build_graph.py`，产出可交互的 `graph/graph.html` |
| 图谱体检 | `graph report` | 健康摘要、枢纽页、脆弱桥、幻影枢纽 |

**多格式 ingest**：除 `.md` 外，把 `.pdf` `.docx` `.pptx` `.xlsx` `.html` `.csv` `.epub` 等直接丢进 `raw/` 再 `ingest` 即可——会先用 [markitdown](https://github.com/microsoft/markitdown) 自动转成 markdown（需先 `pip install markitdown`）。

在 WorkBuddy 中，项目级 Skill `.workbuddy/skills/llm-wiki/SKILL.md` 会自动加载；在 Claude Code / Codex 中，分别通过 `.claude/commands/` 斜杠命令与 `AGENTS.md` 生效。

### 在 Obsidian 中浏览

`wiki/` 用统一的 `[[wikilinks]]`，可当作 Obsidian vault 直接打开：双链可点击跳转，图谱视图能直接看到知识形状。

- **软链模式**：想把 wiki 并进主 vault，可 `ln -sfn <本仓库>/wiki <你的vault>/wiki`
- **图谱视图**：建议过滤掉 `index.md` / `log.md`（如 `-file:index.md -file:log.md`），避免它们成为引力黑洞
- **Dataview**：可安装社区插件 [Dataview](https://blacksmithgu.github.io/obsidian-dataview/) 查询 AI 自动写入的 YAML frontmatter
- 移动本地目录后记得更新软链，否则 Obsidian 里 `wiki/` 会「消失」

## 目录结构

```
statistics-data-analysis/
├── CLAUDE.md / AGENTS.md / GEMINI.md   # schema：AI 的维护规范（先读这个）
├── README.md                           # 本文件
├── LICENSE                             # MIT
├── requirements.txt / pyproject.toml   # 依赖说明（核心工具零依赖）
├── raw/                                # ★ 原始资料层（只读）
│   ├── ai-concepts/                    #   AI 概念：Agent Skill / 上下文 / Skill / 三者关系
│   └── statistics/                     #   统计：第 01 讲 · 描述性统计
├── wiki/                               # ★ AI 维护的知识层
│   ├── index.md                        #   全部页面目录（每次 ingest 后更新）
│   ├── log.md                          #   只追加的操作时间线
│   ├── overview.md                     #   跨全部资料的「活的综述」
│   ├── sources/                        #   5 个来源页
│   ├── concepts/                       #   7 个概念页
│   ├── entities/                       #   3 个实体页
│   └── syntheses/                      #   1 个综合页
├── graph/                              # 知识图谱产物
│   ├── graph.json                      #   节点/边/社区数据
│   └── graph.html                      #   自包含可视化（双击打开）
├── tools/                              # 独立 Python 脚本（纯标准库，无需 API Key）
│   ├── health.py                       #   结构体检
│   ├── lint.py                         #   内容体检（确定性部分）
│   ├── build_graph.py                  #   图谱构建
│   └── README.md                       #   工具说明 & 与上游的差异
├── docs/                               # 进阶说明
├── .claude/commands/                   # 斜杠命令：wiki-ingest / query / health / lint / graph
├── learning-materials/                 # ▼ 素材区（人产出的、供 ingest 的原始素材）
├── notes/  exercises/  data/           # ▼ 素材区：统计课程笔记 / 练习代码 / 数据集
├── scripts/                            # ▼ 素材区：Python 练习脚本
└── .workbuddy/skills/
    ├── llm-wiki/                       #   知识库维护 Skill
    └── concept-material-generator/     #   概念学习资料生成 Skill
```

`learning-materials/`、`notes/`、`exercises/`、`data/` 属于**素材区**，不属于 wiki 三层结构。它们的可靠副本会被复制进 `raw/` 作为不可变来源，wiki 页面只引用 `raw/` 里的副本（原件仍在原地由人维护）。

## 当前内容

知识库索引见 [`wiki/index.md`](wiki/index.md)；整体图景见 [`wiki/overview.md`](wiki/overview.md)。目前有两条主线：

- **AI 概念线**：上下文（有限/共享/位置敏感）→ 上下文工程 → Skill / Agent Skill / 渐进式披露 → MCP 边界。已沉淀综合页 [`wiki/syntheses/agent-context-skill-relationship.md`](wiki/syntheses/agent-context-skill-relationship.md)。
- **统计线**：第 01 讲描述性统计（集中趋势 / 离散程度 / 分布形态）。

### 素材区的 AI 概念学习资料

由 `concept-material-generator` Skill 生成，六部分固定结构（概念解释 / 核心机制 / 应用场景 / 易混淆与边界 / 可核查来源 / 递进自测题）：

| 概念 | 文件 | 生成日期 |
|------|------|----------|
| Agent Skill | `learning-materials/Agent-Skill.md` | 2026-09-06 |
| 大模型上下文 | `learning-materials/大模型上下文.md` | 2026-09-06 |
| Skill | `learning-materials/Skill.md` | 2026-09-09 |

索引见 `learning-materials/index.md`。

## 人工核查与修改说明

AI 生成的内容**必须人工核查后才能当作可靠学习依据**。每次收到新生成的文档，按以下三项核对：

### 核对链接（最优先）
- 逐条检查「可核查资料来源链接」，删除 AI 生成的虚构链接，替换为官方真实可访问的网页链接，保证链接可正常打开。

### 修正概念错误
- 通读文档，修正概念描述模糊之处；区分易混概念的边界（如 Agent 与 Skill），补充对比辨析。

### 补充个人理解
- 在「概念个人解释」部分用自己的话改写总结，加入自己对概念本质的理解；结合项目案例完善应用场景与自测题，保持六部分结构不变。

> 修订记录：2026-09-07，完善 Agent、大模型上下文、Skill 三份学习笔记，替换真实参考链接，补充个人理解与概念辨析。
> 修订记录：2026-09-10，仓库升级为 LLM Wiki 范式：原资料复制进 `raw/` 作为不可变来源并 ingest 为 `wiki/` 页面，新增 schema、工具与知识图谱。
> 修订记录：2026-09-10，按上游项目补全 schema（AGENTS/GEMINI 完整镜像、图谱报告、Phase 3 约束等），新增 `tools/lint.py` 与仓库级文件，并如实标注与上游的实现差异。

## 维护这个知识库

改规矩就改 [`CLAUDE.md`](CLAUDE.md)——它是 AI 的行为宪法。红线五条：**禁止编造来源、`raw/` 只读、不确定不臆断、矛盾立即标注、新页面必须带 frontmatter 并登记 `index.md` 与 `log.md`**。

## 来源与技术栈

- **设计参考**：[SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent)（MIT，约 3.5k stars）。本仓库沿用了它的三层目录结构、页面 Schema 与 ingest/query/lint/health/graph 工作流。
- **工具层为重新实现**：上游 `tools/` 依赖 `networkx` + `litellm` 并需要 API Key；本仓库改为**纯标准库**，语义工作交给正在读规范的 Agent。差异清单见 [`tools/README.md`](tools/README.md)。
- **技术栈**：纯 Python 标准库 + Markdown + `[[wikilinks]]`。无服务器、无数据库，全部在本地，一切皆纯文本。
- **许可证**：MIT，见 [`LICENSE`](LICENSE)。
