# config.py

API_KEYS = {
    "openai": "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"
}

LLM_CONFIG = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": API_KEYS["openai"]
        }
    ]
}
