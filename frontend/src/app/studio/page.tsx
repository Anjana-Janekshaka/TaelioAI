"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import {
  ArrowRight,
  BookOpen,
  Check,
  Copy,
  Download,
  PencilLine,
  Plus,
  Printer,
  Undo2,
} from "lucide-react";
import SiteHeader from "@/components/site/SiteHeader";
import BookCover from "@/components/book/BookCover";
import { ErrorNote, Spinner, StageHeading, downloadText, fileSafe } from "@/components/studio/shared";
import { useAuth } from "@/contexts/AuthContext";
import { useIdeaGeneration, useStreamingStoryWriting } from "@/hooks/useApi";
import { apiService } from "@/lib/api";
import type { IdeaResponse } from "@/lib/api";
import {
  GENRES,
  TONES,
  bandColor,
  nextSeriesNumber,
  readingMinutes,
  takeSpark,
  wordCount,
} from "@/lib/series";

type Stage = "idea" | "story" | "edit" | "book";

interface Book {
  seriesNo: number;
  spark: string;
  genre: string;
  tone: string;
  idea: IdeaResponse | null;
  title: string;
  outline: string;
  characters: string;
  setting: string;
  story: string;
  history: string[]; // earlier versions, newest last
  revisions: number;
}

const BOOK_KEY = "taelio_book";

const emptyBook = (seriesNo: number): Book => ({
  seriesNo,
  spark: "",
  genre: "Mystery",
  tone: "Mysterious",
  idea: null,
  title: "",
  outline: "",
  characters: "",
  setting: "",
  story: "",
  history: [],
  revisions: 0,
});

const EXAMPLE_SPARKS = [
  "A lighthouse keeper whose ledger starts writing back",
  "A time-travelling chef who can only cook yesterday's meals",
  "A library that rearranges itself every night",
  "A detective who can see other people's memories",
];

const REVISION_IDEAS = [
  "Make the ending more surprising",
  "Add more dialogue",
  "Tighten the pacing in the middle",
  "Tell it in the first person",
  "Make the tone darker",
];

const STAGES: { id: Stage; n: number; name: string; note: string }[] = [
  { id: "idea", n: 1, name: "Idea", note: "Title, outline, cast" },
  { id: "story", n: 2, name: "Story", note: "The full text" },
  { id: "edit", n: 3, name: "Edit", note: "Revisions" },
  { id: "book", n: 4, name: "Book", note: "Read and keep" },
];

