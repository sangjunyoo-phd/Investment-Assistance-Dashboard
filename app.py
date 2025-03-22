import streamlit as st
import ollama
import yfinance as yf

import fetch_data
import fetch_news
import llm_engine
from llm_engine import TickerEvaluation, TickerResponse

def to_checkmark(input:bool) -> str:
    return "✅" if input else "❌"

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
textbox1 = st.sidebar.text('Ticker')
textbox2 = st.sidebar.text('Company Name')
textbox3 = st.sidebar.text('')

if USER_QUERY:
    # Initialize the evaluation when a new query is passed
    TICKER_EVALUATION = TickerEvaluation(ticker_exists=False, they_are_same=False, feedback=None)

    # First attempt to query the company name and ticker
    with st.spinner("Guessing company name and ticker..."):
        TICKER_LLM = llm_engine.get_ticker_llm(USER_QUERY, MODEL_NAME)
    ticker = TICKER_LLM.ticker
    name = TICKER_LLM.name
    textbox_search_result.text(f"Search Result\n{name} ({ticker})")

    # Evaluate the first attempt
    with st.spinner('Evaluating LLM response...'):
        TICKER_EVALUATION = llm_engine.evaluate_ticker_llm(TICKER_LLM, USER_QUERY, MODEL_NAME)
    textbox1.text(f'Ticker {to_checkmark(TICKER_EVALUATION.ticker_exists)}')
    textbox2.text(f'Company Name {to_checkmark(TICKER_EVALUATION.they_are_same)}')
    if TICKER_EVALUATION.feedback:
        textbox3.text(TICKER_EVALUATION.feedback)

    while not (TICKER_EVALUATION.ticker_exists and TICKER_EVALUATION.they_are_same):
        # Another query with websearch + knowing prev answer was wrong
        with st.spinner("Correcting company name and ticker..."):
            TICKER_LLM = llm_engine.correct_ticker_llm(USER_QUERY, TICKER_LLM, TICKER_EVALUATION, MODEL_NAME)
        ticker = TICKER_LLM.ticker
        name = TICKER_LLM.ticker
        textbox_search_result.text(f"Search Result\n{name} ({ticker})")

        with st.spinner('Evaluating LLM response...'):
            TICKER_EVALUATION = llm_engine.evaluate_ticker_llm(TICKER_LLM, USER_QUERY, MODEL_NAME)
        textbox1.text(f'Ticker {to_checkmark(TICKER_EVALUATION.ticker_exists)}')
        textbox2.text(f'Company Name {to_checkmark(TICKER_EVALUATION.they_are_same)}')
        if TICKER_EVALUATION.feedback:
            textbox3.text(TICKER_EVALUATION.feedback)

    if TICKER_EVALUATION.ticker_exists and TICKER_EVALUATION.they_are_same:
        textbox3.text("")
        # When passed evaluation, update the search result with company name retrieved from the ticker
        name = yf.Ticker(ticker).info['longName']
        textbox_search_result.text(f"Search Result\n{name} ({ticker})")
        stock = fetch_data.fetch_stock_data(ticker)

        # Visualize Stock data
        fig = fetch_data.generate_figure(stock, name)
        st.plotly_chart(fig)

        # Fetch news and summarize
        with st.spinner("Fetching News..."):
            fetch_news_result = fetch_news.fetch_financial_news(name)
            articles = fetch_news.extract_contents(fetch_news_result)
        with st.spinner("Analyzing News..."):
            llm_analysis_result = llm_engine.analyze_news_llm(articles, MODEL_NAME)
        
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