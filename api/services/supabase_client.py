"""
Supabaseクライアントサービス
"""
from typing import List, Optional, Dict, Any
from supabase import create_client, Client
from api.core.config import settings


class SupabaseService:
    """Supabase操作サービス"""

    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY,
        )

    async def search_onsen_by_location_and_keywords(
        self,
        lat: float,
        lng: float,
        keywords: List[str],
        max_distance_km: float = 50.0,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        位置情報とキーワードで温泉施設を検索

        Args:
            lat: ユーザーの緯度
            lng: ユーザーの経度
            keywords: 検索キーワードリスト
            max_distance_km: 最大距離（km）
            limit: 取得件数上限

        Returns:
            施設リスト
        """
        # 簡易的な矩形範囲フィルタ（50km ≈ 緯度経度0.45度）
        # 厳密な距離計算はアプリケーション側で行う
        lat_delta = 0.45
        lng_delta = 0.45

        # Supabaseクエリ構築
        query = (
            self.client.table("onsen_master")
            .select("*")
            .gte("lat", lat - lat_delta)
            .lte("lat", lat + lat_delta)
            .gte("lng", lng - lng_delta)
            .lte("lng", lng + lng_delta)
            .limit(limit)
        )

        # クエリ実行
        response = query.execute()

        return response.data if response.data else []

    async def get_all_onsen(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        全温泉施設を取得（開発・テスト用）

        Args:
            limit: 取得件数上限

        Returns:
            施設リスト
        """
        response = self.client.table("onsen_master").select("*").limit(limit).execute()

        return response.data if response.data else []

    async def get_onsen_by_id(self, onsen_id: int) -> Optional[Dict[str, Any]]:
        """
        IDで温泉施設を取得

        Args:
            onsen_id: 施設ID

        Returns:
            施設データ または None
        """
        response = self.client.table("onsen_master").select("*").eq("id", onsen_id).execute()

        if response.data and len(response.data) > 0:
            return response.data[0]
        return None


# シングルトンインスタンス
supabase_service = SupabaseService()
