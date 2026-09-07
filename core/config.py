from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    app_name: str = 'AI Lab'
    app_env: str = 'development'
    app_host: str = '0.0.0.0'
    app_port: int = 8010
    llm_provider: str = 'openai'
    openai_api_key: str = ''
    openai_model: str = 'gpt-5.6-luna'
    openai_max_output_tokens: int = 1200
    gemini_api_key: str = ''
    gemini_model: str = ''
    mysql_host: str = '127.0.0.1'
    mysql_port: int = 3306
    mysql_database: str = ''
    mysql_user: str = ''
    mysql_password: str = ''
    mysql_pool_size: int = 5
    redis_url: str = 'redis://127.0.0.1:6379/0'
    mcp_server_name: str = 'ai-lab-mcp'
    max_tool_iterations: int = 8
    rag_default_limit: int = 20
    langgraph_memory_backend: str = 'memory'
    langgraph_recursion_limit: int = 30

@lru_cache
def get_settings() -> Settings:
    return Settings()
