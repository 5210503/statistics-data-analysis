# tools/ · 工具说明

本目录是纯标准库脚本，**不需要任何第三方依赖，也不需要 API Key**。

| 脚本 | 作用 | LLM 调用 |
|---|---|---|
| `health.py` | 结构体检：空文件/存根、索引同步、日志覆盖 | 零 |
| `lint.py` | 内容体检（确定性）：孤立页、断链、稀疏页、实体页线索、Hub 存根、脆弱桥、孤立社区、幻影枢纽 | 零 |
| `build_graph.py` | 两遍构建知识图谱 → `graph/graph.json` + `graph/graph.html` | 零 |

```bash
python tools/health.py            # 结构体检
python tools/health.py --json     # 机器可读
python tools/health.py --save     # 写入 wiki/health-report.md

python tools/lint.py              # 内容体检（确定性部分）
python tools/lint.py --save       # 写入 wiki/lint-report.md

python tools/build_graph.py       # 构建图谱
```

> 运行顺序：`health` → `lint` → `build graph`。先体检再分析，避免给空文件浪费算力。

### 约定：导航页不作为知识节点

`wiki/index.md`、`wiki/log.md`、`wiki/overview.md` 是 schema 里并列的三份**导航 / 元文件**，三个脚本**一律排除**——不计入体检页数，也不作为图谱节点。理由：它们是组织与索引，本身不是知识；尤其 `overview` 链向几乎所有页面，一旦当作节点，会制造出**虚假的枢纽和虚假的跨簇桥梁**。

> **2026-09-23 修正**：`build_graph.py` 此前漏排 `overview.md`，导致图谱节点数比体检多 1（18 vs 17）；更关键的是，两个知识簇之间那条唯一的跨簇「桥」其实完全由 overview 撑起，是假象。排除后真实情况显露：AI 概念簇与统计簇**完全零连接**。已与另两个脚本对齐。

---

## 与上游项目的差异（如实说明）

本仓库的**目录结构、页面 Schema、工作流设计**参考自
[SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent)（MIT）。但**工具层是重新实现的，不是移植**。差异如下：

### 1. 依赖
| | 上游 | 本仓库 |
|---|---|---|
| 依赖 | `networkx~=3.6.1` + `litellm~=1.83.10` | **无（纯标准库）** |
| API Key | `tools/` 脚本需要 `ANTHROPIC_API_KEY` | **不需要** |
| 社区检测 | NetworkX + Louvain | 自研标签传播 |
| 图可视化 | vis.js | 手写自包含渲染（零外链） |

> ⚠️ 上游 `requirements.txt` 记录：`litellm` 1.82.7–1.82.8 曾于 2026-03 遭供应链投毒，须钉到 `~=1.83.10`。本仓库不依赖它，也就规避了该风险。

### 2. 上游有、本仓库未移植的脚本
上游 `tools/` 共 11 个脚本，其中下列脚本**依赖 LLM 或额外库**，本仓库有意不移植：

| 上游脚本 | 用途 | 未移植原因 |
|---|---|---|
| `ingest.py` | 命令行 ingest（调 LLM 生成页面） | 本仓库的 ingest 由 **Agent 本身**完成（读 `CLAUDE.md`/`AGENTS.md` 规范即可），无需脚本 |
| `query.py` | 命令行问答（调 LLM） | 同上，query 由 Agent 完成 |
| `lint.py` | 语义 lint（调 LLM 找矛盾） | 语义部分由 Agent 完成；本仓库的 `lint.py` 只做确定性检查 |
| `heal.py` | 用 LLM 自动补建缺失的概念/实体页 | HL-WA-01：图谱层不得自动建页，只报告 |
| `refresh.py` | 批量重跑 | 按需再补 |
| `file_to_md.py` / `pdf2md.py` | 多格式 / arXiv 转换 | 需要 `markitdown` / `marker-pdf`，按需安装（见根目录 `requirements.txt`） |
| `_utils.py` | 上游脚本的公共工具 | 本仓库各脚本自包含，不需要 |

**设计取舍**：上游把 ingest/query/lint 做成「脚本调 LLM」；本仓库把同一职责交给**正在读这些规范的 Agent**——这本来就是上游 README 主推的「no API key」用法（Claude Code / Codex / Gemini CLI 直接对话）。因此省略这些脚本不损失能力，只省掉了依赖。

### 3. 本仓库额外补充的
- `lint.py` 的**图谱感知检查**（Hub 存根 / 脆弱桥 / 孤立社区 / 幻影枢纽）——上游这部分在 `build_graph.py --report` 与 LLM lint 中，本仓库做成了独立确定性脚本。
