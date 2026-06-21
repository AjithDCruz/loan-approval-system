import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
FASTAPI_HOST = "127.0.0.1"
FASTAPI_PORT = 8000

HAIKU_MODEL = "claude-3-5-haiku-20241022"
MAX_TOKENS = 1000
TEMPERATURE = 0.7

AGENTS = {
    "profile": {"timeout": 10, "model": HAIKU_MODEL},
    "financial": {"timeout": 10, "model": HAIKU_MODEL},
    "decision": {"timeout": 10, "model": HAIKU_MODEL},
    "compliance": {"timeout": 10, "model": HAIKU_MODEL}
}
