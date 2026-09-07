from ai.providers.base import LLMProvider
from ai.providers.openai_provider import OpenAIProvider
from ai.providers.gemini_provider import GeminiProvider
from ai.providers.local_provider import LocalProvider
from core.config import get_settings

def get_llm_provider() -> LLMProvider:
    provider = get_settings().llm_provider.lower()
    if provider == 'openai': return OpenAIProvider()
    if provider == 'gemini': return GeminiProvider()
    if provider == 'local': return LocalProvider()
    raise ValueError(f'LLM provider não suportado: {provider}')
