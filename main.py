from flask import Flask, jsonify
import requests
import os
import ssl

# --- Patch to allow unsafe legacy SSL renegotiation for TCBS ---
try:
    ssl_context = ssl.create_default_context()
    ssl_context.options |= 0x4  # Enable unsafe legacy renegotiation
    ssl._create_default_https_context = lambda: ssl_context
except Exception as e:
    print(f"[SSL PATCH ERROR] {e}")

app = Flask(__name__)

@app.route('/api/tcbs/price/<symbol>', methods=['GET'])
def get_price(symbol):
    try:
        url = f'https://apipubaws.tcbs.com.vn/stock-insight/v2/stock/beta?tickers={symbol.upper()}'
        response = requests.get(url, timeout=10)
        data = response.json()

        items = data.get("data", [])
        if items and "price" in items[0]:
            return jsonify({
                "symbol": symbol.upper(),
                "price": int(items[0]["price"]),
                "exchange": items[0].get("exchangeCode", "HOSE")
            })

        return jsonify({"error": f"{symbol.upper()} not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host='0.0.0.0', port=port)