export default function StudioPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const [book, setBook] = useState<Book | null>(null);
  const [stage, setStage] = useState<Stage>("idea");

  const ideaGen = useIdeaGeneration();
  const writer = useStreamingStoryWriting();
  const [speed, setSpeed] = useState("normal");
  const [showDetails, setShowDetails] = useState(false);

  const [instructions, setInstructions] = useState("");
  const [editing, setEditing] = useState(false);
  const [editError, setEditError] = useState<string | null>(null);
  const [manual, setManual] = useState(false);
  const [copied, setCopied] = useState(false);
  const workRef = useRef<HTMLDivElement>(null);

  // ---- Auth guard ----
  useEffect(() => {
    if (!authLoading && !isAuthenticated) router.replace("/login?next=/studio");
  }, [authLoading, isAuthenticated, router]);

  // ---- Load the book in progress (or start a new one) ----
  useEffect(() => {
    let loaded: Book | null = null;
    try {
      const raw = sessionStorage.getItem(BOOK_KEY);
      if (raw) loaded = JSON.parse(raw) as Book;
    } catch {
      loaded = null;
    }
    const spark = takeSpark();
    if (spark) {
      // Arriving from the landing page with a new spark starts a new book.
      loaded = { ...emptyBook(nextSeriesNumber()), spark: spark.spark, genre: spark.genre || "Mystery" };
    }
    const next = loaded ?? emptyBook(nextSeriesNumber());
    setBook(next);
    setStage(next.story ? "edit" : next.idea || next.title ? "story" : "idea");
  }, []);

  useEffect(() => {
    if (!book) return;
    try {
      sessionStorage.setItem(BOOK_KEY, JSON.stringify(book));
    } catch {
      // storage unavailable; the session still works
    }
  }, [book]);

  const update = useCallback((patch: Partial<Book>) => setBook((b) => (b ? { ...b, ...patch } : b)), []);

  const goto = (s: Stage) => {
    setStage(s);
    workRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  // ---- Commit a finished streamed story to the book ----
  useEffect(() => {
    if (!writer.loading && writer.story && book && writer.story !== book.story && !writer.error) {
      update({ story: writer.story, history: [], revisions: 0 });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [writer.loading]);

  // ---- Actions ----
  const generateIdea = async () => {
    if (!book || !book.spark.trim()) return;
    try {
      const idea = await ideaGen.generateIdea(book.spark.trim(), book.genre, book.tone);
      update({ idea });
    } catch {
      // error shown from hook state
    }
  };

  const useIdea = () => {
    if (!book?.idea) return;
    const i = book.idea;
    update({
      title: i.title || book.title,
      genre: GENRES.some((g) => g.name === i.genre) ? i.genre : book.genre,
      tone: TONES.includes(i.tone) ? i.tone : book.tone,
      outline: i.outline || "",
      characters: (i.characters || []).join("\n"),
      setting: i.setting || "",
    });
    goto("story");
  };

  const writeStory = () => {
    if (!book || !book.title.trim()) return;
    writer.writeStoryStreaming(
      {
        title: book.title.trim(),
        genre: book.genre,
        tone: book.tone,
        outline: book.outline,
        characters: book.characters,
        setting: book.setting,
      },
      speed
    );
  };

  const applyRevision = async () => {
    if (!book || !instructions.trim() || !book.story) return;
    setEditing(true);
    setEditError(null);
    try {
      const res = await apiService.editStory({
        story: book.story,
        edit_instructions: instructions.trim(),
        title: book.title || "Untitled",
        genre: book.genre,
      });
      if (!res.success) throw new Error("The editor couldn't revise this story.");
      update({
        story: res.edited_story,
        history: [...book.history, book.story],
        revisions: book.revisions + 1,
      });
      setInstructions("");
    } catch (err: any) {
      setEditError(err?.response?.data?.detail || err?.message || "Revision failed");
    } finally {
      setEditing(false);
    }
  };

  const undoRevision = () => {
    if (!book || book.history.length === 0) return;
    const history = [...book.history];
    const prev = history.pop()!;
    update({ story: prev, history, revisions: Math.max(0, book.revisions - 1) });
  };

  const newBook = () => {
    const fresh = emptyBook(nextSeriesNumber());
    setBook(fresh);
    ideaGen.reset();
    writer.reset();
    setInstructions("");
    setEditError(null);
    setStage("idea");
  };

  const copyStory = async () => {
    if (!book?.story) return;
    try {
      await navigator.clipboard.writeText(book.story);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      // clipboard blocked
    }
  };

  // ---- Derived ----
  const liveStory = writer.loading ? writer.story : book?.story || "";
  const words = wordCount(liveStory);
  const author = user?.email ? `by ${user.email.split("@")[0]}` : undefined;
  const coverTitle = book?.title || book?.idea?.title || "";
  const band = bandColor(book?.genre);

  const done = useMemo(
    () => ({
      idea: Boolean(book?.idea),
      story: Boolean(book?.story),
      edit: Boolean(book && book.revisions > 0),
      book: false,
    }),
    [book]
  );

  if (authLoading || !isAuthenticated || !book) {
    return (
      <div className="flex min-h-screen items-center justify-center text-ink-mute">
        <Spinner className="mr-3" /> Opening the studio…
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col" style={{ ["--band" as string]: band }}>
      <div className="no-print">
        <SiteHeader variant="bar" />
      </div>

      <div className="mx-auto grid w-full max-w-[90rem] flex-1 gap-0 lg:grid-cols-[15rem_minmax(0,1fr)_20rem]">
        {/* ---------- Stage rail ---------- */}
        <aside className="no-print border-b border-rule bg-paper lg:border-b-0 lg:border-r">
          <nav aria-label="Stages" className="lg:sticky lg:top-0 lg:p-5">
            <ol className="flex overflow-x-auto lg:flex-col lg:gap-1">
              {STAGES.map((s) => {
                const active = stage === s.id;
                const isDone = done[s.id];
                return (
                  <li key={s.id} className="flex-1 lg:flex-none">
                    <button
                      onClick={() => goto(s.id)}
                      aria-current={active ? "step" : undefined}
                      className={`flex w-full items-center gap-3 whitespace-nowrap px-4 py-3 text-left transition-colors lg:rounded-card lg:px-3 ${
                        active ? "bg-sheet shadow-lift" : "hover:bg-ink/5"
                      }`}
                    >
                      <span
                        className={`tnum flex h-7 w-7 flex-none items-center justify-center rounded-full text-sm font-bold ${
                          active ? "band-fill text-white" : isDone ? "bg-ink text-white" : "border border-ink/30 text-ink-mute"
                        }`}
                      >
                        {isDone && !active ? <Check className="h-4 w-4" aria-label="done" /> : s.n}
                      </span>
                      <span>
                        <span className={`block font-semibold ${active ? "text-ink" : "text-ink-soft"}`}>{s.name}</span>
                        <span className="hidden text-xs text-ink-mute lg:block">{s.note}</span>
                      </span>
                    </button>
                  </li>
                );
              })}
            </ol>
            <button onClick={newBook} className="btn-quiet mt-4 hidden w-full justify-start lg:flex">
              <Plus className="h-4 w-4" aria-hidden /> Start a new book
            </button>
          </nav>
        </aside>

        {/* ---------- Work area ---------- */}
        <main ref={workRef} className="min-w-0 scroll-mt-4 bg-sheet px-4 py-10 sm:px-8 lg:px-12 lg:py-12">
          {/* Mobile cover summary */}
          <div className="no-print mb-8 flex items-center gap-4 lg:hidden">
            <BookCover size="sm" title={coverTitle} genre={book.genre} seriesNo={book.seriesNo} />
            <div className="min-w-0">
              <p className="truncate font-display text-lg font-bold">{coverTitle || "Untitled book"}</p>
              <p className="tnum text-sm text-ink-mute">
                {book.genre} · {words.toLocaleString()} words
              </p>
              <button onClick={newBook} className="mt-1 text-sm font-semibold underline underline-offset-2">
                Start a new book
              </button>
            </div>
          </div>

          {/* ===== Idea ===== */}
          {stage === "idea" && (
            <section aria-labelledby="stage-idea">
              <StageHeading
                title="Start with a spark"
                lede="Describe the idea in a line or two. The Idea Generator will grow it into a title, an outline, characters and a setting."
              />
              <div className="max-w-2xl space-y-6">
                <div>
                  <label htmlFor="spark" className="label" id="stage-idea">Your spark</label>
                  <textarea
                    id="spark"
                    rows={3}
                    value={book.spark}
                    onChange={(e) => update({ spark: e.target.value })}
                    placeholder="A lighthouse keeper whose ledger starts writing back…"
                    className="field resize-y text-lg"
                  />
                  <div className="mt-2 flex flex-wrap gap-2">
                    {EXAMPLE_SPARKS.map((ex) => (
                      <button
                        key={ex}
                        onClick={() => update({ spark: ex })}
                        className="rounded-card border border-ink/15 px-2.5 py-1 text-sm text-ink-soft transition-colors hover:border-ink/40 hover:text-ink"
                      >
                        {ex}
                      </button>
                    ))}
                  </div>
                </div>

                <GenreToneFields book={book} update={update} />

                <button onClick={generateIdea} disabled={!book.spark.trim() || ideaGen.loading} className="btn-primary">
                  {ideaGen.loading ? <><Spinner /> Growing your idea…</> : <>Generate the idea</>}
                </button>

                {ideaGen.error && <ErrorNote message={ideaGen.error} onRetry={generateIdea} />}
              </div>

              {book.idea && (
                <article className="mt-12 max-w-3xl rounded-card border border-rule bg-paper/60 p-6 sm:p-8" aria-label="Generated idea">
                  <div className="flex flex-wrap items-baseline justify-between gap-3">
                    <h2 className="font-display text-3xl font-bold leading-tight">{book.idea.title || "Untitled"}</h2>
                    <p className="caps text-sm font-bold" style={{ color: bandColor(book.idea.genre) }}>
                      {book.idea.genre} · {book.idea.tone}
                    </p>
                  </div>
                  <p className="book-text mt-5">{book.idea.outline}</p>
                  <div className="mt-8 grid gap-8 sm:grid-cols-2">
                    <div>
                      <h3 className="caps text-sm font-bold text-ink-mute">Characters</h3>
                      {book.idea.characters && book.idea.characters.length > 0 ? (
                        <ul className="mt-3 space-y-2">
                          {book.idea.characters.map((c, i) => (
                            <li key={i} className="font-book leading-snug">{c}</li>
                          ))}
                        </ul>
                      ) : (
                        <p className="mt-3 text-ink-mute">No characters this time.</p>
                      )}
                    </div>
                    <div>
                      <h3 className="caps text-sm font-bold text-ink-mute">Setting</h3>
                      <p className="mt-3 font-book leading-snug">{book.idea.setting || "No setting this time."}</p>
                    </div>
                  </div>
                  <div className="mt-8 flex flex-wrap gap-3 border-t border-rule pt-6">
                    <button onClick={useIdea} className="btn-primary">
                      Write this story <ArrowRight className="h-4 w-4" aria-hidden />
                    </button>
                    <button onClick={generateIdea} disabled={ideaGen.loading} className="btn-secondary">
                      Try another idea
                    </button>
                  </div>
                </article>
              )}
            </section>
          )}

          {/* ===== Story ===== */}
          {stage === "story" && (
            <section>
              <StageHeading
                title="Write the story"
                lede="Check the title and details, then the Story Writer drafts the whole thing. You'll see it appear line by line."
              />
              <div className="max-w-2xl space-y-6">
                <div>
                  <label htmlFor="title" className="label">Title</label>
                  <input
                    id="title"
                    value={book.title}
                    onChange={(e) => update({ title: e.target.value })}
                    placeholder="The Lighthouse Keeper's Ledger"
                    className="field font-display text-xl font-bold"
                  />
                </div>
                <GenreToneFields book={book} update={update} />

                <div className="rounded-card border border-rule">
                  <button
                    onClick={() => setShowDetails((s) => !s)}
                    aria-expanded={showDetails}
                    className="flex w-full items-center justify-between px-4 py-3 text-left font-semibold"
                  >
                    <span>
                      Outline, characters and setting
                      <span className="ml-2 font-normal text-ink-mute">
                        {book.outline || book.characters || book.setting ? "filled in from your idea" : "optional"}
                      </span>
                    </span>
                    <span aria-hidden className="text-ink-mute">{showDetails ? "Hide" : "Show"}</span>
                  </button>
                  {showDetails && (
                    <div className="space-y-5 border-t border-rule p-4">
                      <div>
                        <label htmlFor="outline" className="label">Outline</label>
                        <textarea id="outline" rows={4} value={book.outline} onChange={(e) => update({ outline: e.target.value })} className="field resize-y" />
                      </div>
                      <div>
                        <label htmlFor="characters" className="label">Characters</label>
                        <textarea id="characters" rows={3} value={book.characters} onChange={(e) => update({ characters: e.target.value })} className="field resize-y" placeholder="One per line" />
                      </div>
                      <div>
                        <label htmlFor="setting" className="label">Setting</label>
                        <textarea id="setting" rows={2} value={book.setting} onChange={(e) => update({ setting: e.target.value })} className="field resize-y" />
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex flex-wrap items-end gap-4">
                  <button onClick={writeStory} disabled={!book.title.trim() || writer.loading} className="btn-primary">
                    {writer.loading ? <><Spinner /> Writing…</> : book.story ? <>Write it again</> : <>Write the story</>}
                  </button>
                  <div>
                    <label htmlFor="speed" className="label text-xs font-semibold text-ink-mute">Writing speed</label>
                    <select id="speed" value={speed} onChange={(e) => setSpeed(e.target.value)} disabled={writer.loading} className="field py-2 text-sm">
                      <option value="slow">Slow, like someone typing</option>
                      <option value="normal">Normal</option>
                      <option value="fast">Fast</option>
                    </select>
                  </div>
                </div>
                {!book.title.trim() && <p className="hint">Give your story a title to start writing.</p>}
                {writer.error && <ErrorNote message={writer.error} onRetry={writeStory} />}
              </div>

              {liveStory && (
                <div className="mt-12">
                  <ReadingPage title={book.title} genre={book.genre} text={liveStory} streaming={writer.loading} />
                  {!writer.loading && book.story && (
                    <div className="mx-auto mt-8 flex max-w-measure flex-wrap gap-3">
                      <button onClick={() => goto("edit")} className="btn-primary">
                        Revise this story <ArrowRight className="h-4 w-4" aria-hidden />
                      </button>
                      <button onClick={() => goto("book")} className="btn-secondary">
                        <BookOpen className="h-4 w-4" aria-hidden /> It&rsquo;s finished
                      </button>
                    </div>
                  )}
                </div>
              )}
            </section>
          )}

          {/* ===== Edit ===== */}
          {stage === "edit" && (
            <section>
              <StageHeading
                title="Revise it"
                lede="Tell the Story Editor what to change, in your own words. Every revision can be undone."
              />
              {!book.story ? (
                <EmptyStage
                  text="There's no story to revise yet. Write one first."
                  action="Go to Story"
                  onAction={() => goto("story")}
                />
              ) : (
                <div className="grid gap-10 xl:grid-cols-[minmax(0,22rem)_minmax(0,1fr)]">
                  <div className="space-y-5 xl:sticky xl:top-6 xl:self-start">
                    <div>
                      <label htmlFor="instructions" className="label">What should change?</label>
                      <textarea
                        id="instructions"
                        rows={4}
                        value={instructions}
                        onChange={(e) => setInstructions(e.target.value)}
                        placeholder="Make the ending more surprising and give Ada a reason to doubt the ledger."
                        className="field resize-y"
                      />
                      <div className="mt-2 flex flex-wrap gap-2">
                        {REVISION_IDEAS.map((r) => (
                          <button
                            key={r}
                            onClick={() => setInstructions(r)}
                            className="rounded-card border border-ink/15 px-2.5 py-1 text-sm text-ink-soft transition-colors hover:border-ink/40 hover:text-ink"
                          >
                            {r}
                          </button>
                        ))}
                      </div>
                    </div>
                    <div className="flex flex-wrap gap-3">
                      <button onClick={applyRevision} disabled={!instructions.trim() || editing || manual} className="btn-primary">
                        {editing ? <><Spinner /> Revising…</> : <>Apply revision</>}
                      </button>
                      <button onClick={undoRevision} disabled={book.history.length === 0 || editing} className="btn-secondary">
                        <Undo2 className="h-4 w-4" aria-hidden /> Undo
                      </button>
                    </div>
                    {editError && <ErrorNote message={editError} onRetry={applyRevision} />}
                    <div className="border-t border-rule pt-5">
                      <button onClick={() => setManual((m) => !m)} className="btn-quiet -ml-3">
                        <PencilLine className="h-4 w-4" aria-hidden /> {manual ? "Done editing by hand" : "Edit the text yourself"}
                      </button>
                      <button onClick={() => goto("book")} className="btn-secondary mt-3 w-full">
                        <BookOpen className="h-4 w-4" aria-hidden /> Finish and read the book
                      </button>
                    </div>
                  </div>

                  <div className={editing ? "opacity-60 transition-opacity" : "transition-opacity"}>
                    {manual ? (
                      <div>
                        <label htmlFor="manual" className="label">Story text</label>
                        <textarea
                          id="manual"
                          value={book.story}
                          onChange={(e) => update({ story: e.target.value })}
                          className="field book-text min-h-[60vh] resize-y"
                        />
                      </div>
                    ) : (
                      <ReadingPage title={book.title} genre={book.genre} text={book.story} />
                    )}
                  </div>
                </div>
              )}
            </section>
          )}

          {/* ===== Book (keepsake) ===== */}
          {stage === "book" && (
            <section>
              {!book.story ? (
                <>
                  <StageHeading title="Your book" lede="Your finished story will be bound here." />
                  <EmptyStage text="Write a story first, then come back to read and keep it." action="Go to Story" onAction={() => goto("story")} />
                </>
              ) : (
                <>
                  <div className="no-print mb-10 flex flex-wrap items-center justify-between gap-4">
                    <h1 className="font-display text-3xl font-bold md:text-[2.5rem]">Your book</h1>
                    <div className="flex flex-wrap gap-2">
                      <button onClick={copyStory} className="btn-secondary">
                        {copied ? <Check className="h-4 w-4" aria-hidden /> : <Copy className="h-4 w-4" aria-hidden />}
                        {copied ? "Copied" : "Copy text"}
                      </button>
                      <button
                        onClick={() => downloadText(`${fileSafe(book.title)}.txt`, `${book.title}\n${author ?? ""}\n\n${book.story}`)}
                        className="btn-secondary"
                      >
                        <Download className="h-4 w-4" aria-hidden /> .txt
                      </button>
                      <button
                        onClick={() =>
                          downloadText(
                            `${fileSafe(book.title)}.md`,
                            `# ${book.title}\n\n*${book.genre} · ${book.tone}${author ? ` · ${author}` : ""}*\n\n${book.story}\n`,
                            "text/markdown"
                          )
                        }
                        className="btn-secondary"
                      >
                        <Download className="h-4 w-4" aria-hidden /> .md
                      </button>
                      <button onClick={() => window.print()} className="btn-secondary">
                        <Printer className="h-4 w-4" aria-hidden /> Print
                      </button>
                    </div>
                  </div>
                  <div className="mb-12 flex justify-center lg:hidden">
                    <BookCover
                      size="md"
                      title={book.title}
                      author={author}
                      genre={book.genre}
                      tone={book.tone}
                      seriesNo={book.seriesNo}
                    />
                  </div>
                  <ReadingPage title={book.title} genre={book.genre} text={book.story} large />
                  <div className="no-print mx-auto mt-12 flex max-w-measure flex-wrap gap-3 border-t border-rule pt-8">
                    <button onClick={() => goto("edit")} className="btn-secondary">Keep revising</button>
                    <button onClick={newBook} className="btn-primary">
                      <Plus className="h-4 w-4" aria-hidden /> Start your next book
                    </button>
                  </div>
                </>
              )}
            </section>
          )}
        </main>

        {/* ---------- Live cover ---------- */}
        <aside className="no-print hidden border-l border-rule bg-paper lg:block" aria-label="Your book so far">
          <div className="sticky top-0 flex flex-col items-center px-6 py-10">
            <BookCover
              title={coverTitle}
              author={author}
              genre={book.genre}
              tone={book.tone}
              seriesNo={book.seriesNo}
            />
            <dl className="tnum mt-8 grid w-full max-w-[17rem] grid-cols-2 gap-x-4 gap-y-4 border-t border-rule pt-6 text-sm">
              <div>
                <dt className="text-ink-mute">Words</dt>
                <dd className="font-display text-2xl font-bold">{words.toLocaleString()}</dd>
              </div>
              <div>
                <dt className="text-ink-mute">Minutes to read</dt>
                <dd className="font-display text-2xl font-bold">{readingMinutes(words)}</dd>
              </div>
              <div>
                <dt className="text-ink-mute">Revisions</dt>
                <dd className="font-display text-2xl font-bold">{book.revisions}</dd>
              </div>
              <div>
                <dt className="text-ink-mute">Stage</dt>
                <dd className="font-display text-2xl font-bold">{STAGES.find((s) => s.id === stage)?.name}</dd>
              </div>
            </dl>
            {writer.loading && (
              <p className="mt-6 flex items-center gap-2 text-sm text-ink-soft" aria-live="polite">
                <Spinner /> The Story Writer is at work
              </p>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}

// ---------- Pieces ----------

function GenreToneFields({ book, update }: { book: Book; update: (p: Partial<Book>) => void }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <div>
        <label htmlFor="genre" className="label">Genre</label>
        <div className="relative">
          <span
            aria-hidden
            className="pointer-events-none absolute left-3.5 top-1/2 h-3 w-3 -translate-y-1/2 rounded-[1px]"
            style={{ background: bandColor(book.genre) }}
          />
          <select id="genre" value={book.genre} onChange={(e) => update({ genre: e.target.value })} className="field pl-9">
            {GENRES.map((g) => (
              <option key={g.name} value={g.name}>{g.name}</option>
            ))}
          </select>
        </div>
      </div>
      <div>
        <label htmlFor="tone" className="label">Tone</label>
        <select id="tone" value={book.tone} onChange={(e) => update({ tone: e.target.value })} className="field">
          {TONES.map((t) => (
            <option key={t} value={t}>{t}</option>
          ))}
        </select>
      </div>
    </div>
  );
}

function ReadingPage({
  title,
  genre,
  text,
  streaming = false,
  large = false,
}: {
  title: string;
  genre: string;
  text: string;
  streaming?: boolean;
  large?: boolean;
}) {
  const paragraphs = text.split(/\n{2,}|\n/).filter((p) => p.trim().length > 0);
  return (
    <article className="mx-auto max-w-measure" aria-busy={streaming} aria-label={title || "Story"}>
      <header className="mb-8 border-b border-rule pb-6 text-center">
        <p className="caps text-sm font-bold" style={{ color: bandColor(genre) }}>{genre}</p>
        <h2 className={`mt-2 font-display font-bold leading-tight [text-wrap:balance] ${large ? "text-4xl md:text-5xl" : "text-3xl"}`}>
          {title || "Untitled"}
        </h2>
      </header>
      <div className={`book-text ${large ? "text-[1.2rem]" : ""}`}>
        {paragraphs.map((p, i) => (
          <p key={i}>
            {p}
            {streaming && i === paragraphs.length - 1 && <span className="stream-caret" aria-hidden />}
          </p>
        ))}
      </div>
    </article>
  );
}

function EmptyStage({ text, action, onAction }: { text: string; action: string; onAction: () => void }) {
  return (
    <div className="max-w-xl rounded-card border border-dashed border-ink/25 p-8">
      <p className="text-lg text-ink-soft">{text}</p>
      <button onClick={onAction} className="btn-primary mt-5">
        {action} <ArrowRight className="h-4 w-4" aria-hidden />
      </button>
    </div>
  );
}
