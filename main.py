
from flask import Flask, jsonify
from tcbs_scraper import fetch_price_from_tcbs
import os

app = Flask(__name__)

@app.route("/api/tcbs/price/<symbol>")
def get_price(symbol):
    price_data = fetch_price_from_tcbs(symbol)
    if price_data:
        return jsonify(price_data)
    return jsonify({"error": f"{symbol} not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
