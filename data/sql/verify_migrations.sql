-- ============================================
-- Migration Verification Script
-- ============================================
-- このスクリプトはマイグレーションの適用状態を確認します
-- Supabase SQL Editor で実行してください
-- ============================================

\echo '========================================='
\echo 'YURIFT Migration Verification'
\echo '========================================='
\echo ''

-- ========================================
-- 1. テーブル存在確認
-- ========================================

\echo '▼ 1. テーブル存在確認'
\echo ''

SELECT
    table_name,
    CASE
        WHEN table_name = 'onsen_master' THEN '✅ (01_create_onsen_master)'
        WHEN table_name = 'search_cache' THEN '✅ (02_create_search_cache)'
        ELSE '❓ Unknown table'
    END as migration
FROM information_schema.tables
WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE'
    AND table_name IN ('onsen_master', 'search_cache')
ORDER BY table_name;

\echo ''

-- ========================================
-- 2. インデックス確認
-- ========================================

\echo '▼ 2. インデックス確認'
\echo ''

SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
    AND tablename IN ('onsen_master', 'search_cache')
ORDER BY tablename, indexname;

\echo ''

-- ========================================
-- 3. RLSポリシー確認
-- ========================================

\echo '▼ 3. RLS (Row Level Security) ポリシー確認'
\echo ''

SELECT
    tablename,
    policyname,
    cmd as command,
    qual as using_expression
FROM pg_policies
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

\echo ''

-- ========================================
-- 4. トリガー確認
-- ========================================

\echo '▼ 4. トリガー確認'
\echo ''

SELECT
    event_object_table as table_name,
    trigger_name,
    event_manipulation as event,
    action_timing as timing
FROM information_schema.triggers
WHERE event_object_schema = 'public'
    AND event_object_table IN ('onsen_master', 'search_cache')
ORDER BY event_object_table, trigger_name;

\echo ''

-- ========================================
-- 5. データ件数確認
-- ========================================

\echo '▼ 5. データ件数確認'
\echo ''

SELECT
    'onsen_master' as table_name,
    COUNT(*) as record_count,
    CASE
        WHEN COUNT(*) = 0 THEN '❌ データなし'
        WHEN COUNT(*) = 15 THEN '✅ サンプルデータ投入済み (03_sample_data)'
        WHEN COUNT(*) > 15 THEN '✅ 本番データ投入済み'
        ELSE '⚠️  不完全なデータ'
    END as status
FROM onsen_master

UNION ALL

SELECT
    'search_cache' as table_name,
    COUNT(*) as record_count,
    CASE
        WHEN COUNT(*) = 0 THEN '✅ 初期状態（キャッシュなし）'
        ELSE format('✅ キャッシュ %s 件', COUNT(*))
    END as status
FROM search_cache;

\echo ''

-- ========================================
-- 6. カラム構造確認
-- ========================================

\echo '▼ 6. カラム構造確認 (onsen_master)'
\echo ''

SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
    AND table_name = 'onsen_master'
ORDER BY ordinal_position;

\echo ''

\echo '▼ 7. カラム構造確認 (search_cache)'
\echo ''

SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
    AND table_name = 'search_cache'
ORDER BY ordinal_position;

\echo ''

-- ========================================
-- 8. サンプルデータ確認（onsen_master）
-- ========================================

\echo '▼ 8. サンプルデータ確認 (onsen_master - 最初の3件)'
\echo ''

SELECT
    id,
    name,
    address,
    lat,
    lng,
    price,
    array_length(keywords, 1) as keyword_count
FROM onsen_master
ORDER BY id
LIMIT 3;

\echo ''

-- ========================================
-- 9. 検証サマリー
-- ========================================

\echo '========================================='
\echo '検証サマリー'
\echo '========================================='
\echo ''

WITH verification AS (
    SELECT
        'onsen_master' as migration_name,
        EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'onsen_master'
        ) as is_applied
    UNION ALL
    SELECT
        'search_cache',
        EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = 'search_cache'
        )
    UNION ALL
    SELECT
        'sample_data',
        (SELECT COUNT(*) FROM onsen_master) >= 15
)
SELECT
    migration_name,
    CASE
        WHEN is_applied THEN '✅ Applied'
        ELSE '❌ Not Applied'
    END as status
FROM verification;

\echo ''
\echo '========================================='
\echo '検証完了'
\echo '========================================='
\echo ''
\echo 'すべてのマイグレーションが正しく適用されている場合:'
\echo '  - onsen_master: ✅ Applied'
\echo '  - search_cache: ✅ Applied'
\echo '  - sample_data:  ✅ Applied (開発環境のみ)'
\echo ''
\echo '問題がある場合は data/sql/README.md を確認してください'
\echo '========================================='
