---
name: llm-wiki
description: 个人知识库（LLM Wiki 范式）维护技能。当用户要求向知识库吸收原始资料（ingest）、基于知识库提问（query）、给知识库做结构或内容体检（health / lint）、生成知识图谱（graph），或在对话中提到 raw/、wiki/、知识库、索引、知识图谱、交叉引用等时使用。本仓库根目录的 CLAUDE.md 是完整规范，执行任何操作前必须先读取并遵守。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
agent_created: true
---

# LLM Wiki — 个人知识库维护器

本仓库是一个 **LLM Wiki**：原始资料先被「编译」成结构化 wiki 页面，之后所有问答都基于 wiki，而不是每次重新检索原文。分工是——**用户负责选材与提问，Agent 负责其余全部维护工作**。

## 1. 先读宪法

**任何操作前，先完整读取仓库根目录的 `CLAUDE.md`。** 它规定了目录结构、页面格式、命名约定、工作流与红线，是唯一权威。本文件只做索引与提醒，不覆盖 CLAUDE.md。

三层架构（不可越界）：

| 层 | 目录 | 谁维护 | 规则 |
|---|---|---|---|
| 原始资料 | `raw/` | 人 | **只读**，Agent 永不修改/删除 |
| 结构化 wiki | `wiki/` | Agent | 建页、改页、维护索引与交叉引用 |
| 规范 | `CLAUDE.md` | 人 + Agent | 共同迭代 |

## 2. 五种操作的触发与要点

### ingest —— 吸收新资料
用户说 `ingest raw/xxx.md`、「把这份资料吸收进知识库」。
按 CLAUDE.md「Ingest 工作流」10 步执行：读源文件 → 读 index/overview → 写 `wiki/sources/<slug>.md` → 更新 `index.md` → 修订 `overview.md` → 建/更新 entities 与 concepts 页面 → 标矛盾 → 追加 `log.md` → **收尾必跑三件套**并汇报变更。

> ⚠️ **收尾三件套不能省**：`python tools/health.py`（断链 / 索引 / 日志）→ `python tools/lint.py`（内容）→ `python tools/build_graph.py`。
> **尤其别忘重跑图谱**——否则 `graph/` 会停留在旧状态，与实际 wiki 不一致。
> 三者退出码已分级，可安全用 `&&` 串联：`0` = 无问题，`1` = 有问题。**只有真问题才让 `lint` 退出 1**；`💡` 类（缺失实体页启发式 / 脆弱桥 / 孤立社区）属提示，不计入退出码——**不要为了消掉它而硬凑跨簇链接**。

### query —— 提问
用户说 `query: <问题>` 或直接问知识库里有什么。
读 `index.md` 定位 → 读相关页面 → 综合答案并用 `[[页面名]]` 标注出处 → **主动问用户是否沉淀为 `wiki/syntheses/` 页面**。

### health —— 结构体检（零成本）
运行 `python tools/health.py`。检查空文件、索引同步、日志覆盖。**不调用 LLM**，可随时跑。

### lint —— 内容体检
**先跑确定性部分**：`python tools/lint.py`（零 LLM 调用）——孤立页、断链、稀疏页（<2 出链）、缺失实体页启发式，以及图谱感知检查（Hub 存根 / 脆弱桥 / 孤立社区 / 幻影枢纽）。
**再用 Grep/Read 查语义部分**（脚本查不了的）：跨页面**矛盾**、**过时摘要**、**数据缺口**。
先 health 再 lint——给空文件做语义分析纯属浪费。

### graph —— 知识图谱
运行 `python tools/build_graph.py`，产出 `graph/graph.json` + 自包含的 `graph/graph.html`；加 `--report` 出图谱健康报告（god nodes / 幻影枢纽 / 脆弱桥）。落盘前脚本会自检脚本括号配平，不通过就不写文件。

> 改过渲染器（`build_graph.py` 里的 HTML 模板）后，跑一次 `node tools/check_graph_html.js` 做深度校验（真实 JS 引擎语法 + mock DOM 跑一遍加载/点击/重置）。**不要只用「零外链」判断页面能不能用**——一处漏写的 `}` 就会让整段脚本解析失败、整页白屏，而文件本身看上去完全正常。

> 约定：`index.md` / `log.md` / `overview.md` 三份**导航页不作为图谱节点**（与 health / lint 的取舍保持一致）。重建会刷新产物里的 `generated` 日期，因此**每次重建 git 都会显示这两个文件被改动**（哪怕图一字未变），属正常现象。

## 3. 红线（违反即失败）

1. **禁止编造来源与链接**——任何 URL / 文献必须真实可核查，不确定就写「待核实」。
2. **`raw/` 只读**——要改内容去改 `wiki/`，并在来源页注明差异。
3. **新页面三件事必做**：带 YAML frontmatter、登记进 `wiki/index.md`、追加 `wiki/log.md`。
4. **不得产生断链**——`[[页面名]]` 必须指向真实存在的页面。
5. **矛盾立即标记**，不留到问答时才暴露。

## 4. 汇报格式

每次操作结束，用简短清单汇报：动了哪些文件、新增/更新了哪些页面、有无断链或矛盾、下一步建议。不要只丢一句「已完成」。
