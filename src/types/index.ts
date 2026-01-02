/**
 * 型定義
 */

// Vibe選択肢の型
export type VibeChoice =
  | "forest"
  | "city"
  | "snow"
  | "bonfire"
  | "hinoki"
  | "concrete"
  | "ocean"
  | "cave"
  | "morning"
  | "sunset"
  | "solo"
  | "party";

// Sensation選択肢の型
export type SensationChoice =
  | "トロトロ"
  | "ビリビリ"
  | "シャキッ"
  | "プンプン"
  | "シュワシュワ"
  | "ドロドロ"
  | "スースー"
  | "おまかせ";

// 位置情報
export interface Location {
  lat: number;
  lng: number;
}

// Drift検索リクエスト
export interface DriftRequest {
  vibes: [VibeChoice, VibeChoice, VibeChoice]; // 必ず3個
  sensations: SensationChoice[]; // 1-4個
  location: Location;
}

// 温泉施設情報
export interface OnsenFacility {
  id: number;
  name: string;
  address: string;
  lat: number;
  lng: number;
  price: number;
  distance_km: number;
  catchphrase: string;
  score: number;
}

// Drift検索レスポンス
export interface DriftResponse {
  facilities: OnsenFacility[];
  cached: boolean;
  search_params: DriftRequest;
}

// エラーレスポンス
export interface ErrorResponse {
  error: string;
  detail?: string;
}
