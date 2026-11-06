import Link from "next/link";

/** Sign-in pages share the cover: series band, white title band, series band. */
export default function AuthShell({ title, lede, children }: { title: string; lede: string; children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col [--band:#e8641c]">
      <div className="band-fill text-ink">
        <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-4 sm:px-6">
          <Link href="/" className="caps text-xl font-bold" aria-label="TaelioAI home">TaelioAI</Link>
          <Link href="/" className="text-[0.95rem] font-semibold hover:underline">Back to home</Link>
        </div>
      </div>
      <main className="flex flex-1 items-center border-y-[6px] border-white bg-sheet px-4 py-14 sm:px-6">
        <div className="mx-auto w-full max-w-md">
          <h1 className="font-display text-4xl font-bold leading-tight">{title}</h1>
          <p className="mt-3 text-lg text-ink-soft">{lede}</p>
          <div className="mt-8">{children}</div>
        </div>
      </main>
      <div className="band-fill h-16" aria-hidden />
    </div>
  );
}
