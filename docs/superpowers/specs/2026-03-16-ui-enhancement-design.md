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
| `bg_secondary` | `#161b22` | `rgba(255,255,255,0.05)` + `backdrop-filter:blur(12px)` | Glass effect |
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

### Plotly Theme Updates

- `paper_bgcolor` and `plot_bgcolor`: `#0f172a`
- Legend background: `rgba(255,255,255,0.05)`
- Legend border: `rgba(255,255,255,0.1)`
- Grid color: `rgba(255,255,255,0.06)`
- Chart bars use `linear-gradient` style via marker color arrays

### Files Changed

- `core/theme.py`: Update `COLORS`, `ROLE_COLOR_BG`, `SHARED_CSS`, `plotly_base_layout()`, `plotly_axis_style()`

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
    """Show skeleton placeholder cards while loading."""
    # Renders gray pulsing cards matching metric-card dimensions
    # + chart placeholder rectangle
    # + regime banner placeholder
```

Uses `st.empty()` containers:
1. Create `placeholder = st.empty()`
2. Render skeleton into placeholder
3. After data loads, replace with real content via `placeholder.empty()` + render real components

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
| `.metric-card` | `fadeInUp` | 0.4s | `nth-child` staggered (0.05s each) |
| `.hero` | `fadeIn` | 0.3s | none |
| `.regime-banner` | `scaleIn` | 0.5s | none |
| Plotly chart container | `fadeIn` | 0.4s | none |

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
| `app.py` | Updated to use new glass theme (automatic via theme.py) |

No new files created. No structural changes. All updates are within existing files.
