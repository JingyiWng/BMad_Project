import logging
import streamlit as st
import yfinance as yf
import pandas as pd

logger = logging.getLogger(__name__)


@st.cache_data(ttl=3600)
def get_history(ticker: str, period: str) -> pd.DataFrame | None:
    """Fetch historical OHLCV data for a ticker. Returns DataFrame with Date + Close, or None on failure."""
    try:
        df = yf.Ticker(ticker).history(period=period)
        if df.empty:
            logger.warning("get_history: empty response for ticker=%s period=%s", ticker, period)
            return None
        df = df.reset_index()[["Date", "Close"]]
        return df
    except Exception as e:
        logger.warning("get_history: failed for ticker=%s period=%s: %s", ticker, period, e)
        return None
