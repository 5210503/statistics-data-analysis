---
description: 知识库结构体检（零 LLM 调用，可每次开工前运行）
allowed-tools: Bash, Read
---

运行结构完整性检查：

```
python tools/health.py
```

（需要机器可读输出时用 `python tools/health.py --json`；需要落盘时用 `python tools/health.py --save`）

检查项见 [CLAUDE.md](CLAUDE.md) 「## 6. Health 工作流」：空文件/存根、index.md 与磁盘文件同步、来源页与 log.md 的 ingest 记录覆盖。

运行后把报告摘要讲给用户听；若有问题，给出具体修复建议（但不要擅自改动 `raw/`）。
