"use client";

import { motion } from "framer-motion";

interface LoadingProps {
  size?: "sm" | "md" | "lg";
  text?: string;
}

export const Loading = ({ size = "md", text }: LoadingProps) => {
  const sizeStyles = {
    sm: "w-6 h-6",
    md: "w-12 h-12",
    lg: "w-16 h-16",
  };

  const dotSize = {
    sm: "w-2 h-2",
    md: "w-3 h-3",
    lg: "w-4 h-4",
  };

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <div className="relative flex items-center justify-center">
        {/* Outer ring */}
        <motion.div
          className={`${sizeStyles[size]} rounded-full border-2 border-neon-cyan/30 border-t-neon-cyan`}
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />

        {/* Inner ring */}
        <motion.div
          className={`absolute ${sizeStyles[size]} rounded-full border-2 border-vapor-purple/30 border-b-vapor-purple`}
          animate={{ rotate: -360 }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
        />

        {/* Center dot */}
        <motion.div
          className={`absolute ${dotSize[size]} rounded-full bg-gradient-to-r from-neon-cyan to-vapor-purple`}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [1, 0.8, 1],
          }}
          transition={{ duration: 1, repeat: Infinity }}
        />
      </div>

      {text && (
        <motion.p
          className="text-sm text-soft-gray font-noto"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          {text}
        </motion.p>
      )}
    </div>
  );
};
