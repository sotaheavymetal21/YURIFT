# YURIFT（ユリフト）

> **流体的UI × AI × 自前DB** で実現する、月額$0-3の次世代日帰り温泉検索アプリ

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)

## ✨ コンセプト

**"Fluid Flow & Deep Immersion"（流体と没入）**

検索フォームを全廃し、ユーザーの直感（画像・オノマトペ）だけを頼りに、最適な「日帰り温泉」へ漂流（Drift）させる新体験。

### 特徴

- 🎨 **ヌルヌル動くモダンUI**: Framer Motion + Tailwind CSS
- 🤖 **AIキャッチコピー生成**: OpenAI API（最小使用）
- 🏔️ **自前温泉データベース**: 外部API依存ゼロで超低コスト
- ⚡️ **FastAPI + Next.js**: フルスタック学習に最適
- 💰 **月額$0-3**: 個人開発として完全に実現可能

---

## 🏗️ アーキテクチャ

### システム構成

```
┌─────────────────┐
│  Next.js (App)  │ ← Vercel Edge (無料)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI        │ ← Vercel Serverless (無料)
│  - ルール検索   │
│  - 距離計算     │
│  - AI連携       │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  External Services          │
│  ┌────────────────────────┐ │
│  │ Supabase (無料)        │ │
│  │ - 温泉マスタDB         │ │
│  │ - キャッシュDB         │ │
│  └────────────────────────┘ │
│  ┌────────────────────────┐ │
│  │ OpenAI (月$0-3)        │ │
│  │ - キャッチコピーのみ   │ │
│  └────────────────────────┘ │
│  ┌────────────────────────┐ │
│  │ Upstash Redis (無料)   │ │
│  │ - Rate Limiting        │ │
│  └────────────────────────┘ │
└─────────────────────────────┘
```

### コスト内訳

| サービス       | プラン       | 月額        |
| -------------- | ------------ | ----------- |
| Vercel         | Hobby        | $0          |
| Supabase       | Free         | $0          |
| Upstash Redis  | Free         | $0          |
| **OpenAI API** | **従量課金** | **$0-3**    |
| **合計**       |              | **$0-3** 🎉 |

---

## 📋 必要な技術スタック

### フロントエンド

- **Framework**: Next.js 15 (App Router, TypeScript)
- **Styling**: Tailwind CSS
- **Animation**: Framer Motion
- **State**: Zustand
- **Icons**: Lucide React

### バックエンド

- **Framework**: FastAPI (Python 3.11+)
- **AI**: OpenAI API (GPT-4o-mini)
- **Database**: Supabase (PostgreSQL)
- **Cache**: Upstash Redis
- **Deploy**: Vercel (Serverless Functions)

---

## 🚀 クイックスタート

**⚡ 5分で起動**: [QUICKSTART.md](QUICKSTART.md) を参照

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/yurift.git
cd yurift
```

### 2. 環境変数の設定

```bash
cp .env.local.example .env.local
```

`.env.local` を編集:

```env
# Frontend
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# Backend
OPENAI_API_KEY=sk-...
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

### 3. 依存関係のインストール

**フロントエンド:**

```bash
npm install
```

**バックエンド:**

```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. 温泉データの準備

```bash
# 1. Supabaseテーブル作成
# docs/データベース設計書_超低コスト版.md の SQLを実行

# 2. 温泉データ収集（Google Sheetsなど）
# docs/実装優先順位クイックガイド_超低コスト版.md 参照

