"""
住所ジオコーディングスクリプト
Google Sheetsで収集した温泉施設データに緯度経度を追加

使い方:
1. Google Sheetsで「施設名」「住所」「料金」「キーワード」を入力
2. CSVでエクスポート（input.csv）
3. このスクリプトを実行
4. output.csvが生成される（lat, lng列が追加）
5. output.csvをSupabaseにインポート

必要なライブラリ:
pip install geopy pandas
"""

import csv
import time
from typing import Optional, Tuple
from geopy.geocoders import Nominatim
import pandas as pd


class AddressGeocoder:
    def __init__(self):
        # Nominatim（OpenStreetMap）を使用（無料）
        self.geolocator = Nominatim(
            user_agent="yurift_onsen_collector_v1",
            timeout=10,
        )

    def geocode(self, address: str) -> Optional[Tuple[float, float]]:
        """
        住所から緯度経度を取得

        Args:
            address: 住所

        Returns:
            (緯度, 経度) または None
        """
        try:
            # Nominatimでジオコーディング
            location = self.geolocator.geocode(address, language="ja")

            if location:
                return (location.latitude, location.longitude)
            else:
                print(f"⚠️  住所が見つかりませんでした: {address}")
                return None

        except Exception as e:
            print(f"❌ エラー: {address} - {str(e)}")
            return None

    def process_csv(self, input_file: str, output_file: str):
        """
        CSVファイルを処理してジオコーディング

        Args:
            input_file: 入力CSVファイルパス
            output_file: 出力CSVファイルパス
        """
        # CSV読み込み
        df = pd.read_csv(input_file)

        # 必須カラムチェック
        required_columns = ["name", "address", "price", "keywords"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"必須カラムがありません: {col}")

        # 緯度経度列を追加
        df["lat"] = None
        df["lng"] = None

        # 各行を処理
        total = len(df)
        for idx, row in df.iterrows():
            address = row["address"]
            print(f"[{idx+1}/{total}] {row['name']} - {address}")

            # ジオコーディング
            coords = self.geocode(address)

            if coords:
                df.at[idx, "lat"] = coords[0]
                df.at[idx, "lng"] = coords[1]
                print(f"  ✅ ({coords[0]}, {coords[1]})")
            else:
                print(f"  ❌ ジオコーディング失敗")

            # Nominatimのレート制限対策（1秒待機）
            time.sleep(1)

        # CSV出力
        df.to_csv(output_file, index=False)
        print(f"\n✅ 完了！ {output_file} を確認してください。")

        # 統計
        success_count = df["lat"].notna().sum()
        print(f"\n成功: {success_count}/{total} 件")


def main():
    """メイン処理"""
    geocoder = AddressGeocoder()

    # CSVファイル処理
    input_csv = "data/input.csv"
    output_csv = "data/output.csv"

    print("=" * 50)
    print("YURIFT 温泉データ ジオコーディングツール")
    print("=" * 50)
    print(f"\n入力ファイル: {input_csv}")
    print(f"出力ファイル: {output_csv}")
    print("\n処理を開始します...\n")

    geocoder.process_csv(input_csv, output_csv)


if __name__ == "__main__":
    main()
