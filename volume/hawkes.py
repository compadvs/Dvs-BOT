"""Volatility Hawkes process utilities adapted from neurotrader888's project."""
from __future__ import annotations

import numpy as np
import pandas as pd


def hawkes_process(data: pd.Series, kappa: float) -> pd.Series:
    assert kappa > 0.0
    alpha = np.exp(-kappa)
    arr = data.to_numpy()
    output = np.zeros(len(data))
    output[:] = np.nan
    for i in range(1, len(data)):
        if np.isnan(output[i - 1]):
            output[i] = arr[i]
        else:
            output[i] = output[i - 1] * alpha + arr[i]
    return pd.Series(output, index=data.index) * kappa


def vol_signal(close: pd.Series, vol_hawkes: pd.Series, lookback: int) -> np.ndarray:
    signal = np.zeros(len(close))
    q05 = vol_hawkes.rolling(lookback).quantile(0.05)
    q95 = vol_hawkes.rolling(lookback).quantile(0.95)
    last_below = -1
    curr_sig = 0.0

    for i in range(len(signal)):
        if vol_hawkes.iloc[i] < q05.iloc[i]:
            last_below = i
            curr_sig = 0.0
        if vol_hawkes.iloc[i] > q95.iloc[i] and vol_hawkes.iloc[i - 1] <= q95.iloc[i - 1] and last_below > 0:
            change = close.iloc[i] - close.iloc[last_below]
            curr_sig = 1 if change > 0 else -1
        signal[i] = curr_sig
    return signal
