# UI Enhancement Design — Regime Suite

**Date:** 2026-03-16
**Approach:** Progressive Enhancement (update existing code incrementally)
**Scope:** Visual theme overhaul + UX improvements within Streamlit

---

## 1. Glass Slate Color System

Replace the current GitHub Dark palette with a Slate + Glassmorphism theme.

### Color Palette

| Token | Current | New | Notes |
|-------|---------|-----|-------|
| `bg_primary` | `#0d1117` | `#0f172a` | Slate 900 |
| `bg_secondary` | `#161b22` | `#1e293b` | Slate 800 (used as token value; glassmorphism via CSS only) |
| `bg_tertiary` | `#070b0f` | `#020617` | Slate 950 |
| `border` | `#30363d` | `rgba(255,255,255,0.1)` | Semi-transparent |
| `border_light` | `#21262d` | `rgba(255,255,255,0.05)` | Subtle separator |
| `text_primary` | `#e6edf3` | `#f1f5f9` | Slate 100 |
| `text_secondary` | `#8b949e` | `#94a3b8` | Slate 400 |
| `text_muted` | `#484f58` | `#475569` | Slate 600 |
| `bull` | `#3fb950` | `#4ade80` | Brighter green |
| `bear` | `#f85149` | `#f87171` | Softer red |
| `neutral` | `#8b949e` | `#94a3b8` | Slate 400 |
| `chop` | `#f0b429` | `#fbbf24` | Amber 400 |
| `accent_blue` | `#58a6ff` | `#60a5fa` | Blue 400 |
| `accent_purple` | `#a371f7` | `#a78bfa` | Violet 400 |

### Glassmorphism Effects

- **Cards:** `background: rgba(255,255,255,0.05)`, `backdrop-filter: blur(12px)`, `border: 1px solid rgba(255,255,255,0.08)`
- **Background glows:** Subtle radial gradients in page corners using `::before` pseudo-elements:
  - Top-right: `radial-gradient(circle at 80% 20%, rgba(96,165,250,0.08), transparent 50%)`
  - Bottom-left: `radial-gradient(circle at 20% 80%, rgba(167,139,250,0.06), transparent 50%)`
- **Hover borders:** Cards glow with accent color on hover: `border-color: rgba(96,165,250,0.3)`

### ROLE_COLOR_BG Updates

| Role | Current | New |
|------|---------|-----|
| bull | `rgba(63,185,80,.12)` | `rgba(74,222,128,.10)` |
| bear | `rgba(248,81,73,.12)` | `rgba(248,113,113,.10)` |
| neutral | `rgba(139,148,158,.10)` | `rgba(148,163,184,.08)` |
| chop | _(missing)_ | `rgba(251,191,36,.08)` |

**Note on `chop`:** In the existing codebase, `chop` is a CSS class alias for the `neutral` role, not a distinct model output. The `render_regime_banner()` function maps `neutral` role → `chop` CSS class. Models only output `bull`, `bear`, and `neutral`. The `chop` entry in `ROLE_COLOR_BG` is used exclusively for banner/chart styling of the neutral regime. No changes needed to model outputs.

### MODEL_COLORS Updates

| Model | Current | New |
|-------|---------|-----|
| HMM | `#58a6ff` | `#60a5fa` |
| GMM | `#a371f7` | `#a78bfa` |
| K-Means | `#f0b429` | `#fbbf24` |
| GARCH | `#f85149` | `#f87171` |
| Ensemble | `#3fb950` | `#4ade80` |

### Plotly Theme Updates

- `paper_bgcolor` and `plot_bgcolor`: `#0f172a`
- Legend background: `rgba(255,255,255,0.05)` (rgba color only, no `backdrop-filter` — Plotly does not support CSS filters)
- Legend border: `rgba(255,255,255,0.1)`
- Grid color: `rgba(255,255,255,0.06)`
- Chart bars use `linear-gradient` style via marker color arrays

### Glassmorphism Note

`COLORS["bg_secondary"]` stores a plain hex value (`#1e293b`). The glassmorphism effects (`backdrop-filter: blur(12px)`, `rgba` backgrounds, glowing borders) are applied only through CSS rules in `SHARED_CSS`, not as color tokens. This keeps the token system compatible with Plotly and inline Python f-strings.

### Regime Banner Background Updates

| Banner | Current | New |
|--------|---------|-----|
| `.regime-banner.bull` | `#0f2a17` | `rgba(74,222,128,0.08)` |
| `.regime-banner.bear` | `#2a0f0f` | `rgba(248,113,113,0.08)` |
| `.regime-banner.chop` | `#1c1c1c` | `rgba(148,163,184,0.06)` |

### Sidebar Styling

The sidebar keeps a solid background (`#0f172a`) rather than glassmorphism, since there is no meaningful content behind it for blur to act on. Border updated to `rgba(255,255,255,0.08)`.

### Hardcoded Inline Colors

The following inline `style=` attributes in page files must be manually updated to use new palette values:

