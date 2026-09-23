# 知识库操作日志

只追加的时间线记录。每条以 `## [YYYY-MM-DD] <操作> | <标题>` 开头，便于 grep：

```
grep "^## \[" wiki/log.md | tail -10
```

操作类型：`init` / `ingest` / `query` / `health` / `lint` / `graph`

---

## [2026-09-10] init | 知识库初始化（LLM Wiki 结构落地）
- 建立三层架构：`raw/`（原始资料，只读）· `wiki/`（AI 维护）· schema（CLAUDE.md）
- 写入 schema 三件套：`CLAUDE.md`（完整规范）、`AGENTS.md`、`GEMINI.md`
- 建立 `.claude/commands/`（wiki-ingest / wiki-query / wiki-health / wiki-lint / wiki-graph）
- 建立 WorkBuddy 项目级 Skill：`.workbuddy/skills/llm-wiki/SKILL.md`
- 建立 `tools/`（health.py · build_graph.py）与 `graph/` 目录
- 复制现有资料进原始资料层：`raw/ai-concepts/`（4 份）· `raw/statistics/`（1 份）

## [2026-09-10] ingest | Agent Skill（Anthropic Agent Skills 格式）
- 新增来源页 `sources/agent-skill-material.md`
- 新增概念页 `concepts/AgentSkill.md` · `concepts/ProgressiveDisclosure.md` · `concepts/MCP.md`
- 新增实体页 `entities/Anthropic.md`
- 一手来源：raw/ai-concepts/agent-skill.md

## [2026-09-10] ingest | 大模型上下文（Context）
- 新增来源页 `sources/llm-context-material.md`
- 新增概念页 `concepts/LLMContext.md` · `concepts/ContextEngineering.md`
- 一手来源：raw/ai-concepts/llm-context.md

## [2026-09-10] ingest | Skill（通用概念：可复用任务能力模板）
- 新增来源页 `sources/skill-material.md`
- 更新概念页 `concepts/Skill.md`
- 新增实体页 `entities/WorkBuddy.md` · `entities/ConceptMaterialGenerator.md`
- 一手来源：raw/ai-concepts/skill.md

## [2026-09-10] ingest | Agent / 大模型上下文 / Skill 三者关系
- 新增来源页 `sources/concept-relationship-summary.md`
- 沉淀综合页 `syntheses/agent-context-skill-relationship.md`
- 一手来源：raw/ai-concepts/concept-relationship.md

## [2026-09-10] ingest | 第 01 讲 · 描述性统计
- 新增来源页 `sources/descriptive-statistics-01.md`
- 新增概念页 `concepts/DescriptiveStatistics.md`
- 一手来源：raw/statistics/descriptive-statistics-01.md（原文件 notes/第01讲-描述性统计.md）

## [2026-09-10] graph | 构建知识图谱
- 运行 `tools/build_graph.py`，产出 `graph/graph.json` 与 `graph/graph.html`

## [2026-09-10] health | 结构体检
- 运行 `tools/health.py`：检查空文件、索引同步、日志覆盖

## [2026-09-23] ingest | 练习 01 · 描述性统计（Python 标准库实现）
- 新增来源页 `sources/statistics-exercise-01.md`
- 更新概念页 `concepts/DescriptiveStatistics.md`（补实测数据、左偏判读与平移不变性验证，关闭遗留问题 2）
- 一手来源：raw/statistics/statistics-exercise-01.py（原件 exercises/ex01_描述统计入门.py）
- 配套数据集：raw/statistics/students-scores.csv（原件 data/students_scores.csv）

## [2026-09-23] graph | 修正 overview 误入图谱
- `build_graph.py` 的排除集补上 `overview.md`，与 health.py / lint.py 对齐（节点数 18 → 17）
- 结果：17 节点 / 82 边（确定 60 / 推断 22）/ 2 社区
- **重要发现**：两个社区**零连接**。此前 lint 报的「脆弱桥（社区间仅 1 条边）」实为 overview 被当作节点所制造的假象——那条边两端都是 overview。

## [2026-09-23] health | 结构体检 + 内容体检
- `health.py`：扫描 17 页，**0 问题**
- `lint.py`：稀疏页由 2 条降为 1 条（`concepts/DescriptiveStatistics.md` 已修复，仅剩 `sources/descriptive-statistics-01.md`）；图谱感知部分改报「孤立社区 ×2」
