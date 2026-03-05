import streamlit as st
import plotly.express as px
from config import PAGE_DETAIL, TICKER_NAMES
from data.fetcher import get_history

# Brand accent colors per ticker
TICKER_COLORS = {
    "AAPL":  "#555555",
    "MSFT":  "#107C10",
    "NVDA":  "#76B900",
    "AMZN":  "#FF9900",
    "GOOGL": "#4285F4",
    "META":  "#0866FF",
    "TSLA":  "#CC0000",
    "BRK-B": "#4E3629",
    "JPM":   "#003087",
    "V":     "#1A1F71",
    "UNH":   "#002677",
    "XOM":   "#D0021B",
    "LLY":   "#D52B1E",
    "JNJ":   "#D51F29",
    "WMT":   "#0071CE",
    "MA":    "#EB001B",
    "AVGO":  "#CC0000",
    "PG":    "#003087",
    "HD":    "#F96302",
    "COST":  "#005DAA",
    "MRK":   "#00857C",
    "ORCL":  "#F80000",
    "CVX":   "#005AA3",
    "ABBV":  "#071D49",
    "NFLX":  "#E50914",
    "KO":    "#F40009",
    "BAC":   "#E31837",
    "CRM":   "#00A1E0",
    "AMD":   "#ED1C24",
    "PEP":   "#004B93",
    "ADBE":  "#FF0000",
    "INTC":  "#0071C5",
    "QCOM":  "#3253DC",
    "DIS":   "#113CCF",
    "IBM":   "#1F70C1",
}

# Company domain for each ticker (used to fetch logos via Clearbit)
TICKER_DOMAINS = {
    "AAPL":  "apple.com",
    "MSFT":  "microsoft.com",
    "NVDA":  "nvidia.com",
    "AMZN":  "amazon.com",
    "GOOGL": "google.com",
    "META":  "meta.com",
    "TSLA":  "tesla.com",
    "BRK-B": "berkshirehathaway.com",
    "JPM":   "jpmorganchase.com",
    "V":     "visa.com",
    "UNH":   "unitedhealthgroup.com",
    "XOM":   "exxonmobil.com",
    "LLY":   "lilly.com",
    "JNJ":   "jnj.com",
    "WMT":   "walmart.com",
    "MA":    "mastercard.com",
    "AVGO":  "broadcom.com",
    "PG":    "pg.com",
    "HD":    "homedepot.com",
    "COST":  "costco.com",
    "MRK":   "merck.com",
    "ORCL":  "oracle.com",
    "CVX":   "chevron.com",
    "ABBV":  "abbvie.com",
    "NFLX":  "netflix.com",
    "KO":    "coca-cola.com",
    "BAC":   "bankofamerica.com",
    "CRM":   "salesforce.com",
    "AMD":   "amd.com",
    "PEP":   "pepsico.com",
    "ADBE":  "adobe.com",
    "INTC":  "intel.com",
    "QCOM":  "qualcomm.com",
    "DIS":   "disney.com",
    "IBM":   "ibm.com",
}


def _logo_url(ticker: str) -> str | None:
    domain = TICKER_DOMAINS.get(ticker)
    return f"https://www.google.com/s2/favicons?domain={domain}&sz=128" if domain else None


def _fallback_logo_html(ticker: str) -> str:
    color = TICKER_COLORS.get(ticker, "#4F46E5")
    initials = ticker[:2]
    return (
        f'<div style="width:36px;height:36px;border-radius:8px;background:{color};'
        f'display:flex;align-items:center;justify-content:center;'
        f'font-size:11px;font-weight:bold;color:white;">{initials}</div>'
    )


def render_stock_card(ticker: str, col) -> None:
    """Render a stock card with current price, % change, 3-month sparkline, and detail button."""
    accent = TICKER_COLORS.get(ticker, "#4F46E5")
    company = TICKER_NAMES.get(ticker, ticker)

    with col:
        with st.container(border=True):
            # Header: logo + ticker + company name
            logo_col, name_col = st.columns([1, 4], vertical_alignment="center")
            with logo_col:
                logo_url = _logo_url(ticker)
                if logo_url:
                    st.image(logo_url, width=36)
                else:
                    st.markdown(_fallback_logo_html(ticker), unsafe_allow_html=True)
            with name_col:
                st.markdown(
                    f"<div style='font-size:1.05rem;font-weight:800;color:#111827;line-height:1.1;'>{ticker}</div>"
                    f"<div style='font-size:0.72rem;color:#6b7280;'>{company}</div>",
                    unsafe_allow_html=True,
                )

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
            fig.update_traces(line_color=accent)
            fig.update_xaxes(title_text="")
            fig.update_yaxes(title_text="")
            st.plotly_chart(fig, use_container_width=True, key=f"chart_{ticker}")

            if st.button("View Details  \u203a", key=f"btn_{ticker}", type="primary"):
                st.session_state["selected_ticker"] = ticker
                st.switch_page(PAGE_DETAIL)
