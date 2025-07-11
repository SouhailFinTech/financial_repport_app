# main.py
import autogen 

# main.py

import streamlit as st
from datetime import datetime

# Import agents from agents.py
from agents import financial_assistant, research_assistant, writer, critic, user_proxy_auto

# Import tasks
from tasks import create_financial_task, create_research_task, writing_task

# Streamlit UI
st.title("📈 Stock Financial Report Generator")

assets = st.text_input("Enter stock tickers:", value="AAPL, MSFT, TSLA")
start_analysis = st.button("Generate Report")

if start_analysis and assets.strip():
    tickers = [ticker.strip() for ticker in assets.split(",")]
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Create dynamic tasks
    financial_task = create_financial_task(tickers, date_str)
    research_task = create_research_task(tickers)

    with st.spinner("Agents working on the analysis..."):
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
