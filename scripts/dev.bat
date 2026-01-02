@echo off
REM YURIFT 開発サーバー起動スクリプト (Windows)

echo.
echo ================================================
echo   YURIFT 開発サーバー起動
echo ================================================
echo.

REM 環境変数チェック
if not exist .env.local (
    echo [警告] .env.local が見つかりません
    echo.
    echo .env.local.example をコピーして設定してください:
    echo    copy .env.local.example .env.local
    echo.
    exit /b 1
)

echo [OK] 環境変数ファイル確認完了
echo.

REM Python仮想環境確認
cd api
if not exist venv (
    echo [INFO] Python仮想環境を作成中...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM FastAPI起動（別ウィンドウ）
echo [INFO] FastAPIサーバー起動中...
start "YURIFT FastAPI" cmd /k "venv\Scripts\activate && uvicorn main:app --reload --port 8000"
timeout /t 3 /nobreak >nul
echo [OK] FastAPI起動完了 - http://localhost:8000
echo.

cd ..

REM Next.js起動（別ウィンドウ）
echo [INFO] Next.jsサーバー起動中...
start "YURIFT Next.js" cmd /k "npm run dev"
timeout /t 3 /nobreak >nul
echo [OK] Next.js起動完了 - http://localhost:3000
echo.

echo ================================================
echo   起動完了！
echo ================================================
echo.
echo   フロントエンド: http://localhost:3000
echo   API Docs:       http://localhost:8000/api/docs
echo.
echo   各ウィンドウでCtrl+Cを押すと終了します
echo.
pause
