---
title: 'Stock Price Tracker Dashboard'
slug: 'stock-price-tracker-dashboard'
created: '2026-03-04'
status: 'completed'
stepsCompleted: [1, 2, 3, 4]
tech_stack: ['Python 3.10+', 'Streamlit', 'yfinance', 'Plotly', 'Pandas']
files_to_modify: ['app.py', 'pages/stock_detail.py', 'config.py', 'data/fetcher.py', 'components/stock_card.py', 'requirements.txt']
code_patterns: ['Streamlit multipage app', 'st.cache_data for caching', 'st.session_state for page state', 'Plotly Express px.line for charts']
test_patterns: ['pytest', 'unit tests for fetcher.py']
---

# Tech-Spec: Stock Price Tracker Dashboard

**Created:** 2026-03-04

## Overview

### Problem Statement

No existing tool to monitor a personal shortlist of stocks with clean trend visualization — need a simple, focused dashboard showing price history for a small watchlist.

### Solution

A Python + Streamlit app that fetches stock data via `yfinance`, displays 3 stock cards with 3-month sparkline charts on the home page, and allows drill-down into a 3-year history view per stock.

### Scope

**In Scope:**
- Dashboard page: 3 stock cards (current price, % change, 3-month Plotly line chart)
- Detail page: full 3-year price history chart per stock
- Hardcoded or config-based watchlist of 3 stock tickers
- Color coding (green/red) for price direction

**Out of Scope:**
- User authentication
- Dynamic stock search / adding stocks from UI
- Price alerts or notifications
- News feed
- Mobile app (Streamlit responsive is sufficient)
- Databricks / Spark

## Context for Development

### Codebase Patterns

Confirmed clean slate — greenfield project. Standard Streamlit multipage app structure:
- `app.py` = home/dashboard entry point
- `pages/` directory = additional pages (Streamlit convention for multipage)
- `@st.cache_data(ttl=3600)` for data caching to avoid redundant API calls
- `st.session_state` for passing selected ticker between pages
- Plotly Express (`px.line`) for line charts rendered via `st.plotly_chart(use_container_width=True)`

### Files to Reference

| File | Purpose |
| ---- | ------- |
| `app.py` | Main dashboard — 3 stock cards in columns |
| `pages/stock_detail.py` | Per-stock detail page with 3-year chart |
| `config.py` | Watchlist tickers and app configuration |
| `data/fetcher.py` | yfinance data fetch logic with caching |
| `components/stock_card.py` | Reusable stock card component |
| `requirements.txt` | Python dependencies |

### Technical Decisions

- **Data source:** `yfinance` — free, no API key required, supports historical OHLCV data
- **Frontend:** Streamlit multipage app (home dashboard + per-stock detail page)
- **Charts:** Plotly Express via `st.plotly_chart(use_container_width=True)`
- **Watchlist config:** Python list in `config.py` (e.g. `TICKERS = ["AAPL", "GOOGL", "MSFT"]`)
- **Storage:** No persistence needed — fetch on load, cache with `@st.cache_data(ttl=3600)`
- **Navigation:** `st.session_state["selected_ticker"]` + `st.switch_page()` for drill-down

## Implementation Plan

### Tasks

- [x] Task 1: Create project scaffold and dependencies
  - File: `requirements.txt`
  - Action: Create with contents: `streamlit`, `yfinance`, `plotly`, `pandas`
  - Notes: Pin major versions for reproducibility (e.g. `streamlit>=1.32.0`)

- [x] Task 2: Create watchlist configuration
  - File: `config.py`
  - Action: Define `TICKERS = ["AAPL", "GOOGL", "MSFT"]` and `APP_TITLE = "Stock Tracker"`
  - Notes: User can change tickers here to customize their watchlist

- [x] Task 3: Create data fetcher module
  - File: `data/fetcher.py`
  - Action: Implement two cached functions:
    - `get_history(ticker, period)` — calls `yf.Ticker(ticker).history(period=period)`, returns DataFrame with Date + Close columns
    - `get_current_price(ticker)` — returns latest close price and % change vs previous close
  - Notes: Decorate both with `@st.cache_data(ttl=3600)`. Handle `yfinance` returning empty DataFrame gracefully (return `None`).

- [x] Task 4: Create reusable stock card component
  - File: `components/stock_card.py`
  - Action: Implement `render_stock_card(ticker, col)` function that:
    - Calls `get_history(ticker, "3mo")` and `get_current_price(ticker)`
    - Renders inside `col`: ticker name, current price, % change (green if positive, red if negative using `st.metric`)
    - Renders a compact Plotly `px.line` chart of 3-month close price
    - Renders a button `"View Details"` that sets `st.session_state["selected_ticker"] = ticker` and calls `st.switch_page("pages/stock_detail.py")`
  - Notes: Use `st.metric(label, value, delta)` for price display — built-in green/red coloring

