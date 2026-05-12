"""
fetch_data.py — Downloads SPY daily OHLC data via yfinance and saves to spy_data.json
"""
import json
import os
from datetime import datetime, timezone
import yfinance as yf

BASE = os.path.dirname(os.path.abspath(__file__))


def fetch_spy_data(start: str = "1993-01-01", end: str | None = None) -> dict:
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    print(f"Downloading SPY data {start} to {end} ...")
    ticker = yf.Ticker("SPY")
    df = ticker.history(start=start, end=end, auto_adjust=True)
    df = df.dropna(subset=["Open", "High", "Low", "Close"])
    df = df.sort_index()

    data = {
        "dates": df.index.strftime("%Y-%m-%d").tolist(),
        "open":  [round(float(x), 4) for x in df["Open"]],
        "high":  [round(float(x), 4) for x in df["High"]],
        "low":   [round(float(x), 4) for x in df["Low"]],
        "close": [round(float(x), 4) for x in df["Close"]],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(os.path.join(BASE, "spy_data.json"), "w") as f:
        json.dump(data, f)

    print(f"Done. Saved {len(data['dates'])} trading days  "
          f"({data['dates'][0]} to {data['dates'][-1]})")
    return data


if __name__ == "__main__":
    fetch_spy_data()
