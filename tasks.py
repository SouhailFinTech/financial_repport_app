# tasks.py

from datetime import datetime

DATE_STR = datetime.now().strftime("%Y-%m-%d")

# === Financial Task ===
financial_task = f"""
Today is {DATE_STR}.
What are the current stock prices of {{tickers}}, and how is the performance over the past 6 months?
Start by retrieving the full name of each stock and use it for all future requests.
Prepare a figure of the normalized price of these stocks and save it to a file named normalized_prices.png.
Include information about:
- P/E ratio
- Dividends
- Price to book
- ROE
Analyze the correlation between the stocks.
Do not use a solution that requires an API key.
If some of the data does not make sense, such as a price of 0, change the query and re-try.
"""

# === Research Task ===
research_task = f"""
Investigate possible reasons for the stock performance leveraging market news headlines.
Retrieve news headlines for {{tickers}}.
Be precise but avoid vague or irrelevant events.
"""

# === Writing Task ===
writing_task = """
Develop an engaging financial report using all information provided.
Include the normalized_prices.png figure.
Create a table comparing all the fundamental ratios and data.
Provide comments and descriptions of all the fundamental ratios and data.
Compare the stocks, consider their correlation and risks.
Provide a summary of the recent news about each stock.
Ensure you comment and summarize the news headlines for each stock.
Provide connections between the news headlines and the fundamental ratios.
Provide an analysis of possible future scenarios.
"""