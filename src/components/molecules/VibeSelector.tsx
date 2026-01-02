"use client";

import { motion } from "framer-motion";
import { useDriftStore } from "@/lib/store";
import type { VibeChoice } from "@/types";
import {
  Trees,
  Building2,
  Snowflake,
  Flame,
  Sparkles,
  Box,
  Waves,
  Mountain,
  Sunrise,
  Sunset,
  User,
  Users,
} from "lucide-react";

// Vibeアイコンマッピング
const VIBE_ICONS: Record<VibeChoice, React.ComponentType<any>> = {
  forest: Trees,
  city: Building2,
  snow: Snowflake,
  bonfire: Flame,
  hinoki: Sparkles,
  concrete: Box,
  ocean: Waves,
  cave: Mountain,
  morning: Sunrise,
  sunset: Sunset,
  solo: User,
  party: Users,
};

// Vibe日本語ラベル
const VIBE_LABELS: Record<VibeChoice, string> = {
  forest: "森",
  city: "都会",
  snow: "雪",
  bonfire: "焚き火",
  hinoki: "檜",
  concrete: "コンクリート",
  ocean: "海",
  cave: "洞窟",
  morning: "朝",
  sunset: "夕日",
  solo: "一人",
  party: "グループ",
};

const VIBES: VibeChoice[] = [
  "forest",
  "city",
  "snow",
  "bonfire",
  "hinoki",
  "concrete",
  "ocean",
  "cave",
  "morning",
  "sunset",
  "solo",
  "party",
];

export const VibeSelector = () => {
  const { selectedVibes, toggleVibe } = useDriftStore();

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold gradient-text">
          Vibe を選ぶ
        </h2>
        <span className="text-sm text-soft-gray">
          {selectedVibes.length} / 3 選択中
        </span>
      </div>

      <p className="text-sm text-soft-gray">
        今日の気分に合うVibeを3つ選んでください
      </p>

      <motion.div
        className="grid grid-cols-3 md:grid-cols-4 gap-3"
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
        {VIBES.map((vibe) => {
          const Icon = VIBE_ICONS[vibe];
          const isSelected = selectedVibes.includes(vibe);
          const isDisabled = !isSelected && selectedVibes.length >= 3;

          return (
            <motion.button
              key={vibe}
              onClick={() => !isDisabled && toggleVibe(vibe)}
              className={`
                relative flex flex-col items-center justify-center gap-2 p-4 rounded-2xl
                transition-all duration-200 cursor-pointer
                ${
                  isSelected
                    ? "bg-gradient-to-br from-neon-cyan to-vapor-purple text-deep-black"
                    : "glass border border-white/10 text-frost-white hover:border-neon-cyan/50"
                }
                ${isDisabled ? "opacity-40 cursor-not-allowed" : ""}
              `}
              variants={{
                hidden: { opacity: 0, scale: 0.8 },
                visible: { opacity: 1, scale: 1 },
              }}
              whileHover={!isDisabled ? { scale: 1.05, y: -2 } : {}}
              whileTap={!isDisabled ? { scale: 0.95 } : {}}
              disabled={isDisabled}
            >
              <Icon className="w-6 h-6" />
              <span className="text-xs font-medium">{VIBE_LABELS[vibe]}</span>

              {/* 選択インジケーター */}
              {isSelected && (
                <motion.div
                  className="absolute -top-1 -right-1 w-5 h-5 bg-deep-black rounded-full flex items-center justify-center"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 500, damping: 25 }}
                >
                  <span className="text-neon-cyan text-xs">✓</span>
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
