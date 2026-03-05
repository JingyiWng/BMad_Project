import pandas as pd
from unittest.mock import patch, MagicMock

from data.fetcher import get_history


def _make_ticker_mock(history_df: pd.DataFrame) -> MagicMock:
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = history_df
    return mock_ticker


class TestGetHistory:
    def test_returns_dataframe_with_date_and_close(self):
        df = pd.DataFrame({
            "Open": [100] * 5,
            "Close": [110, 112, 108, 115, 120],
            "High": [115] * 5,
            "Low": [105] * 5,
            "Volume": [1000] * 5,
        }, index=pd.DatetimeIndex(pd.date_range("2024-01-01", periods=5), name="Date"))
        with patch("data.fetcher.yf.Ticker", return_value=_make_ticker_mock(df)):
            result = get_history("AAPL", "3mo")
        assert result is not None
        assert list(result.columns) == ["Date", "Close"]
        assert len(result) == 5

    def test_returns_none_when_empty_dataframe(self):
        empty_df = pd.DataFrame()
        with patch("data.fetcher.yf.Ticker", return_value=_make_ticker_mock(empty_df)):
            result = get_history("FAKE", "3mo")
        assert result is None

    def test_returns_none_on_exception(self):
        mock_ticker = MagicMock()
        mock_ticker.history.side_effect = Exception("API error")
        with patch("data.fetcher.yf.Ticker", return_value=mock_ticker):
            result = get_history("AAPL", "3mo")
        assert result is None
