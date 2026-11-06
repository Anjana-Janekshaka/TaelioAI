"use client";

import Link from "next/link";
import { ArrowRight, Check } from "lucide-react";
import SiteHeader from "@/components/site/SiteHeader";
import SiteFooter from "@/components/site/SiteFooter";
import { useAuth } from "@/contexts/AuthContext";

const SHARED = [
  "Story ideas from a spark: title, outline, characters, setting",
  "Full stories, written as you watch",
  "Revisions in plain words, with undo",
  "All eight genres and tones",
  "Download as .txt or .md, or print",
];

export default function PlansPage() {
  const { isAuthenticated, user } = useAuth();
  const onFree = isAuthenticated && user?.role !== "pro" && user?.role !== "admin";

  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader variant="bar" />
      <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-16 sm:px-6 lg:py-24">
        <h1 className="font-display text-4xl font-bold leading-tight md:text-5xl">Plans</h1>
        <p className="mt-3 max-w-2xl text-lg text-ink-soft">
          Every plan includes the whole pipeline. Plans differ only in how many requests you can make each minute.
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-2">
          {/* Free */}
          <section className="flex flex-col overflow-hidden rounded-card bg-sheet shadow-book" aria-labelledby="plan-free">
            <div className="band-fill flex items-end justify-between px-6 py-5 text-ink [--band:#e8641c]">
              <h2 id="plan-free" className="caps text-2xl font-bold">Free</h2>
              <p className="caps text-sm font-bold">Available now</p>
            </div>
            <div className="flex flex-1 flex-col border-t-[3px] border-white p-6">
              <p className="tnum font-display text-3xl font-bold">
                About 2 <span className="font-sans text-lg font-semibold text-ink-soft">requests a minute</span>
              </p>
              <ul className="mt-6 flex-1 space-y-3">
                {SHARED.map((f) => (
                  <li key={f} className="flex gap-3">
                    <Check className="mt-0.5 h-5 w-5 flex-none text-genre-fantasy" aria-hidden />
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
              {onFree ? (
                <p className="mt-8 rounded-card bg-paper px-4 py-3 text-center font-semibold">You&rsquo;re on this plan</p>
              ) : (
                <Link href={isAuthenticated ? "/studio" : "/register"} className="btn-primary mt-8 py-3 text-base">
                  {isAuthenticated ? "Open the studio" : "Start for free"} <ArrowRight className="h-5 w-5" aria-hidden />
                </Link>
              )}
            </div>
          </section>

          {/* Pro */}
          <section className="flex flex-col overflow-hidden rounded-card bg-sheet shadow-lift" aria-labelledby="plan-pro">
            <div className="band-fill flex items-end justify-between px-6 py-5 text-white [--band:#151515]">
              <h2 id="plan-pro" className="caps text-2xl font-bold">Pro</h2>
              <p className="caps text-sm font-bold opacity-80">Coming soon</p>
            </div>
            <div className="flex flex-1 flex-col border-t-[3px] border-white p-6">
              <p className="tnum font-display text-3xl font-bold">
                About 10 <span className="font-sans text-lg font-semibold text-ink-soft">requests a minute</span>
              </p>
              <ul className="mt-6 flex-1 space-y-3">
                <li className="flex gap-3">
                  <Check className="mt-0.5 h-5 w-5 flex-none text-genre-fantasy" aria-hidden />
                  <span>Everything in Free</span>
                </li>
                <li className="flex gap-3">
                  <Check className="mt-0.5 h-5 w-5 flex-none text-genre-fantasy" aria-hidden />
                  <span>Five times the request rate, for longer writing sessions</span>
                </li>
              </ul>
              <p className="mt-8 rounded-card border border-dashed border-ink/25 px-4 py-3 text-center text-ink-soft">
                Pro isn&rsquo;t available to sign up for yet.
              </p>
            </div>
          </section>
        </div>
      </main>
      <SiteFooter />
    </div>
  );
}
