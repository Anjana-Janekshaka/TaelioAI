"use client";

import { Suspense } from "react";
import Link from "next/link";
import AuthShell from "@/components/site/AuthShell";
import EmailSignIn from "@/components/site/EmailSignIn";

export default function LoginPage() {
  return (
    <AuthShell title="Welcome back" lede="Sign in with your email to pick up where you left off.">
      <Suspense>
        <EmailSignIn submitLabel="Sign in" busyLabel="Signing in…" />
      </Suspense>
      <p className="mt-8 text-ink-soft">
        New to TaelioAI?{" "}
        <Link href="/register" className="font-semibold text-ink underline underline-offset-2">Create an account</Link>
      </p>
    </AuthShell>
  );
}
