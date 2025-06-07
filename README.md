# DVS Quantum Bot

This project contains a modular trading bot for MetaTrader 5 focusing on assets like XAUUSD, NAS100, BTCUSD and ETHUSD. The code is still experimental but now includes some components adapted from public projects by [neurotrader888](https://github.com/neurotrader888) released under the MIT License.

## Installation

```bash
git clone <repository-url>
cd Dvs-BOT
python -m venv venv
source venv/bin/activate  # on Windows use venv\Scripts\activate
pip install -r requirements.txt
```

Ensure MetaTrader 5 is installed on the machine.

## Configuration

Provide MT5 connection parameters via environment variables before running:

```
MT5_PATH=/path/to/terminal64.exe
MT5_LOGIN=12345678
MT5_PASSWORD=your_password
MT5_SERVER=Broker-Server
```
Then execute `python main.py` to start the bot.

## Modules
- `signals/` – market structure detection using a directional change algorithm
- `volume/` – volumetric tools including permutation entropy
- `models/` – machine learning stubs (LSTM and DNN)
- `models/indicator_score.py` – computes a composite score from classic
  technical indicators
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
