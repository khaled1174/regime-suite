"""
core/metrics.py — Risk / Return Metrics
═════════════════════════════════════════
Shared calculations for all backtesting pages.
"""

import numpy as np
import pandas as pd


def max_drawdown(equity: pd.Series) -> float:
    """Maximum drawdown as a negative decimal (e.g. -0.25 = 25% drawdown)."""
    roll_max = equity.cummax()
    dd = (equity - roll_max) / roll_max
    return dd.min()


def cagr(equity: pd.Series) -> float:
    """Compound Annual Growth Rate."""
    n_days = len(equity)
    if n_days < 2:
        return 0.0
    years = n_days / 252
    return (equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1


def sharpe_ratio(returns: pd.Series, risk_free: float = 0.0) -> float:
    """Annualized Sharpe Ratio."""
    excess = returns - risk_free / 252
    r = excess[excess != 0]
    if len(r) < 2 or r.std() == 0:
        return 0.0
    return (r.mean() / r.std()) * np.sqrt(252)


def calmar_ratio(equity: pd.Series) -> float:
    """Calmar Ratio = CAGR / |Max Drawdown|."""
    c = cagr(equity)
    d = abs(max_drawdown(equity))
    return c / d if d > 0 else 0.0


def sortino_ratio(returns: pd.Series, risk_free: float = 0.0) -> float:
    """Annualized Sortino Ratio (downside deviation only)."""
    excess = returns - risk_free / 252
    downside = excess[excess < 0]
    if len(downside) < 2 or downside.std() == 0:
        return 0.0
    return (excess.mean() / downside.std()) * np.sqrt(252)


def win_rate(returns: pd.Series) -> float:
    """Percentage of positive-return days (when in market)."""
    in_market = returns[returns != 0]
    if len(in_market) == 0:
        return 0.0
    return (in_market > 0).sum() / len(in_market)


def compute_all_metrics(
    equity: pd.Series,
    returns: pd.Series,
    label: str = "Strategy",
) -> dict:
    """Compute full metrics suite for an equity curve."""
    return {
        "label": label,
        "total_ret": equity.iloc[-1] / equity.iloc[0] - 1,
        "cagr": cagr(equity),
        "max_dd": max_drawdown(equity),
        "sharpe": sharpe_ratio(returns),
        "sortino": sortino_ratio(returns),
        "calmar": calmar_ratio(equity),
        "win_rate": win_rate(returns),
        "pct_in_market": (returns != 0).mean(),
        "n_days": len(equity),
    }


# ══════════════════════════════════════════════════════════════════════════════
# BACKTESTING ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def compute_rsi(close: pd.Series, period: int = 3) -> pd.Series:
    """Wilder's RSI."""
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def build_trend_signal(close: pd.Series, fast: int = 10, slow: int = 50) -> pd.Series:
    """SMA crossover: 1 when fast > slow, else 0."""
    sma_f = close.rolling(fast).mean()
    sma_s = close.rolling(slow).mean()
    return (sma_f > sma_s).astype(int)


def build_reversion_signal(
    close: pd.Series,
    rsi_period: int = 3,
    entry_thresh: int = 30,
    exit_thresh: int = 70,
) -> pd.Series:
    """RSI mean reversion: enter when RSI < entry, exit when RSI > exit."""
    rsi = compute_rsi(close, rsi_period)
    signal = np.zeros(len(close))
    in_pos = False
    for i in range(len(close)):
        val = rsi.iloc[i]
        if not in_pos and val < entry_thresh:
            in_pos = True
        elif in_pos and val > exit_thresh:
            in_pos = False
        signal[i] = 1.0 if in_pos else 0.0
    return pd.Series(signal, index=close.index)


def run_regime_backtest(
    df: pd.DataFrame,
    roles: np.ndarray,
    close_col: str = "Close",
    log_ret_col: str = "log_ret",
    sma_fast: int = 10,
    sma_slow: int = 50,
    rsi_period: int = 3,
    rsi_enter: int = 30,
    rsi_exit: int = 70,
) -> pd.DataFrame:
    """
    Run the regime-routing backtest.

    Maps roles → strategies:
        bull    → trend following (SMA crossover)
        bear    → cash (flat)
        neutral → mean reversion (RSI)

    Returns df with added columns:
        strat_trend, strat_reversion, strat_cash,
        composite_signal, signal_lagged,
        strategy_returns, buyhold_returns,
        equity_strategy, equity_buyhold
    """
    bt = df.copy()
    bt["role"] = roles

    # Sub-strategies
    bt["strat_trend"] = build_trend_signal(bt[close_col], sma_fast, sma_slow)
    bt["strat_reversion"] = build_reversion_signal(bt[close_col], rsi_period, rsi_enter, rsi_exit)
    bt["strat_cash"] = 0

    # Master switch
    bt["composite_signal"] = np.where(
        bt["role"] == "bull", bt["strat_trend"],
        np.where(
            bt["role"] == "bear", bt["strat_cash"],
            bt["strat_reversion"],
        ),
    )

    # Shift +1 to prevent look-ahead bias
    bt["signal_lagged"] = bt["composite_signal"].shift(1).fillna(0)

    # Returns
    bt["strategy_returns"] = bt["signal_lagged"] * bt[log_ret_col]
    bt["buyhold_returns"] = bt[log_ret_col]

    # Equity curves
    bt["equity_strategy"] = np.exp(bt["strategy_returns"].cumsum())
    bt["equity_buyhold"] = np.exp(bt["buyhold_returns"].cumsum())

    bt.dropna(inplace=True)

    return bt
