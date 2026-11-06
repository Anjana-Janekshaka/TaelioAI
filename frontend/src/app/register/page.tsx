"use client";

import { Suspense } from "react";
import Link from "next/link";
import AuthShell from "@/components/site/AuthShell";
import EmailSignIn from "@/components/site/EmailSignIn";

export default function RegisterPage() {
  return (
    <AuthShell title="Start your first book" lede="Create a free account with just your email. You'll be writing in under a minute.">
      <div className="mb-6 flex items-center justify-between rounded-card border border-rule bg-paper px-4 py-3">
        <div>
          <p className="font-semibold">Free plan</p>
          <p className="text-sm text-ink-mute">Ideas, stories and revisions in all eight genres</p>
        </div>
        <Link href="/select-tier" className="text-sm font-semibold underline underline-offset-2">See plans</Link>
      </div>
      <Suspense>
        <EmailSignIn submitLabel="Create account" busyLabel="Creating your account…" />
      </Suspense>
      <p className="mt-8 text-ink-soft">
        Already have an account?{" "}
        <Link href="/login" className="font-semibold text-ink underline underline-offset-2">Sign in</Link>
      </p>
    </AuthShell>
  );
}
