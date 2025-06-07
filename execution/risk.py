"""Risk management utilities for DVS Quantum Bot.

This module implements a simple compounding model where the bot
seeks to grow the account by 2.098% per day. The daily target is
distributed across multiple trades. These functions do not guarantee
profit; they merely provide size calculations.
"""
from dataclasses import dataclass


@dataclass
class RiskManager:
    """Calculate position size based on a daily growth target."""

    daily_rate: float = 0.02098
    trades_per_day: int = 100
    reward_risk: float = 3.0  # Take-profit to stop-loss ratio

    def daily_target(self, balance: float) -> float:
        """Return the desired profit for the day."""
        return balance * self.daily_rate

    def profit_per_trade(self, balance: float) -> float:
        """Return the target profit per trade."""
        return self.daily_target(balance) / float(self.trades_per_day)

    def position_size(
        self, balance: float, sl_pips: float, tick_value: float
    ) -> float:
        """Compute lot size for a single trade.

        Parameters
        ----------
        balance: float
            Current account balance.
        sl_pips: float
            Stop-loss in pips for the trade.
        tick_value: float
            Monetary value of one pip per lot.
        """
        if sl_pips <= 0 or tick_value <= 0:
            return 0.0
        profit = self.profit_per_trade(balance)
        risk = profit / self.reward_risk
        return risk / (sl_pips * tick_value)
