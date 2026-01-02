import { create } from "zustand";
import type { VibeChoice, SensationChoice, OnsenFacility } from "@/types";

interface DriftState {
  // Vibe/Sensation選択
  selectedVibes: VibeChoice[];
  selectedSensations: SensationChoice[];

  // 位置情報
  userLocation: { lat: number; lng: number } | null;

  // 検索結果
  searchResults: OnsenFacility[];
  isSearching: boolean;
  searchError: string | null;

  // アクション
  toggleVibe: (vibe: VibeChoice) => void;
  toggleSensation: (sensation: SensationChoice) => void;
  setUserLocation: (location: { lat: number; lng: number }) => void;
  search: () => Promise<void>;
  reset: () => void;
}

export const useDriftStore = create<DriftState>((set, get) => ({
  // 初期状態
  selectedVibes: [],
  selectedSensations: [],
  userLocation: null,
  searchResults: [],
  isSearching: false,
  searchError: null,

  // Vibe選択トグル（最大3個）
  toggleVibe: (vibe) =>
    set((state) => {
      const isSelected = state.selectedVibes.includes(vibe);

      if (isSelected) {
        // 選択解除
        return {
          selectedVibes: state.selectedVibes.filter((v) => v !== vibe),
        };
      } else {
        // 選択追加（最大3個）
        if (state.selectedVibes.length >= 3) {
          return state; // 既に3個選択済み
        }
        return {
          selectedVibes: [...state.selectedVibes, vibe],
        };
      }
    }),

  // Sensation選択トグル（最大4個）
  toggleSensation: (sensation) =>
    set((state) => {
      const isSelected = state.selectedSensations.includes(sensation);

      if (isSelected) {
        // 選択解除
        return {
          selectedSensations: state.selectedSensations.filter(
            (s) => s !== sensation
          ),
        };
      } else {
        // 選択追加（最大4個）
        if (state.selectedSensations.length >= 4) {
          return state; // 既に4個選択済み
        }
        return {
          selectedSensations: [...state.selectedSensations, sensation],
        };
      }
    }),

  // 位置情報設定
  setUserLocation: (location) =>
    set({
      userLocation: location,
    }),

  // Drift検索実行
  search: async () => {
    const { selectedVibes, selectedSensations, userLocation } = get();

    // バリデーション
    if (selectedVibes.length !== 3) {
      set({
        searchError: "Vibeを3つ選択してください",
      });
      return;
    }

    if (selectedSensations.length === 0) {
      set({
        searchError: "Sensationを1つ以上選択してください",
      });
      return;
    }

    if (!userLocation) {
      set({
        searchError: "位置情報を取得してください",
      });
      return;
    }

    // 検索開始
    set({
      isSearching: true,
      searchError: null,
      searchResults: [],
    });

    try {
      // API呼び出し
      const response = await fetch("/api/drift", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          vibes: selectedVibes,
          sensations: selectedSensations,
          location: userLocation,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "検索に失敗しました");
      }

      const data = await response.json();

      set({
        searchResults: data.facilities,
        isSearching: false,
      });
    } catch (error) {
      set({
        searchError:
          error instanceof Error ? error.message : "検索中にエラーが発生しました",
        isSearching: false,
      });
    }
  },

  // リセット
  reset: () =>
    set({
      selectedVibes: [],
      selectedSensations: [],
      userLocation: null,
      searchResults: [],
      isSearching: false,
      searchError: null,
    }),
}));
