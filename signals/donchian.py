"""Donchian breakout signals adapted from neurotrader888's mcpt project."""
from __future__ import annotations

from typing import Tuple
import numpy as np
import pandas as pd


def donchian_breakout(ohlc: pd.DataFrame, lookback: int) -> pd.Series:
    upper = ohlc['close'].rolling(lookback - 1).max().shift(1)
    lower = ohlc['close'].rolling(lookback - 1).min().shift(1)
    signal = pd.Series(np.full(len(ohlc), np.nan), index=ohlc.index)
    signal.loc[ohlc['close'] > upper] = 1
    signal.loc[ohlc['close'] < lower] = -1
    signal = signal.ffill()
    return signal


def optimize_donchian(ohlc: pd.DataFrame) -> Tuple[int, float]:
    best_pf = 0.0
    best_lookback = -1
    r = np.log(ohlc['close']).diff().shift(-1)
    for lookback in range(12, 169):
        signal = donchian_breakout(ohlc, lookback)
        sig_rets = signal * r
        pf = sig_rets[sig_rets > 0].sum() / sig_rets[sig_rets < 0].abs().sum()
        if pf > best_pf:
            best_pf = pf
            best_lookback = lookback
    return best_lookback, float(best_pf)
