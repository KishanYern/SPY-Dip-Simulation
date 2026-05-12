"""
Vercel serverless function — fetches live SPY OHLC data via yfinance
and returns it as JSON (no filesystem writes).
"""
import json
from datetime import datetime, timezone


def handler(request):
    """Vercel Python serverless handler."""
    if request.method == "OPTIONS":
        return Response("", status=200, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        })

    if request.method != "POST":
        return Response(
            json.dumps({"ok": False, "msg": "Method not allowed"}),
            status=405,
            headers={"Content-Type": "application/json"},
        )

    try:
        import yfinance as yf

        end = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        ticker = yf.Ticker("SPY")
        df = ticker.history(start="1993-01-01", end=end, auto_adjust=True)
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

        return Response(
            json.dumps({"ok": True, "data": data}),
            status=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        )

    except Exception as e:
        return Response(
            json.dumps({"ok": False, "msg": str(e)}),
            status=500,
            headers={"Content-Type": "application/json"},
        )
