"use client";

import { motion } from "framer-motion";
import { useEffect, useCallback } from "react";
import { useDriftStore } from "@/lib/store";
import { VibeSelector } from "@/components/molecules/VibeSelector";
import { SensationSelector } from "@/components/molecules/SensationSelector";
import { Button, Card } from "@/components/atoms";
import { MapPin, Compass } from "lucide-react";

export const VibeCheck = () => {
  const {
    selectedVibes,
    selectedSensations,
    userLocation,
    setUserLocation,
    search,
    searchResults,
  } = useDriftStore();

  // 位置情報取得
  const getLocation = useCallback(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
        },
        () => {
          // エラー時はデフォルト位置（東京駅）を設定
          setUserLocation({
            lat: 35.6812,
            lng: 139.7671,
          });
        }
      );
    }
  }, [setUserLocation]);

  // 初回マウント時に位置情報取得
  useEffect(() => {
    if (!userLocation) {
      getLocation();
    }
  }, [userLocation, getLocation]);

  // 検索可能かチェック
  const canSearch =
    selectedVibes.length === 3 &&
    selectedSensations.length >= 1 &&
    userLocation !== null;

  // 検索結果が表示されている場合は非表示
  if (searchResults.length > 0) {
    return null;
  }

  return (
    <motion.div
      className="space-y-8"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      {/* ヘッダー */}
      <div className="text-center space-y-4">
        <motion.h1
          className="text-5xl md:text-6xl font-bold gradient-text"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          YURIFT
        </motion.h1>
        <motion.p
          className="text-lg text-soft-gray font-noto"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          Vibeで選ぶ、新感覚の日帰り温泉検索
        </motion.p>
      </div>

      {/* Vibe選択 */}
      <Card variant="glass">
        <VibeSelector />
      </Card>

      {/* Sensation選択 */}
      <Card variant="glass">
        <SensationSelector />
      </Card>

      {/* 位置情報と検索ボタン */}
      <Card variant={userLocation ? "glow" : "glass"}>
        <div className="space-y-4">
          {/* 位置情報 */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MapPin className="w-5 h-5 text-neon-cyan" />
              <span className="text-sm text-soft-gray">
                {userLocation
                  ? `位置情報取得済み (${userLocation.lat.toFixed(
                      4
                    )}, ${userLocation.lng.toFixed(4)})`
                  : "位置情報を取得中..."}
              </span>
            </div>
            <motion.button
              onClick={getLocation}
              className="text-xs text-neon-cyan hover:underline"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              再取得
            </motion.button>
          </div>

          {/* 検索ボタン */}
          <Button
            variant="primary"
            size="lg"
            className="w-full"
            disabled={!canSearch}
            onClick={search}
          >
            <Compass className="w-5 h-5" />
            <span>Drift を開始</span>
          </Button>

          {/* ヒント */}
          {!canSearch && (
            <motion.p
              className="text-xs text-center text-soft-gray"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              {selectedVibes.length < 3 && "Vibeを3つ選択してください"}
              {selectedVibes.length === 3 &&
                selectedSensations.length === 0 &&
                "Sensationを1つ以上選択してください"}
              {selectedVibes.length === 3 &&
                selectedSensations.length >= 1 &&
                !userLocation &&
                "位置情報を取得しています..."}
            </motion.p>
          )}
        </div>
      </Card>
    </motion.div>
  );
};
