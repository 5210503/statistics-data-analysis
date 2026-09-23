#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LLM Wiki · 内容体检（确定性部分，零 LLM 调用）

只做「不需要理解语义就能判定」的检查，语义矛盾等交给 Agent。
上游 llm-wiki-agent 的 lint.py 依赖 litellm 做语义分析；本仓库改为
「脚本管确定性、Agent 管语义」的分工，故此脚本无需 API Key。

检查项：
  结构类
    1. 孤立页      —— 没有任何其他页面链入
    2. 断链        —— [[wikilink]] 指向不存在的页面
    3. 稀疏页      —— 出链少于 2 条 [[wikilinks]]（链接密度不达标）
    4. 疑似缺失实体页 —— 在 ≥3 个页面出现、却没有独立页面的大写术语
  图谱类（需先 build graph）
    5. Hub 存根    —— 度数 > μ+2σ 的枢纽页，但正文内容稀薄（< 500 字符）
    6. 脆弱桥      —— 两个社区之间仅靠 1 条边连接
    7. 孤立社区    —— 与外部零连接的聚类
    8. 幻影枢纽    —— 被 ≥2 个真实页面引用、却并不存在的页面（= 断链 + 多次被引用）

用法：
  python tools/lint.py            # 人类可读报告
  python tools/lint.py --json     # 机器可读 JSON
  python tools/lint.py --save     # 写入 wiki/lint-report.md
