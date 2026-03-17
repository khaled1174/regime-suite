"""
core/theme.py — Shared Dark Theme & UI Components
═══════════════════════════════════════════════════
Single source of truth for CSS and Plotly styling.
"""

import streamlit as st
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════════════════════════
# COLOR SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

COLORS = {
    "bg_primary": "#0f172a",
    "bg_secondary": "#1e293b",
    "bg_tertiary": "#020617",
    "border": "rgba(255,255,255,0.1)",
    "border_light": "rgba(255,255,255,0.05)",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#475569",
    "bull": "#4ade80",
    "bear": "#f87171",
    "neutral": "#94a3b8",
    "chop": "#fbbf24",
    "accent_blue": "#60a5fa",
    "accent_purple": "#a78bfa",
}

# Role mappings
ROLE_COLOR_BG = {
    "bull": "rgba(74,222,128,.10)",
    "bear": "rgba(248,113,113,.10)",
    "neutral": "rgba(148,163,184,.08)",
    "chop": "rgba(251,191,36,.08)",
}
ROLE_COLOR_LINE = {
    "bull": COLORS["bull"],
    "bear": COLORS["bear"],
    "neutral": COLORS["neutral"],
}
ROLE_NAME = {
    "bull": "Bull / Trending Up",
    "bear": "Bear / Risk-Off",
    "neutral": "Choppy / Transitional",
}
ROLE_EMOJI = {
    "bull": "🟢",
    "bear": "🔴",
    "neutral": "⚪",
}

# Model accent colors (for comparison page)
MODEL_COLORS = {
    "HMM": "#60a5fa",
    "GMM": "#a78bfa",
    "K-Means": "#fbbf24",
    "GARCH": "#f87171",
    "Ensemble": "#4ade80",
}


# ══════════════════════════════════════════════════════════════════════════════
# SHARED CSS
# ══════════════════════════════════════════════════════════════════════════════

