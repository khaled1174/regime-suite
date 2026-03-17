# Live Data Dashboard Refactor — Design Spec

**Date:** 2026-03-16
**File:** `regime_live_data.html`
**Approach:** Clean Split (B) — fix violations + decompose `runAnalysis()`

---

## Hard Rules

| Rule | Enforcement |
|------|-------------|
| `chart.destroy()` | FORBIDDEN — use `chart.data = ...; chart.update()` |
| `innerHTML =` inside switch/run | FORBIDDEN — use pre-rendered CSS layers |
| `display: none` | FORBIDDEN — use `classList.add/remove('hidden','visible')` |
| Chart.js source | `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js` |
| Background color | `#0d1117` |
| Layer swap pattern | `classList.add/remove('hidden','visible')` only |

---

## Violation Fixes

### V1. Remove `chart.destroy()` (line 570)

**Current:**
```js
Object.values(charts).forEach(c => { try { c.destroy(); } catch(e) {} });
charts = {};
charts.hmm = new Chart(...); // rebuilt every time
```

**New:** Init-once + update pattern:
```js
let chartsReady = false;

function initCharts(ds) {
  charts.hmm = new Chart($('c-hmm').getContext('2d'), { /* config with ds data */ });
  // ...all 5 charts
  chartsReady = true;
}

function updateCharts(results) {
  const ds = downsample(results, 120);
  if (!chartsReady) { initCharts(ds); return; }
  charts.hmm.data.labels = ds.labels;
  charts.hmm.data.datasets[0].data = ds.prices;
  charts.hmm.data.datasets[1].data = ds.regBg;
  charts.hmm.update();
  // ...all 5 charts
}
```

### V2. Remove `innerHTML =` (lines 389, 394, 592)

**Current:**
```js
overlay.innerHTML = `<div class="spinner">...</div>`;
```

**New:** 3 pre-rendered overlay layers in HTML:
```html
<div class="loading-overlay" id="loading-overlay">
  <div class="ov-layer visible" id="ov-idle">
    <div style="text-align:center">
      <div style="font-size:28px;margin-bottom:8px">📡</div>
      <div style="font-size:12px;color:#c9d1d9">Press Run Analysis to load live data</div>
      <div style="font-size:10px;color:#6e7681">Fetches real OHLCV from Yahoo Finance</div>
    </div>
  </div>
  <div class="ov-layer hidden" id="ov-loading">
    <div class="spinner"></div>
    <div class="loading-msg" id="loading-text">Fetching...</div>
  </div>
  <div class="ov-layer hidden" id="ov-error">
    <div class="error-msg" id="error-text"></div>
  </div>
</div>
```

Controlled by:
```js
function showOverlay(state, msg) {
  const overlay = $('loading-overlay');
  overlay.classList.remove('gone');
  ['idle','loading','error'].forEach(s => {
    const el = $('ov-' + s);
    el.classList.toggle('visible', s === state);
    el.classList.toggle('hidden', s !== state);
  });
  if (state === 'loading') $('loading-text').textContent = msg;
  if (state === 'error')   $('error-text').textContent = msg;
  if (state === 'done')    overlay.classList.add('gone');
}
```

CSS for overlay layers:
```css
.ov-layer { position:absolute; inset:0; display:flex; flex-direction:column;
            align-items:center; justify-content:center; gap:12px;
            transition: opacity .3s, transform .3s; }
.ov-layer.hidden  { opacity:0; transform:translateY(6px); pointer-events:none; }
.ov-layer.visible { opacity:1; transform:translateY(0); }
```

---

## Decomposition of `runAnalysis()`

### Current: 1 function, ~215 lines
### Target: 5 pipeline stages + helper functions

### Pipeline

```
runAnalysis()           ~20 lines — orchestrator
  ├→ fetchData()        ~8 lines  — async, returns {prices, dates}
  ├→ computeAll()       ~20 lines — pure, returns results{}
  ├→ updateCards()      ~60 lines — DOM textContent only
  ├→ updateCharts()     ~15 lines — chart.update() or initCharts()
  └→ updateBottom()     ~10 lines — delegates to 3 sub-functions
       ├→ updateRegimePanels()   ~20 lines
       ├→ updateStatsPanels()    ~25 lines
       └→ updateTransitionBars() ~20 lines
```

### Global State (minimal)

```js
const $ = id => document.getElementById(id);
let charts = {};
let chartsReady = false;
let current = 'hmm';
```

Everything else is passed as function arguments.

### Function Signatures

