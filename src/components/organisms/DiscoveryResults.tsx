"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useDriftStore } from "@/lib/store";
import { DiscoveryCard } from "./DiscoveryCard";
import { Loading } from "@/components/atoms";
import { RefreshCcw } from "lucide-react";

export const DiscoveryResults = () => {
  const { searchResults, isSearching, searchError, reset } = useDriftStore();

  // 検索中
  if (isSearching) {
    return (
      <motion.div
        className="flex flex-col items-center justify-center py-20"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <Loading size="lg" text="あなたにぴったりの温泉を探しています..." />
      </motion.div>
    );
  }

  // エラー
  if (searchError) {
    return (
      <motion.div
        className="glass rounded-3xl p-8 text-center space-y-4"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
      >
        <p className="text-red-400 text-lg">{searchError}</p>
        <motion.button
          onClick={reset}
          className="px-6 py-3 bg-charcoal-gray rounded-xl text-frost-white flex items-center gap-2 mx-auto"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <RefreshCcw className="w-4 h-4" />
          もう一度試す
        </motion.button>
      </motion.div>
    );
  }

  // 結果なし
  if (searchResults.length === 0) {
    return null;
  }

  // 検索結果表示
  return (
    <motion.div
      className="space-y-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.2 }}
    >
      {/* ヘッダー */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold gradient-text mb-2">
            あなたへのおすすめ
          </h2>
          <p className="text-sm text-soft-gray">
            Vibe/Sensationに基づいて厳選した3つの温泉
          </p>
        </div>

        <motion.button
          onClick={reset}
          className="px-4 py-2 glass rounded-xl text-frost-white flex items-center gap-2 hover:border-neon-cyan/50 transition-colors"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <RefreshCcw className="w-4 h-4" />
          リセット
        </motion.button>
      </div>

      {/* カード一覧 */}
      <AnimatePresence mode="popLayout">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {searchResults.map((facility, index) => (
            <DiscoveryCard
              key={facility.id}
              facility={facility}
              index={index}
            />
          ))}
        </div>
      </AnimatePresence>

      {/* 再検索ボタン */}
      <motion.div
        className="text-center pt-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
      >
        <p className="text-sm text-soft-gray mb-4">
          他の温泉も探してみますか？
        </p>
        <motion.button
          onClick={reset}
          className="px-8 py-3 bg-gradient-to-r from-neon-cyan to-vapor-purple text-deep-black font-semibold rounded-2xl"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          別のVibeで探す
        </motion.button>
      </motion.div>
    </motion.div>
  );
};
