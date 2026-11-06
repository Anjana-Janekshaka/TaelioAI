import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";

// Self-hosted variable fonts (SIL OFL 1.1, licences in ./fonts), so builds
// never depend on fetching from Google Fonts.
const display = localFont({
  src: "./fonts/JosefinSans-Variable.woff2",
  weight: "100 700",
  variable: "--font-display",
  display: "swap",
});

const ui = localFont({
  src: "./fonts/Figtree-Variable.woff2",
  weight: "300 900",
  variable: "--font-ui",
  display: "swap",
});

const book = localFont({
  src: [
    { path: "./fonts/Literata-Variable.woff2", weight: "200 900", style: "normal" },
    { path: "./fonts/Literata-Italic-Variable.woff2", weight: "200 900", style: "italic" },
  ],
  variable: "--font-book",
  display: "swap",
});

export const metadata: Metadata = {
  title: "TaelioAI - Your AI Storytelling Companion",
  description: "Turn a spark into a finished story: TaelioAI's agents build the idea, write the story and revise it with you.",
  keywords: ["story writing", "creative writing", "storytelling", "fiction", "writing companion"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${display.variable} ${ui.variable} ${book.variable}`}>
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
