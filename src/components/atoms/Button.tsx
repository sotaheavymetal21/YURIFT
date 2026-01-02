"use client";

import { motion, HTMLMotionProps } from "framer-motion";
import { forwardRef } from "react";

interface ButtonProps extends Omit<HTMLMotionProps<"button">, "children"> {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  children: React.ReactNode;
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { variant = "primary", size = "md", children, isLoading, className = "", ...props },
    ref
  ) => {
    const baseStyles =
      "font-outfit font-semibold rounded-2xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden";

    const variantStyles = {
      primary:
        "bg-gradient-to-r from-neon-cyan to-vapor-purple text-deep-black hover:shadow-lg hover:shadow-neon-cyan/50",
      secondary:
        "bg-charcoal-gray text-frost-white border-2 border-neon-cyan/30 hover:border-neon-cyan hover:shadow-lg hover:shadow-neon-cyan/30",
      ghost:
        "bg-transparent text-frost-white hover:bg-white/5 border border-white/10 hover:border-white/20",
    };

    const sizeStyles = {
      sm: "px-4 py-2 text-sm",
      md: "px-6 py-3 text-base",
      lg: "px-8 py-4 text-lg",
    };

    return (
      <motion.button
        ref={ref}
        className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        disabled={isLoading}
        {...props}
      >
        {isLoading ? (
          <motion.div
            className="flex items-center justify-center gap-2"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <motion.div
              className="w-4 h-4 border-2 border-current border-t-transparent rounded-full"
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            />
            <span>読み込み中...</span>
          </motion.div>
        ) : (
          children
        )}

        {/* Ripple effect */}
        <motion.span
          className="absolute inset-0 bg-white/20"
          initial={{ scale: 0, opacity: 0 }}
          whileTap={{ scale: 2, opacity: [0, 0.3, 0] }}
          transition={{ duration: 0.6 }}
        />
      </motion.button>
    );
  }
);

Button.displayName = "Button";
