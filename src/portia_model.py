import os
from dotenv import load_dotenv
load_dotenv()

try:
    from portia import Config, LLMProvider, Portia, DefaultToolRegistry
    HAS_PORTIA = True
except Exception:
    HAS_PORTIA = False

from src.config import settings

def create_portia_runtime():
    if not HAS_PORTIA:
        return None
    if not settings.GEMINI_API_KEY:
        return None
    config = Config.from_default(
        llm_provider=LLMProvider.GOOGLE,
        default_model=settings.GEMINI_MODEL,
        google_api_key=settings.GEMINI_API_KEY.get_secret_value() if settings.GEMINI_API_KEY else None
    )
    portia = Portia(config=config, tools=DefaultToolRegistry(config=config))
    return portia

portia_runtime = create_portia_runtime()
