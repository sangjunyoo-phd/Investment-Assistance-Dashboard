from duckduckgo_search import DDGS
from textblob import TextBlob

# Fetch news articles for a stock from DuckDuckGo
def fetch_financial_news(ticker):
    ddgs = DDGS()
    query = f"{ticker} stock analysis news"
    results = ddgs.text(query, max_results=10)
    return [result["body"] for result in results if "body" in result]

# Function to perform sentiment analysis on a news article using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns sentiment polarity (-1 to 1)

if __name__ == "__main__":
    ticker = 'META'
    fetch_result = fetch_financial_news(ticker)
    sentiment_analysis_result = []

    for result in fetch_result:
        analysis = analyze_sentiment(result)
        print(analysis)

    # print(analysis)