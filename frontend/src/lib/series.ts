// The TaelioAI series: each genre has its own cover band colour.

export interface Genre {
  name: string;
  color: string;
  /** Text colour that stays legible on the band (small text). */
  onBand: string;
}

export const GENRES: Genre[] = [
  { name: "Fantasy", color: "#1f7a4d", onBand: "#ffffff" },
  { name: "Science Fiction", color: "#2b5fa8", onBand: "#ffffff" },
  { name: "Mystery", color: "#5b3c96", onBand: "#ffffff" },
  { name: "Romance", color: "#c8325a", onBand: "#ffffff" },
  { name: "Horror", color: "#7a1f2b", onBand: "#ffffff" },
  { name: "Thriller", color: "#b07c12", onBand: "#151515" },
  { name: "Adventure", color: "#e8641c", onBand: "#151515" },
  { name: "Drama", color: "#0f7480", onBand: "#ffffff" },
];

export const TONES = [
  "Adventurous",
  "Dark",
  "Light-hearted",
  "Mysterious",
  "Romantic",
  "Gritty",
  "Whimsical",
  "Dramatic",
];

export const SERIES_COLOR = "#e8641c";

export function genreFor(name?: string | null): Genre | undefined {
  if (!name) return undefined;
  const key = name.trim().toLowerCase();
  return GENRES.find((g) => g.name.toLowerCase() === key);
}

export function bandColor(name?: string | null): string {
  return genreFor(name)?.color ?? SERIES_COLOR;
}

export function onBandColor(name?: string | null): string {
  return genreFor(name)?.onBand ?? "#151515";
}

export function wordCount(text: string): number {
  const trimmed = text.trim();
  return trimmed ? trimmed.split(/\s+/).length : 0;
}

export function readingMinutes(words: number): number {
  return words === 0 ? 0 : Math.max(1, Math.round(words / 230));
}

export function padNo(n: number): string {
  return String(n).padStart(3, "0");
}

// ---- Per-browser conveniences (never required for the app to work) ----

const DRAFT_KEY = "taelio_spark";

export interface SparkDraft {
  spark: string;
  genre: string;
}

export function saveSpark(draft: SparkDraft) {
  try {
    sessionStorage.setItem(DRAFT_KEY, JSON.stringify(draft));
  } catch {
    // storage unavailable
  }
}

export function takeSpark(): SparkDraft | null {
  try {
    const raw = sessionStorage.getItem(DRAFT_KEY);
    if (!raw) return null;
    sessionStorage.removeItem(DRAFT_KEY);
    return JSON.parse(raw) as SparkDraft;
  } catch {
    return null;
  }
}

export function nextSeriesNumber(): number {
  try {
    const n = Number(localStorage.getItem("taelio_series_count") || "0") + 1;
    localStorage.setItem("taelio_series_count", String(n));
    return n;
  } catch {
    return 1;
  }
}

// ---- Plain-language errors ----

export function friendlyError(raw: string | null | undefined): { title: string; detail: string } {
  const text = raw || "";
  if (/rate limit/i.test(text)) {
    return {
      title: "Slow down a little",
      detail: "You've reached your plan's limit on requests per minute. Wait a minute, then try again.",
    };
  }
  if (/GEMINI_API_KEY|api key/i.test(text)) {
    return {
      title: "The story engine isn't set up yet",
      detail: "The server is missing its AI provider key, so nothing can be written right now. Whoever runs this TaelioAI server needs to add it.",
    };
  }
  if (/network error|failed to fetch|ERR_CONNECTION/i.test(text)) {
    return {
      title: "Can't reach TaelioAI",
      detail: "The server didn't answer. Check your connection, or that the backend is running, then try again.",
    };
  }
  if (/authentication|token|401/i.test(text)) {
    return {
      title: "Please sign in again",
      detail: "Your session has ended. Sign in with your email to keep writing.",
    };
  }
  return {
    title: "Something went wrong",
    detail: text ? text.replace(/^Internal server error:\s*/i, "") : "Please try again.",
  };
}
