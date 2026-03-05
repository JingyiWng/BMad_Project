"""
E2E tests for the main dashboard (app.py) using Streamlit AppTest.
These tests simulate a user loading the dashboard page.
"""
import pandas as pd
import pytest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


def _make_history(n=5):
    return pd.DataFrame({
        "Date": pd.date_range("2024-01-01", periods=n),
        "Close": [100.0 + i * 2 for i in range(n)],
    })


class TestDashboard:
    def test_no_exception_on_load_with_data(self):
        with patch("components.stock_card.get_history", return_value=_make_history()):
            at = AppTest.from_file("app.py")
            at.run()
        assert not at.exception

    def test_renders_subheader_for_each_ticker(self):
        with patch("components.stock_card.get_history", return_value=_make_history()):
            at = AppTest.from_file("app.py")
            at.run()
        assert not at.exception
        from config import TICKERS
        subheader_texts = [s.value for s in at.subheader]
        for ticker in TICKERS:
            assert ticker in subheader_texts

    def test_renders_metric_for_each_ticker(self):
        with patch("components.stock_card.get_history", return_value=_make_history()):
            at = AppTest.from_file("app.py")
            at.run()
        assert not at.exception
        from config import TICKERS
        assert len(at.metric) == len(TICKERS)

    def test_shows_error_for_each_ticker_when_history_unavailable(self):
        with patch("components.stock_card.get_history", return_value=None):
            at = AppTest.from_file("app.py")
            at.run()
        assert not at.exception
        from config import TICKERS
        assert len(at.error) == len(TICKERS)

    def test_view_details_button_exists_for_each_ticker(self):
        with patch("components.stock_card.get_history", return_value=_make_history()):
            at = AppTest.from_file("app.py")
            at.run()
        assert not at.exception
        from config import TICKERS
        view_detail_buttons = [b for b in at.button if b.label == "View Details"]
        assert len(view_detail_buttons) == len(TICKERS)

    def test_metric_values_reflect_last_close_price(self):
        history = _make_history(5)  # closes: 100, 102, 104, 106, 108
        with patch("components.stock_card.get_history", return_value=history):
            at = AppTest.from_file("app.py")
            at.run()
        assert not at.exception
        metric_values = [m.value for m in at.metric]
        assert any("$108.00" in v for v in metric_values)
