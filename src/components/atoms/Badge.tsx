"use client";

import { motion, HTMLMotionProps } from "framer-motion";
import { forwardRef } from "react";

interface BadgeProps extends Omit<HTMLMotionProps<"span">, "children"> {
  variant?: "default" | "selected" | "neon" | "vapor";
  children: React.ReactNode;
}

export const Badge = forwardRef<HTMLSpanElement, BadgeProps>(
  ({ variant = "default", children, className = "", ...props }, ref) => {
    const baseStyles =
      "inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium transition-all duration-200";

    const variantStyles = {
      default: "bg-white/10 text-frost-white border border-white/20",
      selected:
        "bg-gradient-to-r from-neon-cyan to-vapor-purple text-deep-black font-semibold",
      neon: "bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/50 neon-glow",
      vapor: "bg-vapor-purple/20 text-vapor-purple border border-vapor-purple/50",
    };

    return (
      <motion.span
        ref={ref}
        className={`${baseStyles} ${variantStyles[variant]} ${className}`}
        layout
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        transition={{ duration: 0.2 }}
        {...props}
      >
        {children}
      </motion.span>
    );
  }
);

Badge.displayName = "Badge";
