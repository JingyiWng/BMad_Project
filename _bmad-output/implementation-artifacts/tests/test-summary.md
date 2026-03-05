# Test Automation Summary

**Date:** 2026-03-05
**Framework:** pytest + streamlit.testing.v1 (AppTest)
**Result:** 28 passed, 0 failed

---

## Generated Tests

### Unit Tests — Config

- [x] `tests/test_config.py` — TICKERS env-var parsing, uppercase normalization, whitespace stripping, default fallback, page constant types (6 tests)

### Unit Tests — Data Fetcher (pre-existing)

- [x] `tests/test_fetcher.py` — `get_history` happy path, empty response → None, exception → None (3 tests)

### Unit Tests — Stock Card Component

- [x] `tests/test_stock_card.py` — Error when history is None, error when history too short, metric renders correct price, pct change positive/negative, View Details button rendered, session state set and page switched on click (7 tests)

### E2E Tests — Dashboard (`app.py`)

- [x] `tests/test_app_e2e.py` — No exception on load, subheader per ticker, metric per ticker, error per ticker when data unavailable, View Details button per ticker, metric value reflects last close (6 tests)

### E2E Tests — Stock Detail Page (`pages/stock_detail.py`)

- [x] `tests/test_stock_detail_e2e.py` — Error shown when no ticker in session, Back button shown without ticker, chart renders with ticker in session state, ticker name in page title, error shown when history unavailable, Back button shown with data (6 tests)

---

## Coverage

| Area | Files | Tests |
|---|---|---|
| config.py | 1 | 6 |
| data/fetcher.py | 1 | 3 |
| components/stock_card.py | 1 | 7 |
| app.py (E2E) | 1 | 6 |
| pages/stock_detail.py (E2E) | 1 | 6 |
| **Total** | **5** | **28** |

---

## Bug Found and Fixed

Tests revealed a duplicate element ID bug in `components/stock_card.py`: `st.plotly_chart` was called without a `key` argument, causing a `StreamlitDuplicateElementId` error when multiple tickers rendered on the dashboard simultaneously.

**Fix applied:** Added `key=f"chart_{ticker}"` to the `st.plotly_chart` call in [components/stock_card.py](components/stock_card.py:37).

---

## Next Steps

- Run tests in CI (add `pytest tests/` to your pipeline)
- Add edge cases for unusual ticker symbols or very short history windows as needed
