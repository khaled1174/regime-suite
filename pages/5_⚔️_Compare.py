"""
Page 5: Model Comparison Dashboard
═══════════════════════════════════
The hero page — runs HMM, GMM, K-Means on the same data and compares.
"""
import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.theme import (
    apply_theme, disclaimer, footer, COLORS, MODEL_COLORS,
    plotly_base_layout, plotly_axis_style,
    ROLE_COLOR_LINE, ROLE_NAME, ROLE_EMOJI,
)
from core.data import load_market_data, get_observation_matrix
from core.models import fit_hmm, fit_gmm, fit_kmeans, ensemble_vote

st.set_page_config(page_title="Compare Models", page_icon="⚔️", layout="wide")
apply_theme()
disclaimer()

with st.sidebar:
    st.markdown("## ⚔️ Comparison Config")
    st.markdown("---")
    ticker = st.text_input("Ticker Symbol", value="SPY").upper().strip()
    lookback = st.slider("Lookback (years)", 2, 15, 10)
    n_states = st.selectbox("Number of States", [2, 3, 4], index=1)
    st.markdown("---")
    run_btn = st.button("🚀 Run All Models")
    st.markdown("---")
    st.markdown("""
    <div style='color:#8b949e;font-size:.78rem;line-height:1.6'>
    <b style='color:#e6edf3'>What this does</b><br>
    Runs HMM, GMM, and K-Means on <em>identical data</em>,
    then compares how each model classifies every day.<br><br>
    <b style='color:#3fb950'>Agreement Score</b> = % of days where
    all models assign the same role.
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <p class="hero-title">⚔️ Model Comparison Arena</p>
  <p class="hero-sub">
    Same data · Three models · Who classifies best?
  </p>
</div>
""", unsafe_allow_html=True)

