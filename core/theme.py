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
    "bg_primary": "#0d1117",
    "bg_secondary": "#161b22",
    "bg_tertiary": "#070b0f",
    "border": "#30363d",
    "border_light": "#21262d",
    "text_primary": "#e6edf3",
    "text_secondary": "#8b949e",
    "text_muted": "#484f58",
    "bull": "#3fb950",
    "bear": "#f85149",
    "neutral": "#8b949e",
    "chop": "#f0b429",
    "accent_blue": "#58a6ff",
    "accent_purple": "#a371f7",
}

# Role mappings
ROLE_COLOR_BG = {
    "bull": "rgba(63,185,80,.12)",
    "bear": "rgba(248,81,73,.12)",
    "neutral": "rgba(139,148,158,.10)",
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
    "HMM": "#58a6ff",
    "GMM": "#a371f7",
    "K-Means": "#f0b429",
    "GARCH": "#f85149",
    "Ensemble": "#3fb950",
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
    .stApp { background-color: #0d1117; color: #e6edf3; }
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    section[data-testid="stSidebar"] * { color: #e6edf3 !important; }
    header[data-testid="stHeader"] { background: #0d1117 !important; }
    [data-testid="stAppViewContainer"] { background: #0d1117 !important; }

    /* ── CRITICAL: Kill Streamlit's default padding ── */
    .block-container {
        background: #0d1117 !important;
        padding-top: 3rem !important;
        padding-bottom: 0 !important;
    }
    /* Remove extra gap Streamlit adds between elements */
    .element-container { margin-bottom: 0 !important; }
    [data-testid="stVerticalBlock"] > [style*="flex-direction"] { gap: 0.3rem !important; }

    /* ── Hero (compact single-line) ── */
    .hero {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px 20px;
        margin-bottom: 10px;
        display: flex;
        align-items: baseline;
        gap: 12px;
    }
    .hero-title {
        font-size: 1.2rem; font-weight: 700; letter-spacing: -0.3px;
        background: linear-gradient(90deg, #58a6ff, #3fb950);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 0; white-space: nowrap;
    }
    .hero-sub { color: #8b949e; font-size: .78rem; margin: 0; }

    /* ── Metric Cards (compact) ── */
    .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; margin-bottom: 10px; }
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 10px 14px;
        transition: transform .15s ease, border-color .15s ease;
    }
    .metric-card:hover { transform: translateY(-1px); border-color: #58a6ff40; }
    .metric-card.green  { border-top: 3px solid #3fb950; }
    .metric-card.red    { border-top: 3px solid #f85149; }
    .metric-card.gray   { border-top: 3px solid #8b949e; }
    .metric-card.amber  { border-top: 3px solid #f0b429; }
    .metric-card.blue   { border-top: 3px solid #58a6ff; }
    .metric-card.purple { border-top: 3px solid #a371f7; }
    .card-label { color: #8b949e; font-size: .65rem; font-weight: 600;
                  letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }
    .card-state { font-size: .88rem; font-weight: 700; margin-bottom: 4px; }
    .card-state.green { color: #3fb950; }
    .card-state.red   { color: #f85149; }
    .card-state.gray  { color: #8b949e; }
    .card-metrics { display: flex; gap: 16px; }
    .card-metric-item { flex: 1; }
    .card-metric-val  { font-size: 1.05rem; font-weight: 700; color: #e6edf3; }
    .card-metric-lbl  { font-size: .62rem; color: #8b949e; margin-top: 1px; }

    /* ── Regime Banner (compact) ── */
    .regime-banner {
        border-radius: 8px;
        padding: 14px 20px;
        margin-top: 10px;
        text-align: center;
    }
    .regime-banner.bull  { background: #0f2a17; border: 2px solid #3fb950; }
    .regime-banner.bear  { background: #2a0f0f; border: 2px solid #f85149; }
    .regime-banner.chop  { background: #1c1c1c; border: 2px solid #8b949e; }
    .regime-title { font-size: .72rem; font-weight: 600; letter-spacing: 2px;
                    text-transform: uppercase; opacity: .7; margin-bottom: 4px; }
    .regime-label { font-size: 1.6rem; font-weight: 800; margin: 0; }
    .regime-label.bull { color: #3fb950; }
    .regime-label.bear { color: #f85149; }
    .regime-label.gray { color: #8b949e; }
    .regime-desc { font-size: .78rem; color: #8b949e; margin-top: 4px; }

    /* ── Summary Table ── */
    .tbl-wrap { background:#0d1117; border:1px solid #30363d; border-radius:8px; overflow:hidden; margin-top:24px; }
    .tbl-hdr  { background:#161b22; padding:14px 20px; font-size:.7rem; letter-spacing:2px;
                 text-transform:uppercase; color:#8b949e; font-weight:600; }
    .tbl-grid { display:grid; }
    .tbl-head { background:#161b22; font-size:.72rem; letter-spacing:1px; color:#8b949e;
                 padding:10px 16px; text-transform:uppercase; font-weight:600; }
    .tbl-cell { padding:12px 16px; border-top:1px solid #21262d; font-size:.88rem; color:#c9d1d9; }
    .tbl-cell.lbl { font-weight:600; color:#e6edf3; }
    .tbl-cell.pos { color:#3fb950; font-weight:600; }
    .tbl-cell.neg { color:#f85149; font-weight:600; }
    .tbl-cell.warn{ color:#f0b429; font-weight:600; }

    /* ── Agreement Badge ── */
    .agree-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: .78rem;
        font-weight: 600;
    }
    .agree-badge.high { background: #0f2a17; color: #3fb950; border: 1px solid #3fb95040; }
    .agree-badge.mid  { background: #1c1a0f; color: #f0b429; border: 1px solid #f0b42940; }
    .agree-badge.low  { background: #2a0f0f; color: #f85149; border: 1px solid #f8514940; }

    /* ── Inputs ── */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background: #0d1117 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
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

    hr { border-color: #30363d !important; }

    /* ── Disclaimer (subtle, not a box) ── */
    .disclaimer {
        font-size: .68rem;
        color: #6e7681;
        text-align: center;
        padding: 4px 0;
        margin-bottom: 4px;
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
    <div style='text-align:center;color:#484f58;font-size:.75rem;padding-bottom:16px'>
      Market Regime Detection Suite · Educational use only · Not financial advice
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PLOTLY HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def plotly_base_layout(**overrides) -> dict:
    """Base Plotly layout for dark theme — all charts use this."""
    base = dict(
        paper_bgcolor=COLORS["bg_primary"],
        plot_bgcolor=COLORS["bg_primary"],
        font=dict(color=COLORS["text_primary"], family="Inter, Segoe UI, sans-serif"),
        hovermode="x unified",
        legend=dict(
            bgcolor=COLORS["bg_secondary"],
            bordercolor=COLORS["border"],
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
        gridcolor=COLORS["border_light"],
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
