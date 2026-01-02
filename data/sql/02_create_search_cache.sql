-- ============================================
-- Migration: 02_create_search_cache
-- Date: 2026-01-02
-- Author: @yurift
-- Description: Drift検索の結果を7日間キャッシュしてOpenAI APIコストを削減
-- Rollback: 02_rollback_create_search_cache.sql
-- Dependencies: なし
-- ============================================

-- ▼▼▼ Migration Start ▼▼▼

-- ========================================
-- 1. テーブル作成
-- ========================================

CREATE TABLE IF NOT EXISTS search_cache (
    -- キャッシュキー（ハッシュ値）
    cache_key TEXT PRIMARY KEY,

    -- 検索パラメータ（JSON）
    search_params JSONB NOT NULL,

    -- 検索結果（JSON）
    result JSONB NOT NULL,

    -- メタデータ
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ NOT NULL
);

-- ========================================
-- 2. インデックス作成
-- ========================================

-- 期限切れキャッシュ削除用
CREATE INDEX IF NOT EXISTS idx_cache_expires ON search_cache (expires_at);

-- 検索パラメータ検索用（GINインデックス）
CREATE INDEX IF NOT EXISTS idx_cache_params ON search_cache USING GIN (search_params);

-- ========================================
-- 3. RLS (Row Level Security) 設定
-- ========================================

-- RLS有効化
ALTER TABLE search_cache ENABLE ROW LEVEL SECURITY;

-- 期限切れデータは読み取り不可
CREATE POLICY cache_valid_reads ON search_cache
    FOR SELECT
    USING (expires_at > CURRENT_TIMESTAMP);

-- 挿入ポリシー（全ユーザーが挿入可能、サービスロールキー使用時）
CREATE POLICY cache_insert ON search_cache
    FOR INSERT
    WITH CHECK (true);

-- ========================================
-- 4. コメント追加（ドキュメント）
-- ========================================
COMMENT ON TABLE search_cache IS 'Drift検索結果キャッシュテーブル（TTL: 7日間）';
COMMENT ON COLUMN search_cache.cache_key IS 'キャッシュキー（search_paramsのハッシュ値）';
COMMENT ON COLUMN search_cache.search_params IS '検索パラメータ（JSON）';
COMMENT ON COLUMN search_cache.result IS '検索結果（JSON）';
COMMENT ON COLUMN search_cache.expires_at IS 'キャッシュ有効期限';
COMMENT ON COLUMN search_cache.created_at IS '作成日時';

-- ▲▲▲ Migration End ▲▲▲

-- ============================================
-- Verification (実行後の確認用クエリ)
-- ============================================

-- テーブル存在確認
-- SELECT EXISTS (
--     SELECT FROM information_schema.tables
--     WHERE table_schema = 'public'
--     AND table_name = 'search_cache'
-- );

-- テーブル構造確認
-- \d search_cache

-- RLSポリシー確認
-- SELECT * FROM pg_policies WHERE tablename = 'search_cache';

-- インデックス確認
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = 'search_cache';

-- ============================================
-- Notes
-- ============================================
-- - TTL: 7日間（expires_at で管理）
-- - RLSポリシーにより期限切れデータは自動的に読み取り不可
-- - キャッシュヒット率目標: 85%
-- - 位置情報は粗粒度化してキャッシュキーを生成
-- ============================================
