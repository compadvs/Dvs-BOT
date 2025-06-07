"""Volumetric and liquidity analysis module."""
from typing import List, Dict

import numpy as np

from .entropy import permutation_entropy


def volume_profile(data: List[Dict]) -> Dict[str, List[float]]:
    """Calculate a very basic volume profile using tick volume."""
    if not data:
        return {"hvns": [], "lvns": []}

    volumes = np.array([d.get("tick_volume", 0) for d in data])
    prices = np.array([d["close"] for d in data])
    bins = np.linspace(prices.min(), prices.max(), 20)
    hist, _ = np.histogram(prices, bins=bins, weights=volumes)
    hvn_threshold = np.percentile(hist, 75)
    lvn_threshold = np.percentile(hist, 25)
    hvns = [float(bins[i]) for i, v in enumerate(hist) if v >= hvn_threshold]
    lvns = [float(bins[i]) for i, v in enumerate(hist) if v <= lvn_threshold]
    return {"hvns": hvns, "lvns": lvns}


def liquidity_zones(data: List[Dict]) -> List[Dict]:
    """Detect supply and demand zones using volume spikes."""
    if not data:
        return []

    volumes = np.array([d.get("tick_volume", 0) for d in data])
    threshold = np.mean(volumes) + 2 * np.std(volumes)
    zones = []
    for i, volume in enumerate(volumes):
        if volume > threshold:
            zones.append({"index": i, "volume": int(volume)})
    return zones


def volume_entropy(data: List[Dict]) -> np.ndarray:
    """Compute permutation entropy of volume series."""
    volumes = np.array([d.get("tick_volume", 0) for d in data])
    return permutation_entropy(volumes, order=3, mult=28)