**`app.py`:**
- Line 42: `color:#58a6ff` → `color:#60a5fa`
- Line 48: `color:#a371f7` → `color:#a78bfa`
- Line 56: `color:#f0b429` → `color:#fbbf24`
- Line 64: `color:#f85149` → `color:#f87171`
- Line 72: `color:#3fb950` → `color:#4ade80`
- Line 79: `border-top:3px solid #8b949e` → `border-top:3px solid #94a3b8`
- Line 92: `background:#161b22;border:1px solid #30363d` → `background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);backdrop-filter:blur(12px)`
- All `color:#8b949e` → `color:#94a3b8`
- All `color:#e6edf3` → `color:#f1f5f9`
- All `color:#58a6ff` (step numbers) → `color:#60a5fa`

**`pages/5_Compare.py`:**
- Inline `ROLE_BG` dict must be removed and replaced with `ROLE_COLOR_BG` from `core/theme.py`

**All page files (`pages/1_HMM.py`, `pages/2_GMM.py`, `pages/3_K-Means.py`):**
- Sidebar text colors: `color:#8b949e` → `color:#94a3b8`, `color:#e6edf3` → `color:#f1f5f9`
- Bull/bear/neutral inline colors updated to new values

### Files Changed

- `core/theme.py`: Update `COLORS`, `MODEL_COLORS`, `ROLE_COLOR_BG`, `SHARED_CSS`, `plotly_base_layout()`, `plotly_axis_style()`
- `app.py`: Replace all hardcoded inline color values with new palette
- `pages/1_HMM.py`: Replace inline color values
- `pages/2_GMM.py`: Replace inline color values
- `pages/3_K-Means.py`: Replace inline color values
- `pages/5_Compare.py`: Replace inline `ROLE_BG` dict + inline color values

---

## 2. Smart Presets in Sidebar

Add preset buttons at the top of each model page's sidebar to auto-fill configuration.

### Preset Definitions

```python
PRESETS = {
    "Conservative": {"ticker": "SPY", "lookback": 10, "n_states": 2},
    "Aggressive":   {"ticker": "QQQ", "lookback": 5,  "n_states": 3},
    "High Vol":     {"ticker": "VIX", "lookback": 3,  "n_states": 4},
}
```

### Behavior

1. Preset buttons appear as a horizontal group at the top of the sidebar (styled as pill buttons)
2. Clicking a preset updates `st.session_state` with the preset's values
3. The active preset is highlighted with accent color
4. Input fields below reflect the preset values but remain editable (Custom mode)
5. If the user manually changes any value after selecting a preset, it switches to Custom

### UI Layout (Sidebar)

```
[Conservative] [Aggressive] [High Vol]
─────────────────────────────────────
Ticker Symbol: [SPY]
Lookback (years): [10]
States: [2]
─────────────────────────────────────
[Run Analysis]
```

### Implementation

- New helper function `render_presets(page_key: str)` in `core/theme.py`
- Uses `st.session_state` with page-specific keys (e.g., `hmm_ticker`, `hmm_lookback`)
- Each page calls `render_presets()` in its sidebar block before the input fields

#### `render_presets()` pseudocode

```python
def render_presets(page_key: str) -> dict:
    """
    Render preset buttons and return current config values.
    Returns: {"ticker": str, "lookback": int, "n_states": int}
    """
    # Initialize session state defaults if not set
    if f"{page_key}_preset" not in st.session_state:
        st.session_state[f"{page_key}_preset"] = None

    # Render preset buttons as columns
    cols = st.columns(len(PRESETS))
    for i, (name, config) in enumerate(PRESETS.items()):
        with cols[i]:
            if st.button(name, key=f"{page_key}_preset_{name}"):
                st.session_state[f"{page_key}_preset"] = name
                st.session_state[f"{page_key}_ticker"] = config["ticker"]
                st.session_state[f"{page_key}_lookback"] = config["lookback"]
                st.session_state[f"{page_key}_n_states"] = config["n_states"]
                st.rerun()

    # Return current values (preset or custom)
    return {
        "ticker": st.session_state.get(f"{page_key}_ticker", "SPY"),
        "lookback": st.session_state.get(f"{page_key}_lookback", 10),
        "n_states": st.session_state.get(f"{page_key}_n_states", 3),
    }
```

- Pages read values via: `config = render_presets("hmm")`
- Custom detection: if user changes any input field via `on_change` callback, set `st.session_state[f"{page_key}_preset"] = None`
- Compare page uses the same presets (same ticker/lookback/states apply to all 3 models)

### Files Changed

- `core/theme.py`: Add `PRESETS` dict, `render_presets()` function, preset button CSS
- `pages/1_HMM.py`: Integrate presets in sidebar
- `pages/2_GMM.py`: Integrate presets in sidebar
- `pages/3_K-Means.py`: Integrate presets in sidebar
- `pages/5_Compare.py`: Integrate presets in sidebar

---

## 3. Skeleton Loading + Staged Messages

Replace `st.spinner` with a two-phase loading experience.

### Phase 1: Staged Status Messages

Use `st.status()` to show progressive steps:

