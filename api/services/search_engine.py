"""
ルールベース検索エンジン
"""
from typing import List, Dict, Any
from api.services.distance_calculator import haversine_distance
from api.services.supabase_client import supabase_service
from api.utils.vibe_mapping import get_vibe_keywords, get_sensation_keywords


class SearchEngine:
    """
    Drift検索エンジン
    ルールベースのキーワードマッチングとスコアリング
    """

    def __init__(self):
        self.supabase = supabase_service

    async def search(
        self,
        vibes: List[str],
        sensations: List[str],
        user_lat: float,
        user_lng: float,
        max_distance_km: float = 50.0,
    ) -> List[Dict[str, Any]]:
        """
        Drift検索実行

        Args:
            vibes: Vibe選択肢（3個）
            sensations: Sensation選択肢（1-4個）
            user_lat: ユーザー緯度
            user_lng: ユーザー経度
            max_distance_km: 最大距離（km）

        Returns:
            スコア順にソートされた施設リスト（上位20件）
        """
        # キーワード取得
        vibe_keywords = get_vibe_keywords(vibes)
        sensation_keywords = get_sensation_keywords(sensations)
        all_keywords = vibe_keywords + sensation_keywords

        # Supabaseから候補施設を取得
        facilities = await self.supabase.search_onsen_by_location_and_keywords(
            lat=user_lat,
            lng=user_lng,
            keywords=all_keywords,
            max_distance_km=max_distance_km,
            limit=100,  # 広めに取得してアプリ側でフィルタ
        )

        # スコアリングとフィルタリング
        scored_facilities = []
        for facility in facilities:
            # 距離計算
            distance_km = haversine_distance(
                user_lat, user_lng, facility["lat"], facility["lng"]
            )

            # 距離フィルタ
            if distance_km > max_distance_km:
                continue

            # スコア計算
            score = self._calculate_score(
                facility=facility,
                vibe_keywords=vibe_keywords,
                sensation_keywords=sensation_keywords,
                distance_km=distance_km,
            )

            scored_facilities.append(
                {
                    **facility,
                    "distance_km": distance_km,
                    "score": score,
                }
            )

        # スコア順にソート（降順）
        scored_facilities.sort(key=lambda x: x["score"], reverse=True)

        # 上位20件を返す
        return scored_facilities[:20]

    def _calculate_score(
        self,
        facility: Dict[str, Any],
        vibe_keywords: List[str],
        sensation_keywords: List[str],
        distance_km: float,
    ) -> float:
        """
        施設のマッチングスコアを計算

        スコア = 距離スコア (50点) + キーワードマッチスコア (50点)

        Args:
            facility: 施設データ
            vibe_keywords: Vibeキーワードリスト
            sensation_keywords: Sensationキーワードリスト
            distance_km: ユーザーからの距離

        Returns:
            スコア（0-100）
        """
        # 1. 距離スコア（50点満点）
        # 0-10km: 50点
        # 10-30km: 30点
        # 30-50km: 10点
        if distance_km <= 10:
            distance_score = 50.0
        elif distance_km <= 30:
            distance_score = 50.0 - ((distance_km - 10) / 20) * 20  # 50 → 30
        else:
            distance_score = 30.0 - ((distance_km - 30) / 20) * 20  # 30 → 10

        distance_score = max(0, distance_score)

        # 2. キーワードマッチスコア（50点満点）
        facility_keywords = facility.get("keywords", [])
        if not facility_keywords:
            facility_keywords = []

        # Vibeマッチ（30点）
        vibe_match_count = sum(
            1 for keyword in vibe_keywords if keyword in facility_keywords
        )
        vibe_score = (vibe_match_count / len(vibe_keywords)) * 30 if vibe_keywords else 0

        # Sensationマッチ（20点）
        sensation_match_count = sum(
            1 for keyword in sensation_keywords if keyword in facility_keywords
        )
        sensation_score = (
            (sensation_match_count / len(sensation_keywords)) * 20 if sensation_keywords else 0
        )

        keyword_score = vibe_score + sensation_score

        # 合計スコア
        total_score = distance_score + keyword_score

        return round(total_score, 2)


# シングルトンインスタンス
search_engine = SearchEngine()
