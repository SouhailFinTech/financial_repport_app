import autogen

financial_assistant = autogen.AssistantAgent(
    name="Financial_assistant",
    llm_config=llm_config,
    system_message="You are a financial analyst. Analyze stock prices, ratios, and performance.",
)

research_assistant = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
    system_message="You are a researcher. Find relevant news headlines and market events.",
)

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="""You are a professional writer, known for your insightful and engaging finance reports.
    Transform complex concepts into compelling narratives. Include all metrics provided.
    Only return the final markdown report."""
)
