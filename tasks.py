# tasks.py
from datetime import datetime

def create_financial_task(tickers, date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    return f"""Today is {date_str}.
What are the current stock prices of {', '.join(tickers)}, and how is the performance over the past 6 months in terms of percentage change?
Start by retrieving the full name of each stock and use it for all future requests.
Prepare a figure of the normalized price of these stocks and save it to a file named normalized_prices.png. Include information about, if applicable:
- P/E ratio
- Forward P/E
- Dividends
- Price to book
- Debt/Equity
- ROE
Analyze the correlation between the stocks.
Do not use a solution that requires an API key.
If some of the data does not make sense, such as a price of 0, change the query and re-try."""

def create_research_task(tickers):
    return f"""
Investigate possible reasons for the stock performance leveraging market news headlines.
Retrieve news headlines for {', '.join(tickers)}.
Be precise but avoid vague or irrelevant events."""

writing_task = """
Develop an engaging financial report using all information provided.
Include the normalized_prices.png figure.
Create a table comparing all the fundamental ratios and data.
Provide comments and descriptions of all the fundamental ratios and data.
Compare the stocks, consider their correlation and risks.
Provide a summary of the recent news about each stock.
Ensure you comment and summarize the news headlines for each stock.
Provide connections between the news headlines and the fundamental ratios.
Provide an analysis of possible future scenarios."""
