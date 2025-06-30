# main.py

import streamlit as st
from datetime import datetime

# Import agents and tasks
from agents import financial_assistant, research_assistant, writer, user_proxy_auto
from tasks import create_financial_task, create_research_task, writing_task

st.title("📈 Stock Financial Report Generator")

assets = st.text_input("Enter stock tickers:", value="AAPL, MSFT, TSLA")
start_analysis = st.button("Generate Report")

if start_analysis and assets.strip():
    tickers = [ticker.strip() for ticker in assets.split(",")]
    date_str = datetime.now().strftime("%Y-%m-%d")

    ft = create_financial_task(tickers, date_str)
    rt = create_research_task(tickers)

    with st.spinner("Agents working..."):
        chat_results = autogen.initiate_chats([
            {"sender": user_proxy_auto, "recipient": financial_assistant, "message": ft},
            {"sender": user_proxy_auto, "recipient": research_assistant, "message": rt},
            {"sender": critic, "recipient": writer, "message": writing_task},
        ])

        try:
            report_content = chat_results[-1].chat_history[-1]["content"]
            st.image("./coding/normalized_prices.png", caption="Normalized Price Chart")
            st.markdown(report_content)
        except Exception as e:
            st.error(f"Error generating report: {e}")
