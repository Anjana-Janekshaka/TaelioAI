"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ArrowRight } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { apiService } from "@/lib/api";
import { ErrorNote, Spinner } from "@/components/studio/shared";

/** Passwordless email sign-in. New emails get an account automatically. */
export default function EmailSignIn({ submitLabel, busyLabel }: { submitLabel: string; busyLabel: string }) {
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();
  const params = useSearchParams();
  const { login } = useAuth();

  const next = params.get("next");
  const destination = next && next.startsWith("/") && !next.startsWith("//") ? next : "/studio";

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const res = await apiService.login(email.trim());
      localStorage.setItem("auth_token", res.access_token);
      localStorage.setItem("refresh_token", res.refresh_token);
      localStorage.setItem("user_id", res.user_id);
      localStorage.setItem("user_email", res.email);
      localStorage.setItem("user_role", res.role);
      login({ id: res.user_id, email: res.email, role: res.role });
      router.push(destination);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || "Sign-in failed");
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="space-y-5">
      <div>
        <label htmlFor="email" className="label">Email address</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          className="field text-lg"
        />
        <p className="hint">No password needed. If this email is new, we&rsquo;ll create your account.</p>
      </div>
      {error && <ErrorNote message={error} />}
      <button type="submit" disabled={busy} className="btn-primary w-full py-3 text-base">
        {busy ? <><Spinner /> {busyLabel}</> : <>{submitLabel} <ArrowRight className="h-5 w-5" aria-hidden /></>}
      </button>
    </form>
  );
}
