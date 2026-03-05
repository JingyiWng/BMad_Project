import streamlit as st
from config import APP_TITLE, TICKERS
from components.stock_card import render_stock_card

st.set_page_config(page_title=APP_TITLE, layout="wide")

st.title(APP_TITLE)

cols = st.columns(len(TICKERS))
for ticker, col in zip(TICKERS, cols):
    render_stock_card(ticker, col)

st.markdown(
    "<div style='text-align: center; color: grey; margin-top: 2rem;'>Made with ❤️ by Jenn & Claude Code</div>",
    unsafe_allow_html=True,
)
