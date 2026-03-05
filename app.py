import streamlit as st
from config import APP_TITLE, TICKERS
from components.stock_card import render_stock_card

st.set_page_config(page_title=APP_TITLE, layout="wide")

st.title(APP_TITLE)

cols = st.columns(len(TICKERS))
for ticker, col in zip(TICKERS, cols):
    render_stock_card(ticker, col)
