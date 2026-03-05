import os

APP_TITLE = "Stock Tracker"

PAGE_DASHBOARD = "app.py"
PAGE_DETAIL = "pages/stock_detail.py"

_env_tickers = os.environ.get("STOCK_TICKERS")
TICKERS = [t.strip().upper() for t in _env_tickers.split(",")] if _env_tickers else ["META", "GOOGL", "MSFT"]

ALL_TICKERS = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "BRK-B", "JPM", "V",
    "UNH", "XOM", "LLY", "JNJ", "WMT", "MA", "AVGO", "PG", "HD", "COST",
    "MRK", "ORCL", "CVX", "ABBV", "NFLX", "KO", "BAC", "CRM", "AMD", "PEP",
    "ADBE", "INTC", "QCOM", "DIS", "IBM",
]

TICKER_NAMES = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "AMZN": "Amazon",
    "GOOGL": "Alphabet",
    "META": "Meta Platforms",
    "TSLA": "Tesla",
    "BRK-B": "Berkshire Hathaway",
    "JPM": "JPMorgan Chase",
    "V": "Visa",
    "UNH": "UnitedHealth Group",
    "XOM": "Exxon Mobil",
    "LLY": "Eli Lilly",
    "JNJ": "Johnson & Johnson",
    "WMT": "Walmart",
    "MA": "Mastercard",
    "AVGO": "Broadcom",
    "PG": "Procter & Gamble",
    "HD": "Home Depot",
    "COST": "Costco Wholesale",
    "MRK": "Merck",
    "ORCL": "Oracle",
    "CVX": "Chevron",
    "ABBV": "AbbVie",
    "NFLX": "Netflix",
    "KO": "Coca-Cola",
    "BAC": "Bank of America",
    "CRM": "Salesforce",
    "AMD": "Advanced Micro Devices",
    "PEP": "PepsiCo",
    "ADBE": "Adobe",
    "INTC": "Intel",
    "QCOM": "Qualcomm",
    "DIS": "Walt Disney",
    "IBM": "IBM",
}

MAX_STOCK_SELECTION = 6
# BACKLOG: Prices are displayed with a hardcoded "$" symbol. yfinance returns prices in the
# native currency of the exchange, so non-USD tickers (e.g. BP.L on LSE) will show the wrong
# symbol. Fix: fetch ticker.info["currency"] and map to the correct symbol per ticker.
