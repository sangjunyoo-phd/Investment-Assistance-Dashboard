import yfinance as yf
import ollama
import pandas as pd
from pydantic import BaseModel

# Define Structured Output
class TickerResponse(BaseModel):
    name: str
    ticker: str

class TickerEvaluation(BaseModel):
    they_are_same:bool

def get_ticker_llm(user_query: str, 
                   model_name: str) -> TickerResponse:
    response = ollama.chat(
        model = model_name,
        messages = [
            {
                "role": "user",
                "content": f"What is the company or index name and yahoo finance ticker for this company? {user_query}"
            }
        ],
        format = TickerResponse.model_json_schema()
    )

    return TickerResponse.model_validate_json(response.message.content)

def evaluate_ticker_llm(llm_response: TickerResponse,
                        model_name:str) -> bool:
    ticker, name = llm_response.ticker, llm_response.name
    name_from_ticker = yf.Ticker(ticker).info['longName']

    evaluation = ollama.chat(
        model = model_name,
        messages = [
            {"role": "user",
            "content": f"Do these two mean the same company? {name} and {name_from_ticker}"}
        ],
        format = TickerEvaluation.model_json_schema()
    )

    return TickerEvaluation.model_validate_json(evaluation.message.content).they_are_same


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