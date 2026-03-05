"""
E2E tests for the stock detail page (pages/stock_detail.py) using Streamlit AppTest.
These tests simulate a user landing on the detail page with/without a ticker selected.
"""
import pandas as pd
import pytest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


def _make_history(n=20):
    return pd.DataFrame({
        "Date": pd.date_range("2021-01-01", periods=n),
        "Close": [200.0 + i * 5 for i in range(n)],
    })


class TestStockDetailPage:
    def test_shows_error_when_no_ticker_selected(self):
        at = AppTest.from_file("pages/stock_detail.py")
        at.run()
        assert not at.exception
        assert len(at.error) > 0
        assert "No stock selected" in at.error[0].value

    def test_back_button_shown_when_no_ticker(self):
        at = AppTest.from_file("pages/stock_detail.py")
        at.run()
        assert not at.exception
        button_labels = [b.label for b in at.button]
        assert "← Back to Dashboard" in button_labels

    def test_renders_chart_with_ticker_in_session_state(self):
        with patch("data.fetcher.get_history", return_value=_make_history()):
            at = AppTest.from_file("pages/stock_detail.py")
            at.session_state["selected_ticker"] = "AAPL"
            at.run()
        assert not at.exception
        # No error element expected when data loads successfully
        assert len(at.error) == 0

    def test_shows_ticker_name_in_title(self):
        with patch("data.fetcher.get_history", return_value=_make_history()):
            at = AppTest.from_file("pages/stock_detail.py")
            at.session_state["selected_ticker"] = "GOOGL"
            at.run()
        assert not at.exception
        title_text = at.title[0].value if at.title else ""
        assert "GOOGL" in title_text

    def test_shows_error_when_history_unavailable(self):
        with patch("data.fetcher.get_history", return_value=None):
            at = AppTest.from_file("pages/stock_detail.py")
            at.session_state["selected_ticker"] = "FAKE"
            at.run()
        assert not at.exception
        assert len(at.error) > 0

    def test_back_to_dashboard_button_shown_with_data(self):
        with patch("data.fetcher.get_history", return_value=_make_history()):
            at = AppTest.from_file("pages/stock_detail.py")
            at.session_state["selected_ticker"] = "MSFT"
            at.run()
        assert not at.exception
        button_labels = [b.label for b in at.button]
        assert "← Back to Dashboard" in button_labels
