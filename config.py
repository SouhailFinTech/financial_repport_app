import autogen
import openai

# Use Phi-3 via LM Studio
llm_config = {
    "model": "microsoft/phi-3-mini-4k-instruct-gguf",
    "api_key": "no-key-needed",
    "base_url": "http://localhost:1234/v1",
    "temperature": 0.7,
    "max_tokens": 2048,
}
