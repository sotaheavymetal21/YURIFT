"""
キャッシュサービス
Supabaseのsearch_cacheテーブルを使用（TTL: 7日間）
"""
import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from supabase import create_client, Client
from api.core.config import settings


class CacheService:
    """
    検索結果キャッシュサービス

    - キャッシュキー: search_paramsのハッシュ値
    - TTL: 7日間（CACHE_TTL_DAYS設定）
    - 位置情報の丸め: 緯度経度を小数点第2位まで（約1.1km範囲）
    """

    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY,
        )
        self.ttl_days = settings.CACHE_TTL_DAYS

    def _generate_cache_key(self, search_params: Dict[str, Any]) -> str:
        """
        検索パラメータからキャッシュキーを生成

        位置情報は小数点第2位まで丸める（キャッシュヒット率向上）

        Args:
            search_params: 検索パラメータ

        Returns:
            キャッシュキー（SHA256ハッシュ）
        """
        # 位置情報を丸める
        rounded_params = {
            "vibes": sorted(search_params["vibes"]),  # ソートして順序を統一
            "sensations": sorted(search_params["sensations"]),
            "location": {
                "lat": round(search_params["location"]["lat"], 2),
                "lng": round(search_params["location"]["lng"], 2),
            },
        }

        # JSON文字列化してハッシュ
        params_str = json.dumps(rounded_params, sort_keys=True)
        cache_key = hashlib.sha256(params_str.encode()).hexdigest()

        return cache_key

    async def get(self, search_params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        キャッシュから検索結果を取得

        Args:
            search_params: 検索パラメータ

        Returns:
            キャッシュされた検索結果 または None
        """
        try:
            cache_key = self._generate_cache_key(search_params)

            # Supabaseから取得
            response = (
                self.client.table("search_cache")
                .select("result, expires_at")
                .eq("cache_key", cache_key)
                .execute()
            )

            if not response.data or len(response.data) == 0:
                return None

            cache_data = response.data[0]

            # 有効期限チェック（念のため）
            expires_at = datetime.fromisoformat(cache_data["expires_at"].replace("Z", "+00:00"))
            if expires_at < datetime.now(expires_at.tzinfo):
                # 期限切れ（本来はRLSで除外されるはず）
                return None

            return cache_data["result"]

        except Exception as e:
            print(f"⚠️  キャッシュ取得エラー: {str(e)}")
            return None

    async def set(self, search_params: Dict[str, Any], result: Dict[str, Any]) -> bool:
        """
        検索結果をキャッシュに保存

        Args:
            search_params: 検索パラメータ
            result: 検索結果

        Returns:
            成功したらTrue
        """
        try:
            cache_key = self._generate_cache_key(search_params)
            expires_at = datetime.utcnow() + timedelta(days=self.ttl_days)

            # Supabaseに保存（upsert）
            self.client.table("search_cache").upsert(
                {
                    "cache_key": cache_key,
                    "search_params": search_params,
                    "result": result,
                    "expires_at": expires_at.isoformat(),
                }
            ).execute()

            return True

        except Exception as e:
            print(f"⚠️  キャッシュ保存エラー: {str(e)}")
            return False

    async def clear_expired(self) -> int:
        """
        期限切れキャッシュを削除（メンテナンス用）

        Returns:
            削除件数
        """
        try:
            now = datetime.utcnow().isoformat()

            # 期限切れレコードを削除
            response = (
                self.client.table("search_cache").delete().lt("expires_at", now).execute()
            )

            return len(response.data) if response.data else 0

        except Exception as e:
            print(f"⚠️  期限切れキャッシュ削除エラー: {str(e)}")
            return 0


# シングルトンインスタンス
cache_service = CacheService()
