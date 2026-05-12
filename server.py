"""
server.py — Tiny Flask dev server. Auto-fetches data on first run, then serves the dashboard.
"""
import os
import subprocess
import sys
import webbrowser
from flask import Flask, send_file, jsonify

app = Flask(__name__, static_folder=".")
BASE = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return send_file(os.path.join(BASE, "index.html"))


@app.route("/spy_data.json")
def spy_data():
    path = os.path.join(BASE, "spy_data.json")
    if not os.path.exists(path):
        return jsonify({"error": "spy_data.json not found. Run fetch_data.py first."}), 404
    return send_file(path, mimetype="application/json")


@app.route("/api/refresh", methods=["POST"])
def refresh():
    """Re-downloads SPY data on demand and returns it."""
    try:
        from fetch_data import fetch_spy_data
        data = fetch_spy_data()
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "msg": str(e)}), 500


if __name__ == "__main__":
    data_path = os.path.join(BASE, "spy_data.json")
    if not os.path.exists(data_path):
        print("spy_data.json not found - fetching now ...")
        subprocess.run([sys.executable, os.path.join(BASE, "fetch_data.py")])

    url = "http://localhost:5050"
    print(f"\n  SPY Dip Buyer Simulator -> {url}\n")
    webbrowser.open(url)
    app.run(port=5050, debug=False)
