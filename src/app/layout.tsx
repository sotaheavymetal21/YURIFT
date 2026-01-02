import type { Metadata } from "next";
import { Outfit, Noto_Sans_JP } from "next/font/google";
import "./globals.css";

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
  display: "swap",
});

const notoSansJP = Noto_Sans_JP({
  subsets: ["latin"],
  variable: "--font-noto-sans-jp",
  display: "swap",
  weight: ["400", "500", "700"],
});

export const metadata: Metadata = {
  title: "YURIFT - 超低コスト日帰り温泉検索",
  description:
    "Vibeで選ぶ、新感覚の日帰り温泉検索。AIがあなたの気分に合った温泉を見つけます。",
  openGraph: {
    title: "YURIFT",
    description: "Vibeで選ぶ、新感覚の日帰り温泉検索",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja" className={`${outfit.variable} ${notoSansJP.variable}`}>
      <body className="antialiased bg-deep-black text-frost-white">
        {children}
      </body>
    </html>
  );
}
