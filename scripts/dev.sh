#!/bin/bash

# YURIFT 開発サーバー起動スクリプト

echo "🚀 YURIFT 開発サーバーを起動します..."
echo ""

# 環境変数チェック
if [ ! -f .env.local ]; then
    echo "⚠️  .env.local が見つかりません"
    echo "📝 .env.local.example をコピーして設定してください:"
    echo "   cp .env.local.example .env.local"
    echo ""
    exit 1
fi

echo "✅ 環境変数ファイル確認OK"
echo ""

# バックエンド起動
echo "🔧 FastAPIサーバー起動中..."
cd api

# venv確認
if [ ! -d "venv" ]; then
    echo "📦 Python仮想環境を作成中..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# FastAPIをバックグラウンドで起動
uvicorn main:app --reload --port 8000 &
FASTAPI_PID=$!
echo "✅ FastAPI起動完了 (PID: $FASTAPI_PID) → http://localhost:8000"
echo ""

cd ..

# フロントエンド起動
echo "⚛️  Next.jsサーバー起動中..."
npm run dev &
NEXTJS_PID=$!
echo "✅ Next.js起動完了 (PID: $NEXTJS_PID) → http://localhost:3000"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 YURIFT 開発サーバー起動完了！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 フロントエンド: http://localhost:3000"
echo "🔌 API Docs:       http://localhost:8000/api/docs"
echo ""
echo "終了するには Ctrl+C を押してください"
echo ""

# シグナルハンドリング
trap 'echo ""; echo "🛑 サーバーを停止中..."; kill $FASTAPI_PID $NEXTJS_PID; exit 0' INT

# プロセスを待機
wait
