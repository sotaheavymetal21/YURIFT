# 🗄️ データベースマイグレーションガイド

YURIFTプロジェクトのデータベーススキーマ管理方法です。

---

## 📋 現在のアプローチ（MVP段階）

### 手動SQLマイグレーション + Git管理

**採用理由**:
- テーブル数が少ない（2テーブル）
- 個人開発〜小規模チーム（1-2人）
- スキーマ変更頻度が低い
- Supabase特有機能（RLS、Triggers）を使用

---

## 🚀 マイグレーション実行手順

### 初回セットアップ

```bash
# 1. Supabase SQL Editorにアクセス
# https://app.supabase.com/project/{project_id}/sql

# 2. 以下のSQLファイルを順番に実行
data/sql/01_create_onsen_master.sql
data/sql/02_create_search_cache.sql
data/sql/03_sample_data.sql  # 開発環境のみ
```

### スキーマ変更時

```bash
# 1. 新しいマイグレーションファイルを作成
data/sql/04_add_column_example.sql

# 2. SQLファイルに以下のヘッダーを追加
-- Migration: 04_add_column_example
-- Date: 2026-01-02
-- Description: Add column example to onsen_master
-- Rollback: 04_rollback_add_column_example.sql

# 3. マイグレーション実行
# Supabase SQL Editorで実行

# 4. ロールバック用SQLも作成（推奨）
data/sql/04_rollback_add_column_example.sql
```

---

## 📝 マイグレーションファイルの命名規則

```
data/sql/
├── 01_create_onsen_master.sql       # 初期テーブル
├── 02_create_search_cache.sql       # 初期テーブル
├── 03_sample_data.sql               # サンプルデータ
├── 04_add_review_table.sql          # 新機能: レビュー機能
├── 04_rollback_add_review_table.sql # ロールバック用
├── 05_add_index_to_reviews.sql      # インデックス追加
└── README.md                        # マイグレーション履歴
```

**命名ルール**:
- `{番号}_{説明}.sql` 形式
- 番号は2桁（01, 02, 03...）
- 説明はスネークケース
- ロールバック用は `{番号}_rollback_{説明}.sql`

---

## 📊 マイグレーション履歴の記録

### `data/sql/README.md` を作成

```markdown
# マイグレーション履歴

| # | ファイル | 実行日 | 説明 | 実行者 |
|---|---------|-------|------|-------|
| 01 | create_onsen_master.sql | 2026-01-01 | 温泉マスターテーブル作成 | @yourname |
| 02 | create_search_cache.sql | 2026-01-01 | キャッシュテーブル作成 | @yourname |
| 03 | sample_data.sql | 2026-01-01 | サンプルデータ投入 | @yourname |
| 04 | add_review_table.sql | 2026-01-10 | レビュー機能追加 | @yourname |
```

---

## 🔄 ロールバック手順

### 例: レビューテーブルを削除する場合

```sql
-- data/sql/04_rollback_add_review_table.sql
-- Rollback for: 04_add_review_table.sql

DROP TABLE IF EXISTS reviews CASCADE;

-- インデックスも削除
-- DROP INDEX IF EXISTS idx_reviews_onsen_id;
```

**実行手順**:
```bash
# 1. ロールバックSQLをSupabase SQL Editorで実行
# 2. マイグレーション履歴を更新
# 3. Gitコミット
git add data/sql/04_rollback_add_review_table.sql
git commit -m "Rollback: Remove review table"
```

---

## 🛡️ ベストプラクティス

### 1. マイグレーションファイルのテンプレート

```sql
-- ============================================
-- Migration: {番号}_{説明}
-- Date: YYYY-MM-DD
-- Author: @yourname
-- Description: {詳細な説明}
-- Rollback: {ロールバックファイル名}
-- ============================================

-- ▼ Migration Start ▼

-- 1. テーブル作成
CREATE TABLE IF NOT EXISTS {table_name} (
    -- カラム定義
);

-- 2. インデックス作成
CREATE INDEX {index_name} ON {table_name} ({column});

-- 3. RLSポリシー設定
ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;

CREATE POLICY {policy_name} ON {table_name}
    FOR SELECT
    USING (true);

-- 4. コメント追加
COMMENT ON TABLE {table_name} IS '{説明}';

-- ▲ Migration End ▲

-- ============================================
-- Verification
-- ============================================
-- SELECT * FROM {table_name} LIMIT 1;
-- \d {table_name}
```

