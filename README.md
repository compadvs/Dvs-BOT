# DVS Quantum Bot

This project contains a modular trading bot for MetaTrader 5 focusing on assets like XAUUSD, NAS100, BTCUSD and ETHUSD. The code is still experimental but now includes some components adapted from public projects by [neurotrader888](https://github.com/neurotrader888) released under the MIT License.

## Modules
- `signals/` – market structure detection using a directional change algorithm
- `volume/` – volumetric tools including permutation entropy
- `models/` – machine learning stubs (LSTM and DNN)
- `execution/` – MetaTrader 5 trade execution and risk management
- `journal/` – daily emotional journal utilities

`main.py` ties everything together. A new `RiskManager` class calculates lot
sizes to reach a theoretical daily target of **2.098%** spread across roughly
100 trades. This is purely an example and does not guarantee profit.

Additional signal generation modules adapt open source code from
`TrendLineAutomation`, `market-structure`, `mcpt`, and `VolatilityHawkes`
by **neurotrader888** (MIT License) for detecting trendlines, Donchian
breakouts, and volatility signals.

The new `signals/breakout.py` module combines these tools to trade
breakouts on the **M5** and **H4** timeframes. The take‑profit target is
set to the next detected range floor or roof, allowing both scalping and
swing trades depending on the timeframe.
