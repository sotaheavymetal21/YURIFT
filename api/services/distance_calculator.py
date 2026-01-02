"""
距離計算サービス（Haversine公式）
"""
import math


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    2点間の距離を計算（Haversine公式）

    Args:
        lat1: 地点1の緯度
        lng1: 地点1の経度
        lat2: 地点2の緯度
        lng2: 地点2の経度

    Returns:
        距離（km）
    """
    # 地球の半径（km）
    R = 6371.0

    # ラジアンに変換
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)

    # 差分計算
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad

    # Haversine公式
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return round(distance, 2)  # 小数点第2位まで


def is_within_range(
    user_lat: float, user_lng: float, facility_lat: float, facility_lng: float, max_km: float = 50.0
) -> bool:
    """
    施設がユーザーの指定範囲内にあるかチェック

    Args:
        user_lat: ユーザーの緯度
        user_lng: ユーザーの経度
        facility_lat: 施設の緯度
        facility_lng: 施設の経度
        max_km: 最大距離（km）デフォルト50km

    Returns:
        範囲内ならTrue
    """
    distance = haversine_distance(user_lat, user_lng, facility_lat, facility_lng)
    return distance <= max_km
