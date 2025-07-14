from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/api/tcbs/price/<symbol>', methods=['GET'])
def get_price(symbol):
    try:
        url = f'https://apipubaws.tcbs.com.vn/stock-insight/v2/stock/beta?tickers={symbol.upper()}'
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
