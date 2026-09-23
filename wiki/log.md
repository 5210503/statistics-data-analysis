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
