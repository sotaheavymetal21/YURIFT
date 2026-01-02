"""
Drift検索APIエンドポイント
"""
from fastapi import APIRouter, HTTPException, Request, Response
from api.models.request import DriftRequest
from api.models.response import DriftResponse, OnsenFacility, ErrorResponse
from api.services.search_engine import search_engine
from api.services.openai_service import openai_service
from api.services.cache_service import cache_service
from api.services.rate_limiter import rate_limiter

router = APIRouter()


@router.post(
    "/drift",
    response_model=DriftResponse,
    summary="Drift検索",
    description="Vibe/Sensationに基づいて日帰り温泉を検索（3件返却）",
)
async def drift_search(drift_request: DriftRequest, request: Request, response: Response):
    """
    Drift検索エンドポイント

    ユーザーのVibe/Sensation選択と位置情報から、
    最適な日帰り温泉施設を3件レコメンド

    Args:
        drift_request: Drift検索リクエスト
        request: FastAPIリクエスト（IPアドレス取得用）
        response: FastAPIレスポンス（ヘッダー設定用）

    Returns:
        DriftResponse: 検索結果（3施設）

    Raises:
        HTTPException: 検索エラー時
    """
    try:
        # 1. レート制限チェック
        client_ip = request.client.host if request.client else "unknown"
        allowed, remaining, reset_seconds = await rate_limiter.check_rate_limit(client_ip)

        # レート制限ヘッダー設定
        response.headers["X-RateLimit-Limit"] = str(rate_limiter.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(reset_seconds)

        if not allowed:
            raise HTTPException(
                status_code=429,
                detail=f"レート制限に達しました。{reset_seconds}秒後に再試行してください。",
            )

        # 2. 検索パラメータ準備
        search_params = {
            "vibes": drift_request.vibes,
            "sensations": drift_request.sensations,
            "location": {
                "lat": drift_request.location.lat,
                "lng": drift_request.location.lng,
            },
        }

        # 3. キャッシュチェック
        cached_result = await cache_service.get(search_params)

        if cached_result:
            # キャッシュヒット
            return DriftResponse(**cached_result, cached=True)

        # 4. ルールベース検索実行
        facilities = await search_engine.search(
            vibes=drift_request.vibes,
            sensations=drift_request.sensations,
            user_lat=drift_request.location.lat,
            user_lng=drift_request.location.lng,
            max_distance_km=50.0,
        )

        # 5. 上位3件を取得
        top_3_facilities = facilities[:3]

        if len(top_3_facilities) == 0:
            raise HTTPException(
                status_code=404,
                detail="近くに温泉施設が見つかりませんでした。別の場所で試してください。",
            )

        # 6. OpenAIでキャッチフレーズ生成（3施設まとめて）
        catchphrases = await openai_service.generate_catchphrases(
            facilities=top_3_facilities,
            vibes=drift_request.vibes,
            sensations=drift_request.sensations,
        )

        # 7. レスポンス構築
        result_facilities = []
        for i, facility in enumerate(top_3_facilities):
            result_facilities.append(
                OnsenFacility(
                    id=facility["id"],
                    name=facility["name"],
                    address=facility["address"],
                    lat=facility["lat"],
                    lng=facility["lng"],
                    price=facility["price"],
                    distance_km=facility["distance_km"],
                    catchphrase=catchphrases[i] if i < len(catchphrases) else "温泉を楽しむ",
                    score=facility["score"],
                )
            )

        result = DriftResponse(
            facilities=result_facilities,
            cached=False,
            search_params=search_params,
        )

        # 8. キャッシュ保存
        await cache_service.set(search_params, result.dict())

        return result

    except HTTPException:
        # HTTPExceptionはそのまま再送出
        raise

    except Exception as e:
        # その他のエラーは500として返す
        from api.core.config import settings

        if settings.is_production():
            # 本番環境では詳細を隠す
            raise HTTPException(
                status_code=500,
                detail="検索中にエラーが発生しました。しばらく時間をおいて再度お試しください。",
            )
        else:
            # 開発環境では詳細を表示
            raise HTTPException(
                status_code=500,
                detail=f"検索中にエラーが発生しました: {str(e)}",
            )
