from flask import Flask, jsonify
import requests
import os
import ssl

# --- Patch SSL để hỗ trợ legacy TLS của TCBS ---
try:
    ssl_context = ssl.create_default_context()
    ssl_context.options |= 0x4  # Bật legacy renegotiation
    ssl._create_default_https_context = lambda: ssl_context
except Exception as e:
    print(f"SSL Legacy Patch Error: {e}")

app = Flask(__name__)

@app.route('/api/tcbs/price/<symbol>', methods=['GET'])
def get_price(symbol):
    try:
        url = f'https://apipub.tcbs.com.vn/stock-insight/v1/stock/overview?tickers={symbol.upper()}'
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return jsonify({"error": f"TCBS API Error: {response.status_code}"}), 500

        data = response.json()
        items = data.get("data", [])

        if len(items) > 0 and "price" in items[0]:
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
