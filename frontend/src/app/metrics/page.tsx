"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import SiteHeader from "@/components/site/SiteHeader";
import SiteFooter from "@/components/site/SiteFooter";
import ModerationMetrics from "@/components/ModerationMetrics";
import { Spinner } from "@/components/studio/shared";
import { useAuth } from "@/contexts/AuthContext";

export default function MetricsPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) router.replace("/login?next=/metrics");
  }, [isLoading, isAuthenticated, router]);

  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader variant="bar" />
      <main className="flex-1 bg-sheet">
        <div className="mx-auto grid max-w-7xl gap-12 px-4 py-12 sm:px-6 lg:grid-cols-[minmax(0,1fr)_18rem] lg:py-16">
          {isLoading || !isAuthenticated ? (
            <p className="flex items-center gap-3 text-ink-mute"><Spinner /> Loading…</p>
          ) : (
            <ModerationMetrics />
          )}

          <aside className="space-y-8 text-sm leading-relaxed text-ink-soft lg:border-l lg:border-rule lg:pl-8 lg:pt-2">
            <div>
              <h2 className="text-base font-semibold text-ink">How it works</h2>
              <p className="mt-2">
                When TaelioAI&rsquo;s Content Moderator agent reviews a piece of content, it checks for inappropriate
                keywords, safety patterns and quality issues, and the result is recorded here.
              </p>
            </div>
            <div>
              <h2 className="text-base font-semibold text-ink">Safety scores</h2>
              <p className="mt-2">
                Content is scored from 0 to 100; higher is safer. Scores below 70 may need a review, and scores below 50
                are flagged as potentially unsafe.
              </p>
            </div>
          </aside>
        </div>
      </main>
      <SiteFooter />
    </div>
  );
}
