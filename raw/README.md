# raw/ —— 原始资料层（不可变）

这里是知识库的**唯一事实来源（source of truth）**。

## 规则

- **只由人放入，AI 只读。** 任何 Agent 都不得修改、重命名或删除本目录下的文件。
- 需要修正内容时，改 `wiki/` 里的对应页面，并在来源页注明与原文的差异。
- 新增资料：直接把文件丢进来（`raw/ai-concepts/` 或 `raw/statistics/`，也可新建分类子目录），然后说 `ingest raw/<路径>`。

## 目录

```
raw/
├── ai-concepts/                     # AI 概念相关原始文档
│   ├── agent-skill.md               #   Agent Skill（Anthropic 格式）
│   ├── llm-context.md               #   大模型上下文
│   ├── skill.md                     #   Skill 通用概念
│   └── concept-relationship.md      #   Agent / 上下文 / Skill 三者关系
└── statistics/                      # 统计与数据分析原始文档
    └── descriptive-statistics-01.md #   第 01 讲 · 描述性统计
```

## 这些文件的来源

`raw/ai-concepts/` 下的四份是**副本**，原件在仓库的素材区：

| raw/ 副本 | 原件位置 |
|---|---|
| `ai-concepts/agent-skill.md` | `learning-materials/Agent-Skill.md` |
| `ai-concepts/llm-context.md` | `learning-materials/大模型上下文.md` |
| `ai-concepts/skill.md` | `learning-materials/Skill.md` |
| `ai-concepts/concept-relationship.md` | `concept-relationship.md` |
| `statistics/descriptive-statistics-01.md` | `notes/第01讲-描述性统计.md` |

> 原件仍由人（及 concept-material-generator Skill）维护；`raw/` 保存的是被 ingest 时的**冻结快照**，用于保证 wiki 页面引用的出处稳定可追溯。原件更新后，重新复制进 `raw/` 并再次 ingest 即可。
