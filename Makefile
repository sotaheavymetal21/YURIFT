.PHONY: help install dev setup-db clean test migration-new migration-list migration-verify

# デフォルトターゲット
help:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  YURIFT 開発コマンド"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "📦 セットアップ:"
	@echo "  make install         - 依存関係をインストール"
	@echo "  make setup-db        - データベースセットアップ"
	@echo ""
	@echo "🚀 開発:"
	@echo "  make dev             - 開発サーバー起動"
	@echo "  make dev-frontend    - フロントエンドのみ起動"
	@echo "  make dev-backend     - バックエンドのみ起動"
	@echo ""
	@echo "🗄️  マイグレーション:"
	@echo "  make migration-new   - 新しいマイグレーション作成"
	@echo "  make migration-list  - マイグレーション一覧表示"
	@echo "  make migration-verify- マイグレーション検証"
	@echo ""
	@echo "🔧 その他:"
	@echo "  make clean           - 一時ファイル削除"
	@echo "  make test            - テスト実行"
	@echo "  make lint            - Lint実行"
	@echo "  make build           - ビルド"
	@echo ""

# 依存関係インストール
install:
	@echo "📦 フロントエンド依存関係インストール中..."
	npm install
	@echo ""
	@echo "📦 バックエンド依存関係インストール中..."
	cd api && python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt
	@echo ""
	@echo "✅ インストール完了！"

# 開発サーバー起動
dev:
	@./scripts/dev.sh

# データベースセットアップ
setup-db:
	@./scripts/setup-db.sh

# クリーンアップ
clean:
	@echo "🧹 クリーンアップ中..."
	rm -rf node_modules
	rm -rf .next
	rm -rf api/venv
	rm -rf api/__pycache__
	rm -rf api/**/__pycache__
	@echo "✅ クリーンアップ完了"

# テスト実行（将来用）
test:
	@echo "🧪 テスト実行..."
	@echo "（テストは未実装です）"

# フロントエンドのみ起動
dev-frontend:
	@echo "⚛️  Next.js起動中..."
	npm run dev

# バックエンドのみ起動
dev-backend:
	@echo "🔧 FastAPI起動中..."
	cd api && \
	. venv/bin/activate && \
	uvicorn main:app --reload --port 8000

# 依存関係更新
upgrade:
	@echo "📦 依存関係更新中..."
	npm update
	cd api && \
	. venv/bin/activate && \
	pip install --upgrade -r requirements.txt
	@echo "✅ 更新完了"

# ビルド（デプロイ前確認）
build:
	@echo "🏗️  ビルド中..."
	npm run build
	@echo "✅ ビルド完了"

# Lint & Format
lint:
	@echo "🔍 Lint実行中..."
	npm run lint
	@echo "✅ Lint完了"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# マイグレーション管理
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 新しいマイグレーション作成
migration-new:
	@echo "🗄️  新しいマイグレーション作成"
	@echo ""
	@read -p "マイグレーション名（例: add_review_table）: " name; \
	if [ -z "$$name" ]; then \
		echo "❌ マイグレーション名を入力してください"; \
		exit 1; \
	fi; \
	number=$$(ls -1 data/sql/[0-9][0-9]_*.sql 2>/dev/null | wc -l | tr -d ' '); \
	next_number=$$(printf "%02d" $$((number + 1))); \
	migration_file="data/sql/$${next_number}_$${name}.sql"; \
	rollback_file="data/sql/$${next_number}_rollback_$${name}.sql"; \
	echo ""; \
	echo "📝 作成するファイル:"; \
	echo "  - $$migration_file"; \
	echo "  - $$rollback_file"; \
	echo ""; \
	cp data/sql/TEMPLATE_migration.sql $$migration_file; \
	cp data/sql/TEMPLATE_rollback.sql $$rollback_file; \
	sed -i.bak "s/{番号}/$$next_number/g" $$migration_file && rm $$migration_file.bak; \
	sed -i.bak "s/{番号}/$$next_number/g" $$rollback_file && rm $$rollback_file.bak; \
	sed -i.bak "s/{説明}/$$name/g" $$migration_file && rm $$migration_file.bak; \
	sed -i.bak "s/{説明}/$$name/g" $$rollback_file && rm $$rollback_file.bak; \
	sed -i.bak "s/YYYY-MM-DD/$$(date +%Y-%m-%d)/g" $$migration_file && rm $$migration_file.bak; \
	sed -i.bak "s/YYYY-MM-DD/$$(date +%Y-%m-%d)/g" $$rollback_file && rm $$rollback_file.bak; \
	echo "✅ マイグレーションファイルを作成しました"; \
	echo ""; \
	echo "📋 次のステップ:"; \
	echo "  1. $$migration_file を編集"; \
	echo "  2. $$rollback_file を編集"; \
	echo "  3. Supabase SQL Editorでマイグレーションを実行"; \
	echo "  4. data/sql/README.md の履歴を更新"; \
	echo "  5. git add して commit"

# マイグレーション一覧表示
migration-list:
	@echo "🗄️  マイグレーション一覧"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "📋 マイグレーションファイル:"
	@echo ""
	@ls -1 data/sql/[0-9][0-9]_*.sql | grep -v rollback | while read file; do \
		filename=$$(basename $$file); \
		number=$${filename:0:2}; \
		name=$${filename:3}; \
		name=$${name%.sql}; \
		echo "  $$number. $$name"; \
	done
	@echo ""
	@echo "🔄 ロールバックファイル:"
	@echo ""
	@ls -1 data/sql/[0-9][0-9]_rollback_*.sql | while read file; do \
		filename=$$(basename $$file); \
		number=$${filename:0:2}; \
		name=$${filename:12}; \
		name=$${name%.sql}; \
		echo "  $$number. $$name (rollback)"; \
	done
	@echo ""
	@echo "📚 詳細は data/sql/README.md を参照"

# マイグレーション検証
migration-verify:
	@echo "🔍 マイグレーション検証"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "📝 検証SQLをSupabase SQL Editorで実行してください:"
	@echo ""
	@echo "  data/sql/verify_migrations.sql"
	@echo ""
	@echo "または、以下のコマンドで内容を確認:"
	@echo ""
	@echo "  cat data/sql/verify_migrations.sql"
	@echo ""
	@cat data/sql/verify_migrations.sql
