# agents.py

import autogen
from config import llm_config

# Define Agents

# Financial Analyst Agent
financial_assistant = autogen.AssistantAgent(
    name="Financial_assistant",
    llm_config=llm_config,
)

# Researcher Agent
research_assistant = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
)

# Writer Agent
writer = autogen.AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="""
    You are a professional writer, known for your insightful and engaging finance reports.
    Transform complex concepts into compelling narratives.
    Include all metrics provided to you as context in your analysis.
    Only answer with the financial report written in markdown directly, do not include a markdown language block indicator.
    Only return your final work without additional comments.
    """
)

# Critic Agent
critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="You are a critic. You review the work of the writer and provide constructive feedback.",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
)

# Legal Reviewer
legal_reviewer = autogen.AssistantAgent(
    name="Legal_Reviewer",
    llm_config=llm_config,
    system_message="""
    You are a legal reviewer, known for your ability to ensure that content is legally compliant 
    and free from any potential legal issues.
    Make sure your suggestion is concise (within 3 bullet points), concrete, and to the point.
    Begin the review by stating your role.
    """
)

# Consistency Reviewer
consistency_reviewer = autogen.AssistantAgent(
    name="Consistency_reviewer",
    llm_config=llm_config,
    system_message="""
    You are a consistency reviewer, known for your ability to ensure that the written content is consistent throughout the report.
    Refer numbers and data in the report to determine which version should be chosen in case of contradictions.
    Make sure your suggestion is concise (within 3 bullet points), concrete, and to the point.
    Begin the review by stating your role.
    """
)

# Text Alignment Reviewer
textalignment_reviewer = autogen.AssistantAgent(
    name="Text_Alignment_Reviewer",
    llm_config=llm_config,
    system_message="""
    You are a text data alignment reviewer, known for your ability to ensure that the written content aligns with the numbers/data presented.
    You must ensure that the text clearly describes the numbers provided in the text without contradictions.
    Make sure your suggestion is concise (within 3 bullet points), concrete, and to the point.
    Begin the review by stating your role.
    """
)

# Completion Reviewer
completion_reviewer = autogen.AssistantAgent(
    name="Completion_Reviewer",
    llm_config=llm_config,
    system_message="""
    You are a content completion reviewer, known for your ability to check that financial reports contain all the required elements.
    You always verify that the report contains:
    - A news report about each asset
    - A description of the different ratios and prices
    - A description of possible future scenarios
    - A table comparing fundamental ratios and at least one figure
    Make sure your suggestion is concise (within 3 bullet points), concrete, and to the point.
    Begin the review by stating your role.
    """
)

# Meta Reviewer
meta_reviewer = autogen.AssistantAgent(
    name="Meta_Reviewer",
    llm_config=llm_config,
    system_message="""
    You are a meta reviewer, you aggregate and review the work of other reviewers and give a final suggestion on the content.
    """
)

# Reflection Message Function
def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content.\n\n{recipient.chat_messages_for_summary(sender)[-1]['content']}'''

# Nested Review Chats
review_chats = [
    {
        "recipient": legal_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return review into a JSON object only: {'Reviewer':'','Review':''}."
        },
        "max_turns": 1
    },
    {
        "recipient": textalignment_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return review into a JSON object only: {'reviewer':'','review':''}"
        },
        "max_turns": 1
    },
    {
        "recipient": consistency_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return review into a JSON object only: {'reviewer':'','review':''}"
        },
        "max_turns": 1
    },
    {
        "recipient": completion_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return review into a JSON object only: {'reviewer':'','review':''}"
        },
        "max_turns": 1
    },
    {
        "recipient": meta_reviewer,
        "message": "Aggregate feedback from all reviewers and give final suggestions on the writing.",
        "max_turns": 1
    }
]

# Register nested chats under critic
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
