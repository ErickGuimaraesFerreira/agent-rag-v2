from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # O Pydantic procura essas variáveis no ambiente ou no arquivo .env
    google_api_key: str
    
    # Valores padrão caso não estejam no .env
    model_id: str = "gemini-2.0-flash"
    knowledge_dir: Path = Path("knowledge")
    lancedb_uri: str = "lancedb_data"
    table_name: str = "pdfs_local"
    
    # Configuração para ler do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instância global para ser usada no projeto
settings = Settings()