SHARED_CSS = """
<style>
    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* ── Layout tweaks ── */
    .block-container {
        background: transparent !important;
        padding-top: 3rem !important;
        padding-bottom: 0 !important;
    }

    /* ── Hero (compact single-line) ── */
    .hero {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 12px 20px;
        margin-bottom: 10px;
        display: flex;
        align-items: baseline;
        gap: 12px;
        animation: fadeIn 0.3s ease both;
    }
    .hero-title {
        font-size: 1.2rem; font-weight: 700; letter-spacing: -0.3px;
        background: linear-gradient(90deg, #a78bfa, #4ade80);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 0; white-space: nowrap;
    }
    .hero-sub { color: #94a3b8; font-size: .78rem; margin: 0; }

    /* ── Metric Cards (compact + glassmorphism) ── */
    .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; margin-bottom: 10px; }
    .metric-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 10px 14px;
        transition: transform .15s ease, border-color .15s ease;
        animation: fadeInUp 0.4s ease both;
    }
    .metric-grid > .metric-card:nth-child(1) { animation-delay: 0s; }
    .metric-grid > .metric-card:nth-child(2) { animation-delay: 0.05s; }
    .metric-grid > .metric-card:nth-child(3) { animation-delay: 0.10s; }
    .metric-grid > .metric-card:nth-child(4) { animation-delay: 0.15s; }
    .metric-grid > .metric-card:nth-child(5) { animation-delay: 0.20s; }
    .metric-grid > .metric-card:nth-child(6) { animation-delay: 0.25s; }
    .metric-card:hover { transform: translateY(-1px); border-color: rgba(167,139,250,0.3); }
    .metric-card.green  { border-top: 3px solid #4ade80; }
    .metric-card.red    { border-top: 3px solid #f87171; }
    .metric-card.gray   { border-top: 3px solid #94a3b8; }
    .metric-card.amber  { border-top: 3px solid #fbbf24; }
    .metric-card.blue   { border-top: 3px solid #60a5fa; }
    .metric-card.purple { border-top: 3px solid #a78bfa; }
    .card-label { color: #94a3b8; font-size: .65rem; font-weight: 600;
                  letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }
    .card-state { font-size: .88rem; font-weight: 700; margin-bottom: 4px; }
    .card-state.green { color: #4ade80; }
    .card-state.red   { color: #f87171; }
    .card-state.gray  { color: #94a3b8; }
    .card-metrics { display: flex; gap: 16px; }
    .card-metric-item { flex: 1; }
    .card-metric-val  { font-size: 1.05rem; font-weight: 700; color: #f1f5f9; }
    .card-metric-lbl  { font-size: .62rem; color: #94a3b8; margin-top: 1px; }

    /* ── Regime Banner (compact + glassmorphism) ── */
    .regime-banner {
        border-radius: 8px;
        padding: 14px 20px;
        margin-top: 10px;
        text-align: center;
        animation: scaleIn 0.5s ease both;
    }
    .regime-banner.bull  { background: rgba(74,222,128,0.08); border: 2px solid #4ade80; }
    .regime-banner.bear  { background: rgba(248,113,113,0.08); border: 2px solid #f87171; }
    .regime-banner.chop  { background: rgba(148,163,184,0.06); border: 2px solid #94a3b8; }
    .regime-title { font-size: .72rem; font-weight: 600; letter-spacing: 2px;
                    text-transform: uppercase; opacity: .7; margin-bottom: 4px; }
    .regime-label { font-size: 1.6rem; font-weight: 800; margin: 0; }
    .regime-label.bull { color: #4ade80; }
    .regime-label.bear { color: #f87171; }
    .regime-label.gray { color: #94a3b8; }
    .regime-desc { font-size: .78rem; color: #94a3b8; margin-top: 4px; }

    /* ── Summary Table ── */
    .tbl-wrap { background:#0f172a; border:1px solid rgba(255,255,255,0.1); border-radius:8px; overflow:hidden; margin-top:24px; }
    .tbl-hdr  { background:#1e293b; padding:14px 20px; font-size:.7rem; letter-spacing:2px;
                 text-transform:uppercase; color:#94a3b8; font-weight:600; }
    .tbl-grid { display:grid; }
    .tbl-head { background:#1e293b; font-size:.72rem; letter-spacing:1px; color:#94a3b8;
                 padding:10px 16px; text-transform:uppercase; font-weight:600; }
    .tbl-cell { padding:12px 16px; border-top:1px solid rgba(255,255,255,0.05); font-size:.88rem; color:#cbd5e1; }
    .tbl-cell.lbl { font-weight:600; color:#f1f5f9; }
    .tbl-cell.pos { color:#4ade80; font-weight:600; }
    .tbl-cell.neg { color:#f87171; font-weight:600; }
    .tbl-cell.warn{ color:#fbbf24; font-weight:600; }

    /* ── Agreement Badge ── */
    .agree-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: .78rem;
        font-weight: 600;
    }
    .agree-badge.high { background: rgba(74,222,128,0.08); color: #4ade80; border: 1px solid rgba(74,222,128,0.25); }
    .agree-badge.mid  { background: rgba(251,191,36,0.08); color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }
    .agree-badge.low  { background: rgba(248,113,113,0.08); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }

    /* ── Inputs ── */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: #0f172a !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 6px !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #238636, #2ea043);
        color: #fff !important;
        border: none; border-radius: 6px;
        padding: 10px; font-weight: 600; font-size: .95rem;
        cursor: pointer; transition: opacity .2s;
    }
    .stButton>button:hover { opacity: .85; }

    /* ── Preset Buttons ── */
    .preset-btn {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: .78rem;
        font-weight: 600;
        cursor: pointer;
        transition: all .2s ease;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.05);
        color: #94a3b8;
    }
    .preset-btn:hover { border-color: rgba(167,139,250,0.3); color: #f1f5f9; }
    .preset-btn.active { background: rgba(167,139,250,0.15); border-color: #a78bfa; color: #a78bfa; }

    hr { border-color: rgba(255,255,255,0.1) !important; }

    /* ── Disclaimer (subtle, not a box) ── */
    .disclaimer {
        font-size: .68rem;
        color: #475569;
        text-align: center;
        padding: 4px 0;
        margin-bottom: 4px;
    }

    /* ── Skeleton Loading ── */
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

    /* ── Animations ── */
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

    /* Plotly chart fade-in */
    [data-testid="stPlotlyChart"] { animation: fadeIn 0.4s ease both; }

    /* ── Accessibility ── */
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            transition-duration: 0.01ms !important;
        }
    }
</style>
"""


def apply_theme():
    """Inject shared CSS into the page."""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)


def disclaimer():
    """Show the mandatory disclaimer."""
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>Educational use only.</strong> Past performance does not indicate future results.
        Not financial advice. Never trade with money you can't afford to lose.
    </div>
    """, unsafe_allow_html=True)


def footer():
    """Shared footer."""
    st.markdown("""
    <hr style='margin-top:32px'>
    <div style='text-align:center;color:#475569;font-size:.75rem;padding-bottom:16px'>
      Market Regime Detection Suite · Educational use only · Not financial advice
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PLOTLY HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def plotly_base_layout(**overrides) -> dict:
    """Base Plotly layout for dark theme — all charts use this."""
    base = dict(
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color=COLORS["text_primary"], family="Inter, Segoe UI, sans-serif"),
        hovermode="x unified",
        legend=dict(
            bgcolor="rgba(255,255,255,0.05)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        margin=dict(t=60, b=20, l=20, r=20),
    )
    base.update(overrides)
    return base


def plotly_axis_style() -> dict:
    """Shared axis style."""
    return dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.06)",
        zeroline=False,
    )


