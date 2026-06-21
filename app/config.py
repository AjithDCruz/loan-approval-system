import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
FASTAPI_HOST = "127.0.0.1"
FASTAPI_PORT = 8000

HAIKU_MODEL = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
MAX_TOKENS = 1000
TEMPERATURE = 0.7

AGENTS = {
    "profile": {"timeout": 10, "model": HAIKU_MODEL},
    "financial": {"timeout": 10, "model": HAIKU_MODEL},
    "decision": {"timeout": 10, "model": HAIKU_MODEL},
    "compliance": {"timeout": 10, "model": HAIKU_MODEL}
}
