# 项目长期备忘

## 项目约定
- **concept-material-generator Skill**（.workbuddy/skills/concept-material-generator/）：用户给出任意 AI 概念名词时生成学习资料，输出固定六部分（概念个人解释 / 核心机制或组成 / 具体应用场景 / 易混淆问题或使用边界 / 可核查资料来源链接 / 难度递进自测题），保存到 `learning-materials/<概念名>.md`，并同步更新 `learning-materials/index.md` 索引；禁止编造链接。用户要求（2026-09-06 迭代）：① 先去概念原始出处（官方发布/文档/标准官网）用 WebSearch+WebFetch 查证一手资料再写；② 呈现遵循"少即是多"——文字精简、核心机制用 1-3 张 Mermaid 图可视化、默认主题配色克制、自测题答案用 `<details>` 折叠，降低认知负荷；③ 自测题难度递进：识别 → 理解 → 应用 → 辨析。
- `.gitignore` 屏蔽密钥、API Key、凭据文件（.env、*.pem、*.key、*apikey* 等）。
- **SKILL.md 第 4 节"输出结构"是用户自定义的 Skill 概念示例版模板**（非通用占位版），2026-09-07 曾被误判为"模板污染"而改动，用户要求恢复——后续维护该 skill 时不要动这一节。

## Git 远程推送
- **远程仓库**：origin = `https://gh-proxy.com/https://github.com/5210503/statistics-data-analysis.git`（gh-proxy 代理，本机直连 github.com 不通）。gh-proxy 偶发 502，重试即可。
- **认证（2026-09-23 重写，务必按此做）**：Windows 凭据管理器已存有效 PAT（host=gh-proxy.com，用户名 5210503，`ghp_` 开头 40 位）。**但本机 GCM 在 push 环节会静默挂起**——直接 `git push origin main` 会卡死、无任何输出（实测 3 分钟被超时掐断），而 `git credential fill` 取凭据本身是正常的，**故障点只在 GCM 的 push 认证交互**。可靠做法：先用 `git credential fill` 取出 PAT，再内嵌 URL 且显式禁用 helper：
  ```bash
  TOKEN=$(printf "protocol=https\nhost=gh-proxy.com\n" | git credential fill | grep '^password=' | sed 's/^password=//')
  git -c credential.helper= push "https://5210503:${TOKEN}@gh-proxy.com/https://github.com/5210503/statistics-data-analysis.git" main --verbose --progress
  rm -f <存放 token 的临时文件>   # 用完必须清理
  ```
  实测 **12 秒**完成 88 KiB 推送。另：`git-upload-pack`（下载）握手约 1.3s，`git-receive-pack`（上传）约 7s——上传通道明显慢，但通。
- **已知怪癖**：git 在本机更新 `.git/refs/remotes/origin/*` 跟踪引用会静默失败（update-ref 返回成功但值不变）；推送/拉取成功后若 `git status` 仍显示 ahead，手动创建 `.git/refs/remotes/origin/<分支>` 文件写入远程最新 commit hash 即可。
- **.workbuddy/ 已入库**：用户 2026-09-07 明确选择连 同 .workbuddy/（记忆+skill）一起推送到远程，后续推送保持包含。

## LLM Wiki 知识库（2026-09-10 起）

- 仓库已是 **LLM Wiki 范式**：`raw/`（原始资料，只读）→ `wiki/`（AI 维护：index / log / overview + sources / entities / concepts / syntheses）→ `graph/`（图谱产物）。规范见根目录 `CLAUDE.md`，`AGENTS.md` / `GEMINI.md` 是其入口。
- **维护触发**：WorkBuddy 侧靠项目级 Skill `.workbuddy/skills/llm-wiki/SKILL.md` 自动加载；Claude Code 侧靠 `.claude/commands/wiki-*.md`。操作词：`ingest` / `query` / `health` / `lint` / `build graph`。
- **工具**：`python tools/health.py`（结构体检，零 LLM 调用，正常应为 0 问题，可加 `--json` / `--save`）、`python tools/lint.py`（内容体检·确定性：孤立页/断链/稀疏页/缺失实体页启发式 + 图谱感知：Hub存根/脆弱桥/孤立社区/幻影枢纽）、`python tools/build_graph.py`（重建 graph.json + 自包含 graph.html，`--report`/`--save` 出图谱健康报告）。纯标准库，无需 API Key。
- **与上游的关系（重要）**：结构/Schema/工作流参考 `SamurAIGPT/llm-wiki-agent`（MIT，3504★），但**工具层是重写而非移植**（上游依赖 networkx+litellm、需 API Key）。差异清单见 `tools/README.md`。schema 三件套 `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` 是**完整镜像**（等价内容、不同入口），不要改成薄指针。
- **硬约束（改动知识库时必须遵守）**：① `raw/` 只读，永不修改删除；② 禁止编造来源与链接，不确定就写「待核实」；③ 新页面必须带 YAML frontmatter + 登记 `wiki/index.md` + 追加 `wiki/log.md`；④ wikilink 必须指向真实存在的页面。
- **命名约定**：概念/实体页 TitleCase（`Skill.md`、`Anthropic.md`），来源页 kebab-case 且带语义后缀（`skill-material.md`），避免 Obsidian 大小写不敏感造成的同名冲突。
- **素材区**：`learning-materials/`（concept-material-generator 输出）、`notes/`、`exercises/`、`data/` 不属于三层架构；其内容需先复制进 `raw/` 再 ingest。
- 已知问题：Markdown 表格内不要用转义的 wikilink（`[[X\|Y]]` 会断链）。
