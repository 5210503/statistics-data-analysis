---
description: 从全部 [[wikilinks]] 构建知识图谱（可选生成图谱健康报告）
allowed-tools: Bash, Read, Write, Glob, Grep
---

目标：执行 [CLAUDE.md](CLAUDE.md) 中定义的 **Graph 工作流**（见「## 8. Graph 工作流」）。

运行：

```
python tools/build_graph.py
```

产出 `graph/graph.json`（节点/边/社区数据）与 `graph/graph.html`（自包含可视化，双击即可打开）。

需要**图谱健康报告**时用：

```
python tools/build_graph.py --report
```

报告含：健康摘要、孤立节点、God nodes（枢纽页）、脆弱桥、**幻影枢纽**（被 ≥2 页引用却不存在 —— 「该建页」信号）。

> 幻影枢纽只报告、绝不自动建页（HG-WA-01）。

**取舍约定**：`index.md` / `log.md` / `overview.md` 三份导航页**不作为图谱节点**（与 health / lint 保持一致）。理由：它们链向几乎所有页面，一旦当节点就会制造虚假枢纽与虚假跨桥。

**注意**：重建会刷新产物里的 `generated` 日期，所以**每次重建后 `git status` 都会显示 `graph.json` / `graph.html` 被修改**，哪怕图一字未变——这是正常的，按需提交即可。

若环境没有 Python，退路：用 Grep 找出所有 `[[wikilinks]]`，手工构建节点/边列表写入 `graph.json`，再用同一 HTML 模板渲染。

完成后告知用户：节点数、边数、社区情况，以及最「中心」的几个页面。