```python
with st.status("Running analysis...", expanded=True) as status:
    status.update(label="Downloading market data...")
    df = load_market_data(ticker, lookback)

    status.update(label="Training model...")
    result = fit_model(X, ...)

    status.update(label="Analyzing regimes...")
    # post-processing

    status.update(label="Complete!", state="complete", expanded=False)
```

### Phase 2: Skeleton Cards

Before data loads, show placeholder cards with shimmer animation:

```python
def render_skeleton(n_cards=3):
    """Show skeleton placeholder cards while loading. Returns HTML string."""
    cards = ""
    for _ in range(n_cards):
        cards += """
        <div class="metric-card" style="min-height:90px">
          <div class="skeleton-block" style="width:60px;height:10px;margin-bottom:8px"></div>
          <div class="skeleton-block" style="width:120px;height:16px;margin-bottom:12px"></div>
          <div style="display:flex;gap:16px">
            <div class="skeleton-block" style="flex:1;height:24px"></div>
            <div class="skeleton-block" style="flex:1;height:24px"></div>
            <div class="skeleton-block" style="flex:1;height:24px"></div>
          </div>
        </div>"""

    chart_placeholder = '<div class="skeleton-block" style="height:420px;margin:10px 0"></div>'
    banner_placeholder = '<div class="skeleton-block" style="height:80px;margin-top:10px;border-radius:8px"></div>'

    return f'<div class="metric-grid">{cards}</div>{chart_placeholder}{banner_placeholder}'
```

### Visual Sequencing

1. User clicks "Run Analysis"
2. **Skeleton cards + chart placeholder** appear immediately in the main content area (via `st.empty()`)
3. **`st.status()` widget** appears above the skeleton, showing staged progress messages
4. When loading completes, `st.status()` collapses with "Complete!" state
5. Skeleton placeholders are replaced with real content via `placeholder.empty()` + render real components

### Shimmer CSS

```css
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.skeleton-block {
    background: linear-gradient(90deg,
        rgba(255,255,255,0.03) 25%,
        rgba(255,255,255,0.08) 50%,
        rgba(255,255,255,0.03) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 8px;
}
```

### Files Changed

- `core/theme.py`: Add `render_skeleton()` function, shimmer CSS to `SHARED_CSS`
- `pages/1_HMM.py`: Replace `st.spinner` with `st.status()` + skeleton
- `pages/2_GMM.py`: Same
- `pages/3_K-Means.py`: Same
- `pages/5_Compare.py`: Same

---

## 4. CSS Animations

Add smooth entrance animations for UI elements.

### Keyframes

```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.95); }
    to   { opacity: 1; transform: scale(1); }
}
```

### Application

| Element | Animation | Duration | Delay |
|---------|-----------|----------|-------|
| `.metric-card` | `fadeInUp` | 0.4s | staggered (see CSS below) |
| `.hero` | `fadeIn` | 0.3s | none |
| `.regime-banner` | `scaleIn` | 0.5s | none |
| Plotly chart container | `fadeIn` | 0.4s | none |

#### Staggered Card Animation CSS

```css
.metric-card {
    animation: fadeInUp 0.4s ease both;
}
.metric-grid > .metric-card:nth-child(1) { animation-delay: 0s; }
.metric-grid > .metric-card:nth-child(2) { animation-delay: 0.05s; }
.metric-grid > .metric-card:nth-child(3) { animation-delay: 0.10s; }
.metric-grid > .metric-card:nth-child(4) { animation-delay: 0.15s; }
.metric-grid > .metric-card:nth-child(5) { animation-delay: 0.20s; }
.metric-grid > .metric-card:nth-child(6) { animation-delay: 0.25s; }
```

### Accessibility

```css
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

### Files Changed

- `core/theme.py`: Add keyframes and animation properties to `SHARED_CSS`

---

## Summary of All Files Changed

| File | Changes |
|------|---------|
| `core/theme.py` | New color system, glassmorphism CSS, presets system, skeleton loading, animations |
| `pages/1_HMM.py` | Presets integration, skeleton + status loading |
| `pages/2_GMM.py` | Presets integration, skeleton + status loading |
| `pages/3_K-Means.py` | Presets integration, skeleton + status loading |
| `pages/5_Compare.py` | Presets integration, skeleton + status loading |
| `app.py` | Replace all hardcoded inline colors with new palette values |

No new files created. No structural changes. All updates are within existing files.

---

## Additional Cleanup (Pre-existing Issues)

- **`st.plotly_chart` parameter:** Replace `width="stretch"` with `use_container_width=True` in all page files (the `width` parameter is not a valid Streamlit API)
- **Hero gradient:** Update `linear-gradient(90deg, #58a6ff, #3fb950)` → `linear-gradient(90deg, #60a5fa, #4ade80)` in `SHARED_CSS`
- **`SHARED_CSS` hardcoded colors:** All hex values inside `SHARED_CSS` (e.g., `#0d1117`, `#161b22`, `#30363d`, `#3fb950`, `#f85149`, `#8b949e`) must be updated to match the new palette. The implementer should do a find-and-replace pass across all CSS rules in the string.

---

## Requirements

- **Streamlit >= 1.30.0** (already satisfied in `requirements.txt` — covers `st.status()` which was introduced in 1.25)
