"""
Market Regime Detection Suite
══════════════════════════════
Landing page — overview of all available models and tools.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.theme import apply_theme, disclaimer, footer

st.set_page_config(
    page_title="Regime Suite",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
disclaimer()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <p class="hero-title">📡 Market Regime Detection Suite</p>
  <p class="hero-sub">
    Compare multiple ML methodologies for market regime classification.
    Free &amp; open-source. For educational purposes only.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Model Cards ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-grid">
  <div class="metric-card blue" style="cursor:default">
    <div class="card-label">Model 1</div>
    <div class="card-state" style="color:#60a5fa">Hidden Markov Model</div>
    <div style="color:#94a3b8;font-size:.82rem;line-height:1.6;margin-top:8px">
      Probabilistic state detection with temporal transitions.
      Learns latent regimes from returns + volatility.
    </div>
  </div>
  <div class="metric-card purple" style="cursor:default">
    <div class="card-label">Model 2</div>
    <div class="card-state" style="color:#a78bfa">Gaussian Mixture</div>
    <div style="color:#94a3b8;font-size:.82rem;line-height:1.6;margin-top:8px">
      Soft clustering with probability assignments.
      Each day gets a probability per regime.
    </div>
  </div>
  <div class="metric-card amber" style="cursor:default">
    <div class="card-label">Model 3</div>
    <div class="card-state" style="color:#fbbf24">K-Means Clustering</div>
    <div style="color:#94a3b8;font-size:.82rem;line-height:1.6;margin-top:8px">
      Hard clustering — fast, simple, no probabilities.
      Good baseline for regime classification.
    </div>
  </div>
  <div class="metric-card red" style="cursor:default">
    <div class="card-label">Model 4</div>
    <div class="card-state" style="color:#f87171">GARCH Volatility</div>
    <div style="color:#94a3b8;font-size:.82rem;line-height:1.6;margin-top:8px">
      Volatility-focused regime detection.
      Models time-varying variance with GARCH(1,1).
    </div>
  </div>
  <div class="metric-card green" style="cursor:default">
    <div class="card-label">Ensemble</div>
    <div class="card-state" style="color:#4ade80">Majority Voter</div>
    <div style="color:#94a3b8;font-size:.82rem;line-height:1.6;margin-top:8px">
      Combines all models via majority vote.
      Confidence score based on agreement level.
    </div>
  </div>
  <div class="metric-card" style="cursor:default;border-top:3px solid #94a3b8">
    <div class="card-label">Tool</div>
    <div class="card-state" style="color:#94a3b8">Backtest Lab</div>
    <div style="color:#94a3b8;font-size:.82rem;line-height:1.6;margin-top:8px">
      Regime-routing backtester. Each regime deploys
      its optimal sub-strategy automatically.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── How to Use ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);backdrop-filter:blur(12px);border-radius:10px;padding:24px 28px;margin-top:8px">
  <div style="font-weight:700;font-size:1rem;color:#f1f5f9;margin-bottom:12px">How to use</div>
  <div style="color:#94a3b8;font-size:.88rem;line-height:1.8">
    <b style="color:#a78bfa">1.</b> Use the sidebar to navigate between models.<br>
    <b style="color:#a78bfa">2.</b> Each model page lets you pick a ticker and run the analysis.<br>
    <b style="color:#a78bfa">3.</b> The <b style="color:#f1f5f9">Compare</b> page runs all models on the same data side by side.<br>
    <b style="color:#a78bfa">4.</b> The <b style="color:#f1f5f9">Ensemble</b> page combines them via majority vote.<br>
    <b style="color:#a78bfa">5.</b> The <b style="color:#f1f5f9">Backtest Lab</b> routes each regime to the correct sub-strategy.
  </div>
</div>
""", unsafe_allow_html=True)

footer()
