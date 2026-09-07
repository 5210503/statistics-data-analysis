# 项目长期备忘

## 项目约定
- **concept-material-generator Skill**（.workbuddy/skills/concept-material-generator/）：用户给出任意 AI 概念名词时生成学习资料，输出固定六部分（概念个人解释 / 核心机制或组成 / 具体应用场景 / 易混淆问题或使用边界 / 可核查资料来源链接 / 难度递进自测题），保存到 `learning-materials/<概念名>.md`，并同步更新 `learning-materials/index.md` 索引；禁止编造链接。用户要求（2026-09-06 迭代）：① 先去概念原始出处（官方发布/文档/标准官网）用 WebSearch+WebFetch 查证一手资料再写；② 呈现遵循"少即是多"——文字精简、核心机制用 1-3 张 Mermaid 图可视化、默认主题配色克制、自测题答案用 `<details>` 折叠，降低认知负荷；③ 自测题难度递进：识别 → 理解 → 应用 → 辨析。
- `.gitignore` 屏蔽密钥、API Key、凭据文件（.env、*.pem、*.key、*apikey* 等）。
- **SKILL.md 第 4 节"输出结构"是用户自定义的 Skill 概念示例版模板**（非通用占位版），2026-09-07 曾被误判为"模板污染"而改动，用户要求恢复——后续维护该 skill 时不要动这一节。

## Git 远程推送
- **远程仓库**：origin = `https://gh-proxy.com/https://github.com/5210503/statistics-data-analysis.git`（gh-proxy 代理，本机直连 github.com 不通）。gh-proxy 偶发 502，重试即可。
- **认证**：Windows 凭据管理器已存有效 PAT（host=gh-proxy.com，用户名 5210503，2026-09-07 更新）。WorkBuddy 环境里 GCM 无法弹交互登录窗，凭据失效时需用户提供 PAT，用 `https://用户名:token@gh-proxy.com/...` 一次性推送，再 `git credential approve` 存回凭据管理器。
- **已知怪癖**：git 在本机更新 `.git/refs/remotes/origin/*` 跟踪引用会静默失败（update-ref 返回成功但值不变）；推送/拉取成功后若 `git status` 仍显示 ahead，手动创建 `.git/refs/remotes/origin/<分支>` 文件写入远程最新 commit hash 即可。
- **.workbuddy/ 已入库**：用户 2026-09-07 明确选择连 同 .workbuddy/（记忆+skill）一起推送到远程，后续推送保持包含。
