"use client";

import { motion, HTMLMotionProps } from "framer-motion";
import { forwardRef } from "react";

interface CardProps extends HTMLMotionProps<"div"> {
  variant?: "default" | "glass" | "glow";
  children: React.ReactNode;
}

export const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ variant = "glass", children, className = "", ...props }, ref) => {
    const baseStyles = "rounded-3xl p-6";

    const variantStyles = {
      default: "bg-charcoal-gray border border-white/10",
      glass: "glass backdrop-blur-xl bg-white/5 border border-white/10",
      glow: "glass backdrop-blur-xl bg-white/5 border border-neon-cyan/30 neon-glow",
    };

    return (
      <motion.div
        ref={ref}
        className={`${baseStyles} ${variantStyles[variant]} ${className}`}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        {...props}
      >
        {children}
      </motion.div>
    );
  }
);

Card.displayName = "Card";
