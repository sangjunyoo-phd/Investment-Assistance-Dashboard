import ollama
from pydantic import BaseModel
import yfinance as yf
from duckduckgo_search import DDGS

# Define Structured Output
class TickerResponse(BaseModel):
    name: str
    ticker: str

class TickerEvaluation(BaseModel):
    ticker_exists:bool
    they_are_same:bool
    feedback: str|None


def get_ticker_llm(user_query: str, 
                   model_name: str) -> TickerResponse:
    # Do the first guess based on user query
    response = ollama.chat(
          model = model_name,
          messages = [
              {
                  "role": "system", 
                  "content": "You are a helpful financial assistance. Your task is to make a best guess about company name and its yahoo finance ticker."},
              {
                  "role": "user", 
                  "content": f"What is the company or index name and yahoo finance ticker for this company? {user_query}"}],
          format = TickerResponse.model_json_schema())
    
    structured_response = TickerResponse.model_validate_json(response.message.content)
    print(f"FirstInference\nName: {structured_response.name}\tTicker: {structured_response.ticker}")
    return structured_response

def correct_ticker_llm(user_query:str,
                       prev_response:TickerResponse,
                       prev_evaluation:TickerEvaluation,
                       model_name:str) -> TickerResponse:
    search_results = DDGS().text(user_query, max_results = 5)
    titles = ""
    for result in search_results:
        titles += result["title"] + " "

    system_prompt = f"""
        Your role is to correct the incorrect guess on company name and its yahoo ticker. They may be wrong because
        1. the inference on company name is incorrect.
        2. the company name is correct but yahoo ticker of the company is incorrect.

        You will have at least two more information to make a better inference.
        1. The previous incorrect inference on company name and its ticker. You need to change at least one of them.
        2. Web search result about the user query.
        3. Feedback from another ticker-evaluation llm agent.
    """

    user_prompt = f"""
        From the websearch result below extract the most relevant company (or index) name and its yahoo finance ticker.
        Incorrect company name: {prev_response.name} and ticker: {prev_response.ticker}
        Web Search Results: {titles}\n
    """

    if prev_evaluation.feedback:
        # if there is a feedback, include that into the user_prompt
        user_prompt += f"\nFeedback from another agent: {prev_evaluation.feedback}"
    
    response = ollama.chat(
        model = model_name,
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
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
        return TickerEvaluation(ticker_exists=False, they_are_same=False, 
                                feedback="Ticker is not found from the yahoo finance. Correct the ticker.")
    else:
        # When no error has encountered; ticker exists
        evaluation = ollama.chat(
            model = model_name,
            messages = [
                {
                    "role": "system",
                    "content": "Your role is to evaluate the other LLM's respond about company name and its yahoo finance ticker and provide a feedback."
                },
                {
                    "role": "user",
                    "content": f"""You passed the ticker existence test. 
                                LLM-guessed company name is {name}, LLM-guessed ticker of the company is {ticker}.
                                The company name retrieved from the LLM guessed ticker with yahoo finance is {name_from_ticker}.
                                They may not match extactly the same, but do they mean the same company?
                                If they mean differenc companies, provide a brief and concise feed back on what made this wrong.
                                """
                }],
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
    
    a = None

    if a:
        print('AA')
    else:
        print('AAA')