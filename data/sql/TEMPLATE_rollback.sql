-- ============================================
-- Rollback Migration: {番号}_rollback_{説明}
-- Date: YYYY-MM-DD
-- Author: @yourname
-- Description: Rollback for {番号}_{説明}.sql
-- Original Migration: {番号}_{説明}.sql
-- ============================================

-- ⚠️ WARNING: このスクリプトはデータを削除します
-- 実行前に必ずバックアップを取得してください

-- ▼▼▼ Rollback Start ▼▼▼

-- ========================================
-- 1. RLSポリシー削除
-- ========================================

DROP POLICY IF EXISTS {table_name}_select ON {table_name};
DROP POLICY IF EXISTS {table_name}_insert ON {table_name};
DROP POLICY IF EXISTS {table_name}_update ON {table_name};
DROP POLICY IF EXISTS {table_name}_delete ON {table_name};

-- カスタムポリシー削除
-- DROP POLICY IF EXISTS {custom_policy_name} ON {table_name};

-- ========================================
-- 2. トリガー削除
-- ========================================

DROP TRIGGER IF EXISTS update_{table_name}_updated_at ON {table_name};

-- カスタムトリガー削除
-- DROP TRIGGER IF EXISTS {custom_trigger_name} ON {table_name};

-- トリガー関数削除（他のテーブルで使用していない場合のみ）
-- DROP FUNCTION IF EXISTS {function_name}();

-- ========================================
-- 3. インデックス削除
-- ========================================

DROP INDEX IF EXISTS idx_{table_name}_{column};

-- 追加のインデックス削除
-- DROP INDEX IF EXISTS idx_{table_name}_{col1}_{col2};
-- DROP INDEX IF EXISTS idx_{table_name}_{jsonb_column};

-- ========================================
-- 4. 制約削除
-- ========================================

-- 外部キー制約削除
-- ALTER TABLE {table_name}
--     DROP CONSTRAINT IF EXISTS fk_{table_name}_{ref_table};

-- ユニーク制約削除
-- ALTER TABLE {table_name}
--     DROP CONSTRAINT IF EXISTS uq_{table_name}_{column};

-- チェック制約削除
-- ALTER TABLE {table_name}
--     DROP CONSTRAINT IF EXISTS chk_{table_name}_{column};

-- ========================================
-- 5. テーブル削除
-- ========================================

-- CASCADE: 関連する外部キー参照も削除
DROP TABLE IF EXISTS {table_name} CASCADE;

-- ⚠️ データが完全に削除されます
-- RESTRICT を使用すると、依存関係がある場合は削除を拒否
-- DROP TABLE IF EXISTS {table_name} RESTRICT;

-- ========================================
-- 6. カラム削除のみの場合（テーブル全体を削除しない場合）
-- ========================================

-- ALTER TABLE {table_name} DROP COLUMN IF EXISTS {column_name} CASCADE;

-- ========================================
-- 7. データ削除のみの場合
-- ========================================

-- DELETE FROM {table_name} WHERE condition;
-- または
-- TRUNCATE TABLE {table_name} CASCADE;

-- ▲▲▲ Rollback End ▲▲▲

-- ============================================
-- Verification (実行後の確認用クエリ)
-- ============================================

-- テーブルが削除されたことを確認
-- SELECT EXISTS (
--     SELECT FROM information_schema.tables
--     WHERE table_schema = 'public'
--     AND table_name = '{table_name}'
-- );
-- 期待値: false

-- 関連テーブルへの影響確認
-- SELECT * FROM {related_table} LIMIT 5;

-- ============================================
-- Rollback完了後の手順
-- ============================================
-- 1. data/sql/README.md の履歴テーブルを更新
-- 2. ステータスを "🔴 Rolled Back" に変更
-- 3. Gitコミット
--    git add data/sql/{番号}_rollback_{説明}.sql
--    git add data/sql/README.md
--    git commit -m "Rollback: {説明}"
-- ============================================

-- ============================================
-- Notes
-- ============================================
-- - ロールバック実行前に必ずバックアップを取得
-- - 本番環境での実行は特に慎重に
-- - データ損失のリスクを理解した上で実行
-- - チームメンバーに事前通知
-- ============================================
