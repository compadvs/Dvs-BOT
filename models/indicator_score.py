"""Indicator-based scoring for trade setups."""
from __future__ import annotations

from typing import Dict

import pandas as pd
import pandas_ta as ta


def indicator_score(ohlc: pd.DataFrame) -> Dict[str, float]:
    """Return aggregate score from multiple indicators.

    Parameters
    ----------
    ohlc : pandas.DataFrame
        Data frame with columns `open`, `high`, `low`, `close`, `volume`.
    """
    if ohlc.empty:
        return {"score": 0.0}

    close = ohlc["close"]
    high = ohlc["high"]
    low = ohlc["low"]
    volume = ohlc.get("volume", ohlc.get("tick_volume"))

    signals = []

    # Moving Average cross
    sma50 = ta.sma(close, length=50)
    sma200 = ta.sma(close, length=200)
    if not sma50.empty and not sma200.empty:
        signals.append(1 if sma50.iloc[-1] > sma200.iloc[-1] else -1)

    # RSI overbought/oversold
    rsi = ta.rsi(close, length=14)
    if not rsi.empty:
        val = rsi.iloc[-1]
        if val < 30:
            signals.append(1)
        elif val > 70:
            signals.append(-1)

    # MACD crossover
    macd = ta.macd(close)
    if not macd.empty:
        m = macd["MACD_12_26_9"].iloc[-1]
        s = macd["MACDs_12_26_9"].iloc[-1]
        if m > s:
            signals.append(1)
        elif m < s:
            signals.append(-1)

    # Bollinger Bands
    bb = ta.bbands(close, length=20, std=2)
    if not bb.empty:
        upper = bb["BBU_20_2.0"].iloc[-1]
        lower = bb["BBL_20_2.0"].iloc[-1]
        price = close.iloc[-1]
        if price > upper:
            signals.append(-1)
        elif price < lower:
            signals.append(1)

    # Fibonacci retracement using last 100 bars
    lookback_high = high[-100:].max()
    lookback_low = low[-100:].min()
    if lookback_high != lookback_low:
        ratio = (close.iloc[-1] - lookback_low) / (lookback_high - lookback_low)
        if ratio < 0.382:
            signals.append(1)
        elif ratio > 0.618:
            signals.append(-1)

    # VWAP intraday
    if volume is not None:
        vwap = ta.vwap(high, low, close, volume)
        if not vwap.empty:
            signals.append(1 if close.iloc[-1] > vwap.iloc[-1] else -1)

    # ATR volatility for trailing stop context
    atr = ta.atr(high, low, close, length=14)
    if not atr.empty:
        avg_atr = atr[-20:].mean()
        if atr.iloc[-1] > avg_atr:
            signals.append(1)

    # SuperTrend
    st = ta.supertrend(high, low, close, length=10, multiplier=3)
    if not st.empty and "SUPERTd_10_3.0" in st:
        signals.append(1 if st["SUPERTd_10_3.0"].iloc[-1] > 0 else -1)

    # Stochastic Oscillator
    stoch = ta.stoch(high, low, close)
    if not stoch.empty and "STOCHk_14_3_3" in stoch:
        k = stoch["STOCHk_14_3_3"].iloc[-1]
        if k < 20:
            signals.append(1)
        elif k > 80:
            signals.append(-1)

    # Ichimoku Cloud
    ichi = ta.ichimoku(high, low, close)
    if not ichi.empty and {"ISA_9", "ISB_26"}.issubset(ichi.columns):
        base = ichi["ISA_9"].iloc[-1]
        span_b = ichi["ISB_26"].iloc[-1]
        price = close.iloc[-1]
        if price > max(base, span_b):
            signals.append(1)
        elif price < min(base, span_b):
            signals.append(-1)

    score = float(sum(signals))
    return {"score": score}
