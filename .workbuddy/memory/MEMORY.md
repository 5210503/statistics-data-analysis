# 项目长期备忘

## 项目约定
- **concept-material-generator Skill**（.workbuddy/skills/concept-material-generator/）：用户给出任意 AI 概念名词时生成学习资料，输出固定六部分（概念个人解释 / 核心机制或组成 / 具体应用场景 / 易混淆问题或使用边界 / 可核查资料来源链接 / 难度递进自测题），保存到 `learning-materials/<概念名>.md`，并同步更新 `learning-materials/index.md` 索引；禁止编造链接。用户要求（2026-09-06 迭代）：① 先去概念原始出处（官方发布/文档/标准官网）用 WebSearch+WebFetch 查证一手资料再写；② 呈现遵循"少即是多"——文字精简、核心机制用 1-3 张 Mermaid 图可视化、默认主题配色克制、自测题答案用 `<details>` 折叠，降低认知负荷；③ 自测题难度递进：识别 → 理解 → 应用 → 辨析。
- `.gitignore` 屏蔽密钥、API Key、凭据文件（.env、*.pem、*.key、*apikey* 等）。
- **SKILL.md 第 4 节"输出结构"是用户自定义的 Skill 概念示例版模板**（非通用占位版），2026-09-07 曾被误判为"模板污染"而改动，用户要求恢复——后续维护该 skill 时不要动这一节。

## Python 教学脚本写作规范（2026-09-24 定）
- **脚本放 `scripts/python-basics/`**（`03_变量.py` ~ `07_函数.py` 这一批；2026-09-24 用户要求从 `scripts/` 根目录迁入该子文件夹），**讲义放 `notes/`**（`第02讲-变量.md` 等）。体例对齐 `notes/第01讲-描述性统计.md`：为什么学 / 核心概念 / Python 快速上手 / 本讲小结 / 思考题 五节。`scripts/` 根目录只留用户自己的 `01.py` / `02.py` / `01.ipynb`。
- **不套 concept-material-generator 模板**——该 skill 限定「AI 领域概念」，语法类内容不适用。
- **铁律：print 里禁 emoji 与非 GBK 字符**（✅ ❌ ⚠️ → ★…）。Windows 中文控制台是 cp936，打印这些会 `UnicodeEncodeError` 直接崩。分隔线一律 ASCII（`====`/`----`/`>>`）；中文、`（）`、`——`、`·` 安全。**验收方式**：`PYTHONIOENCODING=gbk python x.py` 必须 exit=0。
- 其他硬规范：只标准库、禁 `input()` 阻塞、禁随机性（需要时 `random.seed(42)`）、统一 `demo_xxx()` + `main()` + `if __name__ == "__main__"` 结构、脚本 100~180 行、讲义 70~120 行、末尾附「动手改一改」挑战。
- **并行子 agent 分工原则**：一人一讲、只允许写自己那两个文件，索引/进度类共享文件一律由主 agent 统一写，避免并行写冲突。子 agent 自报"已通过"后**主 agent 必须自己复跑验收**。

## Git 远程推送
- **远程仓库**：origin = `https://gh-proxy.com/https://github.com/5210503/statistics-data-analysis.git`（gh-proxy 代理，本机直连 github.com 不通）。gh-proxy 偶发 502 / 卡顿，**重试即可**——实测同一条推送命令卡满 4 分钟无输出，重试后 14 秒完成。
- **认证与推送（2026-09-23 定位根因）**：凭据管理器里存有**有效** PAT（host=gh-proxy.com，用户 5210503）。
  - **根因**：`git config --system credential.helper` = `helper-selector`（GCM 的交互式选择器），无界面环境会**死等输入**，使 `git credential fill` / `push` 静默挂起（实测 90s+ 零输出）。**空值清空 helper 再只挂 GCM 绝对路径**即可（实测 2 秒）：
    ```bash
    GCM="C:/Users/毛粤兰/.workbuddy/binaries/PortableGit/versions/1.2.0/mingw64/bin/git-credential-manager.exe"
    TOKEN=$(printf "protocol=https\nhost=gh-proxy.com\n" | timeout 40 \
      git -c credential.helper= -c credential.helper="$GCM" credential fill 2>/dev/null \
      | grep '^password=' | sed 's/^password=//')
    ```
  - **推送**（实测可用，**无需把 token 写进 URL**）：`git -c credential.helper= -c credential.helper="$GCM" push origin main`；万一失效再用内嵌写法 `git -c credential.helper= push "https://5210503:${TOKEN}@gh-proxy.com/https://github.com/5210503/statistics-data-analysis.git" main`。
  - **坑**：别用 `git push ... | tail` 判退出码——`$?` 取到 `tail` 的状态，会**推送失败却显示 exit=0**。用 `PIPESTATUS`，或重定向到文件后再读 `$?`。
  - 读操作匿名可用（`ls-remote` 不需认证），只有写需要 token。
- **跟踪引用怪癖（每次推送后必做）**：git 更新 `.git/refs/remotes/origin/*` 会静默失败——远程引用实际存在 `.git/packed-refs` 中，且 `.git/refs/remotes/origin/` **目录可能不存在**（直接重定向会报 No such file or directory）。推送成功后手动写松散引用覆盖它：
  ```bash
  mkdir -p .git/refs/remotes/origin && printf '%s\n' "$(git rev-parse HEAD)" > .git/refs/remotes/origin/main
  ```
  验证：`git status --branch` 应显示 `## main...origin/main` 且无 ahead/behind。
