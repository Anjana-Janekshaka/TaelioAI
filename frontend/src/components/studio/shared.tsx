"use client";

import { AlertCircle, RotateCcw } from "lucide-react";
import { friendlyError } from "@/lib/series";

export function ErrorNote({ message, onRetry }: { message: string; onRetry?: () => void }) {
  const { title, detail } = friendlyError(message);
  return (
    <div className="notice-error" role="alert">
      <AlertCircle className="mt-0.5 h-5 w-5 flex-none" aria-hidden />
      <div className="flex-1">
        <p className="font-semibold">{title}</p>
        <p className="mt-0.5 text-ink-soft">{detail}</p>
        {onRetry && (
          <button onClick={onRetry} className="mt-2 inline-flex items-center gap-1.5 font-semibold text-alert underline underline-offset-2">
            <RotateCcw className="h-3.5 w-3.5" aria-hidden /> Try again
          </button>
        )}
      </div>
    </div>
  );
}

export function StageHeading({ title, lede }: { title: string; lede: string }) {
  return (
    <div className="mb-8">
      <h1 className="font-display text-3xl font-bold leading-tight md:text-[2.5rem]">{title}</h1>
      <p className="mt-2 max-w-2xl text-lg text-ink-soft">{lede}</p>
    </div>
  );
}

export function Spinner({ className = "" }: { className?: string }) {
  return (
    <span
      aria-hidden
      className={`inline-block h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent ${className}`}
    />
  );
}

export function downloadText(filename: string, content: string, type = "text/plain") {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export function fileSafe(name: string) {
  return (name || "story").trim().replace(/[^\w\- ]+/g, "").replace(/\s+/g, "_") || "story";
}
