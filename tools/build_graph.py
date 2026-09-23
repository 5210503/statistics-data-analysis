#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LLM Wiki · 知识图谱构建（纯标准库，无需 API Key）

两遍构建：
  Pass 1 确定性 —— 解析全部 [[wikilinks]]              → EXTRACTED 边
  Pass 2 语义性 —— 共同邻居 / 共享标签 / 共同来源推断隐性关系 → INFERRED 边（带置信度）

再对无向图跑标签传播做社区聚类，输出：
  graph/graph.json   节点 / 边 / 社区数据
  graph/graph.html   自包含可视化（零依赖，双击即可打开）

用法：python tools/build_graph.py
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
GRAPH_DIR = ROOT / "graph"

FM_RE = re.compile(r"^\ufeff?\s*---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")
# 导航/元文件：不是知识节点，不参与图谱。
# index / log / overview 是 schema 里并列的三份「AI 维护的导航文件」，
# 三者都排除——与 health.py / lint.py 保持一致。
# （overview 若被当作节点，会因其链向几乎所有页面而制造出虚假的枢纽与跨簇桥梁。）
SKIP = {"index.md", "log.md", "overview.md", "health-report.md", "lint-report.md"}
GENERIC_TAGS = {"ai-concept", "synthesis"}  # 过于宽泛，不作为推断依据

PALETTE = ["#4285f4", "#ea4335", "#34a853", "#f9ab00",
           "#a142f4", "#00acc1", "#ff7043", "#5f6368"]


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def parse_page(p: Path):
    text = read(p)
    m = FM_RE.match(text)
    fm_raw = m.group(1) if m else ""
    meta = {}
    if fm_raw:
        for line in fm_raw.splitlines():
            if ":" in line and not line.strip().startswith("#"):
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip()
    tags = []
    tm = re.search(r"tags:\s*\[(.*?)\]", fm_raw)
    if tm:
        tags = [t.strip().strip('"\'') for t in tm.group(1).split(",") if t.strip()]
    sources = []
    sm = re.search(r"sources:\s*\[(.*?)\]", fm_raw)
    if sm:
        sources = [s.strip().strip('"\'') for s in sm.group(1).split(",") if s.strip()]
    title = meta.get("title", "").strip().strip('"')
    return {
        "id": p.stem,
        "label": p.stem,
        "title": title or p.stem,
        "type": meta.get("type", "overview").strip(),
        "tags": tags,
        "sources": sources,
        "file": p.relative_to(ROOT).as_posix(),
        "text": text,
    }


def label_propagation(ids, adj, iters=40):
    labels = {i: i for i in ids}
    for _ in range(iters):
        changed = False
        for i in sorted(ids):
            if not adj[i]:
                continue
            counts = Counter(labels[j] for j in adj[i])
            top = max(counts.values())
            cands = [l for l, c in counts.items() if c == top]
            new = labels[i] if labels[i] in cands else min(cands)
            if new != labels[i]:
                labels[i] = new
                changed = True
        if not changed:
            break
    merged = defaultdict(list)
    for i, l in labels.items():
        merged[l].append(i)
    comms = sorted(merged.values(), key=lambda m: (-len(m), m[0]))
    group = {}
    for gi, members in enumerate(comms):
        for m in members:
            group[m] = gi
    return group, comms


