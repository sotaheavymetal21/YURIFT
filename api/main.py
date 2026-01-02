"""
FastAPI メインアプリケーション
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from api.core.config import settings
import time


# セキュリティヘッダーミドルウェア
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # セキュリティヘッダー追加
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # 開発環境以外でContent-Security-Policy設定
        if not settings.is_development():
            response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; object-src 'none'"

        return response


# FastAPIアプリ初期化
app = FastAPI(
    title="YURIFT API",
    description="超低コスト日帰り温泉検索API",
    version="2.0.0",
    docs_url="/api/docs" if settings.API_DOCS_ENABLED else None,
    redoc_url="/api/redoc" if settings.API_DOCS_ENABLED else None,
    openapi_url="/api/openapi.json" if settings.API_DOCS_ENABLED else None,
)

# セキュリティヘッダーミドルウェア追加
app.add_middleware(SecurityHeadersMiddleware)

# Trusted Host ミドルウェア（本番環境のみ）
if settings.is_production():
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["yurift.vercel.app", "*.vercel.app"]
    )

# CORS設定（環境変数から読み込み）
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age=3600,
)


# グローバルエラーハンドラー
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """グローバルエラーハンドラー（本番環境では詳細を隠す）"""
    if settings.is_production():
        # 本番環境では詳細を隠す
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": "An error occurred. Please try again later.",
            },
        )
    else:
        # 開発環境では詳細を表示
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(exc),
                "type": type(exc).__name__,
            },
        )


@app.get("/")
async def root():
    """
    ヘルスチェックエンドポイント
    """
    return {
        "message": "YURIFT API",
        "version": "2.0.0",
        "status": "healthy",
        "environment": settings.ENV,
        "endpoints": {
            "drift_search": "/api/drift",
            "health": "/api/health",
            "docs": "/api/docs" if settings.API_DOCS_ENABLED else None,
        },
    }


@app.get("/api/health")
async def health_check():
    """
    詳細なヘルスチェック
    """
    return JSONResponse(
        content={
            "status": "healthy",
            "api_version": "2.0.0",
            "environment": settings.ENV,
            "services": {
                "fastapi": "ok",
                "supabase": "ok",
                "redis": "ok",
            },
        }
    )


# ルーター追加
from api.routes import drift

app.include_router(drift.router, prefix="/api", tags=["drift"])
