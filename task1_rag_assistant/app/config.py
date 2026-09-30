from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    llm_provider: str = "openai"

    openai_api_key: str = ""
    openai_model: str = "gpt-5-mini"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.7-flash"

    vllm_base_url: str = "http://localhost:8000/v1"
    vllm_model: str = "Qwen/Qwen3-0.6B"

    temperature: float = 0.2
    top_p: float = 0.9

    rag_top_k: int = 4
    chroma_dir: str = "./chroma_db"
    upload_dir: str = "./uploads"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
