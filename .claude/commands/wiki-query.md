---
description: 基于 wiki 页面回答问题，并可沉淀为综合页
argument-hint: <问题>
allowed-tools: Read, Write, Edit, Glob, Grep
---

目标：执行 [CLAUDE.md](CLAUDE.md) 中定义的 **Query 工作流**。

问题：$ARGUMENTS

步骤：
1. 读 `wiki/index.md` 定位相关页面
2. 用 Read 读取这些页面
3. 综合出答案，用 `[[页面名]]` 行内标注出处
4. 主动询问是否把答案沉淀为 `wiki/syntheses/<slug>.md`（若用户同意，写入后更新 index.md 与 log.md）

铁律：答案只能基于 wiki 中真实存在的内容，不得编造未记载的事实或链接。
