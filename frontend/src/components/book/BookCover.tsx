"use client";

import { bandColor, onBandColor, padNo } from "@/lib/series";

interface BookCoverProps {
  title?: string;
  author?: string;
  genre?: string;
  tone?: string;
  seriesNo?: number;
  /** "lg" for the studio panel, "sm" for thumbnails. */
  size?: "sm" | "md" | "lg";
  className?: string;
}

/**
 * A three-band paperback cover. The bands take the genre colour; the title
 * sits on the white middle band. Empty fields show as ruled placeholders so
 * the cover reads as "still being made".
 */
export default function BookCover({
  title,
  author,
  genre,
  tone,
  seriesNo,
  size = "lg",
  className = "",
}: BookCoverProps) {
  const band = bandColor(genre);
  const onBand = onBandColor(genre);
  const sizes = {
    sm: { w: "w-28", title: "text-[0.8rem]", meta: "text-[0.5rem]", pad: "px-2.5" },
    md: { w: "w-48", title: "text-lg", meta: "text-[0.6rem]", pad: "px-4" },
    lg: { w: "w-full max-w-[17rem]", title: "text-[1.6rem]", meta: "text-[0.7rem]", pad: "px-5" },
  }[size];

  return (
    <figure
      className={`${sizes.w} aspect-[11/17] flex flex-col overflow-hidden rounded-[2px] bg-sheet shadow-book ${className}`}
      style={{ ["--band" as string]: band }}
      aria-label={title ? `Cover of ${title}` : "Book cover in progress"}
    >
      {/* Top band: series line */}
      <div className={`band-fill flex basis-[30%] flex-col justify-between py-3 ${sizes.pad}`} style={{ color: onBand }}>
        <span className={`caps ${sizes.meta} font-bold`}>TaelioAI</span>
        <span className={`caps tnum ${sizes.meta} opacity-90`}>
          {seriesNo ? `No. ${padNo(seriesNo)}` : "The series"}
        </span>
      </div>

      {/* Middle band: title and author */}
      <div className={`flex flex-1 flex-col items-center justify-center gap-2 border-y-[3px] border-white text-center ${sizes.pad}`}>
        {title ? (
          <p className={`font-display font-bold leading-[1.05] text-ink ${sizes.title} [text-wrap:balance]`}>{title}</p>
        ) : (
          <span aria-hidden className="block h-2.5 w-3/4 rounded-full bg-rule" />
        )}
        {size !== "sm" && (
          <>
            <span aria-hidden className="block h-px w-10 bg-ink/30" />
            {author ? (
              <p className={`caps ${sizes.meta} text-ink-soft`}>{author}</p>
            ) : (
              <span aria-hidden className="block h-1.5 w-1/3 rounded-full bg-rule" />
            )}
          </>
        )}
      </div>

      {/* Bottom band: genre and tone */}
      <div className={`band-fill flex basis-[22%] items-end justify-between py-3 ${sizes.pad}`} style={{ color: onBand }}>
        <span className={`caps ${sizes.meta} font-bold`}>{genre || "Genre"}</span>
        {size !== "sm" && <span className={`caps ${sizes.meta} opacity-90`}>{tone || ""}</span>}
      </div>
    </figure>
  );
}