# 3. インポート
cd data/scripts
python import_to_supabase.py
```

### 5. 開発サーバー起動

**フロントエンド:**

```bash
npm run dev
# → http://localhost:3000
```

**バックエンド:**

```bash
cd api
uvicorn main:app --reload --port 8000
# → http://localhost:8000
```

---

## 🎯 実装の進め方

### Phase 0: 基盤構築（Day 1）

- Next.js + FastAPI セットアップ
- Supabaseプロジェクト作成

### Phase 1: データ収集（Day 2）

- 温泉データ100件収集
- Geocoding & インポート

### Phase 2: バックエンド（Day 3-4）

- ルールベース検索エンジン
- 距離計算 (Haversine公式)
- OpenAI キャッチコピー生成

### Phase 3: キャッシュ（Day 5）

- Supabase キャッシュ
- Upstash Rate Limiting

### Phase 4: フロントエンド（Day 6-8）

- Vibe Check UI
- Sensation Check UI
- Loading & Discovery

### Phase 5: デプロイ（Day 9）

- Vercel デプロイ
- 環境変数設定

### Phase 6: 最適化（Day 10）

- パフォーマンス改善
- エラーハンドリング

**総実装時間: 60時間（約7-10営業日）**

詳細は [実装優先順位クイックガイド](docs/実装優先順位クイックガイド_超低コスト版.md) を参照。

---

## 🔧 主な技術的工夫

### 1. コスト削減

**❌ 高コスト版（月$220）:**

- Google Places API: $192/月
- OpenAI大量使用: $28/月

**✅ 超低コスト版（月$0-3）:**

- 自前温泉DB: $0
- OpenAI最小使用: $0-3/月
- ルールベースマッピング: $0

### 2. FastAPIで学ぶポイント

- **距離計算アルゴリズム** (Haversine公式)
- **スコアリングロジック** (キーワードマッチ + 距離)
- **Supabase連携** (PostgreSQL CRUD)
- **非同期処理** (async/await)
- **OpenAI API統合**
- **レート制限実装** (Redis)

### 3. パフォーマンス最適化

- **キャッシュヒット率85%**: 位置情報の粗粒度化
- **バッチ処理**: OpenAI API を3施設まとめて1回
- **インデックス**: lat/lng, prefecture, type

---

## 📊 パフォーマンス目標

| 指標                        | 目標    | 実測見込み |
| --------------------------- | ------- | ---------- |
| API レスポンス (Cache Hit)  | <100ms  | 50-80ms    |
| API レスポンス (Cache Miss) | <2000ms | 800-1500ms |
| Lighthouse Performance      | 80+     | 85-90      |
| 月間コスト (DAU 100)        | <$5     | $0.12-3    |

---

## 🛡️ セキュリティ

### 実装済みセキュリティ対策

- ✅ **Rate Limiting**: 5回/日/IP (Upstash Redis + Sliding Window Counter)
- ✅ **Input Validation**: Pydantic厳格モード + 許可リスト検証
- ✅ **Row Level Security**: Supabase RLS有効（期限切れデータ除外）
- ✅ **API Key管理**: 環境変数 + Pydantic形式バリデーション
- ✅ **CORS**: 環境変数から動的設定（本番は自ドメインのみ）
- ✅ **セキュリティヘッダー**: HSTS, CSP, X-Frame-Options, X-XSS-Protection 等
- ✅ **エラーハンドリング**: 本番環境で詳細を隠蔽
- ✅ **API Docs保護**: 本番環境で無効化
- ✅ **依存関係**: npm audit結果 0 vulnerabilities

### セキュリティスコア

| カテゴリ             | スコア               |
| -------------------- | -------------------- |
| 環境変数管理         | 100% ✅              |
| セキュリティヘッダー | 100% ✅              |
| 依存関係             | 100% ✅              |
| コード品質           | 100% ✅              |
| 総合評価             | **デプロイ準備完了** |

詳細は **[SECURITY_AUDIT_REPORT.md](SECURITY_AUDIT_REPORT.md)** を参照してください。

---

## 🗺️ ロードマップ

### Phase 1: MVP（現在）

- ✅ 基本機能実装
- ✅ 温泉データ100件
- ✅ 超低コスト運用

### Phase 2: 機能拡張

- [ ] ユーザー認証 (Supabase Auth)
- [ ] お気に入り機能
- [ ] 検索履歴
- [ ] ユーザー投稿機能

### Phase 3: スケール

- [ ] PostGIS導入（距離検索高速化）
- [ ] 温泉データ1,000件
- [ ] Cloudflare導入
- [ ] モバイルアプリ (React Native)

---

## 🤝 コントリビューション

温泉データの追加、バグ修正、機能提案など、コントリビューション大歓迎です！

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 ライセンス

MIT License - 自由に使ってください！

---

## 💬 お問い合わせ

- **Issues**: [GitHub Issues](https://github.com/yourusername/yurift/issues)
- **Email**: your-email@example.com
- **Twitter**: [@yourusername](https://twitter.com/yourusername)

---

## 🙏 謝辞

- **OpenAI**: GPT-4o-mini API
- **Vercel**: 素晴らしいホスティング
- **Supabase**: PostgreSQL BaaS
- **Upstash**: Redis サービス
- **温泉データ**: 公開データソース提供者の皆様

---

**Built with ❤️ and ♨️ by [Your Name]**
