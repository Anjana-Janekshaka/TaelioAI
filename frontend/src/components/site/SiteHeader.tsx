"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { ChevronDown, LogOut, Menu, X } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

interface SiteHeaderProps {
  /**
   * "band": transparent, sits inside a coloured cover band and inherits its
   * --band / --on-band colours. "bar": its own series-orange bar.
   */
  variant?: "band" | "bar";
}

const tierName = (role?: string) => (role === "pro" ? "Pro" : role === "admin" ? "Admin" : "Free");

export default function SiteHeader({ variant = "bar" }: SiteHeaderProps) {
  const { user, isAuthenticated, logout } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);
  const [accountOpen, setAccountOpen] = useState(false);
  const accountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!accountOpen) return;
    const close = (e: MouseEvent) => {
      if (accountRef.current && !accountRef.current.contains(e.target as Node)) setAccountOpen(false);
    };
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setAccountOpen(false);
    document.addEventListener("mousedown", close);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", close);
      document.removeEventListener("keydown", onKey);
    };
  }, [accountOpen]);

  const handleLogout = () => {
    logout();
    setAccountOpen(false);
    setMenuOpen(false);
    router.push("/");
  };

  const links = [
    { href: "/studio", label: "Studio", show: true },
    { href: "/metrics", label: "Content safety", show: isAuthenticated },
    { href: "/select-tier", label: "Plans", show: true },
  ].filter((l) => l.show);

  const shell =
    variant === "bar"
      ? "band-fill [--band:#e8641c] [--on-band:#151515]"
      : "bg-transparent";

  const name = user?.email?.split("@")[0];

  return (
    <header className={`${shell} relative z-40 text-[color:var(--on-band,#151515)]`}>
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="caps text-xl font-bold leading-none" aria-label="TaelioAI home">
          TaelioAI
        </Link>

        {/* Desktop nav */}
        <nav className="hidden items-center gap-1 md:flex" aria-label="Main">
          {links.map((l) => {
            const active = pathname === l.href;
            return (
              <Link
                key={l.href}
                href={l.href}
                aria-current={active ? "page" : undefined}
                className={`rounded-card px-3 py-2 text-[0.95rem] font-semibold transition-colors hover:bg-black/10 ${
                  active ? "underline decoration-2 underline-offset-[6px]" : ""
                }`}
              >
                {l.label}
              </Link>
            );
          })}

          <span aria-hidden className="mx-2 h-5 w-px bg-current opacity-30" />

          {isAuthenticated ? (
            <div className="relative" ref={accountRef}>
              <button
                onClick={() => setAccountOpen((o) => !o)}
                aria-expanded={accountOpen}
                aria-haspopup="menu"
                className="flex items-center gap-2 rounded-card px-3 py-2 text-[0.95rem] font-semibold transition-colors hover:bg-black/10"
              >
                <span className="max-w-[10rem] truncate">{name || "Account"}</span>
                <span className="caps rounded-[2px] bg-black/15 px-1.5 py-0.5 text-[0.65rem]">{tierName(user?.role)}</span>
                <ChevronDown className="h-4 w-4" aria-hidden />
              </button>
              {accountOpen && (
                <div
                  role="menu"
                  className="absolute right-0 mt-2 w-64 rounded-card border border-ink/10 bg-sheet py-2 text-ink shadow-lift"
                >
                  <div className="border-b border-rule px-4 pb-3 pt-1">
                    <p className="truncate text-sm font-semibold">{user?.email}</p>
                    <p className="text-sm text-ink-mute">{tierName(user?.role)} plan</p>
                  </div>
                  <Link role="menuitem" href="/studio" className="block px-4 py-2 text-sm hover:bg-paper" onClick={() => setAccountOpen(false)}>
                    Studio
                  </Link>
                  <Link role="menuitem" href="/metrics" className="block px-4 py-2 text-sm hover:bg-paper" onClick={() => setAccountOpen(false)}>
                    Content safety
                  </Link>
                  <Link role="menuitem" href="/select-tier" className="block px-4 py-2 text-sm hover:bg-paper" onClick={() => setAccountOpen(false)}>
                    Plans
                  </Link>
                  <button
                    role="menuitem"
                    onClick={handleLogout}
                    className="flex w-full items-center gap-2 px-4 py-2 text-left text-sm text-alert hover:bg-alert-tint"
                  >
                    <LogOut className="h-4 w-4" aria-hidden />
                    Sign out
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <Link href="/login" className="rounded-card px-3 py-2 text-[0.95rem] font-semibold transition-colors hover:bg-black/10">
                Sign in
              </Link>
              <Link href="/register" className="btn ml-1 bg-ink py-2 text-white hover:bg-ink-soft">
                Start writing
              </Link>
            </>
          )}
        </nav>

        {/* Mobile toggle */}
        <button
          className="rounded-card p-2 hover:bg-black/10 md:hidden"
          onClick={() => setMenuOpen((o) => !o)}
          aria-expanded={menuOpen}
          aria-label={menuOpen ? "Close menu" : "Open menu"}
        >
          {menuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {/* Mobile nav */}
      {menuOpen && (
        <nav className="border-t border-ink/10 bg-sheet px-4 pb-5 pt-3 text-ink shadow-lift md:hidden" aria-label="Main">
          {links.map((l) => (
            <Link key={l.href} href={l.href} className="block rounded-card px-2 py-3 font-semibold hover:bg-paper" onClick={() => setMenuOpen(false)}>
              {l.label}
            </Link>
          ))}
          <div className="mt-3 border-t border-rule pt-3">
            {isAuthenticated ? (
              <>
                <p className="px-2 text-sm font-semibold">{user?.email}</p>
                <p className="px-2 text-sm text-ink-mute">{tierName(user?.role)} plan</p>
                <button onClick={handleLogout} className="mt-2 flex items-center gap-2 rounded-card px-2 py-3 font-semibold text-alert">
                  <LogOut className="h-4 w-4" aria-hidden /> Sign out
                </button>
              </>
            ) : (
              <div className="flex gap-3 pt-1">
                <Link href="/login" className="btn-secondary flex-1">Sign in</Link>
                <Link href="/register" className="btn-primary flex-1">Start writing</Link>
              </div>
            )}
          </div>
        </nav>
      )}
    </header>
  );
}
