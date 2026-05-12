"""
Vercel serverless function — fetches live SPY OHLC data via yfinance
and returns it as JSON (no filesystem writes).
"""
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime, timezone


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
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

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "data": data}).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "msg": str(e)}).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
