from duckduckgo_search import DDGS

# Fetch news articles for a stock using DuckDuckGo
def fetch_financial_news(name):
    results = DDGS().news(keywords=f"{name} financial report", max_results=10)
    return results

def extract_contents(results):
    # Extract list of articles to a single string
    articles = ''
    articles = articles.join([r['body'] for r in results])
    return articles

def list_to_markdown_bullet_points(list_of_string):
    markdown_output = ""
    for item in list_of_string:
        markdown_output += f"* {item}\n"
    return markdown_output