"""
Page 1: HMM Regime Classification
"""
import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.theme import (
    apply_theme, disclaimer, footer, COLORS,
    plotly_base_layout, plotly_axis_style,
    add_regime_shading, render_state_cards, render_regime_banner,
    render_presets, render_skeleton,
    ROLE_NAME, ROLE_COLOR_LINE,
)
from core.data import load_market_data, get_observation_matrix
from core.models import fit_hmm

st.set_page_config(page_title="HMM Regime", page_icon="📡", layout="wide")
apply_theme()

with st.sidebar:
    st.markdown("## 📡 HMM Config")
    st.markdown("---")
    config = render_presets("hmm")
    st.markdown("---")
    ticker = st.text_input("Ticker Symbol", value=config["ticker"], key="hmm_ticker_input").upper().strip()
    lookback = st.slider("Lookback (years)", 2, 15, value=config["lookback"], key="hmm_lookback_input")
    n_states = st.selectbox("HMM States", [2, 3, 4], index=[2, 3, 4].index(config["n_states"]) if config["n_states"] in [2, 3, 4] else 1, key="hmm_states_input")
    st.markdown("---")
    run_btn = st.button("🚀 Run HMM Analysis")
    st.markdown("---")
    st.markdown("""
    <div style='color:#94a3b8;font-size:.78rem;line-height:1.6'>
    <b style='color:#f1f5f9'>How it works</b><br>
    HMM learns latent <em>regimes</em> from log returns &amp; realized volatility.
    States ordered by mean return.<br><br>
    <b style='color:#4ade80'>Green</b> = bull · <b style='color:#f87171'>Red</b> = bear · <b style='color:#94a3b8'>Gray</b> = transitional
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <p class="hero-title">📡 HMM Regime Terminal</p>
  <p class="hero-sub">Probabilistic State Detection · Temporal Transitions</p>
</div>
""", unsafe_allow_html=True)

if not run_btn:
    st.markdown("""
    <div style='text-align:center;padding:40px 0;color:#94a3b8'>
      <p style='font-size:.95rem;margin:0'>Configure and click <b style="color:#4ade80">Run HMM Analysis</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

placeholder = st.empty()
placeholder.markdown(render_skeleton(n_cards=n_states), unsafe_allow_html=True)

with st.status("Running analysis...", expanded=True) as status:
    status.update(label="Downloading market data...")
    df = load_market_data(ticker, lookback)

    if df.empty:
        placeholder.empty()
        st.error(f"❌ No data returned for **{ticker}**.")
        st.stop()

    X = get_observation_matrix(df)

    status.update(label="Training Hidden Markov Model...")
    result = fit_hmm(X, df["log_ret"].values, df["real_vol"].values, n_states=n_states)

    status.update(label="Analyzing regimes...")
    status.update(label="Complete!", state="complete", expanded=False)

placeholder.empty()

df["state"] = result.states
df["role"] = result.roles

roles_map = {}
for s in range(n_states):
    mask = result.states == s
    if mask.any():
        roles_map[s] = result.roles[mask][0]

render_state_cards(result.state_stats, roles_map)

# ── CHART ─────────────────────────────────────────────────────────────────────
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df.index, y=df["Close"], mode="lines",
    line=dict(color=COLORS["accent_blue"], width=1.5), name=ticker,
))
add_regime_shading(fig, df, role_col="role")

for role, name in ROLE_NAME.items():
    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode="markers",
        marker=dict(size=10, color=ROLE_COLOR_LINE[role], symbol="square"),
        name=name, showlegend=True,
    ))

fig.update_layout(**plotly_base_layout(
    height=420,
    title=dict(text=f"<b>{ticker}</b> — HMM Regime Overlay", font=dict(size=14), x=0),
))
fig.update_xaxes(**plotly_axis_style(), rangeslider=dict(visible=False))
fig.update_yaxes(**plotly_axis_style(), title="Price (USD)")

st.plotly_chart(fig, use_container_width=True)

render_regime_banner(result.roles[-1], df.index[-1].strftime("%B %d, %Y"))

with st.expander("🔬 HMM Model Details"):
    st.markdown("**Transition Matrix:**")
    tm = result.extra["transition_matrix"]
    tm_df = pd.DataFrame(tm, columns=[f"→ S{i}" for i in range(n_states)],
                         index=[f"S{i}" for i in range(n_states)])
    st.dataframe(tm_df.style.format("{:.3f}"), use_container_width=True)
    st.metric("Log-Likelihood", f"{result.extra['log_likelihood']:.2f}")

disclaimer()
footer()