def build_report(data: dict) -> str:
    """生成图谱健康报告（Markdown）：健康摘要 / 孤立节点 / God nodes / 脆弱桥 / 幻影枢纽。"""
    nodes = data["nodes"]
    edges = data["edges"]
    comms = data["communities"]
    n = len(nodes) or 1

    adj = {nd["id"]: set() for nd in nodes}
    for e in edges:
        s, t = e["source"], e["target"]
        if s in adj and t in adj:
            adj[s].add(t)
            adj[t].add(s)
    degrees = [len(adj[nd["id"]]) for nd in nodes]
    mu = statistics.mean(degrees) if degrees else 0.0
    sd = statistics.pstdev(degrees) if len(degrees) > 1 else 0.0
    hub_cut = mu + 2 * sd

    node_comm = {m: c["id"] for c in comms for m in c["members"]}

    orphans = [nd for nd in nodes if len(adj[nd["id"]]) == 0]
    god = [nd for nd in nodes if len(adj[nd["id"]]) > hub_cut]

    bridge = Counter()
    for e in edges:
        cs, ct = node_comm.get(e["source"]), node_comm.get(e["target"])
        if cs is None or ct is None or cs == ct:
            continue
        bridge[tuple(sorted((cs, ct)))] += 1
    fragile = [(p, c) for p, c in bridge.items() if c == 1]
    linked_c = {c for pair in bridge for c in pair}
    isolated_c = [c for c in comms if c["id"] not in linked_c]

    phantom = Counter()
    for b in data.get("broken_links", []):
        phantom[b["link"].lower()] += 1
    phantoms = [(k, v) for k, v in phantom.most_common() if v >= 2]

    density = len(edges) / n

    L = ["# LLM Wiki · 图谱健康报告", ""]
    L.append(f"> 生成日期：{data['generated']}")
    L.append("")
    L.append("## 健康摘要")
    L.append(f"- 节点：{len(nodes)} · 边：{len(edges)} · 社区：{len(comms)}")
    L.append(f"- 边/节点比：{density:.2f} · 平均度：{mu:.2f}（σ={sd:.2f}，枢纽阈值 μ+2σ={hub_cut:.2f}）")
    L.append(f"- 孤立节点占比：{len(orphans)}/{n}（{len(orphans)/n*100:.0f}%）")
    L.append("")

    def block(title, items, fmt, empty="无"):
        L.append(f"## {title}")
        L.extend(fmt(i) for i in items) if items else L.append(f"✅ {empty}")
        L.append("")

    block("Hub 存根（God nodes，度数 > μ+2σ）", god,
          lambda x: f"- `{x['id']}` —— 度数 {x['degree']}")
    block("孤立节点（图谱中零连接）", orphans,
          lambda x: f"- `{x['id']}`")
    block("脆弱桥（社区间仅 1 条边）", fragile,
          lambda x: f"- 社区 {x[0][0]} ↔ {x[0][1]}：仅 1 条边")
    block("孤立社区（与外部零连接）", isolated_c,
          lambda x: f"- 社区 {x['id']}（{x['size']} 个节点）")
    block("幻影枢纽（被 ≥2 个页面引用却不存在 → 建页信号）", phantoms,
          lambda x: f"- `[[{x[0]}]]` —— 被 {x[1]} 个页面引用")

    L.append("---")
    L.append("说明：幻影枢纽只**报告**、绝不自动建页（HG-WA-01）——LLM 产生的 wikilink 可能是幻觉。")
    return "\n".join(L)


_JS_BEFORE_REGEX = set("=(,:[!&|?;{}+-*%<>~^")
_JS_KEYWORDS_BEFORE_REGEX = ("return", "typeof", "instanceof", "in", "of", "new",
                             "delete", "void", "case", "do", "else", "yield", "await")


