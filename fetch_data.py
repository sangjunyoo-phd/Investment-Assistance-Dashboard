import yfinance as yf
import numpy as np
import pandas as pd
import plotly.express as px

def fetch_stock_data(ticker:str) -> pd.DataFrame:
    """
    Fetch the stock data of a ticker from yahoo finance.

    Args:
        ticker: A stock ticker string symbol
    
    Returns:
        Stock Data
    """
    stock = yf.download(ticker, period="18mo")
    stock.columns = stock.columns.droplevel(1) # Make the multi-index columns to a single level column; compatible with plotly
    return stock

def calculate_SMA(stock:pd.DataFrame, window:int) -> pd.DataFrame:
    """
    Calculate the SMA (Top Hat Filter) with a given window size of the past 6 months.
    """
    # Get the six_month_ago date: The first date shown on the graph
    six_month_ago = stock.index[-1] - pd.DateOffset(months = 6)
    six_month_ago = stock.index[stock.index > six_month_ago].min().strftime("%Y-%m-%d")

    # Fetch the right amount of data for SMA calculation
    six_month_ago_index = np.where(stock.index == six_month_ago)[0][0]
    stock_for_SMA = stock.iloc[six_month_ago_index-window:].copy()

    SMA = stock_for_SMA["Close"].rolling(window=window).mean()
    stock[f'SMA {window}'] = SMA
    return stock

def generate_figure(stock: pd.DataFrame,
                    name: str):
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
                title=f"{name} Stock Price & SMAs (6 mo)")
    fig.update_layout(
        xaxis_title='',
        yaxis_title='Value ($)'
    )
    return fig