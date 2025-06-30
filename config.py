import autogen
import streamlit as st
import openai

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
    system_message="You are a financial analyst. Analyze stock prices and ratios."
)

research_assistant = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
    system_message="You are a researcher. Find relevant news headlines and market events."
)

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="""You are a professional writer. Create compelling finance reports."""
)

# Critic and Reviewers (as in your original code)
# [Paste them here after defining llm_config]
