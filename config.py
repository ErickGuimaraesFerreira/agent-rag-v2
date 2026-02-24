from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_api_key: str

    model_id: str = "gemini-2.0-flash"
    knowledge_dir: Path = Path("knowledge")
    lancedb_uri: str = "lancedb_data"
    table_name: str = "pdfs_local"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    model_id: str = "gemini-2.5-flash"
    knowledge_dir: Path = Path("knowledge")
    lancedb_uri: str = "lancedb_data"
    table_name: str = "pdfs_local"
    jwt_secret: str = "JWT_SECRET"  

    agentops_api_key: Optional[str] = None
    langchain_tracing_v2: str = "false"
    langchain_api_key: Optional[str] = ""
    langchain_project: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
