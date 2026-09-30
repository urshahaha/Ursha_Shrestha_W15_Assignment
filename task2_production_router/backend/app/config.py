from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    router_model_dir: str = "./model/week14_distilbert_router"
    router_confidence_threshold: float = 0.45
    router_max_length: int = 128

    max_concurrent_inference: int = 4
    cache_ttl_seconds: int = 300

    openai_api_key: str = ""
    fallback_openai_model: str = "gpt-5.6-luna"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
