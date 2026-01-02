"use client";

import { motion } from "framer-motion";
import { MapPin, Coins, Navigation } from "lucide-react";
import type { OnsenFacility } from "@/types";
import { Card, Badge } from "@/components/atoms";

interface DiscoveryCardProps {
  facility: OnsenFacility;
  index: number;
}

export const DiscoveryCard = ({ facility, index }: DiscoveryCardProps) => {
  const openMap = () => {
    const url = `https://www.google.com/maps/search/?api=1&query=${facility.lat},${facility.lng}`;
    window.open(url, "_blank");
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 50, rotateX: 20 }}
      animate={{ opacity: 1, y: 0, rotateX: 0 }}
      transition={{
        duration: 0.6,
        delay: index * 0.15,
        type: "spring",
        stiffness: 100,
      }}
      whileHover={{ y: -8, scale: 1.02 }}
      style={{ perspective: "1000px" }}
    >
      <Card variant="glow" className="relative overflow-hidden group cursor-pointer">
        {/* ランキングバッジ */}
        <motion.div
          className="absolute -top-3 -left-3 w-16 h-16 bg-gradient-to-br from-neon-cyan to-vapor-purple rounded-full flex items-center justify-center font-bold text-2xl text-deep-black z-10"
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ delay: index * 0.15 + 0.3, type: "spring" }}
        >
          {index + 1}
        </motion.div>

        {/* スコアバッジ */}
        <div className="absolute top-4 right-4">
          <Badge variant="neon" className="font-mono">
            {facility.score.toFixed(0)} pts
          </Badge>
        </div>

        <div className="space-y-4 pt-4">
          {/* 施設名 */}
          <div>
            <h3 className="text-2xl font-bold text-frost-white font-noto mb-2">
              {facility.name}
            </h3>
            <p className="text-sm text-vapor-purple italic font-outfit">
              {facility.catchphrase}
            </p>
          </div>

          {/* 情報 */}
          <div className="space-y-2">
            {/* 住所 */}
            <div className="flex items-start gap-2 text-sm">
              <MapPin className="w-4 h-4 text-neon-cyan flex-shrink-0 mt-0.5" />
              <span className="text-soft-gray">{facility.address}</span>
            </div>

            {/* 料金 */}
            <div className="flex items-center gap-2 text-sm">
              <Coins className="w-4 h-4 text-neon-cyan flex-shrink-0" />
              <span className="text-frost-white font-semibold">
                ¥{facility.price.toLocaleString()}
              </span>
            </div>

            {/* 距離 */}
            <div className="flex items-center gap-2 text-sm">
              <Navigation className="w-4 h-4 text-vapor-purple flex-shrink-0" />
              <span className="text-soft-gray">
                あなたから {facility.distance_km} km
              </span>
            </div>
          </div>

          {/* マップボタン */}
          <motion.button
            onClick={openMap}
            className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-neon-cyan to-vapor-purple text-deep-black font-semibold flex items-center justify-center gap-2"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <MapPin className="w-4 h-4" />
            地図で見る
          </motion.button>
        </div>

        {/* ホバー時のグロー効果 */}
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-neon-cyan/10 to-vapor-purple/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none rounded-3xl"
          initial={false}
        />
      </Card>
    </motion.div>
  );
};
