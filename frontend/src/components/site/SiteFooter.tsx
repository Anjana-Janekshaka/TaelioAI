import Link from "next/link";

/** The colophon: a quiet close, like the last printed page of a paperback. */
export default function SiteFooter() {
  return (
    <footer className="border-t border-rule bg-paper">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-10 sm:px-6 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="caps text-lg font-bold">TaelioAI</p>
          <p className="mt-1 max-w-sm text-sm text-ink-mute">
            A storytelling companion. Set in Josefin Sans, Figtree and Literata.
          </p>
        </div>
        <nav aria-label="Footer" className="flex flex-wrap gap-x-6 gap-y-2 text-sm font-semibold">
          <Link href="/studio" className="hover:underline">Studio</Link>
          <Link href="/select-tier" className="hover:underline">Plans</Link>
          <Link href="/login" className="hover:underline">Sign in</Link>
        </nav>
        <p className="tnum text-sm text-ink-mute">© {new Date().getFullYear()} TaelioAI</p>
      </div>
    </footer>
  );
}
