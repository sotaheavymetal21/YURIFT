-- ============================================
-- Migration: {番号}_{説明}
-- Date: YYYY-MM-DD
-- Author: @yourname
-- Description: {詳細な説明を記載}
-- Rollback: {番号}_rollback_{説明}.sql
-- Dependencies: {依存するマイグレーション番号（例: 01, 02）}
-- ============================================

-- ▼▼▼ Migration Start ▼▼▼

-- ========================================
-- 1. テーブル作成
-- ========================================

CREATE TABLE IF NOT EXISTS {table_name} (
    -- 基本カラム
    id BIGSERIAL PRIMARY KEY,

    -- 追加カラムをここに記載
    -- column_name TYPE CONSTRAINT,

    -- メタデータ
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 2. インデックス作成
-- ========================================

-- 検索用インデックス
CREATE INDEX IF NOT EXISTS idx_{table_name}_{column}
    ON {table_name} ({column});

-- 複合インデックス（必要に応じて）
-- CREATE INDEX IF NOT EXISTS idx_{table_name}_{col1}_{col2}
--     ON {table_name} ({col1}, {col2});

-- GINインデックス（配列、JSONB用）
-- CREATE INDEX IF NOT EXISTS idx_{table_name}_{jsonb_column}
--     ON {table_name} USING GIN ({jsonb_column});

-- ========================================
-- 3. 制約追加
-- ========================================

-- 外部キー制約
-- ALTER TABLE {table_name}
--     ADD CONSTRAINT fk_{table_name}_{ref_table}
--     FOREIGN KEY ({column}) REFERENCES {ref_table}(id)
--     ON DELETE CASCADE;

-- ユニーク制約
-- ALTER TABLE {table_name}
--     ADD CONSTRAINT uq_{table_name}_{column}
--     UNIQUE ({column});

-- チェック制約
-- ALTER TABLE {table_name}
--     ADD CONSTRAINT chk_{table_name}_{column}
--     CHECK ({column} >= 0);

-- ========================================
-- 4. トリガー作成
-- ========================================

-- updated_at 自動更新トリガー
CREATE TRIGGER update_{table_name}_updated_at
    BEFORE UPDATE ON {table_name}
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- カスタムトリガー（必要に応じて）
-- CREATE OR REPLACE FUNCTION {function_name}()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     -- トリガーロジック
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;
--
-- CREATE TRIGGER {trigger_name}
--     AFTER INSERT ON {table_name}
--     FOR EACH ROW
--     EXECUTE FUNCTION {function_name}();

-- ========================================
-- 5. RLS (Row Level Security) 設定
-- ========================================

-- RLS有効化
ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;

-- SELECT ポリシー（全ユーザーが読み取り可能）
CREATE POLICY {table_name}_select ON {table_name}
    FOR SELECT
    USING (true);

-- INSERT ポリシー（認証済みユーザーのみ）
-- CREATE POLICY {table_name}_insert ON {table_name}
--     FOR INSERT
--     WITH CHECK (auth.uid() = user_id);

-- UPDATE ポリシー（自分のデータのみ更新可能）
-- CREATE POLICY {table_name}_update ON {table_name}
--     FOR UPDATE
--     USING (auth.uid() = user_id)
--     WITH CHECK (auth.uid() = user_id);

-- DELETE ポリシー（自分のデータのみ削除可能）
-- CREATE POLICY {table_name}_delete ON {table_name}
--     FOR DELETE
--     USING (auth.uid() = user_id);

-- ========================================
-- 6. コメント追加（ドキュメント）
-- ========================================

COMMENT ON TABLE {table_name} IS '{テーブルの説明}';
COMMENT ON COLUMN {table_name}.id IS '主キー（自動採番）';
-- COMMENT ON COLUMN {table_name}.{column} IS '{カラムの説明}';

-- ========================================
-- 7. 初期データ投入（必要に応じて）
-- ========================================

-- INSERT INTO {table_name} (column1, column2) VALUES
--     ('value1', 'value2'),
--     ('value3', 'value4');

-- ▲▲▲ Migration End ▲▲▲

-- ============================================
-- Verification (実行後の確認用クエリ)
-- ============================================

-- テーブル存在確認
-- SELECT EXISTS (
--     SELECT FROM information_schema.tables
--     WHERE table_schema = 'public'
--     AND table_name = '{table_name}'
-- );

-- テーブル構造確認
-- \d {table_name}

-- インデックス確認
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = '{table_name}';

-- RLSポリシー確認
-- SELECT * FROM pg_policies WHERE tablename = '{table_name}';

-- データ確認
-- SELECT COUNT(*) FROM {table_name};
-- SELECT * FROM {table_name} LIMIT 5;

-- ============================================
-- Notes
-- ============================================
-- - このマイグレーションを実行する前にバックアップを取得してください
-- - 本番環境での実行前に開発環境でテストしてください
-- - ロールバックSQLを必ず作成してください
-- ============================================
