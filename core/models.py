"""
core/models.py — Regime Detection Models
═══════════════════════════════════════════
All models share the same interface:
    model.fit(X) → returns self
    model.predict(X) → returns array of state labels
    model.get_stats(X, states) → returns dict of per-state metrics
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Protocol

import warnings
warnings.filterwarnings("ignore")


# ══════════════════════════════════════════════════════════════════════════════
# SHARED TYPES & UTILITIES
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class RegimeResult:
    """Standardized output from any regime model."""
    states: np.ndarray             # integer state labels per day
    n_states: int                  # number of detected states
    roles: np.ndarray              # "bull" / "bear" / "neutral" per day
    state_stats: dict              # per-state: mean_ret, mean_vol, pct_time
    model_name: str                # e.g. "HMM", "GMM", "K-Means"
    extra: dict = field(default_factory=dict)  # model-specific info


def assign_roles(states: np.ndarray, log_returns: np.ndarray, n_states: int) -> np.ndarray:
    """
    Assign bull/bear/neutral roles based on mean return per state.
    Highest mean return → bull, lowest → bear, rest → neutral.
    """
    df_temp = pd.DataFrame({"state": states, "ret": log_returns})
    mean_ret = df_temp.groupby("state")["ret"].mean()
    sorted_states = mean_ret.sort_values()

    bull_state = int(sorted_states.index[-1])
    bear_state = int(sorted_states.index[0])

    roles = np.array(["neutral"] * len(states))
    roles[states == bull_state] = "bull"
    roles[states == bear_state] = "bear"

    return roles


def compute_state_stats(
    states: np.ndarray,
    log_returns: np.ndarray,
    real_vol: np.ndarray,
    n_states: int,
) -> dict:
    """Compute per-state statistics."""
    df_temp = pd.DataFrame({
        "state": states,
        "ret": log_returns,
        "vol": real_vol,
    })

    stats = {}
    for s in range(n_states):
        mask = df_temp["state"] == s
        subset = df_temp[mask]
        if len(subset) == 0:
            continue
        stats[s] = {
            "mean_ret": subset["ret"].mean(),
            "mean_vol": subset["vol"].mean(),
            "pct_time": len(subset) / len(df_temp),
            "count": len(subset),
        }

    return stats


# ══════════════════════════════════════════════════════════════════════════════
# MODEL 1: Hidden Markov Model (HMM)
# ══════════════════════════════════════════════════════════════════════════════

def fit_hmm(
    X: np.ndarray,
    log_returns: np.ndarray,
    real_vol: np.ndarray,
    n_states: int = 3,
    n_iter: int = 200,
    random_state: int = 42,
) -> RegimeResult:
    """
    Gaussian HMM regime detection.
    X: observation matrix (log_ret, real_vol [, norm_vol])
    """
    from hmmlearn.hmm import GaussianHMM

    model = GaussianHMM(
        n_components=n_states,
        covariance_type="full",
        n_iter=n_iter,
        random_state=random_state,
    )
    model.fit(X)
    states = model.predict(X)

    roles = assign_roles(states, log_returns, n_states)
    stats = compute_state_stats(states, log_returns, real_vol, n_states)

    return RegimeResult(
        states=states,
        n_states=n_states,
        roles=roles,
        state_stats=stats,
        model_name="HMM",
        extra={
            "transition_matrix": model.transmat_,
            "means": model.means_,
            "log_likelihood": model.score(X),
        },
    )


# ══════════════════════════════════════════════════════════════════════════════
# MODEL 2: Gaussian Mixture Model (GMM)
# ══════════════════════════════════════════════════════════════════════════════

def fit_gmm(
    X: np.ndarray,
    log_returns: np.ndarray,
    real_vol: np.ndarray,
    n_states: int = 3,
    random_state: int = 42,
) -> RegimeResult:
    """
    GMM-based regime classification.
    No temporal ordering — each day classified independently.
    """
    from sklearn.mixture import GaussianMixture

    model = GaussianMixture(
        n_components=n_states,
        covariance_type="full",
        n_init=5,
        random_state=random_state,
    )
    model.fit(X)
    states = model.predict(X)
    probs = model.predict_proba(X)

    roles = assign_roles(states, log_returns, n_states)
    stats = compute_state_stats(states, log_returns, real_vol, n_states)

    return RegimeResult(
        states=states,
        n_states=n_states,
        roles=roles,
        state_stats=stats,
        model_name="GMM",
        extra={
            "probabilities": probs,
            "bic": model.bic(X),
            "aic": model.aic(X),
            "means": model.means_,
        },
    )


# ══════════════════════════════════════════════════════════════════════════════
# MODEL 3: K-Means Clustering
# ══════════════════════════════════════════════════════════════════════════════

def fit_kmeans(
    X: np.ndarray,
    log_returns: np.ndarray,
    real_vol: np.ndarray,
    n_states: int = 3,
    random_state: int = 42,
) -> RegimeResult:
    """
    K-Means hard clustering for regime detection.
    Simplest approach — no probabilities, no temporal info.
    """
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    # K-Means needs scaled data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(
        n_clusters=n_states,
        n_init=10,
        random_state=random_state,
    )
    states = model.fit_predict(X_scaled)

    roles = assign_roles(states, log_returns, n_states)
    stats = compute_state_stats(states, log_returns, real_vol, n_states)

    return RegimeResult(
        states=states,
        n_states=n_states,
        roles=roles,
        state_stats=stats,
        model_name="K-Means",
        extra={
            "inertia": model.inertia_,
            "centers": scaler.inverse_transform(model.cluster_centers_),
        },
    )


# ══════════════════════════════════════════════════════════════════════════════
# MODEL 4: GARCH Volatility Regimes
# ══════════════════════════════════════════════════════════════════════════════

def fit_garch_regimes(
    log_returns: np.ndarray,
    real_vol: np.ndarray,
    n_states: int = 3,
    random_state: int = 42,
) -> RegimeResult:
    """
    GARCH(1,1) → fitted volatility → quantile-based regime classification.

    Uses arch library for GARCH fitting, then classifies volatility regimes
    by percentile thresholds.
    """
    from arch import arch_model

    # Scale returns to percentage for arch library
    returns_pct = log_returns * 100

    model = arch_model(
        returns_pct,
        vol="Garch",
        p=1,
        q=1,
        dist="normal",
        rescale=False,
    )
    result = model.fit(disp="off")

    # Conditional volatility (annualized, back to decimal)
    cond_vol = result.conditional_volatility / 100 * np.sqrt(252)

    # Classify into regimes by volatility quantiles
    thresholds = np.percentile(cond_vol, [100 / n_states * i for i in range(1, n_states)])

    states = np.zeros(len(cond_vol), dtype=int)
    for i, thresh in enumerate(thresholds):
        states[cond_vol > thresh] = i + 1

    # For GARCH: highest vol state = bear, lowest = bull
    # (inverse of return-based assignment)
    vol_means = pd.DataFrame({"state": states, "vol": cond_vol}).groupby("state")["vol"].mean()
    sorted_by_vol = vol_means.sort_values()

    roles = np.array(["neutral"] * len(states))
    roles[states == int(sorted_by_vol.index[0])] = "bull"    # lowest vol → bull
    roles[states == int(sorted_by_vol.index[-1])] = "bear"   # highest vol → bear

    stats = compute_state_stats(states, log_returns, real_vol, n_states)

    return RegimeResult(
        states=states,
        n_states=n_states,
        roles=roles,
        state_stats=stats,
        model_name="GARCH",
        extra={
            "conditional_vol": cond_vol,
            "params": {
                "omega": result.params.get("omega", 0),
                "alpha": result.params.get("alpha[1]", 0),
                "beta": result.params.get("beta[1]", 0),
            },
            "aic": result.aic,
            "bic": result.bic,
        },
    )


# ══════════════════════════════════════════════════════════════════════════════
# ENSEMBLE: Majority Vote
# ══════════════════════════════════════════════════════════════════════════════

def ensemble_vote(results: list[RegimeResult]) -> RegimeResult:
    """
    Majority vote across multiple regime models.

    Uses ROLES (bull/bear/neutral) for voting, not raw state numbers
    (since state 0 in HMM ≠ state 0 in GMM).

    Returns consensus roles + agreement score per day.
    """
    n_days = len(results[0].roles)
    n_models = len(results)

    # Collect role votes per day
    role_votes = np.array([r.roles for r in results])  # shape: (n_models, n_days)

    # Majority vote
    consensus_roles = np.array(["neutral"] * n_days)
    agreement_scores = np.zeros(n_days)

    for i in range(n_days):
        votes = role_votes[:, i]
        unique, counts = np.unique(votes, return_counts=True)
        winner_idx = np.argmax(counts)
        consensus_roles[i] = unique[winner_idx]
        agreement_scores[i] = counts[winner_idx] / n_models

    # Create synthetic integer states from roles for compatibility
    role_to_int = {"bull": 0, "bear": 1, "neutral": 2}
    states = np.array([role_to_int[r] for r in consensus_roles])

    # Can't compute proper state stats without consistent states
    # Use the first model's log_returns proxy
    model_names = [r.model_name for r in results]

    return RegimeResult(
        states=states,
        n_states=3,
        roles=consensus_roles,
        state_stats={},  # filled by caller if needed
        model_name=f"Ensemble ({'+'.join(model_names)})",
        extra={
            "agreement_scores": agreement_scores,
            "mean_agreement": agreement_scores.mean(),
            "individual_results": results,
        },
    )
