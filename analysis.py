import requests
from textblob import TextBlob  # Sentiment analysis tool
from duckduckgo_search import DDGS  # DuckDuckGo for web search
import yfinance as yf
import matplotlib.pyplot as plt

# Function to perform sentiment analysis on a news article using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns sentiment polarity (-1 to 1)

# Fetch news articles for a stock from DuckDuckGo
def fetch_financial_news(ticker):
    ddgs = DDGS()
    query = f"{ticker} stock analysis news"
    results = ddgs.text(query, max_results=10)
    return [r["body"] for r in results if "body" in r]

# Use the LLM to summarize strengths and weaknesses
def summarize_news_with_llm(news_articles):
    # Here you would call your LLM (OpenAI or local model) to summarize the strengths and weaknesses
    # For example, this could use the OpenAI API or LM Studio locally:
    summarized = "\n".join(news_articles[:3])  # Dummy summarization for now
    return summarized

# Fetch stock data using yfinance
def get_stock_data(ticker):
    stock = yf.download(ticker, period="6mo")
    return stock

# # Compute technical indicators (SMA, RSI) with pandas_ta
# def compute_technical_indicators(stock):
#     stock["SMA_50"] = ta.sma(stock["Close"], length=50)
#     stock["SMA_200"] = ta.sma(stock["Close"], length=200)
#     stock["RSI"] = ta.rsi(stock["Close"], length=14)
#     return stock


if __name__ == '__main__':
    # Main workflow
    ticker = "NVDA"  # Example ticker
    news_articles = fetch_financial_news(ticker)
    print('============== News Articles ==============')
    print(news_articles)
    print('===========================================\n')
    sentiments = [analyze_sentiment(article) for article in news_articles]
    print("Sentiments:", sentiments)

    # # Summarize the news (Strengths/Weaknesses)
    # summary = summarize_news_with_llm(news_articles)
    # print("\nLLM Summary of Strengths/Weaknesses:")
    # print(summary)

    # # Fetch stock data and compute technical indicators
    # stock = get_stock_data(ticker)
    # stock = compute_technical_indicators(stock)

    # # Plot stock price and indicators
    # plt.figure(figsize=(12,6))
    # plt.plot(stock["Close"], label="Stock Price")
    # plt.plot(stock["SMA_50"], label="50-day SMA", linestyle="--")
    # plt.plot(stock["SMA_200"], label="200-day SMA", linestyle="--")
    # plt.legend()
    # plt.show()

    # # Combine sentiment analysis with Buy/Sell signal based on sentiment
    # average_sentiment = sum(sentiments) / len(sentiments)
    # if average_sentiment > 0.5:
    #     print("\nRecommendation: Buy (Positive sentiment across news)")
    # elif average_sentiment < -0.5:
    #     print("\nRecommendation: Sell (Negative sentiment across news)")
    # else:
    #     print("\nRecommendation: Hold (Neutral sentiment across news)")

    # # Combine qualitative insights from LLM with technical analysis
    # if stock["RSI"].iloc[-1] < 30:
    #     print("\nTechnical Signal: Buy (RSI under 30 suggests oversold condition)")
    # elif stock["RSI"].iloc[-1] > 70:
    #     print("\nTechnical Signal: Sell (RSI over 70 suggests overbought condition)")
