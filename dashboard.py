import streamlit as st
import yfinance as yf
import plotly.express as px

st.title("Investment Decision Dashboard")

ticker = st.text_input("Enter Stock Ticker:", "NVDA")
if ticker:
    stock = yf.download(ticker, period="6mo")
    stock.columns = stock.columns.droplevel(1)

    # Compute indicators
    # stock["SMA_50"] = talib.SMA(stock["Close"], timeperiod=50)
    # stock["SMA_200"] = talib.SMA(stock["Close"], timeperiod=200)

    # Plot stock price
    fig = px.line(stock, 
                  x=stock.index, 
                  y=['Close'], #, "SMA_50", "SMA_200"], 
                  title=f"{ticker} Stock Price & SMAs")
    st.plotly_chart(fig)

    # Fetch news and summarize
    # news = fetch_financial_news(ticker)
    # summary = summarize_news(news)
    summary = 'Temporary Place Holder'
    st.subheader("Top Strengths & Weaknesses")
    st.write(summary)