```js
// Data
async function fetchData(ticker, years) → { prices: number[], dates: string[] }

// Compute — all pure functions
function computeAll(prices, dates, K) → {
  rets: number[],           // log returns
  datesR: string[],         // dates aligned to returns (dates.slice(1))
  pricesR: number[],        // prices aligned to returns (prices.slice(1))
  vols: number[],           // rolling 20d annualized vol
  gVol: number[],           // GARCH conditional vol (annualized %)
  hReg: number[],           // HMM regime labels [0,1,2]
  hmmStats: {ret,vol,pct}[],// per-state mean return, mean vol, % of time (3 items)
  hmmBull: number[],        // binary array: 1 if hReg===0, else 0
  gmm: {bull[],neut[],bear[]}, // GMM probability arrays
  km: {labels[],cents[],sorted[]}, // from runKMeans
  kmLabels: number[],       // remapped labels after centroid sorting
  gReg: {labels[],loThr,hiThr}, // from garchRegimes
  ensBull: number[],        // per-day ensemble score (0-4)
  ensLabel: number,         // final ensemble verdict (0/1/2)
  curRegimes: {hmm,gmm,km,garch}, // current-day regime per model
  lastPrice: number,
  prevPrice: number,
  K: number
}
function runKMeans(rets, vols, K) → { labels: number[], cents: object[], sorted: array }
function garchRegimes(gVol) → { labels: number[], loThr: number, hiThr: number }
function ensembleVote(hReg, gmm, kmLabels, gReg) → { scores: number[], label: number }

// View — DOM updates only
function showOverlay(state, msg?)
function updateCards(results)
function updateCharts(results)
function initCharts(downsampledData)
function downsample(results, maxPoints) → { labels, prices, regBg, gmmB, gmmN, gmmBr, gVol, gRet, ensS, hmmP }
function updateBottom(results)
function updateRegimePanels(results)
function updateStatsPanels(results)
function updateTransitionBars(results)

// Navigation — unchanged
function go(model)
```

### Extraction Details

| Current lines | Extracted to | What it does |
|--------------|-------------|-------------|
| 391-401 | `fetchData()` | fetchYahoo + validation + split prices/dates |
| 402-427 | `computeAll()` | calls all model functions, assembles results |
| 413-416 | `runKMeans()` | kmeans() + centroid sorting + label mapping |
| 419-421 | `garchRegimes()` | percentile thresholds on gVol |
| 424-427 | `ensembleVote()` | majority voting across 4 models |
| 429-553 | `updateCards()` | all getElementById().textContent updates for cards, badges, sidebar price |
| 555-586 | `updateCharts()` + `initCharts()` + `downsample()` | chart data pipeline |
| 501-549 | `updateBottom()` → 3 sub-functions | regime panels, stats, transition bars |

### Dead Code Removal

- `rollRet()` call on line 403 — result `rrets` is assigned but never consumed downstream. Remove the call first, then remove the function definition on line 307.
- `globalData` (line 380) — declared but never used, remove it

### Additional `innerHTML` Violations

Lines 589 and 593 use `btn.innerHTML` with HTML entities:
```js
btn.innerHTML = '↺ Refresh';      // line 589
btn.innerHTML = '▶ Run Analysis'; // line 593
```
Fix: use `textContent` with unicode directly:
```js
btn.textContent = '\u21BA Refresh';       // ↺
btn.textContent = '\u25B6 Run Analysis';  // ▶
```

---

## Allowed Patterns

- `.style.color = ...` and `.style.width = ...` — allowed for dynamic regime colors and transition bar widths. These are data-driven values that change per-run and cannot be pre-defined as CSS classes.
- `.textContent = ...` — the primary method for all DOM text updates.
- `classList.add/remove('hidden','visible')` — the only method for show/hide.

---

## What Does NOT Change

- HTML structure of sidebar, nav, state cards, bottom panels — identical
- `go()` function — already compliant, untouched
- `fetchYahoo()` — untouched (data layer)
- Math helpers: `returns()`, `rollVol()`, `garch()`, `pct()`, `pctS()` — untouched
- Model approximations: `hmmRegimes()`, `gmmProbs()`, `kmeans()` — untouched
- CSS for all existing components — untouched
- Chart.js CDN source — untouched
- All element IDs — untouched

---

## File Output

Single file: `regime_live_data.html` (self-contained, no external JS modules)

### Section Order in File

```
1. <style>         — existing CSS + new .ov-layer rules
2. <div class="app"> — HTML with modified loading overlay
3. <script src=Chart.js>
4. <script>
   a. Constants:    MODELS, GROUPS, META
   b. Globals:      $, charts, chartsReady, current
   c. Navigation:   go()
   d. Utilities:    pct, pctS, returns, rollVol, garch
   e. Models:       hmmRegimes, gmmProbs, kmeans, runKMeans, garchRegimes, ensembleVote
   f. Data:         fetchYahoo, fetchData
   g. View:         showOverlay, updateCards, initCharts, downsample, updateCharts,
                    updateRegimePanels, updateStatsPanels, updateTransitionBars, updateBottom
   h. Orchestrator: runAnalysis
```
