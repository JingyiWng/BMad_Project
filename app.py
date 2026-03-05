import math
import streamlit as st
from config import APP_TITLE, TICKERS, ALL_TICKERS, MAX_STOCK_SELECTION, TICKER_NAMES
from components.stock_card import render_stock_card

st.set_page_config(page_title=APP_TITLE, layout="wide")

st.title(APP_TITLE)

st.caption(f"You can select up to {MAX_STOCK_SELECTION} stocks.")

selected = st.multiselect(
    "Select stocks to display",
    options=ALL_TICKERS,
    default=None,
    placeholder="Choose one or more stocks...",
    max_selections=MAX_STOCK_SELECTION,
    format_func=lambda t: f"{t} — {TICKER_NAMES.get(t, t)}",
)

if not selected:
    st.caption("No stocks picked yet — showing all default stocks.")
    selected = TICKERS

n = len(selected)
if n <= 3:
    rows = [selected]
else:
    mid = math.ceil(n / 2)  # e.g. 4→[2,2], 5→[3,2], 6→[3,3]
    rows = [selected[:mid], selected[mid:]]

for row_tickers in rows:
    cols = st.columns(len(row_tickers))
    for ticker, col in zip(row_tickers, cols):
        render_stock_card(ticker, col)

st.markdown(
    "<div style='text-align: center; color: grey; margin-top: 2rem;'>Made with ❤️ by Jenn & Claude Code</div>",
    unsafe_allow_html=True,
)
