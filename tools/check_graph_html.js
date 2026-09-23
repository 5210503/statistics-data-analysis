#!/usr/bin/env node
// 可选工具：深度校验 graph/graph.html（需要 Node.js；核心工具链仍为纯标准库）。
//
//   node tools/check_graph_html.js
//
// 做三件事：
//   ① 抽出内联 <script>（确认零外链、确实自包含）
//   ② 交给真实 JS 引擎做语法检查（build_graph.py 的括号自检只挡括号手误，
//      挡不住 GRAPH.node.map(...) 这类属性名笔误——那会运行时 TypeError、同样白屏）
//   ③ 在 mock DOM / Canvas 里把脚本跑一遍，验证加载与交互路径不抛异常
//
// 之所以值得常备：一处内联脚本的语法/属性笔误会让整页白屏，
// 而 HTML 文件本身看上去完全正常、数据也合法，靠"看文件"发现不了。
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const HTML = path.join(ROOT, 'graph', 'graph.html');
const GRAPH_JSON = path.join(ROOT, 'graph', 'graph.json');

let fails = 0;
const ok = m => console.log('✅ ' + m);
const bad = m => { fails++; console.log('✗ ' + m); };

// ── ① 抽出内联脚本 ───────────────────────────────────────────────
const html = fs.readFileSync(HTML, 'utf8');
const blocks = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (!blocks.length) { bad('未找到内联 <script>'); process.exit(1); }
const js = blocks.join('\n');
const external = /<(?:script|link)[^>]+(?:src|href)=["'](?:https?:)?\/\//i.test(html);
if (external) bad('页面含外部资源引用，不再是自包含');
else ok(`自包含：0 外链，内联脚本 ${js.length} 字符 / ${blocks.length} 块`);

// ── ② 真实引擎语法检查 ───────────────────────────────────────────
try {
  new vm.Script(js, { filename: 'graph.html:inline' });
  ok('脚本语法通过（真实 JS 引擎解析）');
} catch (e) {
  bad('脚本语法错误：' + e.message);
  process.exit(1);
}

// ── ③ mock DOM / Canvas 跑一遍 ───────────────────────────────────
const ctxStub = new Proxy({ measureText: t => ({ width: String(t).length * 7 }) }, {
  get: (t, p) => (p in t ? t[p] : () => {}),
  set: (t, p, v) => { t[p] = v; return true; },
});
const elements = {};
const makeEl = id => ({
  id, style: {}, dataset: {}, textContent: '', innerHTML: '', width: 0, height: 0,
  classList: { add() {}, remove() {} },
  addEventListener() {},
  getBoundingClientRect: () => ({ left: 0, top: 0, width: 800, height: 600 }),
  getContext: () => ctxStub,
  querySelectorAll: () => [],
});

let raf = 0;
const sandbox = {
  console,
  document: { getElementById: id => (elements[id] ||= makeEl(id)) },
  window: { devicePixelRatio: 1, addEventListener() {} },
  requestAnimationFrame: fn => { if (raf++ < 3) fn(); },
};

const probe = `
globalThis.__probe = (() => {
  const out = {};
  out.counts = [GRAPH.nodes.length, GRAPH.edges.length];
  out.dangling = GRAPH.edges.filter(e => !byId.has(e.source) || !byId.has(e.target)).length;
  const target = nodes.find(n => n.id === 'AgentSkill') || nodes[0];
  renderPanel(target);
  out.panel = document.getElementById('panel').innerHTML;
  out.meta = document.getElementById('meta').textContent;
  out.legend = document.getElementById('comm-legend').innerHTML;
  renderPanel(null);
  out.panelReset = document.getElementById('panel').innerHTML;
  return out;
})();
`;

try {
  vm.runInNewContext(js + probe, sandbox, { filename: 'graph.html:inline' });
  ok('加载 / 点击 / 重置 全路径无异常');
} catch (e) {
  bad(`运行期抛错：${e.name}: ${e.message}`);
  process.exit(1);
}

const p = sandbox.__probe;
if (!p) { bad('探针未返回结果'); process.exit(1); }

// 与 graph.json 对齐
const gj = JSON.parse(fs.readFileSync(GRAPH_JSON, 'utf8'));
const same = p.counts[0] === gj.nodes.length && p.counts[1] === gj.edges.length;
(same ? ok : bad)(`内嵌数据与 graph.json 一致：${p.counts[0]} 节点 / ${p.counts[1]} 边（json: ${gj.nodes.length} / ${gj.edges.length}）`);
if (p.dangling === 0) ok('无悬空边（每条边的两端都存在于节点集）');
else bad(`${p.dangling} 条边的端点不存在`);
if (Math.max(p.counts[0], 0) > 0 && p.panelReset.includes('关于这张图')) ok('面板渲染与重置正常');
else bad('面板渲染异常');
if (p.meta && p.legend) ok(`文案就绪：${p.meta}`);
else bad('meta / 图例未填充');

console.log(fails ? `\n${fails} 项未通过` : '\ngraph.html 深度校验全部通过');
process.exit(fails ? 1 : 0);
