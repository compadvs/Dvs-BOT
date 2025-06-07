"""Market structure analysis module for DVS Quantum Bot."""
from dataclasses import dataclass
from typing import List, Dict

import numpy as np


@dataclass
class SwingPoint:
    """Represents a swing high or low point."""
    index: int
    price: float
    type: str  # 'high' or 'low'


def directional_change(close: np.ndarray, high: np.ndarray, low: np.ndarray, sigma: float) -> Dict[str, List[SwingPoint]]:
    """Detect market extremes using the directional change algorithm.

    This implementation adapts the logic from neurotrader888's
    `TechnicalAnalysisAutomation` project, released under the MIT License.
    """
    up_move = True
    tmp_max = high[0]
    tmp_min = low[0]
    tmp_max_i = 0
    tmp_min_i = 0
    tops: List[SwingPoint] = []
    bottoms: List[SwingPoint] = []

    for i in range(len(close)):
        if up_move:
            if high[i] > tmp_max:
                tmp_max = high[i]
                tmp_max_i = i
            elif close[i] < tmp_max - tmp_max * sigma:
                tops.append(SwingPoint(tmp_max_i, tmp_max, 'high'))
                up_move = False
                tmp_min = low[i]
                tmp_min_i = i
        else:
            if low[i] < tmp_min:
                tmp_min = low[i]
                tmp_min_i = i
            elif close[i] > tmp_min + tmp_min * sigma:
                bottoms.append(SwingPoint(tmp_min_i, tmp_min, 'low'))
                up_move = True
                tmp_max = high[i]
                tmp_max_i = i

    return {'highs': tops, 'lows': bottoms}


def analyze_structure(data: List[Dict], sigma: float = 0.02) -> Dict[str, List[SwingPoint]]:
    """Analyze market structure based on directional changes."""
    if not data:
        return {'highs': [], 'lows': []}

    close = np.array([d['close'] for d in data])
    high = np.array([d['high'] for d in data])
    low = np.array([d['low'] for d in data])
    return directional_change(close, high, low, sigma)

