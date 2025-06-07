"""Binance execution utilities for DVS Quantum Bot."""
from __future__ import annotations

from typing import Optional, List, Dict, Any

from binance.client import Client

_client: Optional[Client] = None


def connect(api_key: str | None = None, api_secret: str | None = None) -> bool:
    """Initialize Binance client."""
    global _client
    if not api_key or not api_secret:
        return False
    try:
        _client = Client(api_key, api_secret)
        # Test connectivity
        _client.ping()
        return True
    except Exception:
        _client = None
        return False


def fetch_klines(symbol: str, interval: str = "1m", limit: int = 100) -> List[Dict[str, Any]]:
    """Fetch historical klines from Binance."""
    if _client is None:
        return []
    data = _client.get_klines(symbol=symbol, interval=interval, limit=limit)
    out: List[Dict[str, Any]] = []
    for d in data:
        out.append(
            {
                "open_time": d[0],
                "open": float(d[1]),
                "high": float(d[2]),
                "low": float(d[3]),
                "close": float(d[4]),
                "volume": float(d[5]),
            }
        )
    return out


def place_order(symbol: str, side: str, quantity: float) -> Dict[str, Any]:
    """Place a market order on Binance (placeholder)."""
    if _client is None:
        return {}
    try:
        order = _client.create_order(symbol=symbol, side=side, type="MARKET", quantity=quantity)
        return order
    except Exception:
        return {}
