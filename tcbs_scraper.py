
import requests
from bs4 import BeautifulSoup

def fetch_price_from_tcbs(symbol: str):
    try:
        url = f"https://tcinvest.tcbs.com.vn/stock-detail/{symbol.upper()}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)

        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        price_tag = soup.select_one("div[data-testid='stock-detail-header-price']")

        if not price_tag:
            return None

        price_text = price_tag.get_text(strip=True).replace(",", "")
        if not price_text.isdigit():
            return None

        return {
            "symbol": symbol.upper(),
            "price": int(price_text),
            "exchange": "HOSE"
        }
    except Exception as e:
        print(f"[SCRAPER ERROR] {symbol}: {e}")
        return None
