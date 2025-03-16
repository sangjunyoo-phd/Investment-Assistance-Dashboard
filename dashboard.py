from quantitative_analysis import fetch_stock_data, calculate_SMA
import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Investment Decision Dashboard")

ticker = st.text_input("Enter Stock Ticker:", "NVDA")
if ticker:
    stock = fetch_stock_data(ticker)

    # Compute SMA and update dataframe
    stock = calculate_SMA(stock, 50)
    stock = calculate_SMA(stock, 200)

    # Get the six_month_ago date: The first date shown on the graph
    six_month_ago = stock.index[-1] - pd.DateOffset(months = 6)
    six_month_ago = stock.index[stock.index > six_month_ago].min().strftime("%Y-%m-%d")
    
    # Plot stock price
    fig = px.line(stock.loc[stock.index > six_month_ago], 
                  x=stock.loc[stock.index > six_month_ago].index, 
                  y=['Close', "SMA 50", "SMA 200"], 
                  title=f"{ticker} Stock Price & SMAs (6 mo)")
    st.plotly_chart(fig)

    # Fetch news and summarize
    # news = fetch_financial_news(ticker)
    # summary = summarize_news(news)
    summary = 'Temporary Place Holder'
    st.subheader("Top Strengths & Weaknesses")
    st.write(summary)