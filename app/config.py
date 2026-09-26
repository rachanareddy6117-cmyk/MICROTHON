import os
from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    APP_NAME: str = "PQC-Migrate"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    # Database (PostgreSQL with automatic fallback to async SQLite for local/test use)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./pqc_migrate.db")
    DATABASE_SYNC_URL: str = os.getenv("DATABASE_SYNC_URL", "sqlite:///./pqc_migrate.db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "pqc-migrate-master-secret-key-replace-in-prod-2026")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # KMS & Envelope Encryption
    KMS_PROVIDER: str = os.getenv("KMS_PROVIDER", "local_simulated")  # 'aws', 'gcp', 'vault', 'local_simulated'
    KMS_MASTER_KEY_ID: str = os.getenv("KMS_MASTER_KEY_ID", "pqc-master-kek-01")
    KMS_MASTER_KEY_HEX: str = os.getenv("KMS_MASTER_KEY_HEX", "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")
    
    # Sandbox
    SANDBOX_CONTAINER_IMAGE: str = "pqc-migrate-sandbox:latest"
    SANDBOX_TIMEOUT_SECONDS: int = 120
    SANDBOX_MAX_MEMORY_MB: int = 512
    SANDBOX_TEMP_DIR: str = os.path.abspath("./sandbox_storage")
    
    # Ingestion limits
    MAX_UPLOAD_SIZE_BYTES: int = 50 * 1024 * 1024  # 50MB
    MAX_UNCOMPRESSED_ZIP_BYTES: int = 250 * 1024 * 1024  # 250MB
    MAX_ZIP_RATIO: int = 100  # Zip bomb prevention
    
    class Config:
        env_file = ".env"

settings = Settings()
