---
description: 知识库内容体检（孤立页、断链、稀疏页、图谱问题、语义矛盾）
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

目标：执行 [CLAUDE.md](CLAUDE.md) 中定义的 **Lint 工作流**（见「## 7. Lint 工作流」）。

**第一步 · 确定性检查（先跑，零成本）**

```
python tools/lint.py
```

覆盖：孤立页、断链、稀疏页（出链 < 2）、疑似缺失实体页（低置信度启发式）、
Hub 存根、脆弱桥、孤立社区、幻影枢纽。

**第二步 · 语义检查（需读全文）**

- 跨页面**矛盾**
- 新资料进来后未更新的**过时摘要**
- **数据缺口**（知识库答不上来、建议补哪些来源）

> 先 `python tools/health.py` 确认结构没问题，再做语义层检查——给空文件做语义分析纯属浪费 token。

输出 lint 报告，询问是否保存到 `wiki/lint-report.md`。
