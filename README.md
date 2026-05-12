# 📈 SPY Dip Buyer Simulator

An interactive backtesting dashboard that simulates a **"buy-the-dip"** strategy on SPY (S&P 500 ETF) against three baselines: Dollar-Cost Averaging (DCA), lump-sum Buy & Hold, and cash earning a risk-free rate.

Live data is pulled via **yfinance** (1993 → present). All simulation logic runs client-side in the browser — no database, no backend state.

---

## Features

- **Dip-buyer strategy** — triggers a limit-order buy when SPY drops ≥ N% intraday from open, with a configurable per-trigger investment amount and total budget cap
- **Three baselines** on the same chart:
  - 📗 DCA — spreads the budget evenly across every trading day in the window
  - 🟡 SPY Buy & Hold — lump sum invested on day 1
  - ⬜ Cash — budget compounding at ~4.5% APY (HYSA / T-bill proxy)
- **Regime analysis** — set Start Year and End Year to isolate any historical period (dot-com crash, GFC, COVID, bull runs)
- **Stat cards** — final values and returns for all strategies, dip-day counts, remaining cash
- **Trade log** — every qualifying dip with date, open, low, dip %, limit fill price, and shares bought
- **Live refresh** — fetches the latest SPY data on demand via a serverless API call

---

## Strategy Details

### Dip Detection
A trading day qualifies as a dip if:
```
(open - low) / open >= threshold
```
This uses adjusted OHLC data (splits + dividends factored in), so percentage dips are preserved correctly.

### Fill Price
Buys are simulated as **limit orders** filled at:
```
fill_price = open × (1 - threshold)
```
This reflects a realistic limit order placed at the trigger price, rather than assuming fill at the day's close (which would require seeing the future intraday low).

### Budget Constraint
- `qualifyingDays` counts every day the threshold was met, regardless of cash remaining
- `actualBuys` counts only the days a purchase was executed (limited by budget)
- When the budget is exhausted, the remaining shares continue to grow with the market

---

## Project Structure

```
S&P-Forward-Sim/
├── index.html          # Dashboard UI + simulation logic (all client-side JS)
├── spy_data.json       # Cached SPY OHLC data (1993–present)
├── api/
│   └── refresh.py      # Vercel serverless function — POST /api/refresh
├── fetch_data.py       # Local script to download/refresh spy_data.json
├── server.py           # Local Flask dev server
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment config
└── .vercelignore       # Excludes local-dev files from Vercel upload
```

---

## Local Development

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# Clone the repo
git clone <your-repo-url>
cd S&P-Forward-Sim

# Install dependencies
pip install -r requirements.txt

# (Optional) Fetch fresh data manually
python fetch_data.py

# Start the dev server
python server.py
```

The server will open `http://localhost:5050` automatically. If `spy_data.json` doesn't exist yet, it will be fetched automatically on first run.

### Refreshing Data Locally
Click **"Force Fetch Latest SPY Data"** in the UI, or run:
```bash
python fetch_data.py
```

---

## Deploying to Vercel

### Prerequisites
- [Node.js](https://nodejs.org/) (for the Vercel CLI)
- A [Vercel account](https://vercel.com)

### Steps

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from the project directory
cd S&P-Forward-Sim
vercel
```

Follow the prompts. On first deploy, Vercel will detect the Python serverless function in `api/refresh.py` automatically.

### How it works on Vercel

| Path | Served by |
|------|-----------|
| `/` | `index.html` (static) |
| `/spy_data.json` | `spy_data.json` (static, CDN-cached 1 hour) |
| `POST /api/refresh` | `api/refresh.py` (Python serverless function) |

> **⚠️ Vercel Hobby Plan Note**
> The free Hobby plan caps serverless function execution at **10 seconds**. Fetching 30+ years of SPY data via yfinance can take 10–30s. If the refresh button times out, either upgrade to the Vercel Pro plan (60s limit, already configured in `vercel.json`) or narrow the date range in `api/refresh.py`.
>
> The static `spy_data.json` always loads instantly regardless of plan tier.

---

## Controls

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Budget ($)** | Total capital available to deploy | $20,000 |
| **Dip Threshold (%)** | Minimum intraday drop from open to trigger a buy | 0.5% |
| **Invest per Trigger ($)** | Amount invested on each qualifying dip day | $100 |
| **Start Year** | Beginning of the backtest window | 2010 |
| **End Year** | End of the backtest window | 2026 |

---

## Requirements

```
yfinance>=0.2.0
pandas>=1.5.0
flask>=2.3.0
```