def js_balance_errors(js: str):
    """极简 JS 扫描器：跳过字符串 / 模板串 / 注释 / 正则字面量后，
    检查 () [] {} 是否配平。纯标准库，用来兜住“模板手误产出一个打不开的页面”。

    局限：这不是真正的语法分析（不做 ASI、不解析 JSX），只能挡住括号类手误；
    但正是这类手误会让浏览器整段脚本解析失败、页面一片空白，且肉眼极难发现。
    """
    stack, errors = [], []
    i, n = 0, len(js)
    prev, prev_word = "", ""

    while i < n:
        c = js[i]

        if c == "/" and js[i + 1:i + 2] == "/":          # 行注释
            j = js.find("\n", i)
            i = n if j < 0 else j
            continue
        if c == "/" and js[i + 1:i + 2] == "*":          # 块注释
            j = js.find("*/", i + 2)
            if j < 0:
                return ["块注释 /* 未闭合"]
            i = j + 2
            continue

        # / 处在“期待操作数”的位置 → 正则字面量（否则是除号）
        if c == "/" and (prev in _JS_BEFORE_REGEX or prev_word in _JS_KEYWORDS_BEFORE_REGEX):
            i += 1
            in_class = False
            while i < n and js[i] != "\n":
                ch = js[i]
                if ch == "\\":
                    i += 2
                    continue
                if ch == "[":
                    in_class = True
                elif ch == "]" and in_class:
                    in_class = False
                elif ch == "/" and not in_class:
                    break
                i += 1
            if i >= n or js[i] == "\n":
                return ["正则字面量未闭合"]
            i += 1
            while i < n and (js[i].isalpha() or js[i].isdigit()):
                i += 1
            prev, prev_word = "/", ""
            continue

        if c in "'\"`":                                  # 字符串 / 模板串
            quote, i = c, i + 1
            while i < n:
                ch = js[i]
                if ch == "\\":
                    i += 2
                    continue
                if ch == quote:
                    break
                if quote == "`" and ch == "$" and js[i + 1:i + 2] == "{":
                    depth, i = 1, i + 2                # 插值 ${...}
                    while i < n and depth:
                        depth += (js[i] == "{") - (js[i] == "}")
                        i += 1
                    continue
                i += 1
            if i >= n:
                return [f"字符串 {quote} 未闭合"]
            i += 1
            prev, prev_word = quote, ""
            continue

        if c in "([{":
            stack.append(c)
        elif c in ")]}":
            if not stack:
                errors.append(f"多余的 '{c}'")
            elif "([{".index(stack.pop()) != ")]}".index(c):
                errors.append(f"'{c}' 与前文括号不匹配")
        if not c.isspace():
            prev_word = prev_word + c if (c.isalnum() or c in "_$") else ""
            prev = c
        i += 1

    if stack:
        errors.append("未闭合的 " + " ".join(f"'{o}'" for o in stack))
    return errors


