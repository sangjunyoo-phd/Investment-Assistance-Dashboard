import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker:str) -> pd.DataFrame:
    """
    Fetch the 6month stock data of single ticker from yahoo finance.
    """
    stock = yf.download(ticker, period="18mo")
    stock.columns = stock.columns.droplevel(1) # Make the multi-index columns to a single level column; compatible with plotly
    return stock

def calculate_technical_indicators(stock: pd.DataFrame) -> pd.DataFrame:
    stock["SMA_50"] = stock["Close"].rolling(window=50).mean()
    stock["SMA_200"] = stock["Close"].rolling(window=200).mean()
    # return stock

if __name__ == "__main__":
    ticker = 'NVDA'
    stock = fetch_stock_data(ticker)
    stock = calculate_technical_indicators(stock)

    stock.head()