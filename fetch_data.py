import yfinance as yf
import numpy as np
import pandas as pd

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