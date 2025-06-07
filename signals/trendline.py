"""Trend line utilities adapted from neurotrader888's TrendLineAutomation.
"""
from __future__ import annotations

from typing import Tuple
import numpy as np


def _check_trend_line(support: bool, pivot: int, slope: float, y: np.ndarray) -> float:
    intercept = -slope * pivot + y[pivot]
    line_vals = slope * np.arange(len(y)) + intercept
    diffs = line_vals - y

    if support and diffs.max() > 1e-5:
        return -1.0
    if not support and diffs.min() < -1e-5:
        return -1.0
    return float((diffs ** 2.0).sum())


def _optimize_slope(support: bool, pivot: int, init_slope: float, y: np.ndarray) -> Tuple[float, float]:
    slope_unit = (y.max() - y.min()) / len(y)
    opt_step = 1.0
    min_step = 0.0001
    curr_step = opt_step
    best_slope = init_slope
    best_err = _check_trend_line(support, pivot, init_slope, y)
    get_derivative = True
    derivative = None

    while curr_step > min_step:
        if get_derivative:
            slope_change = best_slope + slope_unit * min_step
            test_err = _check_trend_line(support, pivot, slope_change, y)
            derivative = test_err - best_err
            if test_err < 0.0:
                slope_change = best_slope - slope_unit * min_step
                test_err = _check_trend_line(support, pivot, slope_change, y)
                derivative = best_err - test_err
            if test_err < 0.0:
                raise ValueError("Derivative failed. Check data")
            get_derivative = False

        if derivative > 0.0:
            test_slope = best_slope - slope_unit * curr_step
        else:
            test_slope = best_slope + slope_unit * curr_step

        test_err = _check_trend_line(support, pivot, test_slope, y)
        if test_err < 0 or test_err >= best_err:
            curr_step *= 0.5
        else:
            best_err = test_err
            best_slope = test_slope
            get_derivative = True
    return best_slope, -best_slope * pivot + y[pivot]


def fit_trendlines_high_low(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Return slopes and intercepts for support and resistance lines."""
    x = np.arange(len(close))
    coefs = np.polyfit(x, close, 1)
    line_points = coefs[0] * x + coefs[1]
    upper_pivot = int((high - line_points).argmax())
    lower_pivot = int((low - line_points).argmin())

    support_coefs = _optimize_slope(True, lower_pivot, coefs[0], low)
    resist_coefs = _optimize_slope(False, upper_pivot, coefs[0], high)
    return support_coefs, resist_coefs
