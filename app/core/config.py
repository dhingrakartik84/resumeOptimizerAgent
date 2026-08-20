from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Resume Agent System"

    environment: str = "local"

    log_level: str = "INFO"

    ollama_base_url: str = "http://localhost:11434"

    ollama_model: str = "llama3.2:1b"

    ollama_timeout_seconds: float = 500.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()