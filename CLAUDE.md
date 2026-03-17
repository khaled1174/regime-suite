# Regime Suite

## Project Overview
- Streamlit multi-page app for market regime detection
- Models: HMM, GMM, K-Means, GARCH, Ensemble
- Remote: https://github.com/khaled1174/regime-suite (branch: main)

## Structure
- `app.py` — Landing page (hero section, model cards grid)
- `pages/` — Model pages (HMM, GMM, K-Means, Compare)
- `core/theme.py` — Central theme: Glass Slate colors, CSS, presets, skeleton, helpers
- `core/data.py` — `load_market_data()`, `get_observation_matrix()`
- `core/models.py` — `fit_hmm()`, `fit_gmm()`, `fit_kmeans()`, `ensemble_vote()`
- `core/metrics.py` — Metrics utilities
- `docs/` — Design specs

## Completed Work
- Glass Slate theme (Tailwind Slate palette: #0f172a, #1e293b, #f1f5f9)
- Glassmorphism CSS (backdrop-filter:blur, rgba backgrounds, radial gradient glows)
- Smart presets via `st.session_state` with page-specific keys
- Skeleton loading with CSS shimmer animation + `st.status()` staged messages
- CSS entrance animations (fadeInUp, fadeIn, scaleIn) with staggered delays
- `prefers-reduced-motion` accessibility support
- Plotly dark theme charts with glassmorphism legend
- Role-based regime colors: bull (#4ade80), bear (#f87171), neutral/chop (#fbbf24)
- Compare page: agreement score, multi-model subplot, rolling agreement, disagreement table
- Code pushed to GitHub main (force-pushed master→main)

## Pending
- App not yet deployed (options: `streamlit run app.py` locally or Streamlit Community Cloud)
- GARCH page (`pages/4_...`) not yet implemented
- Backtest Lab page not yet implemented

## Tech Notes
- `gh` CLI not installed on this machine — use git directly
- Python dependencies in `requirements.txt`
- Run locally: `streamlit run app.py`
