"use client";

import { VibeCheck } from "@/components/organisms/VibeCheck";
import { DiscoveryResults } from "@/components/organisms/DiscoveryResults";

export default function Home() {
  return (
    <main className="min-h-screen bg-deep-black">
      <div className="container mx-auto px-4 py-12 max-w-6xl">
        {/* Vibe Check（検索フォーム） */}
        <VibeCheck />

        {/* Discovery Results（検索結果） */}
        <DiscoveryResults />
      </div>
    </main>
  );
}