- **.workbuddy/ 已入库**：用户 2026-09-07 明确选择连同 .workbuddy/（记忆+skill）一起推送到远程，后续推送保持包含。

## LLM Wiki 知识库（2026-09-10 起）

- 仓库已是 **LLM Wiki 范式**：`raw/`（原始资料，只读）→ `wiki/`（AI 维护：index / log / overview + sources / entities / concepts / syntheses）→ `graph/`（图谱产物）。规范见根目录 `CLAUDE.md`，`AGENTS.md` / `GEMINI.md` 是其入口。
- **维护触发**：WorkBuddy 侧靠项目级 Skill `.workbuddy/skills/llm-wiki/SKILL.md` 自动加载；Claude Code 侧靠 `.claude/commands/wiki-*.md`。操作词：`ingest` / `query` / `health` / `lint` / `build graph`。
- **工具**：`python tools/health.py`（结构体检，零 LLM 调用，正常应为 0 问题）、`python tools/lint.py`（内容体检·确定性：孤立页/断链/稀疏页/缺失实体页启发式 + 图谱感知：Hub存根/脆弱桥/孤立社区/幻影枢纽）、`python tools/build_graph.py`（重建 graph.json + 自包含 graph.html）。三者纯标准库、无需 API Key；health/lint 支持 `--json`/`--save`，build_graph 支持 `--report`/`--save`。可选深度校验：`node tools/check_graph_html.js`（需 Node）。
- **退出码分级（2026-09-23 修正）**：`health`/`lint` 一律 `0`=无问题、`1`=有问题，可安全用 `&&` 串联。`lint` **只有真问题**（孤立页/断链/稀疏页/Hub 存根/幻影枢纽）才退 1；**💡 提示**（缺失实体页启发式/脆弱桥/孤立社区）不计入退出码——否则本仓库恒退 1，退出码失去信号，还会静默掐断 `health && lint && build_graph` 使图谱永不重建。**别为了消掉 💡 而硬凑跨簇链接。**
- **`graph.html` 必须先过健全性检查（2026-09-23 事故）**：模板曾漏写一个 `}`，浏览器解析整段脚本即失败 → **页面白屏**；而文件零外链、内嵌数据合法，肉眼完全查不出——**产物因此从未真正渲染过**。现在 `build_graph.py` 落盘前自检括号配平（不过就不写文件），另有 `tools/check_graph_html.js` 用真实 JS 引擎语法检查 + mock DOM 跑一遍加载/点击/重置。**改过渲染器后必须跑一次深度校验，不要只用「零外链」判断页面可用。**
- **生成物逐字节可复现**：三个写入方都显式 `newline="\n"`。Windows 下 `write_text` 默认按 `os.linesep` 写 CRLF，同一份数据跨平台字节不同，会让 diff 与校验失去意义。（注意：本机 `core.autocrlf=true`，工作区文件在 checkout 时仍会被转成 CRLF、blob 保持 LF。）
- **与上游的关系（重要）**：结构/Schema/工作流参考 `SamurAIGPT/llm-wiki-agent`（MIT，3504★），但**工具层是重写而非移植**（上游依赖 networkx+litellm、需 API Key）。差异清单见 `tools/README.md`。schema 三件套 `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` 是**完整镜像**（等价内容、不同入口），不要改成薄指针。
- **硬约束（改动知识库时必须遵守）**：① `raw/` 只读，永不修改删除；② 禁止编造来源与链接，不确定就写「待核实」；③ 新页面必须带 YAML frontmatter + 登记 `wiki/index.md` + 追加 `wiki/log.md`；④ wikilink 必须指向真实存在的页面。
- **命名约定**：概念/实体页 TitleCase（`Skill.md`、`Anthropic.md`），来源页 kebab-case 且带语义后缀（`skill-material.md`），避免 Obsidian 大小写不敏感造成的同名冲突。
- **素材区**：`learning-materials/`（concept-material-generator 输出）、`notes/`、`exercises/`、`data/`、`scripts/`（Python 练习脚本）不属于三层架构；其内容需先复制进 `raw/` 再 ingest。
- **导航页约定（三个工具必须一致）**：`index.md` / `log.md` / `overview.md` 在 health / lint / build_graph 中**一律排除**——不计页数、不作图谱节点。2026-09-23 修复了 `build_graph.py` 漏排 `overview.md` 的 bug：overview 链向几乎所有页面，一旦当节点就会制造**虚假枢纽与虚假跨桥**（当时那条唯一的跨簇「桥」两端都是 overview）。
- **两条主线尚未连通（图谱实测）**：AI 概念簇（14 节点）与统计簇（3 节点）**零 wikilink 连接**。正规的「桥」是写 `syntheses/` 综合页，导航页不算桥；建议等统计线再厚一些（第 02 讲后）再写。
- **当前规模（2026-09-23）**：wiki 内容页 17 · `raw/` 资料 8 · 入库文件 67；lint 除「两簇未连通」（符合当前进度的真实状态）外全绿。
- 已知问题：Markdown 表格内不要用转义的 wikilink（`[[X\|Y]]` 会断链）。
- **已知行为（不是 bug）**：`build_graph.py` 每次运行都会刷新 `graph.json` / `graph.html` 里的 `generated` 日期字段，因此**只要重建，`git status` 就必然显示这两个文件被修改**，哪怕图谱内容一字未变。属正常现象，按需提交即可。
- **比对文件清单的正确姿势**：别用裸 `git ls-files` 和 `find` 做 `comm`——前者对中文路径输出八进制转义，会把已入库文件误判为未入库。用 `git -c core.quotepath=false ls-files`，两侧统一 `LC_ALL=C sort`。
