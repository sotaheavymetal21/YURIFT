"""
環境変数・設定管理
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    """
    アプリケーション設定
    """

    # 環境
    ENV: str = "development"

    # OpenAI API
    OPENAI_API_KEY: str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # Upstash Redis
    UPSTASH_REDIS_REST_URL: str
    UPSTASH_REDIS_REST_TOKEN: str

    # CORS許可オリジン（環境変数から読み込み、カンマ区切り）
    ALLOWED_ORIGINS: str = "http://localhost:3000,https://yurift.vercel.app"

    # Rate Limiting設定
    RATE_LIMIT_MAX_REQUESTS: int = 5  # 5回/日
    RATE_LIMIT_WINDOW_SECONDS: int = 86400  # 24時間

    # キャッシュ設定
    CACHE_TTL_DAYS: int = 7  # 7日間

    # セキュリティ設定
    API_DOCS_ENABLED: bool = True  # 本番環境ではfalseに

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        """OpenAI APIキーのバリデーション"""
        if not v or not v.startswith("sk-"):
            raise ValueError("Invalid OpenAI API Key format")
        return v

    @field_validator("SUPABASE_URL")
    @classmethod
    def validate_supabase_url(cls, v: str) -> str:
        """Supabase URLのバリデーション"""
        if not v or not v.startswith("https://"):
            raise ValueError("Supabase URL must start with https://")
        if not ".supabase.co" in v:
            raise ValueError("Invalid Supabase URL format")
        return v

    @field_validator("UPSTASH_REDIS_REST_URL")
    @classmethod
    def validate_upstash_url(cls, v: str) -> str:
        """Upstash Redis URLのバリデーション"""
        if not v or not v.startswith("https://"):
            raise ValueError("Upstash URL must start with https://")
        return v

    def get_allowed_origins(self) -> List[str]:
        """CORS許可オリジンをリストで取得"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    def is_production(self) -> bool:
        """本番環境かどうか"""
        return self.ENV.lower() == "production"

    def is_development(self) -> bool:
        """開発環境かどうか"""
        return self.ENV.lower() == "development"

    class Config:
        env_file = ".env.local"
        case_sensitive = True


# シングルトンインスタンス
settings = Settings()
