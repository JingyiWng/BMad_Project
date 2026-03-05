import streamlit as st
import plotly.express as px
from config import PAGE_DASHBOARD
from data.fetcher import get_history

# BACKLOG: Validate ticker from session_state before passing to yfinance (length, alphanumeric
# whitelist). Low risk currently since it's always set from the config TICKERS list, but becomes
# a real concern if a user-facing search/input feature is added.
ticker = st.session_state.get("selected_ticker")

st.set_page_config(page_title=f"{ticker} — Stock Tracker" if ticker else "Stock Tracker", layout="wide")

if not ticker:
    st.error("No stock selected. Please return to the dashboard and click 'View Details'.")
    if st.button("← Back to Dashboard"):
        st.switch_page(PAGE_DASHBOARD)
    st.stop()

st.title(f"{ticker} — 3-Year Price History")

history = get_history(ticker, "3y")

if history is None:
    st.error(f"Unable to load 3-year history for {ticker}.")
else:
    fig = px.line(
        history,
        x="Date",
        y="Close",
        title=f"{ticker} Closing Price (3 Years)",
        labels={"Close": "Closing Price (USD)", "Date": "Date"},
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

if st.button("← Back to Dashboard"):
    st.switch_page(PAGE_DASHBOARD)
