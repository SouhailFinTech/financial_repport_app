# agents.py

from config import llm_config
import autogen

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

legal_reviewer = autogen.AssistantAgent(
    name="Legal_Reviewer",
    llm_config=llm_config,
    system_message="Ensure content is legally compliant.",
)

consistency_reviewer = autogen.AssistantAgent(
    name="Consistency_reviewer",
    llm_config=llm_config,
    system_message="Ensure content consistency throughout the report.",
)

textalignment_reviewer = autogen.AssistantAgent(
    name="Text_Alignment_Reviewer",
    llm_config=llm_config,
    system_message="Ensure text aligns with data presented.",
)

completion_reviewer = autogen.AssistantAgent(
    name="Completion_Reviewer",
    llm_config=llm_config,
    system_message="Check that all elements are included.",
)

meta_reviewer = autogen.AssistantAgent(
    name="Meta_Reviewer",
    llm_config=llm_config,
    system_message="Aggregate feedback from all reviewers and give final suggestions.",
)

def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content.\n\n{recipient.chat_messages_for_summary(sender)[-1]['content']}'''

review_chats = [
    {"recipient": legal_reviewer, "message": reflection_message, "summary_method": "reflection_with_llm"},
    {"recipient": textalignment_reviewer, "message": reflection_message, "summary_method": "reflection_with_llm"},
    {"recipient": consistency_reviewer, "message": reflection_message, "summary_method": "reflection_with_llm"},
    {"recipient": completion_reviewer, "message": reflection_message, "summary_method": "reflection_with_llm"},
    {"recipient": meta_reviewer, "message": "Aggregate feedback.", "max_turns": 1},
]

critic.register_nested_chats(review_chats, trigger=writer)

# User Proxy Agent
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
