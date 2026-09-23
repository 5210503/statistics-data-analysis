#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LLM Wiki · 结构体检（零 LLM 调用）

检查项：
  1. 空文件 / 存根 —— 除 frontmatter 外几乎没有内容的页面
  2. 断链         —— [[wikilink]] 指向不存在的页面
  3. 索引同步     —— wiki/index.md 条目 vs 磁盘真实文件
  4. 日志覆盖     —— 来源页是否都有对应的 ingest 日志

用法：
  python tools/health.py            # 人类可读报告
  python tools/health.py --json     # 机器可读 JSON
  python tools/health.py --save     # 同时写入 wiki/health-report.md
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
INDEX = WIKI / "index.md"
LOG = WIKI / "log.md"
CONTENT_DIRS = ("sources", "entities", "concepts", "syntheses")
STUB_THRESHOLD = 60  # 正文（去 frontmatter 后）少于该字符数视为存根

FM_RE = re.compile(r"^\ufeff?\s*---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", re.DOTALL)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def split_frontmatter(text: str):
    """返回 (frontmatter 原文, 正文)。兼容 BOM 与前置空白。"""
    m = FM_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def parse_kv(fm: str) -> dict:
    out = {}
    for line in fm.splitlines():
        if ":" in line and not line.strip().startswith("#"):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def all_wiki_pages():
    pages = []
    for p in sorted(WIKI.rglob("*.md")):
        if p.name in ("index.md", "log.md", "overview.md", "health-report.md", "lint-report.md"):
            continue
        pages.append(p)
    return pages


def build_id_map(pages):
    """basename(小写) -> 相对 wiki/ 的 posix 路径"""
    m = {}
    for p in pages:
        rel = p.relative_to(WIKI).as_posix()
        m[p.stem.lower()] = rel
    return m


def run_checks():
    if not WIKI.exists():
        print("找不到 wiki/ 目录，请确认在仓库根目录运行。", file=sys.stderr)
        sys.exit(2)

    pages = all_wiki_pages()
    id_map = build_id_map(pages)

    stubs, broken, missing_from_index, missing_on_disk, log_missing = [], [], [], [], []

    # 1 + 2：逐页检查
    for p in pages:
        rel = p.relative_to(WIKI).as_posix()
        text = read(p)
        body = split_frontmatter(text)[1].strip()
        if len(body) < STUB_THRESHOLD:
            stubs.append({"page": rel, "body_chars": len(body)})
        for target in WIKILINK_RE.findall(text):
            key = target.strip().lower()
            if key not in id_map:
                broken.append({"page": rel, "link": target.strip()})

    # 3：索引同步
    disk = {p.relative_to(WIKI).as_posix() for p in pages}
    indexed = set()
    if INDEX.exists():
        for raw in MD_LINK_RE.findall(read(INDEX)):
            raw = raw.split("#")[0].strip()
            if not raw or raw.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (INDEX.parent / raw).resolve()
            if resolved.suffix == ".md" and resolved.exists():
                try:
                    rel = resolved.relative_to(WIKI.resolve()).as_posix()
                except ValueError:
                    continue
                if rel.startswith(CONTENT_DIRS):
                    indexed.add(rel)
    else:
        missing_from_index.append({"page": "index.md", "reason": "index.md 不存在"})
    missing_from_index += [{"page": r} for r in sorted(disk - indexed)]
    missing_on_disk += [{"page": r} for r in sorted(indexed - disk)]

    # 4：日志覆盖
    log_text = read(LOG) if LOG.exists() else ""
    for p in pages:
        if p.parent.name != "sources":
            continue
        slug = p.stem
        if slug not in log_text:
            log_missing.append({"page": p.relative_to(WIKI).as_posix(), "slug": slug})

    issues = len(stubs) + len(broken) + len(missing_from_index) + len(missing_on_disk) + len(log_missing)
    return {
        "generated": date.today().isoformat(),
        "total_pages": len(pages),
        "issues": issues,
        "stubs": stubs,
        "broken_links": broken,
        "missing_from_index": missing_from_index,
        "missing_on_disk": missing_on_disk,
        "log_missing": log_missing,
    }


def render(report: dict) -> str:
    L = []
    L.append("# LLM Wiki · 结构体检报告")
    L.append("")
    L.append(f"> 生成日期：{report['generated']} · 扫描页面：{report['total_pages']} 个 · 问题：{report['issues']} 项")
    L.append("")
    if report["issues"] == 0:
        L.append("✅ 全部通过：无空文件、无断链、索引与日志均已同步。")
        return "\n".join(L)

    def block(title, items, fmt):
        if not items:
            L.append(f"✅ {title}：无问题")
        else:
            L.append(f"⚠️ {title}（{len(items)}）")
            L.extend(fmt(i) for i in items)
        L.append("")

    block("空文件 / 存根", report["stubs"],
          lambda i: f"- `{i['page']}` —— 正文仅 {i['body_chars']} 字符")
    block("断链", report["broken_links"],
          lambda i: f"- `{i['page']}` 中的 `[[{i['link']}]]` 指向不存在的页面")
    block("未登记进 index.md", report["missing_from_index"],
          lambda i: f"- `{i['page']}`")
    block("index.md 指向了不存在的文件", report["missing_on_disk"],
          lambda i: f"- `{i['page']}`")
    block("来源页缺少 ingest 日志", report["log_missing"],
          lambda i: f"- `{i['page']}`（log.md 中未见 `{i['slug']}`）")
    L.append("---")
    L.append("修复建议：补内容 / 修正链接目标 / 在 index.md 登记 / 在 log.md 追加对应条目。")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="LLM Wiki 结构体检")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--save", action="store_true", help="写入 wiki/health-report.md")
    args = ap.parse_args()

    report = run_checks()
    if args.save:
        out = WIKI / "health-report.md"
        out.write_text(render(report), encoding="utf-8", newline="\n")
        print(f"已写入 {out.relative_to(ROOT)}")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render(report))
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
