import os

APP_TITLE = "Stock Tracker"

PAGE_DASHBOARD = "app.py"
PAGE_DETAIL = "pages/stock_detail.py"

_env_tickers = os.environ.get("STOCK_TICKERS")
TICKERS = [t.strip().upper() for t in _env_tickers.split(",")] if _env_tickers else ["META", "GOOGL", "MSFT"]
# BACKLOG: Prices are displayed with a hardcoded "$" symbol. yfinance returns prices in the
# native currency of the exchange, so non-USD tickers (e.g. BP.L on LSE) will show the wrong
# symbol. Fix: fetch ticker.info["currency"] and map to the correct symbol per ticker.
