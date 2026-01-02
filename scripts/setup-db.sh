#!/bin/bash

# Supabaseデータベースセットアップスクリプト

echo "🗄️  YURIFT データベースセットアップ"
echo ""

# 環境変数チェック
if [ ! -f .env.local ]; then
    echo "❌ .env.local が見つかりません"
    echo "先に環境変数を設定してください"
    exit 1
fi

# Supabase URL取得
source .env.local
if [ -z "$SUPABASE_URL" ]; then
    echo "❌ SUPABASE_URL が設定されていません"
    exit 1
fi

echo "✅ Supabase接続先: $SUPABASE_URL"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 以下のSQLをSupabase SQL Editorで実行してください:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  温泉マスターテーブル作成"
echo "   → data/sql/01_create_onsen_master.sql"
echo ""
echo "2️⃣  検索キャッシュテーブル作成"
echo "   → data/sql/02_create_search_cache.sql"
echo ""
echo "3️⃣  サンプルデータ投入（15件）"
echo "   → data/sql/03_sample_data.sql"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "Supabase SQL Editorを開きますか？ (y/N): " choice
if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
    # SupabaseプロジェクトIDを抽出
    PROJECT_ID=$(echo $SUPABASE_URL | sed 's/https:\/\/\(.*\)\.supabase\.co/\1/')
    SQL_EDITOR_URL="https://supabase.com/dashboard/project/$PROJECT_ID/sql/new"

    echo "🌐 ブラウザでSQL Editorを開いています..."

    # OSに応じてブラウザを開く
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$SQL_EDITOR_URL"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "$SQL_EDITOR_URL"
    fi
fi

echo ""
echo "📝 SQLファイルの内容を表示します..."
echo ""

for sql_file in data/sql/*.sql; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📄 $(basename $sql_file)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    cat "$sql_file"
    echo ""
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ セットアップ手順:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. 上記のSQLをSupabase SQL Editorにコピー&ペースト"
echo "2. 順番に実行（01 → 02 → 03）"
echo "3. Table Editorで 'onsen_master' テーブルを確認"
echo "4. 15件のサンプルデータが入っていればOK！"
echo ""