- [x] Task 5: Build main dashboard page
  - File: `app.py`
  - Action:
    - Import `config.TICKERS` and `render_stock_card`
    - Set page config: `st.set_page_config(page_title="Stock Tracker", layout="wide")`
    - Render page title
    - Create 3 columns with `st.columns(3)`
    - Call `render_stock_card(ticker, col)` for each ticker in each column
  - Notes: `layout="wide"` gives more horizontal space for 3 cards

- [x] Task 6: Build stock detail page
  - File: `pages/stock_detail.py`
  - Action:
    - Read `ticker = st.session_state.get("selected_ticker")` — show error if None
    - Call `get_history(ticker, "3y")` for 3-year data
    - Render page title with ticker name
    - Render full-width Plotly `px.line` chart with Date on x-axis, Close on y-axis
    - Add a `"← Back to Dashboard"` button that calls `st.switch_page("app.py")`
  - Notes: Guard against missing session state (user navigating directly to URL)

- [x] Task 7: Create `data/__init__.py` and `components/__init__.py`
  - Files: `data/__init__.py`, `components/__init__.py`
  - Action: Create empty `__init__.py` files to make directories proper Python packages
  - Notes: Required for clean imports across modules

### Acceptance Criteria

- [x] AC 1: Given the app is running, when the dashboard loads, then 3 stock cards are displayed side-by-side in a wide layout, one per configured ticker.

- [x] AC 2: Given a stock card is rendered, when the data loads successfully, then the card shows the ticker symbol, current price, % change from previous close, and a 3-month line chart.

- [x] AC 3: Given a stock card is rendered, when the % change is positive, then the delta is displayed in green; when negative, it is displayed in red.

- [x] AC 4: Given the dashboard is displayed, when the user clicks "View Details" on any stock card, then the app navigates to the detail page showing that stock's 3-year price history.

- [x] AC 5: Given the detail page is displayed, when the 3-year chart renders, then the x-axis shows dates and the y-axis shows closing price, with a clear title indicating the ticker.

- [x] AC 6: Given the detail page is displayed, when the user clicks "← Back to Dashboard", then the app navigates back to the main dashboard.

- [x] AC 7: Given `yfinance` returns an empty or failed response for a ticker, when the card renders, then a user-friendly error message is shown instead of crashing.

- [x] AC 8: Given the app has fetched data for a ticker, when the same ticker data is requested again within 1 hour, then the cached result is returned without a new `yfinance` API call.

## Additional Context

### Dependencies

- `streamlit>=1.32.0` — multipage app, `st.switch_page()`, `st.metric()`
- `yfinance>=0.2.0` — stock data fetching
- `plotly>=5.0.0` — interactive charts via Plotly Express
- `pandas>=2.0.0` — DataFrame manipulation for chart data
- No external APIs, no authentication, no database

### Testing Strategy

**Unit tests** (`pytest`):
- `tests/test_fetcher.py`:
  - Mock `yf.Ticker` to test `get_history()` returns correct DataFrame shape
  - Test `get_current_price()` returns tuple of (price, pct_change)
  - Test `get_history()` returns `None` when yfinance returns empty DataFrame

**Manual testing steps:**
1. Run `streamlit run app.py`
2. Verify 3 cards appear with prices and charts
3. Click "View Details" on each card — confirm correct ticker shown on detail page
4. Verify "← Back to Dashboard" returns to home
5. Temporarily set an invalid ticker in `config.py` — confirm graceful error message

### Notes

- **Risk:** `yfinance` is an unofficial API scraping Yahoo Finance — it can break without notice. If this becomes a production tool, consider migrating to Alpha Vantage or Polygon.io with a free API key.
- **`st.switch_page()` requires Streamlit ≥ 1.32.0** — ensure correct version is installed.
- **Future considerations (out of scope):** Add/remove tickers from UI, price change alerts, volume data, candlestick charts, news feed per stock.
- Session brainstorming file: `_bmad-output/brainstorming/brainstorming-session-2026-03-04-1200.md`

## Review Notes
- Adversarial review completed
- Findings: 12 total (1 noise), 9 fixed, 2 skipped to backlog
- Resolution approach: walk-through
- Critical fix: `st.set_page_config` moved to top of `pages/stock_detail.py`
- Notable improvements: removed redundant API call, added logging, proper test infrastructure (conftest.py, pytest.ini), env-var config override, page path constants
