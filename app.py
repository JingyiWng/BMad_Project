import math
import streamlit as st
from config import APP_TITLE, TICKERS, ALL_TICKERS, MAX_STOCK_SELECTION, TICKER_NAMES
from components.stock_card import render_stock_card

st.set_page_config(page_title=APP_TITLE, layout="wide")

st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #b8cfff 0%, #d0e0f7 45%, #d8ceff 100%);
    border-radius: 18px;
    padding: 1.6rem 2rem;
    text-align: center;
    margin-bottom: 1.75rem;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 800;
    color: #111827;
    margin: 0;
    letter-spacing: -0.5px;
}
div[data-testid="stButton"] button[kind="primary"] {
    background-color: #4F46E5;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.45rem 1.1rem;
    width: 100%;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    background-color: #4338CA;
    border: none;
}
</style>
<div class="hero">
    <h1>Stock Tracker</h1>
</div>
""", unsafe_allow_html=True)

selected = st.multiselect(
    f"Select stocks to display (up to {MAX_STOCK_SELECTION})",
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
    "<div style='text-align: center; color: grey; margin-top: 2rem;'>A BMad Project - Made with ❤️ by Jenn & Claude Code</div>",
    unsafe_allow_html=True,
)
