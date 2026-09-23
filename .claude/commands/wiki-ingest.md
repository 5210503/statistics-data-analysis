---
description: 把 raw/ 下的原始资料吸收进 wiki（Ingest 工作流）
argument-hint: <raw/ 下的文件路径，可多个>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

目标：对指定文件执行本仓库 [CLAUDE.md](CLAUDE.md) 中定义的 **Ingest 工作流**。

目标文件：$ARGUMENTS

请先完整读取 CLAUDE.md，再严格按其中「## 4. Ingest 工作流」的 10 步执行：

1. 读完 `raw/` 源文件
2. 读 `wiki/index.md` 与 `wiki/overview.md`
3. 写 `wiki/sources/<slug>.md`（用来源页格式）
4. 更新 `wiki/index.md`
5. 按需修订 `wiki/overview.md`
6. 建/更新 `wiki/entities/` 页面
7. 建/更新 `wiki/concepts/` 页面
8. 标注与既有内容的矛盾
9. 追加 `wiki/log.md`：`## [YYYY-MM-DD] ingest | <标题>`
10. **收尾校验（三件套不能省）**并输出变更摘要：
    - `python tools/health.py` —— 断链、索引同步、日志覆盖
    - `python tools/lint.py` —— 内容体检 + 图谱感知检查
    - `python tools/build_graph.py` —— **必须重跑**，否则 `graph/` 会停留在旧状态

铁律：`raw/` 只读；不得编造来源；新页面必须带 frontmatter。
