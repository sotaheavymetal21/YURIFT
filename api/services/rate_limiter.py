"""
レート制限サービス
Upstash Redisを使用したSliding Window Counter実装
"""
import time
from typing import Tuple
from redis import Redis
from api.core.config import settings


class RateLimiter:
    """
    Sliding Window Counter アルゴリズムによるレート制限

    - 5リクエスト/日/IP
    - Upstash Redis（REST API経由）
    """

    def __init__(self):
        # Upstash Redis接続（REST API）
        # Note: redis-pyでRESTエンドポイントを使う場合の設定
        # 本番ではupstash-redisライブラリ推奨
        self.redis_client = Redis.from_url(
            settings.UPSTASH_REDIS_REST_URL,
            decode_responses=True,
        )

        self.max_requests = settings.RATE_LIMIT_MAX_REQUESTS
        self.window_seconds = settings.RATE_LIMIT_WINDOW_SECONDS

    def _get_key(self, identifier: str) -> str:
        """
        Redisキー生成

        Args:
            identifier: 識別子（IPアドレスなど）

        Returns:
            Redisキー
        """
        return f"rate_limit:{identifier}"

    async def check_rate_limit(self, identifier: str) -> Tuple[bool, int, int]:
        """
        レート制限チェック

        Args:
            identifier: 識別子（IPアドレス）

        Returns:
            (許可するか, 残りリクエスト数, リセットまでの秒数)
        """
        try:
            key = self._get_key(identifier)
            current_time = int(time.time())

            # パイプライン実行（アトミック操作）
            pipe = self.redis_client.pipeline()

            # 古いタイムスタンプを削除
            pipe.zremrangebyscore(key, 0, current_time - self.window_seconds)

            # 現在のウィンドウ内のリクエスト数を取得
            pipe.zcard(key)

            # 新しいリクエストを追加
            pipe.zadd(key, {str(current_time): current_time})

            # キーのTTL設定（ウィンドウサイズ + 余裕）
            pipe.expire(key, self.window_seconds + 60)

            results = pipe.execute()

            # リクエスト数（zadd前の値）
            request_count = results[1]

            # レート制限チェック
            if request_count >= self.max_requests:
                # 制限超過 - 最古のリクエストタイムスタンプを取得
                oldest = self.redis_client.zrange(key, 0, 0, withscores=True)
                if oldest:
                    oldest_timestamp = int(oldest[0][1])
                    reset_seconds = self.window_seconds - (current_time - oldest_timestamp)
                else:
                    reset_seconds = self.window_seconds

                # 追加したリクエストを削除（制限超過なので）
                self.redis_client.zrem(key, str(current_time))

                return False, 0, max(0, reset_seconds)

            # 許可
            remaining = self.max_requests - request_count - 1
            return True, remaining, self.window_seconds

        except Exception as e:
            print(f"⚠️  レート制限チェックエラー: {str(e)}")
            # エラー時は許可（フェイルオープン）
            return True, self.max_requests, self.window_seconds

    async def reset(self, identifier: str) -> bool:
        """
        特定識別子のレート制限をリセット（管理者用）

        Args:
            identifier: 識別子

        Returns:
            成功したらTrue
        """
        try:
            key = self._get_key(identifier)
            self.redis_client.delete(key)
            return True

        except Exception as e:
            print(f"⚠️  レート制限リセットエラー: {str(e)}")
            return False


# シングルトンインスタンス
rate_limiter = RateLimiter()