def main(argv=None):
    ap = argparse.ArgumentParser(description="LLM Wiki 知识图谱构建")
    ap.add_argument("--report", action="store_true", help="额外生成图谱健康报告")
    ap.add_argument("--save", action="store_true", help="把报告写入 graph/graph-report.md")
    args = ap.parse_args(argv)

    if not WIKI.exists():
        print("找不到 wiki/ 目录。", file=sys.stderr)
        return 2

    pages = [parse_page(p) for p in sorted(WIKI.rglob("*.md")) if p.name not in SKIP]
    by_id = {p["id"]: p for p in pages}
    lower_map = {p["id"].lower(): p["id"] for p in pages}

    adj = {p["id"]: set() for p in pages}
    edges, seen = [], set()

    def add_edge(a, b, kind, conf=None):
        if a == b or a not in by_id or b not in by_id:
            return
        key = tuple(sorted((a, b)))
        if key in seen:
            return
        seen.add(key)
        e = {"source": key[0], "target": key[1], "kind": kind}
        if conf is not None:
            e["confidence"] = round(conf, 2)
        edges.append(e)
        adj[a].add(b)
        adj[b].add(a)

    # Pass 1：确定性 wikilinks
    broken = []
    for p in pages:
        for target in WIKILINK_RE.findall(p["text"]):
            rid = lower_map.get(target.strip().lower())
            if rid is None:
                broken.append((p["id"], target.strip()))
                continue
            add_edge(p["id"], rid, "EXTRACTED")

    # Pass 2：推断边（共同邻居 + 共享标签 + 共同来源）
    base_adj = {k: set(v) for k, v in adj.items()}  # 冻结在 EXTRACTED 结构上，保证确定性
    for i, a in enumerate(pages):
        for b in pages[i + 1:]:
            if tuple(sorted((a["id"], b["id"]))) in seen:
                continue
            ta = set(a["tags"]) - GENERIC_TAGS
            tb = set(b["tags"]) - GENERIC_TAGS
            sa, sb = set(a["sources"]), set(b["sources"])
            base = 0.0
            if ta and tb:
                base += len(ta & tb) / len(ta | tb) * 0.6
            if sa and sb:
                base += len(sa & sb) / len(sa | sb) * 0.4
            na, nb = base_adj[a["id"]], base_adj[b["id"]]
            union = na | nb
            nb_jac = (len(na & nb) / len(union)) if union else 0.0   # 邻居 Jaccard 相似度
            score = 0.6 * nb_jac + 0.4 * base
            if score >= 0.25:
                add_edge(a["id"], b["id"], "INFERRED", score)

    group, comms = label_propagation([p["id"] for p in pages], adj)

    degree = {p["id"]: len(adj[p["id"]]) for p in pages}
    nodes = [{
        "id": p["id"],
        "label": p["label"],
        "title": p["title"],
        "type": p["type"],
        "group": group.get(p["id"], 0),
        "color": PALETTE[group.get(p["id"], 0) % len(PALETTE)],
        "degree": degree[p["id"]],
        "file": p["file"],
    } for p in pages]

    top = sorted(nodes, key=lambda n: (-n["degree"], n["id"]))[:5]
    data = {
        "generated": date.today().isoformat(),
        "stats": {
            "pages": len(nodes),
            "extracted_edges": sum(1 for e in edges if e["kind"] == "EXTRACTED"),
            "inferred_edges": sum(1 for e in edges if e["kind"] == "INFERRED"),
            "communities": len(comms),
        },
        "nodes": nodes,
        "edges": edges,
        "communities": [{"id": i, "size": len(m), "members": m,
                         "color": PALETTE[i % len(PALETTE)]} for i, m in enumerate(comms)],
        "top_nodes": [{"id": n["id"], "degree": n["degree"]} for n in top],
        "broken_links": [{"page": a, "link": b} for a, b in broken],
    }

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    # newline="\n"：生成物跨平台逐字节一致（否则 Windows 上会写成 CRLF）
    (GRAPH_DIR / "graph.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    html = HTML_TEMPLATE.replace("/*__GRAPH_DATA__*/", payload)

    # 落盘前自检：脚本必须语法健全。一处括号手误会让浏览器整段脚本解析失败
    # → 页面白屏，而文件本身看上去完全正常，最难排查。
    script = "".join(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S))
    js_errors = js_balance_errors(script)
    if js_errors:
        print("✗ 生成的脚本未通过括号自检，已放弃写出 graph.html：")
        for e in js_errors:
            print(f"  - {e}")
        return 1

    (GRAPH_DIR / "graph.html").write_text(html, encoding="utf-8", newline="\n")

    # 控制台摘要
    s = data["stats"]
    print("=== 知识图谱构建完成 ===")
    print(f"节点 {s['pages']} 个 · 边 {s['extracted_edges'] + s['inferred_edges']} 条"
          f"（确定 {s['extracted_edges']} / 推断 {s['inferred_edges']}）· 社区 {s['communities']} 个")
    print("最中心的页面：")
    for n in top:
        print(f"  - {n['title']}（{n['id']}） 连接度 {n['degree']}")
    if broken:
        print(f"\n⚠️ 发现 {len(broken)} 条断链：")
        for a, b in broken[:10]:
            print(f"  - {a} -> [[{b}]]")
    print("\n产出：graph/graph.json · graph/graph.html（双击打开）")

    if args.report or args.save:
        report = build_report(data)
        if args.save:
            out = GRAPH_DIR / "graph-report.md"
            out.write_text(report, encoding="utf-8", newline="\n")
            print(f"已写入 {out.relative_to(ROOT)}")
        if args.report:
            print("\n" + report)
    return 0


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>知识库图谱 · LLM Wiki</title>
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; height: 100%; font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif; }
  body { background: #f6f7f9; color: #1f2328; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
  header { padding: 12px 18px; background: #ffffff; border-bottom: 1px solid #e3e6ea; display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
  header h1 { font-size: 15px; margin: 0; font-weight: 600; }
  header .meta { font-size: 12px; color: #6b7280; }
  header .spacer { flex: 1; }
  button { font: inherit; font-size: 12px; padding: 5px 11px; border: 1px solid #d5d9df; background: #fff; border-radius: 6px; cursor: pointer; color: #1f2328; }
  button:hover { background: #f0f2f5; }
  main { flex: 1; display: flex; min-height: 0; }
  #canvas-wrap { flex: 1; position: relative; }
  canvas { display: block; cursor: grab; }
  canvas.dragging { cursor: grabbing; }
  aside { width: 280px; background: #fff; border-left: 1px solid #e3e6ea; padding: 16px; overflow-y: auto; font-size: 13px; }
  aside h2 { font-size: 13px; margin: 0 0 6px; }
  aside .tag { display: inline-block; font-size: 11px; padding: 1px 7px; border-radius: 10px; background: #eef1f5; color: #4b5563; margin: 0 4px 4px 0; }
  aside .row { margin: 8px 0; color: #4b5563; }
  aside .nb { display: block; padding: 4px 6px; border-radius: 5px; cursor: pointer; color: #2563eb; text-decoration: none; }
  aside .nb:hover { background: #f2f6ff; }
  footer { padding: 8px 18px; background: #fff; border-top: 1px solid #e3e6ea; font-size: 12px; color: #6b7280; display: flex; gap: 18px; flex-wrap: wrap; align-items: center; }
  .dot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 5px; vertical-align: middle; }
  .line { display:inline-block; width: 22px; height: 0; border-top: 2px solid #9aa2ad; margin-right: 5px; vertical-align: middle; }
  .line.dashed { border-top-style: dashed; }
  #hint { position: absolute; left: 14px; bottom: 12px; font-size: 12px; color: #8a919b; pointer-events: none; }
</style>
</head>
<body>
<header>
  <h1>知识库图谱</h1>
  <span class="meta" id="meta"></span>
  <span class="spacer"></span>
  <button id="btn-inferred">隐藏推断边</button>
  <button id="btn-labels">只显示枢纽标签</button>
  <button id="btn-reset">重新布局</button>
</header>
<main>
  <div id="canvas-wrap">
    <canvas id="graph"></canvas>
    <div id="hint">滚轮缩放 · 拖拽节点 · 点击查看连接</div>
  </div>
  <aside id="panel">
    <h2>关于这张图</h2>
    <div class="row">节点 = wiki 页面；实线 = 页面里真实存在的 <code>[[wikilink]]</code>；虚线 = 由共享标签/来源推断出的隐性关联。</div>
    <div class="row">点击任意节点查看它的类型、连接度与邻居。</div>
    <div class="row" id="legend-box"></div>
  </aside>
</main>
<footer>
  <span><span class="line"></span>EXTRACTED 确定边</span>
  <span><span class="line dashed"></span>INFERRED 推断边</span>
  <span id="comm-legend"></span>
</footer>
<script>
const GRAPH = /*__GRAPH_DATA__*/;
const canvas = document.getElementById('graph');
const ctx = canvas.getContext('2d');
const wrap = document.getElementById('canvas-wrap');
let W = 0, H = 0, DPR = 1;

const nodes = GRAPH.nodes.map(n => Object.assign({}, n, { x: 0, y: 0, vx: 0, vy: 0 }));
const byId = new Map(nodes.map(n => [n.id, n]));
const links = GRAPH.edges.filter(e => byId.has(e.source) && byId.has(e.target))
                         .map(e => Object.assign({}, e));
let selected = null, hovered = null, dragged = null, showInferred = true, allLabels = true;

function drawInit() {
  const n = nodes.length || 1, R = Math.min(W, H) * 0.34;
  nodes.forEach((p, i) => {
    const a = i / n * Math.PI * 2;
    p.x = W / 2 + Math.cos(a) * R;
    p.y = H / 2 + Math.sin(a) * R;
    p.vx = p.vy = 0;
  });
  selected = null; hovered = null; renderPanel(null);
}

function resize() {
  const r = wrap.getBoundingClientRect();
  W = r.width; H = r.height; DPR = window.devicePixelRatio || 1;
  canvas.width = W * DPR; canvas.height = H * DPR;
  canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
}
window.addEventListener('resize', () => { resize(); });

const radiusOf = n => 9 + Math.min(n.degree, 8) * 2.2;
const neighbors = id => {
  const s = new Set();
  links.forEach(l => { if (l.source === id) s.add(l.target); if (l.target === id) s.add(l.source); });
  return s;
};

function physics() {
  const REP = 26000, SPRING = 0.012, REST = 108, DAMP = 0.86, GRAV = 0.006, ITER = 3;
  for (let step = 0; step < ITER; step++) {
    for (let i = 0; i < nodes.length; i++) {
      const a = nodes[i];
      for (let j = i + 1; j < nodes.length; j++) {
        const b = nodes[j];
        let dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy;
        if (d2 < 1) { d2 = 1; dx = Math.random() - 0.5; dy = Math.random() - 0.5; }
        const d = Math.sqrt(d2), f = REP / d2;
        const fx = dx / d * f, fy = dy / d * f;
        a.vx -= fx; a.vy -= fy; b.vx += fx; b.vy += fy;
      }
    }
    for (const l of links) {
      const a = byId.get(l.source), b = byId.get(l.target);
      let dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy) || 1;
      const f = (d - REST) / d * SPRING;
      const fx = dx * f, fy = dy * f;
      a.vx += fx; a.vy += fy; b.vx -= fx; b.vy -= fy;
    }
    for (const n of nodes) {
      n.vx += (W / 2 - n.x) * GRAV;
      n.vy += (H / 2 - n.y) * GRAV;
    }
    for (const n of nodes) {
      if (n === dragged) continue;
      n.vx *= DAMP; n.vy *= DAMP;
      n.x += n.vx; n.y += n.vy;
      const m = radiusOf(n) + 8;
      n.x = Math.max(m, Math.min(W - m, n.x));
      n.y = Math.max(m, Math.min(H - m, n.y));
    }
  }
}

function draw() {
  ctx.clearRect(0, 0, W, H);
  const focus = hovered || selected;
  const nb = focus ? neighbors(focus) : null;
  const labelBudget = allLabels ? Infinity : 8;

  for (const l of links) {
    if (!showInferred && l.kind === 'INFERRED') continue;
    const a = byId.get(l.source), b = byId.get(l.target);
    const inFocus = !focus || (focus === l.source || focus === l.target);
    ctx.beginPath();
    ctx.setLineDash(l.kind === 'INFERRED' ? [4, 4] : []);
    ctx.strokeStyle = inFocus ? (l.kind === 'INFERRED' ? '#c3c9d2' : '#b6bdc7') : '#eceff3';
    ctx.lineWidth = inFocus ? (l.kind === 'INFERRED' ? 1 : 1.6) : 0.8;
    ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
  }
  ctx.setLineDash([]);

  for (const n of nodes) {
    const r = radiusOf(n);
    const dim = focus && n !== focus && !(nb && nb.has(n.id));
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fillStyle = n.color;
    ctx.globalAlpha = dim ? 0.22 : 1;
    ctx.fill();
    if (n === selected) { ctx.lineWidth = 3; ctx.strokeStyle = '#1f2328'; ctx.stroke(); }
    ctx.globalAlpha = 1;

    if (n.degree >= labelBudget || n === focus || (nb && nb.has(n.id))) {
      const t = n.label, ty = n.y + r + 12;
      ctx.globalAlpha = dim ? 0.3 : 1;
      ctx.font = (n.degree >= 4 ? '600 12px' : '12px') + ' -apple-system, "Microsoft YaHei", sans-serif';
      const w = ctx.measureText(t).width;
      ctx.fillStyle = 'rgba(255,255,255,.82)';
      ctx.fillRect(n.x - w / 2 - 3, ty - 10, w + 6, 14);
      ctx.fillStyle = '#1f2328';
      ctx.textAlign = 'center';
      ctx.fillText(t, n.x, ty);
      ctx.globalAlpha = 1;
    }
  }
}

function loop() { physics(); draw(); requestAnimationFrame(loop); }

function nodeAt(mx, my) {
  for (let i = nodes.length - 1; i >= 0; i--) {
    const n = nodes[i];
    if (Math.hypot(mx - n.x, my - n.y) <= radiusOf(n) + 3) return n;
  }
  return null;
}

canvas.addEventListener('mousemove', e => {
  const r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
  if (dragged) { dragged.x = mx; dragged.y = my; dragged.vx = dragged.vy = 0; return; }
  const n = nodeAt(mx, my);
  hovered = n;
  canvas.style.cursor = n ? 'pointer' : 'grab';
});
canvas.addEventListener('mousedown', e => {
  const r = canvas.getBoundingClientRect();
  const n = nodeAt(e.clientX - r.left, e.clientY - r.top);
  if (n) { dragged = n; canvas.classList.add('dragging'); }
});
window.addEventListener('mouseup', () => { dragged = null; canvas.classList.remove('dragging'); });
canvas.addEventListener('click', e => {
  const r = canvas.getBoundingClientRect();
  const n = nodeAt(e.clientX - r.left, e.clientY - r.top);
  selected = n; renderPanel(n);
});
canvas.addEventListener('wheel', e => {
  e.preventDefault();
}, { passive: false });

function renderPanel(n) {
  const p = document.getElementById('panel');
  if (!n) {
    p.innerHTML = '<h2>关于这张图</h2>' +
      '<div class="row">节点 = wiki 页面；实线 = 页面里真实存在的 <code>[[wikilink]]</code>；' +
      '虚线 = 由共享标签/来源推断出的隐性关联。</div>' +
      '<div class="row">点击任意节点查看它的类型、连接度与邻居。</div>';
    return;
  }
  const nb = Array.from(neighbors(n.id)).sort();
  let html = '<h2>' + esc(n.title) + '</h2>';
  html += '<span class="tag">' + esc(n.type) + '</span>';
  html += '<span class="tag">连接度 ' + n.degree + '</span>';
  html += '<div class="row">文件：<code>' + esc(n.file) + '</code></div>';
  html += '<div class="row"><b>邻居（' + nb.length + '）</b></div>';
  html += nb.map(id => '<a class="nb" data-id="' + esc(id) + '">' + esc(byId.get(id).label) + '</a>').join('');
  p.innerHTML = html;
  p.querySelectorAll('.nb').forEach(el => el.addEventListener('click', () => {
    const t = byId.get(el.dataset.id); selected = t; renderPanel(t);
  }));
}
function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

document.getElementById('btn-inferred').addEventListener('click', e => {
  showInferred = !showInferred;
  e.target.textContent = showInferred ? '隐藏推断边' : '显示推断边';
});
document.getElementById('btn-labels').addEventListener('click', e => {
  allLabels = !allLabels;
  e.target.textContent = allLabels ? '只显示枢纽标签' : '显示全部标签';
});
document.getElementById('btn-reset').addEventListener('click', drawInit);

document.getElementById('meta').textContent =
  GRAPH.stats.pages + ' 个页面 · ' + (GRAPH.stats.extracted_edges + GRAPH.stats.inferred_edges) +
  ' 条边 · ' + GRAPH.stats.communities + ' 个社区 · ' + GRAPH.generated;
document.getElementById('comm-legend').innerHTML = GRAPH.communities.map(c =>
  '<span class="dot" style="background:' + c.color + '"></span>社区 ' + (c.id + 1) + '（' + c.size + '）').join(' ');

resize();
drawInit();
loop();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    sys.exit(main())
