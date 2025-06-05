"""Breakout detection utilities for DVS Quantum Bot.

This module uses Donchian channels and recent swing points to detect
breakouts on the 5-minute and 4-hour timeframes. The take-profit level
is chosen as the next range floor or roof identified from the
market structure.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from .donchian import donchian_breakout
from .market_structure import SwingPoint


def range_levels(structure: Dict[str, List[SwingPoint]]) -> Tuple[float, float]:
    """Return the most recent swing high and low as range levels."""
    highs = structure.get("highs", [])
    lows = structure.get("lows", [])
    high_price = highs[-2].price if len(highs) >= 2 else 0.0
    low_price = lows[-2].price if len(lows) >= 2 else 0.0
    return high_price, low_price


def detect_breakout(
    ohlc: pd.DataFrame, structure: Dict[str, List[SwingPoint]], lookback: int = 20
) -> Tuple[int, float, float]:
    """Return breakout signal along with TP and SL levels."""
    if ohlc.empty:
        return 0, 0.0, 0.0

    signal_series = donchian_breakout(ohlc, lookback)
    latest = signal_series.iloc[-1]
    if np.isnan(latest):
        return 0, 0.0, 0.0

    high_price, low_price = range_levels(structure)
    if latest > 0:
        # breakout to upside
        tp = high_price if high_price else float(ohlc["high"].max())
        sl = low_price if low_price else float(ohlc["low"].min())
        return 1, tp, sl
    if latest < 0:
        tp = low_price if low_price else float(ohlc["low"].min())
        sl = high_price if high_price else float(ohlc["high"].max())
        return -1, tp, sl

    return 0, 0.0, 0.0
