from config import llm_config
import autogen

financial_assistant = autogen.AssistantAgent(
    name="Financial_assistant",
    llm_config=llm_config,
)

research_assistant = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
)

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="""You are a professional writer...""",
)
