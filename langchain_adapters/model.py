from typing import Any
from core.config import get_settings


def get_langchain_model() -> Any:
    """Factory isolada para modelos usados pelo LangChain/LangGraph.

    Mantém a escolha do provider fora do grafo. O fluxo legado em ai/providers/
    continua intacto e pode coexistir com esta camada.
    """
    s = get_settings()
    provider = s.llm_provider.lower().strip()
    if provider == 'openai':
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=s.openai_model,
            api_key=s.openai_api_key,
        )
    if provider == 'gemini':
        from langchain_google_genai import ChatGoogleGenerativeAI
        if not s.gemini_model:
            raise ValueError('GEMINI_MODEL não configurado.')
        return ChatGoogleGenerativeAI(
            model=s.gemini_model,
            google_api_key=s.gemini_api_key,
        )
    raise ValueError(f'Provider LangChain não suportado: {s.llm_provider}')