def add_regime_shading(fig, df, role_col="role", row=1, col=1):
    """Add vrect shading for regime segments to a Plotly figure."""
    df_temp = df.copy()
    df_temp["_seg_id"] = (df_temp[role_col] != df_temp[role_col].shift()).cumsum()

    for _, seg in df_temp.groupby("_seg_id"):
        role = seg[role_col].iloc[0]
        color = ROLE_COLOR_BG.get(role, "rgba(139,148,158,.05)")
        fig.add_vrect(
            x0=seg.index[0],
            x1=seg.index[-1],
            fillcolor=color,
            line_width=0,
            row=row,
            col=col,
        )


# ══════════════════════════════════════════════════════════════════════════════
# UI COMPONENT BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def render_state_cards(state_stats: dict, roles_map: dict | None = None):
    """
    Render metric cards for regime states.
    state_stats: {state_id: {mean_ret, mean_vol, pct_time}}
    roles_map: {state_id: "bull"/"bear"/"neutral"}
    """
    cards_html = '<div class="metric-grid">'

    for s, stat in sorted(state_stats.items()):
        role = roles_map.get(s, "neutral") if roles_map else "neutral"
        cls_map = {"bull": "green", "bear": "red", "neutral": "gray"}
        cls = cls_map.get(role, "gray")

        name = ROLE_NAME.get(role, "Unknown")
        ret_pct = stat["mean_ret"] * 100
        vol_pct = stat["mean_vol"] * 100
        pct_time = stat["pct_time"] * 100

        ret_color = COLORS["bull"] if ret_pct >= 0 else COLORS["bear"]
        ret_sign = "+" if ret_pct >= 0 else ""

        cards_html += f"""
        <div class="metric-card {cls}">
          <div class="card-label">State {s}</div>
          <div class="card-state {cls}">{name}</div>
          <div class="card-metrics">
            <div class="card-metric-item">
              <div class="card-metric-val" style="color:{ret_color}">{ret_sign}{ret_pct:.3f}%</div>
              <div class="card-metric-lbl">Mean Daily Return</div>
            </div>
            <div class="card-metric-item">
              <div class="card-metric-val">{vol_pct:.1f}%</div>
              <div class="card-metric-lbl">Mean Ann. Volatility</div>
            </div>
            <div class="card-metric-item">
              <div class="card-metric-val">{pct_time:.0f}%</div>
              <div class="card-metric-lbl">% of Time</div>
            </div>
          </div>
        </div>"""

    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PRESETS
# ══════════════════════════════════════════════════════════════════════════════

PRESETS = {
    "Conservative": {"ticker": "SPY", "lookback": 10, "n_states": 2},
    "Aggressive":   {"ticker": "QQQ", "lookback": 5,  "n_states": 3},
    "High Vol":     {"ticker": "VIX", "lookback": 3,  "n_states": 4},
}


def render_presets(page_key: str) -> dict:
    """
    Render preset buttons and return current config values.
    Returns: {"ticker": str, "lookback": int, "n_states": int}
    """
    if f"{page_key}_preset" not in st.session_state:
        st.session_state[f"{page_key}_preset"] = None

    cols = st.columns(len(PRESETS))
    for i, (name, config) in enumerate(PRESETS.items()):
        with cols[i]:
            if st.button(name, key=f"{page_key}_preset_{name}"):
                st.session_state[f"{page_key}_preset"] = name
                st.session_state[f"{page_key}_ticker"] = config["ticker"]
                st.session_state[f"{page_key}_lookback"] = config["lookback"]
                st.session_state[f"{page_key}_n_states"] = config["n_states"]
                st.rerun()

    return {
        "ticker": st.session_state.get(f"{page_key}_ticker", "SPY"),
        "lookback": st.session_state.get(f"{page_key}_lookback", 10),
        "n_states": st.session_state.get(f"{page_key}_n_states", 3),
    }


# ══════════════════════════════════════════════════════════════════════════════
# SKELETON LOADING
# ══════════════════════════════════════════════════════════════════════════════

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


def render_regime_banner(role: str, date_str: str):
    """Render the current regime banner at the bottom."""
    banner_cls = "bull" if role == "bull" else ("bear" if role == "bear" else "chop")
    label_cls = "bull" if role == "bull" else ("bear" if role == "bear" else "gray")
    emoji = ROLE_EMOJI.get(role, "⚪")
    name = ROLE_NAME.get(role, "Unknown").upper()

    desc_map = {
        "bull": "High-return, low-volatility trending environment. Momentum strategies tend to outperform.",
        "bear": "Risk-off, negative-return environment. Capital preservation should be the priority.",
        "neutral": "Transitional, choppy environment. Mean-reversion or reduced exposure is advisable.",
    }

    st.markdown(f"""
    <div class="regime-banner {banner_cls}">
      <div class="regime-title">Current Predicted Regime · {date_str}</div>
      <div class="regime-label {label_cls}">{emoji} {name}</div>
      <div class="regime-desc">{desc_map.get(role, '')}</div>
    </div>
    """, unsafe_allow_html=True)
