import streamlit as st
import plotly.express as px
from config import PAGE_DETAIL
from data.fetcher import get_history


def render_stock_card(ticker: str, col) -> None:
    """Render a stock card with current price, % change, 3-month sparkline, and detail button."""
    with col:
        st.subheader(ticker)

        history = get_history(ticker, "3mo")

        if history is None or len(history) < 2:
            st.error(f"Unable to load data for {ticker}.")
            return

        current_price = history["Close"].iloc[-1]
        previous_price = history["Close"].iloc[-2]
        pct_change = ((current_price - previous_price) / previous_price) * 100

        st.metric(
            label="Current Price",
            value=f"${current_price:.2f}",
            delta=f"{pct_change:+.2f}%",
        )

        fig = px.line(history, x="Date", y="Close", title="3-Month Price")
        fig.update_layout(
            height=200,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=False,
        )
        fig.update_xaxes(title_text="")
        fig.update_yaxes(title_text="")
        # BACKLOG: Pass config={"staticPlot": True} to reduce JS overhead for this compact sparkline.
        st.plotly_chart(fig, use_container_width=True)

        if st.button("View Details", key=f"btn_{ticker}"):
            st.session_state["selected_ticker"] = ticker
            st.switch_page(PAGE_DETAIL)
