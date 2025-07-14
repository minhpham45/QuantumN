
from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/api/tcbs/price/<symbol>', methods=['GET'])
def get_price(symbol):
    try:
        url = f'https://apipubaws.tcbs.com.vn/stock-insight/v2/stock/beta/{symbol.upper()}'
        response = requests.get(url, timeout=10)
        data = response.json()

        if "price" in data and isinstance(data["price"], (int, float)):
            return jsonify({
                "symbol": symbol.upper(),
                "price": int(data["price"]),
                "exchange": "HOSE"
            })
        else:
            return jsonify({"error": f"{symbol.upper()} not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host='0.0.0.0', port=port)
