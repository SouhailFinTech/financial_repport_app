   # main.py

import autogen
import openai
import streamlit as st
from datetime import datetime

# Local LLM Config (Ollama)
llm_config = {
    "model": "llama3",
    "api_key": "no-key-needed",
    "base_url": "http://localhost:11434/v1",
    "temperature": 0.7,
    "max_tokens": 8192,
}

# Define Agents
financial_assistant = autogen.AssistantAgent(
    name="Financial_assistant",
    llm_config=llm_config,
    system_message="You are a financial analyst. Analyze stock prices and ratios.",
)

research_assistant = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
    system_message="You are a researcher. Find relevant news headlines and market events.",
)

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="""You are a professional writer.
    Transform complex concepts into compelling narratives.
    Include all metrics provided.
    Return only the markdown report, no extra text."""
)

critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="You are a critic. Provide feedback.",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
)

user_proxy_auto = autogen.UserProxyAgent(
    name="User_Proxy_Auto",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "coding",
        "use_docker": False
    },
)

# Streamlit UI
st.title("📈 Stock Financial Report Generator")

assets = st.text_input("Enter stock tickers:", value="AAPL, MSFT, TSLA")
hit_button = st.button("Start Analysis")

if hit_button and assets.strip():
    tickers = [ticker.strip() for ticker in assets.split(",")]
    date_str = datetime.now().strftime("%Y-%m-%d")

    financial_task = f"""
    Today is {date_str}.
    What are the current stock prices of {', '.join(tickers)}, and how is the performance over the past 6 months?
    Start by retrieving the full name of each stock and use it for all future requests.
    Prepare a figure of the normalized price of these stocks and save it to normalized_prices.png.
    Include information about:
    - P/E ratio
    - Dividends
    - Price to book
    - ROE
    Analyze the correlation between the stocks.
    Do not use a solution that requires an API key.
    If some data does not make sense, such as a price of 0, re-query."""

    research_task = f"""
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

    with st.spinner("Agents working..."):
        chat_results = autogen.initiate_chats([
            {
                "sender": user_proxy_auto,
                "recipient": financial_assistant,
                "message": financial_task,
                "summary_method": "reflection_with_llm",
                "carryover": "Wait for confirmation before termination."
            },
            {
                "sender": user_proxy_auto,
                "recipient": research_assistant,
                "message": research_task,
                "summary_method": "reflection_with_llm",
                "carryover": "Wait for confirmation before termination."
            },
            {
                "sender": critic,
                "recipient": writer,
                "message": writing_task,
                "max_turns": 2,
                "summary_method": "last_msg",
            }
        ])

        try:
            report_content = chat_results[-1].chat_history[-1]["content"]
            st.image("./coding/normalized_prices.png", caption="Normalized Price Chart")
            st.markdown(report_content)
        except Exception as e:
            st.error(f"Error generating report: {e}")
