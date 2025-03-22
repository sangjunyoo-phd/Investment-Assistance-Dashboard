import ollama
from pydantic import BaseModel
import yfinance as yf
from duckduckgo_search import DDGS

# Define Structured Output
class TickerResponse(BaseModel):
    name: str
    ticker: str

class TickerEvaluation(BaseModel):
    ticker_exists: bool
    they_are_same:bool

"""
Evaluation of TickerResponse; check

"""


def get_ticker_llm(user_query: str, 
                   model_name: str) -> TickerResponse:
    response = ollama.chat(
          model = model_name,
          messages = [{
                "role": "user", 
                "content": f"What is the company or index name and yahoo finance ticker for this company? {user_query}"
                }],
          format = TickerResponse.model_json_schema())
    structured_response = TickerResponse.model_validate_json(response.message.content)
    print(f"Name: {structured_response.name}\tTicker: {structured_response.ticker}")
    return structured_response

def search_ticker_llm(user_query:str,
                      prev_response:TickerResponse,
                      model_name:str) -> TickerResponse:
    search_results = DDGS().text(user_query, max_results = 5)
    titles = ""
    for result in search_results:
        titles += result["title"] + " "

    response = ollama.chat(
        model = model_name,
        messages = [{
            "role": "user",
            "content": f"""From the following articles, extract the name of the most relevant company or index and its yahoo finance ticker. 
                        Your last incorrect answer was: company name of {prev_response.name} and ticker of {prev_response.ticker}
                        The articles: {titles}

                        What is your best guess about the company's name and its ticker?"""
        }],
        format = TickerResponse.model_json_schema()
    )

    structured_response = TickerResponse.model_validate_json(response.message.content)
    print(f"Name: {structured_response.name}\tTicker: {structured_response.ticker}")
    return structured_response

def evaluate_ticker_llm(llm_response: TickerResponse,
                        user_query:str, 
                        model_name:str) -> bool:
    ticker, name = llm_response.ticker, llm_response.name
    try:
        name_from_ticker = yf.Ticker(ticker).info['longName']
    except:
        # ticker is unavailable; probably hallucinate the ticker
        return TickerEvaluation(ticker_exists=False, they_are_same=False)
    else:
        # When no error has encountered; ticker exists
        evaluation = ollama.chat(
            model = model_name,
            messages = [
                {"role": "user",
                "content": f"You passed the ticker existence test. Do these two mean the same company? {name} and {name_from_ticker}"}
            ],
            format = TickerEvaluation.model_json_schema()
        )

        return TickerEvaluation.model_validate_json(evaluation.message.content)
    
if __name__ == "__main__":
    # wrong_name_wrong_ticker = TickerResponse(name = 'Imaginary Company', 
    #                                          ticker = 'Thissurelycannotexist')
    
    # right_name_wrong_ticker = TickerResponse(name = 'Google', 
    #                                          ticker = 'NVDA')
    
    # wrong_name_right_ticker = TickerResponse(name = 'Tesla',
    #                                          ticker = 'GOOG')
    
    # input_ticker = wrong_name_wrong_ticker
    # user_query = 'Google'
    # print('UserQuery:', user_query)
    # print('Input:', input_ticker)
        
    # evaluation_output = evaluate_ticker_llm(
    #     input_ticker,
    #     user_query = user_query,
    #     model_name = 'gemma3:1b')
    
    # print('Output:', evaluation_output)
    results = search_ticker_llm('pixel phone', None, None)
    titles = ''
    for r in results:
        titles += r['title'] + " "

    print(titles)