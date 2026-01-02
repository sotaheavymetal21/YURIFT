"use client";

import { motion } from "framer-motion";
import { useDriftStore } from "@/lib/store";
import type { SensationChoice } from "@/types";

const SENSATIONS: SensationChoice[] = [
  "トロトロ",
  "ビリビリ",
  "シャキッ",
  "プンプン",
  "シュワシュワ",
  "ドロドロ",
  "スースー",
  "おまかせ",
];

// Sensation説明文
const SENSATION_DESCRIPTIONS: Record<SensationChoice, string> = {
  トロトロ: "美肌効果のあるとろみのある温泉",
  ビリビリ: "電気風呂や刺激的な炭酸泉",
  シャキッ: "爽快感のある冷泉や水風呂",
  プンプン: "硫黄の香りが漂う温泉街",
  シュワシュワ: "微炭酸の気泡が心地よい",
  ドロドロ: "濁り湯や泥パック温泉",
  スースー: "メントール配合の清涼感",
  おまかせ: "お好みの温泉をおまかせ",
};

export const SensationSelector = () => {
  const { selectedSensations, toggleSensation } = useDriftStore();

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold gradient-text">
          Sensation を選ぶ
        </h2>
        <span className="text-sm text-soft-gray">
          {selectedSensations.length} / 4 選択中
        </span>
      </div>

      <p className="text-sm text-soft-gray">
        求める温泉の感覚を1〜4つ選んでください
      </p>

      <motion.div
        className="grid grid-cols-2 md:grid-cols-4 gap-3"
        initial="hidden"
        animate="visible"
        variants={{
          hidden: { opacity: 0 },
          visible: {
            opacity: 1,
            transition: {
              staggerChildren: 0.05,
            },
          },
        }}
      >
        {SENSATIONS.map((sensation) => {
          const isSelected = selectedSensations.includes(sensation);
          const isDisabled = !isSelected && selectedSensations.length >= 4;

          return (
            <motion.button
              key={sensation}
              onClick={() => !isDisabled && toggleSensation(sensation)}
              className={`
                relative flex flex-col items-start gap-1 p-4 rounded-2xl
                transition-all duration-200 cursor-pointer text-left
                ${
                  isSelected
                    ? "bg-gradient-to-br from-vapor-purple to-neon-cyan text-deep-black"
                    : "glass border border-white/10 text-frost-white hover:border-vapor-purple/50"
                }
                ${isDisabled ? "opacity-40 cursor-not-allowed" : ""}
              `}
              variants={{
                hidden: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0 },
              }}
              whileHover={!isDisabled ? { scale: 1.03, y: -2 } : {}}
              whileTap={!isDisabled ? { scale: 0.97 } : {}}
              disabled={isDisabled}
            >
              <span className="text-lg font-bold font-noto">{sensation}</span>
              <span
                className={`text-xs ${
                  isSelected ? "text-deep-black/70" : "text-soft-gray"
                }`}
              >
                {SENSATION_DESCRIPTIONS[sensation]}
              </span>

              {/* 選択インジケーター */}
              {isSelected && (
                <motion.div
                  className="absolute -top-1 -right-1 w-5 h-5 bg-deep-black rounded-full flex items-center justify-center"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 500, damping: 25 }}
                >
                  <span className="text-vapor-purple text-xs">✓</span>
                </motion.div>
              )}

              {/* Ripple effect */}
              {!isDisabled && (
                <motion.span
                  className="absolute inset-0 bg-white/10 rounded-2xl"
                  initial={{ scale: 0, opacity: 0 }}
                  whileTap={{ scale: 2, opacity: [0, 0.3, 0] }}
                  transition={{ duration: 0.6 }}
                />
              )}
            </motion.button>
          );
        })}
      </motion.div>
    </div>
  );
};
