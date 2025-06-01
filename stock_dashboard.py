import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import datetime

st.title("📈 Real-Time Stock Dashboard (Auto-Update)")

# Default date range: last 30 days
today = datetime.date.today()
default_start = today - datetime.timedelta(days=30)
default_end = today - datetime.timedelta(days=1)

# User inputs
ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL, TSLA, MSFT):", value="AAPL")
start_date = st.date_input("Start Date", value=default_start)
end_date = st.date_input("End Date", value=default_end)

if start_date >= end_date:
    st.error("Error: Start date must be before End date.")
else:
    try:
        # Fetch data automatically when inputs change
        data = yf.download(ticker, start=start_date, end=end_date)

        if not data.empty:
            st.subheader(f"Stock data for {ticker.upper()}")

            # Show last 5 rows of data
            st.dataframe(data.tail())

            # Plot closing price
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price', line=dict(color='blue')))
            fig.update_layout(title=f"{ticker.upper()} Closing Price", xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data found. Try changing the ticker symbol or date range.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
