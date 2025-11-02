from typing import Any, Dict

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # 設定
    debugpy_port: int = 9000  # デバッグ用ポート

    # OpenAI
    openai_base_url: str = ""
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-2024-08-06"
    openai_embedding_model: str = "text-embedding-3-large"
    openai_max_retries: int = 3

    # OpenSearch
    opensearch_host: str = "opensearch"
    opensearch_port: int = 9200
    opensearch_user: str = "admin"
    opensearch_password: str = "secret"
    opensearch_base_url: str = "http://admin:secret@opensearch:9200"
    opensearch_default_index_name: str = "default_index"
