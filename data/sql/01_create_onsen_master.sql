-- ============================================
-- Migration: 01_create_onsen_master
-- Date: 2026-01-02
-- Author: @yurift
-- Description: 日帰り温泉施設の基本情報を格納するマスターテーブル作成
-- Rollback: 01_rollback_create_onsen_master.sql
-- Dependencies: なし（初期マイグレーション）
-- ============================================

-- ▼▼▼ Migration Start ▼▼▼

-- ========================================
-- 1. テーブル作成
-- ========================================

CREATE TABLE IF NOT EXISTS onsen_master (
    -- 基本情報
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,

    -- 位置情報（必須）
    lat DOUBLE PRECISION NOT NULL CHECK (lat >= -90 AND lat <= 90),
    lng DOUBLE PRECISION NOT NULL CHECK (lng >= -180 AND lng <= 180),

    -- 料金情報
    price INTEGER NOT NULL CHECK (price >= 0),

    -- 検索用キーワード
    keywords TEXT[] DEFAULT '{}',

    -- メタデータ
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- ========================================
-- 2. インデックス作成
-- ========================================

-- 位置情報検索用（距離計算の高速化）
CREATE INDEX IF NOT EXISTS idx_onsen_location ON onsen_master (lat, lng);

-- キーワード検索用（GINインデックス）
CREATE INDEX IF NOT EXISTS idx_onsen_keywords ON onsen_master USING GIN (keywords);

-- 料金ソート用
CREATE INDEX IF NOT EXISTS idx_onsen_price ON onsen_master (price);

-- ========================================
-- 3. トリガー作成
-- ========================================

-- updated_at 自動更新のトリガー関数（共通）
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- トリガー設定
CREATE TRIGGER update_onsen_master_updated_at
    BEFORE UPDATE ON onsen_master
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- 4. コメント追加（ドキュメント）
-- ========================================
COMMENT ON TABLE onsen_master IS '日帰り温泉施設マスターテーブル';
COMMENT ON COLUMN onsen_master.id IS '施設ID';
COMMENT ON COLUMN onsen_master.name IS '施設名';
COMMENT ON COLUMN onsen_master.address IS '住所';
COMMENT ON COLUMN onsen_master.lat IS '緯度';
COMMENT ON COLUMN onsen_master.lng IS '経度';
COMMENT ON COLUMN onsen_master.price IS '料金（円）';
COMMENT ON COLUMN onsen_master.keywords IS '検索用キーワード（配列）';
COMMENT ON COLUMN onsen_master.created_at IS '作成日時';
COMMENT ON COLUMN onsen_master.updated_at IS '更新日時（自動更新）';

-- ▲▲▲ Migration End ▲▲▲

-- ============================================
-- Verification (実行後の確認用クエリ)
-- ============================================

-- テーブル存在確認
-- SELECT EXISTS (
--     SELECT FROM information_schema.tables
--     WHERE table_schema = 'public'
--     AND table_name = 'onsen_master'
-- );

-- テーブル構造確認
-- \d onsen_master

-- インデックス確認
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = 'onsen_master';

-- データ確認
-- SELECT COUNT(*) FROM onsen_master;

-- ============================================
-- Notes
-- ============================================
-- - このテーブルは YURIFT の中核となるマスターテーブルです
-- - keywords 配列には Vibe/Sensation マッピングキーワードを格納
-- - lat/lng は距離計算（Haversine公式）に使用
-- ============================================
