# YURIFT データ収集ガイド

温泉データを収集してSupabaseにインポートする手順です。

## 📋 ワークフロー

### 1. データ収集（Google Sheets推奨）

Google Sheetsで以下の列を持つシートを作成：

| name | address | price | keywords |
|------|---------|-------|----------|
| 森の湯 八王子 | 東京都八王子市○○1-2-3 | 800 | 森,自然,緑,トロトロ,美肌,檜風呂 |

- **name**: 施設名
- **address**: 完全な住所（ジオコーディング精度向上のため）
- **price**: 料金（円）
- **keywords**: 検索用キーワード（カンマ区切り）

**キーワード例:**
- Vibe系: `森`, `山`, `自然`, `海`, `雪`, `檜`, `駅近`, `都会`, など
- Sensation系: `トロトロ`, `硫黄`, `プンプン`, `炭酸`, `シュワシュワ`, など
- その他: `静か`, `展望`, `サウナ`, `岩盤浴`, など

### 2. CSVエクスポート

Google Sheetsから `data/input.csv` としてエクスポート

### 3. ジオコーディング実行

```bash
# 必要なライブラリインストール
pip install geopy pandas

# スクリプト実行
python data/scripts/geocode_addresses.py
```

- Nominatim（OSM）を使用して住所から緯度経度を自動取得
- `data/output.csv` が生成される（lat, lng列が追加）
- レート制限対策で1秒/1件のペース

### 4. Supabaseにインポート

```bash
# 必要なライブラリインストール
pip install supabase python-dotenv

# 環境変数設定（.env.local）
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# インポート実行
python data/scripts/import_to_supabase.py
```

## 🗄️ SQLファイル

### `sql/01_create_onsen_master.sql`
- onsen_masterテーブル作成
- インデックス、トリガー設定

### `sql/02_create_search_cache.sql`
- search_cacheテーブル作成
- RLSポリシー設定

### `sql/03_sample_data.sql`
- 15件のサンプルデータ（開発・テスト用）
- 東京・神奈川の日帰り温泉

## 📊 データ収集目標

- **初期リリース**: 100-200件（東京・神奈川・埼玉・千葉）
- **優先エリア**: 都心から50km圏内の日帰り温泉
- **優先施設**: 料金1000円以下、アクセス良好

## 🚨 注意事項

1. **Nominatimレート制限**: 1リクエスト/秒を厳守
2. **住所の正確性**: 詳細な住所ほどジオコーディング精度が向上
3. **キーワード選定**: Vibe/Sensationマッピングに合わせる
4. **重複チェック**: 同じ施設を複数回登録しない

## 💡 Tips

- Google Mapsで施設情報を確認してキーワードを充実させる
- 口コミから特徴的なキーワードを抽出
- 公式サイトで正確な料金・住所を確認
