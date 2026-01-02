"""
レスポンスモデル
"""
from pydantic import BaseModel, Field
from typing import List


class OnsenFacility(BaseModel):
    """
    温泉施設情報
    """

    id: int = Field(..., description="施設ID")
    name: str = Field(..., description="施設名")
    address: str = Field(..., description="住所")
    lat: float = Field(..., description="緯度")
    lng: float = Field(..., description="経度")
    price: int = Field(..., description="料金（円）")
    distance_km: float = Field(..., description="ユーザーからの距離（km）")
    catchphrase: str = Field(..., description="AIキャッチフレーズ")
    score: float = Field(..., description="マッチングスコア（0-100）")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "森の湯",
                "address": "東京都八王子市○○1-2-3",
                "lat": 35.6812,
                "lng": 139.7671,
                "price": 800,
                "distance_km": 2.5,
                "catchphrase": "森の静寂に包まれる、極上のとろとろ湯",
                "score": 92.5,
            }
        }


class DriftResponse(BaseModel):
    """
    Drift検索レスポンス
    """

    facilities: List[OnsenFacility] = Field(..., description="検索結果（3件）")
    cached: bool = Field(..., description="キャッシュヒットしたか")
    search_params: dict = Field(..., description="検索パラメータ")

    class Config:
        json_schema_extra = {
            "example": {
                "facilities": [
                    {
                        "id": 1,
                        "name": "森の湯",
                        "address": "東京都八王子市○○1-2-3",
                        "lat": 35.6812,
                        "lng": 139.7671,
                        "price": 800,
                        "distance_km": 2.5,
                        "catchphrase": "森の静寂に包まれる、極上のとろとろ湯",
                        "score": 92.5,
                    },
                    {
                        "id": 2,
                        "name": "雪見温泉",
                        "address": "東京都檜原村○○2-1-5",
                        "lat": 35.7250,
                        "lng": 139.1491,
                        "price": 1000,
                        "distance_km": 5.8,
                        "catchphrase": "雪景色とひのきの香りで癒される秘湯",
                        "score": 88.0,
                    },
                    {
                        "id": 3,
                        "name": "檜乃湯",
                        "address": "東京都青梅市○○3-4-1",
                        "lat": 35.7878,
                        "lng": 139.2644,
                        "price": 900,
                        "distance_km": 8.2,
                        "catchphrase": "檜の香りとトロトロのお湯で心も体もリセット",
                        "score": 85.5,
                    },
                ],
                "cached": False,
                "search_params": {
                    "vibes": ["forest", "snow", "hinoki"],
                    "sensations": ["トロトロ", "プンプン"],
                    "location": {"lat": 35.6812, "lng": 139.7671},
                },
            }
        }


class ErrorResponse(BaseModel):
    """
    エラーレスポンス
    """

    error: str = Field(..., description="エラーメッセージ")
    detail: str = Field(default="", description="詳細情報")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "detail": "Vibesに重複があります",
            }
        }
