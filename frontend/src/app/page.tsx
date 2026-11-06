"use client";

import { useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowRight } from "lucide-react";
import SiteHeader from "@/components/site/SiteHeader";
import SiteFooter from "@/components/site/SiteFooter";
import BookCover from "@/components/book/BookCover";
import { useAuth } from "@/contexts/AuthContext";
import { GENRES, bandColor, onBandColor, padNo, saveSpark } from "@/lib/series";

const STAGES = [
  { n: 1, name: "Idea", line: "A title, outline, characters and setting, grown from your spark." },
  { n: 2, name: "Story", line: "The full story, written out as you watch." },
  { n: 3, name: "Edit", line: "Revisions in plain words, like “make the ending darker”." },
];

const CREDITS = [
  {
    role: "Idea by",
    agent: "the Idea Generator",
    what: "Turns your spark, genre and tone into a title, an outline, a cast of characters and a setting.",
  },
  {
    role: "Written by",
    agent: "the Story Writer",
    what: "Drafts the complete story from that outline, streaming it onto the page line by line.",
  },
  {
    role: "Revised by",
    agent: "the Story Editor",
    what: "Rewrites the draft to your instructions, as many times as you like, and keeps your original close at hand.",
  },
];

export default function Home() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const [spark, setSpark] = useState("");
  const [genre, setGenre] = useState("Mystery");
  const sparkRef = useRef<HTMLTextAreaElement>(null);

  const band = bandColor(genre);
  const onBand = onBandColor(genre);

  const start = (e?: React.FormEvent) => {
    e?.preventDefault();
    saveSpark({ spark: spark.trim(), genre });
    router.push(isAuthenticated ? "/studio" : "/login?next=/studio");
  };

  const pickFromShelf = (name: string) => {
    setGenre(name);
    window.scrollTo({ top: 0, behavior: "smooth" });
    window.setTimeout(() => sparkRef.current?.focus({ preventScroll: true }), 400);
  };

  return (
    <div className="min-h-screen">
      {/* ---------- The cover ---------- */}
      <section
        className="flex min-h-[100svh] flex-col"
        style={{ ["--band" as string]: band, ["--on-band" as string]: onBand }}
        aria-label="Start a story"
      >
        {/* Top band */}
        <div className="band-fill" style={{ color: onBand }}>
          <SiteHeader variant="band" />
          <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 pb-8 pt-6 sm:px-6 md:flex-row md:items-end md:justify-between md:pb-10 md:pt-10">
            <h1 className="caps text-[clamp(3.25rem,10vw,6rem)] font-bold leading-[0.9]">TaelioAI</h1>
            <p className="caps max-w-xs text-sm font-semibold leading-relaxed md:pb-3 md:text-right">
              A storytelling companion
              <span className="block opacity-80">The series · {genre}</span>
            </p>
          </div>
        </div>

        {/* Middle band: the working cover */}
        <div className="flex flex-1 items-center border-y-[6px] border-white bg-sheet">
          <div className="mx-auto w-full max-w-4xl px-4 py-12 text-center sm:px-6 md:py-16">
            <h2 className="font-display text-[clamp(2.1rem,5.2vw,3.75rem)] font-bold leading-[1.02] tracking-[-0.01em] [text-wrap:balance]">
              Every spark deserves a finished story.
            </h2>
            <p className="mx-auto mt-5 max-w-2xl text-lg leading-relaxed text-ink-soft [text-wrap:pretty]">
              Type the idea you can&rsquo;t stop thinking about. TaelioAI builds it into an outline, writes the
              story, then revises it with you, until it&rsquo;s a book with your name on the cover.
            </p>

            <form onSubmit={start} className="mx-auto mt-9 max-w-3xl text-left">
              <label htmlFor="spark" className="label">Your spark</label>
              <div className="flex flex-col gap-3 sm:flex-row">
                <textarea
                  id="spark"
                  ref={sparkRef}
                  rows={2}
                  value={spark}
                  onChange={(e) => setSpark(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) start(e);
                  }}
                  placeholder="A lighthouse keeper whose ledger starts writing back…"
                  className="field min-h-[3.25rem] flex-1 resize-none py-3 text-lg"
                />
                <button type="submit" className="btn-primary px-6 py-3 text-base sm:self-stretch">
                  Start this story
                  <ArrowRight className="h-5 w-5" aria-hidden />
                </button>
              </div>

              <fieldset className="mt-5">
                <legend className="label">Genre <span className="font-normal text-ink-mute">sets the colour of your cover</span></legend>
                <div className="flex flex-wrap gap-2">
                  {GENRES.map((g) => {
                    const on = g.name === genre;
                    return (
                      <label
                        key={g.name}
                        className={`flex cursor-pointer items-center gap-2 rounded-card border px-3 py-1.5 text-sm font-semibold transition-colors has-[:focus-visible]:outline has-[:focus-visible]:outline-2 has-[:focus-visible]:outline-offset-2 ${
                          on ? "border-ink bg-ink text-white" : "border-ink/20 bg-sheet hover:border-ink/50"
                        }`}
                      >
                        <input
                          type="radio"
                          name="genre"
                          value={g.name}
                          checked={on}
                          onChange={() => setGenre(g.name)}
                          className="sr-only"
                        />
                        <span aria-hidden className="h-3 w-3 rounded-[1px]" style={{ background: g.color }} />
                        {g.name}
                      </label>
                    );
                  })}
                </div>
              </fieldset>
            </form>
          </div>
        </div>

        {/* Bottom band: the pipeline */}
        <div className="band-fill" style={{ color: onBand }}>
          <ol className="mx-auto grid max-w-7xl gap-5 px-4 py-7 sm:px-6 md:grid-cols-3 md:gap-8 md:py-8">
            {STAGES.map((s, i) => (
              <li key={s.n} className="flex items-start gap-3">
                <span className="caps tnum mt-0.5 text-sm font-bold opacity-80">{s.n}</span>
                <div>
                  <p className="caps text-lg font-bold leading-tight">
                    {s.name}
                    {i < STAGES.length - 1 && <ArrowRight className="ml-2 inline h-4 w-4 align-[-2px] opacity-70" aria-hidden />}
                  </p>
                  <p className="mt-1 text-[0.95rem] leading-snug opacity-90">{s.line}</p>
                </div>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* ---------- Credits: how a story gets made ---------- */}
      <section className="mx-auto grid max-w-7xl gap-12 px-4 py-24 sm:px-6 lg:grid-cols-[1fr_1.25fr] lg:gap-20 lg:py-32">
        <div className="lg:pt-6">
          <h2 className="font-display text-4xl font-bold leading-tight md:text-5xl [text-wrap:balance]">
            Three agents, one story. Yours.
          </h2>
          <p className="mt-5 max-w-md text-lg leading-relaxed text-ink-soft">
            TaelioAI isn&rsquo;t a single chat box. Each stage is handled by its own agent, and each hands its work to
            the next, so your spark becomes an idea, the idea becomes a story, and the story gets revised.
          </p>
          <p className="mt-4 max-w-md text-ink-mute">
            Behind them, the workshop also keeps a Content Moderator and a Quality Assurance agent.
          </p>
        </div>

        <div className="rounded-[2px] bg-sheet px-6 py-10 shadow-book sm:px-12 sm:py-14">
          <p className="caps text-center text-sm font-bold text-ink-mute">The making of your book</p>
          <dl className="mt-10 space-y-9">
            {CREDITS.map((c) => (
              <div key={c.role}>
                <dt className="flex items-baseline gap-3">
                  <span className="caps whitespace-nowrap text-sm font-bold text-ink-mute">{c.role}</span>
                  <span aria-hidden className="mb-1 flex-1 border-b border-dotted border-ink/30" />
                  <span className="font-display text-xl font-bold">{c.agent}</span>
                </dt>
                <dd className="mt-2 font-book text-[1.05rem] leading-relaxed text-ink-soft">{c.what}</dd>
              </div>
            ))}
            <div>
              <dt className="flex items-baseline gap-3">
                <span className="caps whitespace-nowrap text-sm font-bold text-ink-mute">Story by</span>
                <span aria-hidden className="mb-1 flex-1 border-b border-dotted border-ink/30" />
                <span className="font-display text-xl font-bold" style={{ color: band }}>you</span>
              </dt>
              <dd className="mt-2 font-book text-[1.05rem] leading-relaxed text-ink-soft">
                The spark, the choices and every revision note are yours. The agents just do the typing.
              </dd>
            </div>
          </dl>
        </div>
      </section>

      {/* ---------- An example page ---------- */}
      <section className="border-y border-rule bg-sheet">
        <div className="mx-auto grid max-w-6xl items-center gap-12 px-4 py-24 sm:px-6 md:grid-cols-[auto_1fr] md:gap-16 lg:py-28">
          <BookCover
            size="md"
            title="The Lighthouse Keeper's Ledger"
            author="by a TaelioAI writer"
            genre="Mystery"
            tone="Mysterious"
            seriesNo={14}
            className="mx-auto -rotate-2"
          />
          <article className="max-w-measure">
            <p className="caps text-sm font-bold" style={{ color: bandColor("Mystery") }}>Chapter one</p>
            <div className="book-text mt-4 text-[1.2rem]">
              <p>
                Every night for eleven years, Ada Quill wrote the same line in the ledger: <em>Lamp lit at dusk. No
                ships seen.</em> On the night the ledger wrote back, she was halfway up the stairs with the oil can, and
                the wind had gone so quiet she could hear the pages turning on their own.
              </p>
              <p>The handwriting was hers. The date was tomorrow&rsquo;s.</p>
            </div>
            <p className="mt-6 text-sm text-ink-mute">
              An example opening, written for this page to show how a finished TaelioAI story reads.
            </p>
          </article>
        </div>
      </section>

      {/* ---------- The shelf ---------- */}
      <section className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:py-28">
        <div className="max-w-2xl">
          <h2 className="font-display text-4xl font-bold leading-tight md:text-5xl">Eight genres. One series.</h2>
          <p className="mt-4 text-lg text-ink-soft">
            Every genre has its own cover colour. Pull one off the shelf to start there.
          </p>
        </div>
        <div className="mt-12 flex items-end gap-1.5 overflow-x-auto pb-2 sm:gap-2" role="list">
          {GENRES.map((g, i) => (
            <button
              key={g.name}
              role="listitem"
              onClick={() => pickFromShelf(g.name)}
              aria-label={`Start a ${g.name} story`}
              className="group flex min-w-[3.25rem] flex-1 flex-col items-center justify-between rounded-t-[2px] px-1 py-4 shadow-lift transition-transform duration-300 ease-out-expo hover:-translate-y-3 focus-visible:-translate-y-3"
              style={{
                background: g.color,
                color: g.onBand,
                height: `${15 + ((i * 7) % 4) * 1.25}rem`,
              }}
            >
              <span className="caps text-[0.6rem] font-bold opacity-80">TA</span>
              <span className="caps whitespace-nowrap text-base font-bold [writing-mode:vertical-rl] rotate-180 sm:text-lg">
                {g.name}
              </span>
              <span className="caps tnum text-[0.65rem] font-bold opacity-80">{padNo(i + 1)}</span>
            </button>
          ))}
        </div>
        <div aria-hidden className="h-3 rounded-b-[2px] bg-ink/85" />
      </section>

      {/* ---------- Close ---------- */}
      <section className="band-fill [--band:#e8641c] text-ink">
        <div className="mx-auto flex max-w-7xl flex-col items-start gap-6 px-4 py-16 sm:px-6 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="font-display text-3xl font-bold md:text-4xl">Your first book is one spark away.</h2>
            <p className="mt-2 text-lg">Free to start. Sign in with just your email.</p>
          </div>
          <Link href={isAuthenticated ? "/studio" : "/register"} className="btn-primary px-6 py-3 text-base">
            {isAuthenticated ? "Open the studio" : "Start writing"}
            <ArrowRight className="h-5 w-5" aria-hidden />
          </Link>
        </div>
      </section>

      <SiteFooter />
    </div>
  );
}
