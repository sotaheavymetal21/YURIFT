"""
リクエストモデル
"""
from pydantic import BaseModel, Field, validator
from typing import Literal, List


# Vibe選択肢の型定義
VibeChoice = Literal[
    "forest",
    "city",
    "snow",
    "bonfire",
    "hinoki",
    "concrete",
    "ocean",
    "cave",
    "morning",
    "sunset",
    "solo",
    "party",
]

# Sensation選択肢
ALLOWED_SENSATIONS = [
    "トロトロ",
    "ビリビリ",
    "シャキッ",
    "プンプン",
    "シュワシュワ",
    "ドロドロ",
    "スースー",
    "おまかせ",
]


class Location(BaseModel):
    """位置情報モデル"""

    lat: float = Field(..., ge=-90, le=90, description="緯度")
    lng: float = Field(..., ge=-180, le=180, description="経度")


class DriftRequest(BaseModel):
    """
    Drift検索リクエスト
    """

    vibes: List[VibeChoice] = Field(..., min_length=3, max_length=3, description="選択されたVibe (3個)")
    sensations: List[str] = Field(..., min_length=1, max_length=4, description="選択されたSensation (1-4個)")
    location: Location = Field(..., description="ユーザー位置情報")

    @validator("vibes")
    def validate_vibes_unique(cls, v):
        """Vibesの重複チェック"""
        if len(v) != len(set(v)):
            raise ValueError("Vibesに重複があります")
        return v

    @validator("sensations")
    def validate_sensations(cls, v):
        """Sensationsのバリデーション"""
        # 重複チェック
        if len(v) != len(set(v)):
            raise ValueError("Sensationsに重複があります")

        # 許可リストチェック
        for sensation in v:
            if sensation not in ALLOWED_SENSATIONS:
                raise ValueError(f"不正なSensation: {sensation}")

        return v

    class Config:
        # 追加フィールドを拒否
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "vibes": ["forest", "snow", "hinoki"],
                "sensations": ["トロトロ", "プンプン"],
                "location": {"lat": 35.6812, "lng": 139.7671},
            }
        }
