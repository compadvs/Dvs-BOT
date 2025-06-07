# Dvs-BOT

This project aims to build a trading bot focused on **BTC/USD**.  
The bot relies on several open source repositories provided by
[neurotrader888](https://github.com/neurotrader888).

## Getting started

First clone the helper repositories:

```bash
./fetch_dependencies.sh
```

After fetching the dependencies you can run a simple moving average
strategy from the `mcpt` library using:

```bash
python btc_ma_strategy.py
```

The script expects a `BTCUSD3600.pq` file with OHLCV data in the
repository root or in the working directory.
