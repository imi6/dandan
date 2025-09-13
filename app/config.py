"""Application configuration"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import json


class Settings(BaseSettings):
    # Application
    app_name: str = Field(default="DanDanPlay-Python", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8888, env="PORT")
    
    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        env="CORS_ORIGINS"
    )
    
    # Upload
    max_upload_size: int = Field(default=5368709120, env="MAX_UPLOAD_SIZE")  # 5GB
    upload_dir: str = Field(default="uploads", env="UPLOAD_DIR")
    
    # DanDanPlay API
    dandan_api_base_url: str = Field(
        default="https://api.dandanplay.net/api/v2",
        env="DANDAN_API_BASE_URL"
    )
    dandan_proxy_url: str = Field(
        default="https://dandan-proxy.wiidede.space/api/v2",
        env="DANDAN_PROXY_URL"
    )
    
    # Redis (optional)
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-change-this-in-production",
        env="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "cors_origins":
                return json.loads(raw_val)
            return raw_val


# Create settings instance
settings = Settings()