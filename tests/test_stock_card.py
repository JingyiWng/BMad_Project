import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from components.stock_card import render_stock_card


def _make_history(closes):
    return pd.DataFrame({
        "Date": pd.date_range("2024-01-01", periods=len(closes)),
        "Close": closes,
    })


class TestRenderStockCard:
    def _make_col(self):
        """Return a MagicMock that works as a Streamlit column context manager."""
        col = MagicMock()
        col.__enter__ = MagicMock(return_value=col)
        col.__exit__ = MagicMock(return_value=False)
        return col

    def test_shows_error_when_history_is_none(self):
        col = self._make_col()
        with patch("components.stock_card.get_history", return_value=None), \
             patch("components.stock_card.st") as mock_st:
            render_stock_card("FAKE", col)
            mock_st.error.assert_called_once()
            mock_st.metric.assert_not_called()

    def test_shows_error_when_history_too_short(self):
        col = self._make_col()
        with patch("components.stock_card.get_history", return_value=_make_history([100.0])), \
             patch("components.stock_card.st") as mock_st:
            render_stock_card("FAKE", col)
            mock_st.error.assert_called_once()
            mock_st.metric.assert_not_called()

    def test_renders_metric_with_correct_price(self):
        col = self._make_col()
        history = _make_history([100.0, 110.0])
        with patch("components.stock_card.get_history", return_value=history), \
             patch("components.stock_card.st") as mock_st, \
             patch("components.stock_card.px"):
            mock_st.button.return_value = False
            render_stock_card("AAPL", col)
            mock_st.metric.assert_called_once()
            call_kwargs = mock_st.metric.call_args
            assert "$110.00" in str(call_kwargs)

    def test_pct_change_positive(self):
        col = self._make_col()
        # 100 -> 110 = +10%
        history = _make_history([100.0, 110.0])
        with patch("components.stock_card.get_history", return_value=history), \
             patch("components.stock_card.st") as mock_st, \
             patch("components.stock_card.px"):
            mock_st.button.return_value = False
            render_stock_card("AAPL", col)
            call_args = mock_st.metric.call_args
            assert "+10.00%" in str(call_args)

    def test_pct_change_negative(self):
        col = self._make_col()
        # 110 -> 99 ≈ -10%
        history = _make_history([110.0, 99.0])
        with patch("components.stock_card.get_history", return_value=history), \
             patch("components.stock_card.st") as mock_st, \
             patch("components.stock_card.px"):
            mock_st.button.return_value = False
            render_stock_card("MSFT", col)
            call_args = mock_st.metric.call_args
            assert "-10.00%" in str(call_args)

    def test_view_details_button_is_rendered(self):
        col = self._make_col()
        history = _make_history([100.0, 110.0])
        with patch("components.stock_card.get_history", return_value=history), \
             patch("components.stock_card.st") as mock_st, \
             patch("components.stock_card.px"):
            mock_st.button.return_value = False
            render_stock_card("AAPL", col)
            mock_st.button.assert_called_once_with("View Details", key="btn_AAPL")

    def test_switches_page_when_button_clicked(self):
        col = self._make_col()
        history = _make_history([100.0, 110.0])
        with patch("components.stock_card.get_history", return_value=history), \
             patch("components.stock_card.st") as mock_st, \
             patch("components.stock_card.px"):
            mock_st.button.return_value = True
            render_stock_card("AAPL", col)
            mock_st.session_state.__setitem__.assert_called_with("selected_ticker", "AAPL")
            mock_st.switch_page.assert_called_once()
