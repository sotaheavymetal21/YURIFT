"""
Supabaseインポートスクリプト
geocode_addresses.pyで生成したCSVをSupabaseにインポート

使い方:
1. .env.localにSupabase認証情報を設定
2. output.csvを準備
3. python import_to_supabase.py を実行

必要なライブラリ:
pip install supabase pandas python-dotenv
"""

import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv


def load_env():
    """環境変数読み込み"""
    load_dotenv(".env.local")

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("環境変数が設定されていません: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY")

    return supabase_url, supabase_key


def import_csv_to_supabase(csv_file: str):
    """
    CSVデータをSupabaseにインポート

    Args:
        csv_file: CSVファイルパス
    """
    # 環境変数読み込み
    supabase_url, supabase_key = load_env()

    # Supabaseクライアント作成
    supabase: Client = create_client(supabase_url, supabase_key)

    # CSV読み込み
    df = pd.read_csv(csv_file)

    # 必須カラムチェック
    required_columns = ["name", "address", "lat", "lng", "price", "keywords"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"必須カラムがありません: {col}")

    # NaN値をスキップ（ジオコーディング失敗したレコード）
    df = df.dropna(subset=["lat", "lng"])

    print(f"インポート対象: {len(df)} 件")

    # 各行をSupabaseに挿入
    success_count = 0
    error_count = 0

    for idx, row in df.iterrows():
        try:
            # キーワードをカンマ区切りから配列に変換
            keywords = row["keywords"].split(",") if pd.notna(row["keywords"]) else []
            keywords = [k.strip() for k in keywords]  # 空白削除

            # データ準備
            data = {
                "name": row["name"],
                "address": row["address"],
                "lat": float(row["lat"]),
                "lng": float(row["lng"]),
                "price": int(row["price"]),
                "keywords": keywords,
            }

            # Supabaseに挿入
            response = supabase.table("onsen_master").insert(data).execute()

            print(f"✅ [{idx+1}/{len(df)}] {row['name']}")
            success_count += 1

        except Exception as e:
            print(f"❌ [{idx+1}/{len(df)}] {row['name']} - エラー: {str(e)}")
            error_count += 1

    print(f"\n完了！")
    print(f"成功: {success_count} 件")
    print(f"失敗: {error_count} 件")


def main():
    """メイン処理"""
    print("=" * 50)
    print("YURIFT Supabaseインポートツール")
    print("=" * 50)

    csv_file = "data/output.csv"
    print(f"\nインポートファイル: {csv_file}\n")

    import_csv_to_supabase(csv_file)


if __name__ == "__main__":
    main()
