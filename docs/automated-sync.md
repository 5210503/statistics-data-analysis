# 自动化同步指南（进阶）

> 让知识库自动保持「最新」，而不是每次都手动 `health` / `build graph`。

## 先讲清楚一件事：哪些步骤可以自动化

LLM Wiki 的 ingest 分两类动作：

| 步骤 | 性质 | 能否无人值守自动化 |
|---|---|---|
| 把文件放进 `raw/` | 同步 | ✅ 可以（拷贝/软链） |
| 运行 `tools/health.py` | 确定性 | ✅ 可以 |
| 运行 `tools/build_graph.py` | 确定性 | ✅ 可以 |
| **ingest（读原文 → 建 wiki 页）** | 需要 LLM 判断 | ⚠️ 需要 Agent 参与，**无法纯脚本无人值守** |

> 上游项目用一个调用 LLM 的 `tools/ingest.py` 来无人值守 ingest；本仓库未移植该脚本（见 [`tools/README.md`](../tools/README.md)），ingest 由 Agent 完成。因此**本仓库可自动化的部分是「同步 + 体检 + 重建图谱」**，ingest 仍需你在会话里说一句 `ingest raw/xxx.md`。

---

## 推荐管线：同步 → 体检 → 重建图谱

### 第 1 步：同步脚本

把笔记库里新写的 markdown 同步进 `raw/`（可用拷贝或软链）。

**Linux / macOS / Git Bash**

```bash
#!/usr/bin/env bash
set -uo pipefail

REPO="$HOME/Desktop/repos/statistics-data-analysis"
LOG="$REPO/automation.log"
ts() { date "+%Y-%m-%d %H:%M:%S"; }

cd "$REPO" || exit 1
echo "[$(ts)] === 同步开始 ===" >> "$LOG"

# 1) 把你自己的 vault → raw/ 的同步逻辑放这里
#    例：rsync -a --include='*.md' --exclude='*' "$HOME/vault/notes/" "$REPO/raw/inbox/"

# 2) 结构体检（零成本）
python tools/health.py --save >> "$LOG" 2>&1

# 3) 内容体检（确定性部分）
python tools/lint.py --save >> "$LOG" 2>&1

# 4) 重建知识图谱
python tools/build_graph.py >> "$LOG" 2>&1

echo "[$(ts)] === 同步完成 ===" >> "$LOG"
```

赋可执行权限：`chmod +x daily-sync.sh`

### 第 2 步：挂到系统计划任务

**Windows（本仓库当前环境）——任务计划程序**

```powershell
$action  = New-ScheduledTaskAction -Execute "bash" `
           -Argument "-lc '$HOME/Desktop/repos/statistics-data-analysis/daily-sync.sh'"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName "LLM-Wiki-Sync" -Action $action -Trigger $trigger
```

**macOS —— launchd**（比 cron 更可靠）：写 `~/Library/LaunchAgents/com.llm-wiki.sync.plist`，`StartCalendarInterval` 设为 2:00，`RunAtLoad` 为 `true`，然后用 `launchctl load` 载入。日志用 `StandardOutPath` / `StandardErrorPath` 收集。

**Linux —— cron**

```
0 2 * * * cd $HOME/Desktop/repos/statistics-data-analysis && ./daily-sync.sh
```

---

## 关于「自动建页」（自我修复）

上游的 `tools/heal.py` 会用 LLM 自动补建缺失的概念/实体页。**本仓库有意不这么做**，依据 schema 的硬规则 **HG-WA-01**：

> 图谱层不得因断链而自动建页——只报告。

原因：LLM 产生的 `[[wikilink]]` 可能是幻觉，自动建页会把噪声放大成「看似真实」的页面。正确做法是让 `tools/lint.py` / `graph report` **报告**幻影枢纽（被多次引用却不存在），由你或 Agent 判断后手动建页。

## 监控

无人值守的夜间任务，靠日志发现问题：脚本里的 `automation.log`（或 launchd 的 `daemon.stderr.log`）就是你的哨兵。建议每周扫一眼——重点看体检报告里是否连续出现新的孤立页或断链。