if not run_btn:
    st.markdown("""
    <div style='text-align:center;padding:80px 0;color:#8b949e'>
      <div style='font-size:3rem;margin-bottom:16px'>⚔️</div>
      <p style='font-size:1.1rem;margin:0'>Click <b style="color:#3fb950">Run All Models</b> to compare</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Data ──────────────────────────────────────────────────────────────────────
with st.spinner(f"Downloading {ticker} data…"):
    df = load_market_data(ticker, lookback)

if df.empty:
    st.error(f"❌ No data for **{ticker}**.")
    st.stop()

X = get_observation_matrix(df)
log_ret = df["log_ret"].values
real_vol = df["real_vol"].values

# ── Fit All Models ────────────────────────────────────────────────────────────
with st.spinner("Training HMM…"):
    hmm_result = fit_hmm(X, log_ret, real_vol, n_states=n_states)
with st.spinner("Training GMM…"):
    gmm_result = fit_gmm(X, log_ret, real_vol, n_states=n_states)
with st.spinner("Training K-Means…"):
    km_result = fit_kmeans(X, log_ret, real_vol, n_states=n_states)

# ── Ensemble Vote ─────────────────────────────────────────────────────────────
ensemble = ensemble_vote([hmm_result, gmm_result, km_result])
agreement = ensemble.extra["agreement_scores"]
mean_agree = ensemble.extra["mean_agreement"]

# ── Agreement Score Banner ────────────────────────────────────────────────────
agree_cls = "high" if mean_agree >= 0.8 else ("mid" if mean_agree >= 0.6 else "low")
agree_color = COLORS["bull"] if mean_agree >= 0.8 else (COLORS["chop"] if mean_agree >= 0.6 else COLORS["bear"])

st.markdown(f"""
<div style="display:flex;gap:16px;margin-bottom:24px;align-items:stretch">
  <div class="metric-card" style="flex:1;border-top:3px solid {agree_color}">
    <div class="card-label">Overall Agreement</div>
    <div class="card-metric-val" style="color:{agree_color};font-size:2rem">{mean_agree*100:.1f}%</div>
    <div class="card-metric-lbl">of days all 3 models agree on the regime role</div>
  </div>
  <div class="metric-card" style="flex:1;border-top:3px solid {COLORS['accent_blue']}">
    <div class="card-label">Current Regime — HMM</div>
    <div class="card-state" style="color:{ROLE_COLOR_LINE[hmm_result.roles[-1]]}">{ROLE_EMOJI[hmm_result.roles[-1]]} {ROLE_NAME[hmm_result.roles[-1]]}</div>
  </div>
  <div class="metric-card" style="flex:1;border-top:3px solid {COLORS['accent_purple']}">
    <div class="card-label">Current Regime — GMM</div>
    <div class="card-state" style="color:{ROLE_COLOR_LINE[gmm_result.roles[-1]]}">{ROLE_EMOJI[gmm_result.roles[-1]]} {ROLE_NAME[gmm_result.roles[-1]]}</div>
  </div>
  <div class="metric-card" style="flex:1;border-top:3px solid {COLORS['chop']}">
    <div class="card-label">Current Regime — K-Means</div>
    <div class="card-state" style="color:{ROLE_COLOR_LINE[km_result.roles[-1]]}">{ROLE_EMOJI[km_result.roles[-1]]} {ROLE_NAME[km_result.roles[-1]]}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Multi-Model Chart ─────────────────────────────────────────────────────────
ROLE_INT = {"bull": 1, "bear": -1, "neutral": 0}

fig = make_subplots(
    rows=4, cols=1,
    shared_xaxes=True,
    row_heights=[0.45, 0.18, 0.18, 0.19],
    vertical_spacing=0.03,
    subplot_titles=[
        f"{ticker} Price + Ensemble Shading",
        "HMM States",
        "GMM States",
        "K-Means States",
    ],
)

# Row 1: Price + ensemble shading
fig.add_trace(go.Scatter(
    x=df.index, y=df["Close"], mode="lines",
    line=dict(color=COLORS["accent_blue"], width=1.5), name=ticker,
), row=1, col=1)

# Ensemble shading
df_ens = df.copy()
df_ens["role"] = ensemble.roles
df_ens["_seg_id"] = (df_ens["role"] != df_ens["role"].shift()).cumsum()
ROLE_BG = {"bull": "rgba(63,185,80,.12)", "bear": "rgba(248,81,73,.12)", "neutral": "rgba(139,148,158,.08)"}

for _, seg in df_ens.groupby("_seg_id"):
    role = seg["role"].iloc[0]
    fig.add_vrect(
        x0=seg.index[0], x1=seg.index[-1],
        fillcolor=ROLE_BG.get(role, "rgba(139,148,158,.05)"),
        line_width=0, row=1, col=1,
    )

# Rows 2-4: Model states as colored dots
for row_idx, (result, model_name, color) in enumerate([
    (hmm_result, "HMM", MODEL_COLORS["HMM"]),
    (gmm_result, "GMM", MODEL_COLORS["GMM"]),
    (km_result, "K-Means", MODEL_COLORS["K-Means"]),
], start=2):
    role_ints = np.array([ROLE_INT.get(r, 0) for r in result.roles])
    colors_arr = [ROLE_COLOR_LINE.get(r, COLORS["neutral"]) for r in result.roles]

    for role_val, role_name in [("bull", "Bull"), ("bear", "Bear"), ("neutral", "Neutral")]:
        mask = result.roles == role_val
        if mask.any():
            fig.add_trace(go.Scatter(
                x=df.index[mask],
                y=role_ints[mask],
                mode="markers",
                marker=dict(color=ROLE_COLOR_LINE[role_val], size=2, symbol="square"),
                name=f"{model_name} {role_name}",
                showlegend=(row_idx == 2),
                legendgroup=role_name,
            ), row=row_idx, col=1)

# Layout
axis_style = plotly_axis_style()
fig.update_layout(**plotly_base_layout(
    height=750,
    legend=dict(
        bgcolor=COLORS["bg_secondary"],
        bordercolor=COLORS["border"],
        borderwidth=1,
        orientation="h", y=1.03, x=0,
    ),
))

for i in range(1, 5):
    fig.update_xaxes(axis_style, row=i, col=1)
    fig.update_yaxes(axis_style, row=i, col=1)

fig.update_yaxes(title="Price", row=1, col=1)
fig.update_yaxes(tickvals=[-1, 0, 1], ticktext=["Bear", "Neutral", "Bull"], row=2, col=1)
fig.update_yaxes(tickvals=[-1, 0, 1], ticktext=["Bear", "Neutral", "Bull"], row=3, col=1)
fig.update_yaxes(tickvals=[-1, 0, 1], ticktext=["Bear", "Neutral", "Bull"], row=4, col=1)

fig.update_annotations(font=dict(color=COLORS["text_secondary"], size=11))

st.plotly_chart(fig, width="stretch")

# ── Agreement Over Time ──────────────────────────────────────────────────────
st.markdown("### Agreement Score Over Time")

fig_agree = go.Figure()
fig_agree.add_trace(go.Scatter(
    x=df.index,
    y=pd.Series(agreement).rolling(20).mean(),
    mode="lines",
    line=dict(color=COLORS["bull"], width=1.5),
    name="20-day Rolling Agreement",
    fill="tozeroy",
    fillcolor="rgba(63,185,80,.1)",
))
fig_agree.add_hline(y=0.67, line_dash="dash", line_color=COLORS["chop"],
                    annotation_text="2/3 threshold", annotation_position="top right")

fig_agree.update_layout(
    **plotly_base_layout(height=250),
    yaxis=dict(**plotly_axis_style(), title="Agreement %", range=[0, 1.05]),
    xaxis=dict(**plotly_axis_style()),
)
st.plotly_chart(fig_agree, width="stretch")

# ── Disagreement Table ────────────────────────────────────────────────────────
with st.expander("📊 Recent Classification Comparison (last 20 days)"):
    compare_df = pd.DataFrame({
        "Date": df.index[-20:].strftime("%Y-%m-%d"),
        "HMM": [f"{ROLE_EMOJI.get(r,'')} {r}" for r in hmm_result.roles[-20:]],
        "GMM": [f"{ROLE_EMOJI.get(r,'')} {r}" for r in gmm_result.roles[-20:]],
        "K-Means": [f"{ROLE_EMOJI.get(r,'')} {r}" for r in km_result.roles[-20:]],
        "Ensemble": [f"{ROLE_EMOJI.get(r,'')} {r}" for r in ensemble.roles[-20:]],
        "Agreement": [f"{a*100:.0f}%" for a in agreement[-20:]],
    })
    st.dataframe(compare_df, width="stretch", hide_index=True)

# ── Consensus Banner ──────────────────────────────────────────────────────────
consensus_role = ensemble.roles[-1]
consensus_agree = agreement[-1]
banner_cls = "bull" if consensus_role == "bull" else ("bear" if consensus_role == "bear" else "chop")
label_cls = "bull" if consensus_role == "bull" else ("bear" if consensus_role == "bear" else "gray")

st.markdown(f"""
<div class="regime-banner {banner_cls}">
  <div class="regime-title">Consensus Regime · {df.index[-1].strftime("%B %d, %Y")}</div>
  <div class="regime-label {label_cls}">{ROLE_EMOJI.get(consensus_role,'')} {ROLE_NAME.get(consensus_role,'').upper()}</div>
  <div class="regime-desc">
    <span class="agree-badge {agree_cls}">{consensus_agree*100:.0f}% Agreement</span>
    &nbsp; HMM: {hmm_result.roles[-1]} · GMM: {gmm_result.roles[-1]} · K-Means: {km_result.roles[-1]}
  </div>
</div>
""", unsafe_allow_html=True)

footer()
