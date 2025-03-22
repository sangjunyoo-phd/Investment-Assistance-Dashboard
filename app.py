import pandas as pd
import streamlit as st
import plotly.express as px
import ollama
import yfinance as yf

import fetch_data
import fetch_news
import llm_engine
from llm_engine import TickerEvaluation, TickerResponse

st.title("Investment Assistance")

# Read the list of models with ollama
model_list = list()
for model in ollama.list().models:
    model_list.append(model.model)

# Set the model from the list
MODEL_NAME = st.sidebar.selectbox("LLM Model", options = model_list)

# User Query input
USER_QUERY = st.sidebar.text_input("Search")

# Initialize textboxes
textbox_search_result = st.sidebar.text(f"Search Result\n  ")
textbox1 = st.sidebar.text('Ticker Exists: ')
textbox2 = st.sidebar.text('Correct Inference: ')

if USER_QUERY:
    # Initialize the evaluation when a new query is passed
    TICKER_EVALUATION = TickerEvaluation(ticker_exists=False, they_are_same=False)

    # First attempt to query the company name and ticker
    TICKER_LLM = llm_engine.get_ticker_llm(USER_QUERY, MODEL_NAME)
    ticker = TICKER_LLM.ticker
    name = yf.Ticker(ticker).info['longName']
    textbox_search_result.text(f"Search Result\n{name} ({ticker})")

    # Evaluate the first attempt
    TICKER_EVALUATION = llm_engine.evaluate_ticker_llm(TICKER_LLM, USER_QUERY, MODEL_NAME)
    textbox1.text(f'Ticker Exists: {TICKER_EVALUATION.ticker_exists}')
    textbox2.text(f'Correct Inference: {TICKER_EVALUATION.they_are_same}')

    while not (TICKER_EVALUATION.ticker_exists and TICKER_EVALUATION.they_are_same):
        # Another query with websearch + knowing prev answer was wrong
        TICKER_LLM = llm_engine.search_ticker_llm(USER_QUERY, TICKER_LLM, MODEL_NAME)
        ticker = TICKER_LLM.ticker
        name = yf.Ticker(ticker).info['longName']
        textbox_search_result.text(f"Search Result\n{name} ({ticker})")

        TICKER_EVALUATION = llm_engine.evaluate_ticker_llm(TICKER_LLM, USER_QUERY, MODEL_NAME)
        textbox1.text(f'Ticker Exists: {TICKER_EVALUATION.ticker_exists}')
        textbox2.text(f'Correct Inference: {TICKER_EVALUATION.they_are_same}')

    if TICKER_EVALUATION.ticker_exists and TICKER_EVALUATION.they_are_same:
        stock = fetch_data.fetch_stock_data(ticker)

        # Compute SMA and update dataframe
        stock = fetch_data.calculate_SMA(stock, 50)
        stock = fetch_data.calculate_SMA(stock, 200)

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
        st.plotly_chart(fig)

        # Fetch news and summarize
        fetch_news_result = fetch_news.fetch_financial_news(name)
        articles = fetch_news.extract_contents(fetch_news_result)
        llm_analysis_result = fetch_news.analyze_news_llm(articles, MODEL_NAME)
        
        # Parse the Analysis
        events = llm_analysis_result.events
        strengths = llm_analysis_result.strengths
        weaknesses = llm_analysis_result.weaknesses
        grade = llm_analysis_result.grade
        comment = llm_analysis_result.comment

        # Convert to markdown
        event_markdown = fetch_news.list_to_markdown_bullet_points(events)
        strength_markdown = fetch_news.list_to_markdown_bullet_points(strengths)
        weakness_markdown = fetch_news.list_to_markdown_bullet_points(weaknesses)

        st.subheader(f'{grade}')
        st.text(comment)
        st.subheader('Key Events')
        st.markdown(event_markdown)
        col1, col2 = st.columns(2)
        col1.subheader('Strengths')
        col1.markdown(strength_markdown)
        col2.subheader('Weaknesses')
        col2.markdown(weakness_markdown)