"""

import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
GRAPH_JSON = ROOT / "graph" / "graph.json"
CONTENT_DIRS = ("sources", "entities", "concepts", "syntheses")

OUTLINK_MIN = 2        # 稀疏页阈值：出链少于此数即告警
HUB_STUB_CHARS = 500   # Hub 存根：正文少于该字符数视为内容稀薄
ENTITY_MIN_PAGES = 3   # 疑似缺失实体页：术语至少出现在这么多页
SKIP = {"index.md", "log.md", "overview.md", "health-report.md", "lint-report.md"}

# 「疑似缺失实体页」是低置信度启发式：先剔除泛词与通用技术词，避免拿噪声冒充结论。
# 真正的实体判定属于 Agent 的语义检查（本脚本只给线索）。
GENERIC_TERMS = {
    "AI", "Agent", "Agents", "LLM", "LLMs", "RAG", "MCP", "API", "APIs",
    "YAML", "JSON", "XML", "HTML", "CSS", "HTTP", "HTTPS", "URL", "URLs",
    "Markdown", "Git", "GitHub", "Obsidian", "Dataview", "Skill", "Skills",
    "Context", "Wiki", "Tokenizer", "Prompt", "Python", "CSV", "PDF",
    "Windows", "Mac", "Linux", "VS", "OK", "ID", "IDs", "N", "The", "This",
}

FM_RE = re.compile(r"^\ufeff?\s*---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
# 专有名词风格的英文术语（首词为 TitleCase，含小写字母），用于「疑似缺失实体页」启发式。
# 要求含小写字母，可自动排除 AI / RAG / YAML 这类全大写缩写。
TERM_RE = re.compile(r"\b([A-Z][a-z][A-Za-z0-9]*(?:\s+[A-Z][A-Za-z0-9]+){0,3})\b")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def split_frontmatter(text: str):
    m = FM_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def wiki_pages():
    out = []
    for p in sorted(WIKI.rglob("*.md")):
        if p.name in SKIP:
            continue
        out.append(p)
    return out


def build_id_map(pages):
    return {p.stem.lower(): p.relative_to(WIKI).as_posix() for p in pages}


def run_checks():
    if not WIKI.exists():
        print("找不到 wiki/ 目录，请确认在仓库根目录运行。", file=sys.stderr)
        sys.exit(2)

    pages = wiki_pages()
    id_map = build_id_map(pages)

    inbound = Counter()                    # 小写 page key -> 入链数
    outbound = defaultdict(set)            # 页面相对路径 -> 指向的 key 集合
    body_len = {}
    term_pages = defaultdict(set)          # 大写术语 -> 出现的页面集合
    broken_refs = Counter()                # 不存在页面的 key -> 被引用次数
    broken_detail = []

    for p in pages:
        rel = p.relative_to(WIKI).as_posix()
        text = read(p)
        _, body = split_frontmatter(text)
        body_len[rel] = len(body.strip())

        for target in WIKILINK_RE.findall(text):
            key = target.strip().lower()
            outbound[rel].add(key)
            if key in id_map:
                inbound[key] += 1
            else:
                broken_refs[key] += 1
                broken_detail.append({"page": rel, "link": target.strip()})

        for term in TERM_RE.findall(body):
            term_pages[term].add(rel)

    # 1. 孤立页：本身存在但不被任何页面链入
    orphans = [rel for rel in (p.relative_to(WIKI).as_posix() for p in pages)
               if inbound.get(Path(rel).stem.lower(), 0) == 0]

    # 2. 断链
    broken_links = sorted(broken_detail, key=lambda d: (d["page"], d["link"]))

    # 3. 稀疏页（出链 < 2）
    sparse = [{"page": rel, "outlinks": len(outbound.get(rel, ()))}
              for rel in (p.relative_to(WIKI).as_posix() for p in pages)
              if len(outbound.get(rel, ())) < OUTLINK_MIN]

    # 4. 疑似缺失实体页：术语出现在 ≥3 页且没有同名页面（低置信度启发式，已剔除泛词）
    known = {p.stem.lower() for p in pages}
    missing_entities = []
    for term, pset in term_pages.items():
        if term.lower() in known or term in GENERIC_TERMS:
            continue
        if len(pset) >= ENTITY_MIN_PAGES:
            missing_entities.append({"term": term, "pages": sorted(pset)})
    missing_entities.sort(key=lambda d: (-len(d["pages"]), d["term"]))

    result = {
        "generated": date.today().isoformat(),
        "total_pages": len(pages),
        "orphans": sorted(orphans),
        "broken_links": broken_links,
        "sparse": sorted(sparse, key=lambda d: d["outlinks"]),
        "missing_entities": missing_entities[:20],
        "hub_stubs": [],
        "fragile_bridges": [],
        "isolated_communities": [],
        "phantom_hubs": [],
    }

    # ===== 图谱类检查 =====
    if GRAPH_JSON.exists():
        g = json.loads(read(GRAPH_JSON))
        nodes = {n["id"]: n for n in g.get("nodes", [])}
        edges = g.get("edges", [])
        communities = g.get("communities", [])

        # 无向邻接（仅用真实边 EXTRACTED 判定结构关系）
        adj = {nid: set() for nid in nodes}
        for e in edges:
            s, t = e.get("source"), e.get("target")
            if s in adj and t in adj:
                adj[s].add(t)
                adj[t].add(s)

        degrees = [len(adj[nid]) for nid in nodes]
        if degrees:
            mu = statistics.mean(degrees)
            sd = statistics.pstdev(degrees)
            hub_cut = mu + 2 * sd
        else:
            mu = sd = hub_cut = 0.0

        # 5. Hub 存根：度数异常高但内容稀薄
        for nid, n in nodes.items():
            if len(adj[nid]) > hub_cut and body_len.get(n.get("file", "").replace("wiki/", ""), 10 ** 9) < HUB_STUB_CHARS:
                result["hub_stubs"].append({
                    "node": nid, "degree": len(adj[nid]),
                    "chars": body_len.get(n.get("file", "").replace("wiki/", ""), 0),
                })

        # 社区归属
        node_comm = {}
        for c in communities:
            for m in c["members"]:
                node_comm[m] = c["id"]

        # 6. 脆弱桥：社区对之间仅 1 条边
        bridge = Counter()
        for e in edges:
            s, t = e.get("source"), e.get("target")
            cs, ct = node_comm.get(s), node_comm.get(t)
            if cs is None or ct is None or cs == ct:
                continue
            bridge[tuple(sorted((cs, ct)))] += 1
        result["fragile_bridges"] = [{"communities": list(pair), "edges": n}
                                     for pair, n in sorted(bridge.items()) if n == 1]

        # 7. 孤立社区：与外部零连接
        comm_ids = {c["id"] for c in communities}
        linked = set()
        for pair in bridge:
            linked.update(pair)
        result["isolated_communities"] = [{"id": c["id"], "size": c["size"]}
                                          for c in communities if c["id"] not in linked]

        # 8. 幻影枢纽：断链且被 ≥2 个页面引用
        result["phantom_hubs"] = [{"link": k, "referenced_by": n}
                                  for k, n in broken_refs.most_common() if n >= 2]

        result["graph_stats"] = {
            "nodes": len(nodes), "edges": len(edges),
            "communities": len(communities),
            "mean_degree": round(mu, 2), "std_degree": round(sd, 2),
            "hub_cutoff": round(hub_cut, 2),
        }
    else:
        result["graph_stats"] = None

    return result


# 检查项分级：error 计入退出码；hint 只是线索 / 结构性观察，不影响退出码。
# 理由：hint 类在健康的知识库里也会长期存在（低置信度启发式、簇间零连接这类观察），
# 若一并计入退出码，lint 就会永远返回 1 —— 退出码失去信号意义，还会静默掐断
# `health && lint && build_graph` 这类流水线，图谱于是再也不重建。
SEVERITY = {
    "orphans": "error",
    "broken_links": "error",
    "sparse": "error",
    "hub_stubs": "error",
    "phantom_hubs": "error",
    "missing_entities": "hint",
    "fragile_bridges": "hint",
    "isolated_communities": "hint",
}


def count_by_level(r: dict):
    """返回 (问题数, 提示数)。"""
    err = sum(len(r.get(k, [])) for k, lv in SEVERITY.items() if lv == "error")
    hint = sum(len(r.get(k, [])) for k, lv in SEVERITY.items() if lv == "hint")
    return err, hint


def render(r: dict) -> str:
    L = ["# LLM Wiki · 内容体检报告（确定性部分）", ""]
    L.append(f"> 生成日期：{r['generated']} · 扫描页面：{r['total_pages']} 个")

    def block(title, items, fmt, empty="无问题", level="error"):
        L.append("")
        if items:
            L.append(f"{'⚠️' if level == 'error' else '💡'} {title}（{len(items)}）")
            L.extend(fmt(i) for i in items)
        else:
            L.append(f"✅ {title}：{empty}")

    block("孤立页（无任何入链）", r["orphans"], lambda x: f"- `{x}`")
    block("断链", r["broken_links"],
          lambda i: f"- `{i['page']}` 中的 `[[{i['link']}]]` 指向不存在的页面")
    block("稀疏页（出链 < 2）", r["sparse"],
          lambda i: f"- `{i['page']}` —— 出链仅 {i['outlinks']} 条")
    block("疑似缺失实体页（启发式 · 低置信度，仅作线索）", r["missing_entities"],
          lambda i: f"- **{i['term']}** —— 出现于 {len(i['pages'])} 页：{', '.join('`'+p+'`' for p in i['pages'])}",
          level="hint")

    if r.get("graph_stats"):
        s = r["graph_stats"]
        L.append("")
        L.append(f"📊 图谱：{s['nodes']} 节点 / {s['edges']} 边 / {s['communities']} 社区 · "
                 f"平均度 {s['mean_degree']}（σ={s['std_degree']}），枢纽阈值 {s['hub_cutoff']}")
        block("Hub 存根（枢纽页却内容稀薄）", r["hub_stubs"],
              lambda i: f"- `{i['node']}` —— 度数 {i['degree']}，正文仅 {i['chars']} 字符")
        block("脆弱桥（社区间仅 1 条边）", r["fragile_bridges"],
              lambda i: f"- 社区 {i['communities'][0]} ↔ {i['communities'][1]}：仅 1 条边",
              level="hint")
        block("孤立社区（与外部零连接）", r["isolated_communities"],
              lambda i: f"- 社区 {i['id']}（{i['size']} 个节点）",
              level="hint")
        block("幻影枢纽（被多次引用却不存在）", r["phantom_hubs"],
              lambda i: f"- `[[{i['link']}]]` —— 被 {i['referenced_by']} 个页面引用（建页信号）")
    else:
        L.append("")
        L.append("ℹ️ 未找到 `graph/graph.json`，已跳过图谱类检查。先运行 `python tools/build_graph.py`。")

    n_err, n_hint = count_by_level(r)
    L.append("")
    L.append(f"合计：**{n_err} 个问题** · {n_hint} 条提示　（退出码只反映问题数；💡 是线索，不必强行消除）")
    L.append("")
    L.append("---")
    L.append("说明：本报告只覆盖确定性检查。跨页面的**语义矛盾、过时摘要**需由 Agent 用读全文的方式判定。")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="LLM Wiki 内容体检（确定性部分）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--save", action="store_true", help="写入 wiki/lint-report.md")
    args = ap.parse_args()

    r = run_checks()
    if args.save:
        out = WIKI / "lint-report.md"
        out.write_text(render(r), encoding="utf-8", newline="\n")
        print(f"已写入 {out.relative_to(ROOT)}")

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(render(r))

    errors, _ = count_by_level(r)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
