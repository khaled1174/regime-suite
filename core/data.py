"""
core/data.py — Shared Data Loading & Feature Engineering
═══════════════════════════════════════════════════════════
Single source of truth for market data across all pages.
"""

import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


@st.cache_data(ttl=3600, show_spinner=False)
def load_market_data(ticker: str, lookback_years: int = 10) -> pd.DataFrame:
    """
    Download OHLCV data from yfinance and compute features.

    Returns DataFrame with columns:
        Close, Volume, log_ret, real_vol, norm_vol
    """
    end = pd.Timestamp.today().normalize()
    start = end - pd.DateOffset(years=lookback_years)

    try:
        raw = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    except Exception:
        return pd.DataFrame()

    if raw.empty:
        return pd.DataFrame()

    # Flatten multi-index if present (yfinance >= 0.2.31)
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    df = raw[["Close", "Volume"]].copy()

    # ── Feature Engineering ────────────────────────────────────────────────
    # 1. Log returns
    df["log_ret"] = np.log(df["Close"] / df["Close"].shift(1))

    # 2. 14-day realized volatility (annualized)
    df["real_vol"] = df["log_ret"].rolling(14).std() * np.sqrt(252)

    # 3. Normalized volume (z-score over 20-day window)
    vol_mean = df["Volume"].rolling(20).mean()
    vol_std = df["Volume"].rolling(20).std()
    df["norm_vol"] = (df["Volume"] - vol_mean) / vol_std.replace(0, np.nan)

    df.dropna(inplace=True)

    return df


def get_observation_matrix(
    df: pd.DataFrame,
    features: list[str] | None = None,
) -> np.ndarray:
    """
    Extract observation matrix X from the DataFrame.

    Default features: log_ret + real_vol (2D).
    Optional: add norm_vol for 3D observation space.
    """
    if features is None:
        features = ["log_ret", "real_vol"]

    return df[features].values


def generate_synthetic_data(
    n_days: int = 1500,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic regime-switching market data for testing.
    Uses a 3-state Markov chain with realistic parameters.
    """
    rng = np.random.default_rng(seed)

    regime_params = {
        0: dict(mu=0.0006, sigma=0.008),   # Bull
        1: dict(mu=-0.0008, sigma=0.018),  # Bear
        2: dict(mu=0.0001, sigma=0.011),   # Chop
    }

    trans = np.array([
        [0.97, 0.01, 0.02],  # from Bull
        [0.02, 0.95, 0.03],  # from Bear
        [0.04, 0.03, 0.93],  # from Chop
    ])

    states, returns = [], []
    cur = 0
    for _ in range(n_days):
        states.append(cur)
        p = regime_params[cur]
        r = rng.normal(p["mu"], p["sigma"])
        returns.append(r)
        cur = rng.choice(3, p=trans[cur])

    idx = pd.date_range(end=pd.Timestamp.today(), periods=n_days, freq="B")
    df = pd.DataFrame({
        "hmm_state": states,
        "log_returns": returns,
    }, index=idx)

    # Reconstruct price for SMA/RSI calculations
    df["close"] = 100 * np.exp(df["log_returns"].cumsum())

    return df
