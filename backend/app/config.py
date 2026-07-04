import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Security Governance Platform"
    app_version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")

    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/ai_security_db"
    )
    database_echo: bool = environment == "development"

    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    azure_subscription_id: str = os.getenv("AZURE_SUBSCRIPTION_ID", "")
    azure_resource_group: str = os.getenv("AZURE_RESOURCE_GROUP", "")
    azure_tenant_id: str = os.getenv("AZURE_TENANT_ID", "")
    azure_client_id: str = os.getenv("AZURE_CLIENT_ID", "")
    azure_client_secret: str = os.getenv("AZURE_CLIENT_SECRET", "")
    azure_keyvault_url: str = os.getenv("AZURE_KEYVAULT_URL", "")

    jwt_secret: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 24

    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    api_v1_str: str = "/api/v1"

    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