### 2. 環境ごとの実行管理

```bash
# 開発環境
export SUPABASE_PROJECT_ID=dev-project-id

# ステージング環境
export SUPABASE_PROJECT_ID=staging-project-id

# 本番環境
export SUPABASE_PROJECT_ID=prod-project-id
```

### 3. マイグレーション前のバックアップ

```bash
# Supabase Dashboard → Database → Backups
# または
pg_dump -h db.{project_id}.supabase.co -U postgres -d postgres > backup_$(date +%Y%m%d).sql
```

---

## 🚨 注意事項

### やってはいけないこと ❌

1. **既存のマイグレーションファイルを編集しない**
   - 新しいマイグレーションファイルを作成する

2. **本番環境で直接SQLを実行しない**
   - 必ずマイグレーションファイルとして記録

3. **ロールバックSQLを用意せずに実行しない**
   - 特に本番環境では必須

4. **データ削除を伴う変更は慎重に**
   - バックアップ取得後に実行

### やるべきこと ✅

1. **マイグレーション前にバックアップ**
2. **開発環境で先にテスト**
3. **ロールバックSQLを準備**
4. **マイグレーション履歴を記録**
5. **チームに事前通知**

---

## 🔮 将来の移行計画

### Phase 2: スケール時（DAU 100+、チーム3人以上）

**Supabase CLI Migration に移行**:

```bash
# 1. Supabase CLI インストール
npm install -g supabase

# 2. プロジェクト初期化
supabase init

# 3. 既存SQLをマイグレーションに変換
cp data/sql/01_create_onsen_master.sql supabase/migrations/20260101000000_create_onsen_master.sql
cp data/sql/02_create_search_cache.sql supabase/migrations/20260101000001_create_search_cache.sql

# 4. 新しいマイグレーション作成
supabase migration new add_review_table

# 5. 適用
supabase db push
```

**移行タイミング**:
- ✅ チーム規模が3人以上になった時
- ✅ スキーマ変更が週1回以上になった時
- ✅ 複数環境（dev, staging, prod）を管理する必要が出た時
- ✅ CI/CDでマイグレーションを自動化したい時

**移行しない場合**:
- ❌ 個人開発のまま
- ❌ スキーマが安定している
- ❌ テーブル数が5個以下

---

## 📚 参考リンク

- **Supabase Migrations**: https://supabase.com/docs/guides/cli/local-development#database-migrations
- **Supabase CLI**: https://supabase.com/docs/guides/cli
- **PostgreSQL Backup**: https://www.postgresql.org/docs/current/backup-dump.html

---

## 🤝 チーム開発時のワークフロー

### 1. 新機能開発者

```bash
# 1. ブランチ作成
git checkout -b feature/add-review

# 2. マイグレーション作成
# data/sql/04_add_review_table.sql

# 3. ローカルDBで実行
# Supabase SQL Editorで実行

# 4. コミット
git add data/sql/04_add_review_table.sql
git add data/sql/04_rollback_add_review_table.sql
git add data/sql/README.md
git commit -m "Add review table migration"

# 5. プルリクエスト
git push origin feature/add-review
```

### 2. レビュアー

```bash
# 1. ブランチをチェックアウト
git checkout feature/add-review

# 2. マイグレーションSQLをレビュー
cat data/sql/04_add_review_table.sql

# 3. ローカルで実行テスト
# Supabase SQL Editorで実行

# 4. 問題なければマージ
```

### 3. 他のメンバー

```bash
# 1. mainブランチをpull
git pull origin main

# 2. 新しいマイグレーションを確認
cat data/sql/README.md

# 3. 自分のローカルDBに適用
# Supabase SQL Editorで data/sql/04_add_review_table.sql を実行
```

---

**現在のYURIFTプロジェクトでは、このシンプルなアプローチで十分です。**

スケール時に Supabase CLI への移行を検討してください。
