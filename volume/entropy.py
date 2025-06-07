"""Permutation entropy utilities.

Adapted from neurotrader888's PermutationEntropy project (MIT License).
"""
from __future__ import annotations

import math
from typing import List

import numpy as np
import pandas as pd


def ordinal_patterns(arr: np.ndarray, order: int) -> np.ndarray:
    """Return array of ordinal pattern indices."""
    assert order >= 2
    fac = math.factorial(order)
    order_minus_one = order - 1
    mults = [fac / math.factorial(i + 1) for i in range(1, order)]
    ordinals = np.full(len(arr), np.nan)

    for i in range(order_minus_one, len(arr)):
        window = arr[i - order_minus_one : i + 1]
        pattern_ordinal = 0
        for l in range(1, order):
            count = 0
            for r in range(l):
                if window[order_minus_one - l] >= window[order_minus_one - r]:
                    count += 1
            pattern_ordinal += count * mults[l - 1]
        ordinals[i] = int(pattern_ordinal)

    return ordinals


def permutation_entropy(arr: np.ndarray, order: int, mult: int) -> np.ndarray:
    """Compute normalized permutation entropy."""
    fac = math.factorial(order)
    lookback = fac * mult
    ent = np.full(len(arr), np.nan)
    ordinals = ordinal_patterns(arr, order)

    for i in range(lookback + order - 1, len(arr)):
        window = ordinals[i - lookback + 1 : i + 1]
        freqs = pd.Series(window).value_counts().to_dict()
        for key in freqs:
            freqs[key] = freqs[key] / lookback

        value = 0.0
        for v in freqs.values():
            value += v * math.log2(v)
        ent[i] = -value / math.log2(fac)

    return ent

