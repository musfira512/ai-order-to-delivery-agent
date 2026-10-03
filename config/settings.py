import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "groq/openai/gpt-oss-120b"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not configured.")
