from duckduckgo_search import DDGS
from pydantic import BaseModel
import ollama
from typing import Literal

class NewsAnalysisStructure(BaseModel):
    events: list[str]
    strengths: list[str]
    weaknesses: list[str]
    grade: Literal['Strongly Recommend', 'Recommend', 'Neutral', 'Risky', 'Highly Risky']
    comment: str

# Fetch news articles for a stock using DuckDuckGo
def fetch_financial_news(name):
    results = DDGS().news(keywords=f"{name} financial report")
    return results

def extract_contents(results):
    # Extract list of articles to a single string
    articles = ''
    articles = articles.join([r['body'] for r in results])
    return articles

def analyze_news_llm(articles, model_name):
    news_analysis_prompt = """
    You are a helpful financial analyst. Your task is to read and analyze articles about a company,
    and extract three key events, strengths and weaknesses based on the article and your analysis for buy or sell decision of the company's stock or index fund's ETF.
    Grade the stock or ETF based on your analysis and provide a very short single-sentence comment.
    """

    response = ollama.chat(
        model = 'gemma3:4b', 
        messages =[{
            'role': 'system', 
            'content': news_analysis_prompt}, 
            {
                'role': 'user', 
                'content': articles
                }], 
        format = NewsAnalysisStructure.model_json_schema())
    return NewsAnalysisStructure.model_validate_json(response.message.content)

def list_to_markdown_bullet_points(list_of_string):
    markdown_output = ""
    for item in list_of_string:
        markdown_output += f"* {item}\n"
    return markdown_output