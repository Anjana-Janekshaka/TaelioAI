import type { Metadata } from "next";
import { Josefin_Sans, Figtree, Literata } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";

const display = Josefin_Sans({
  subsets: ["latin"],
  weight: ["600", "700"],
  variable: "--font-display",
  display: "swap",
});

const ui = Figtree({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-ui",
  display: "swap",
});

const book = Literata({
  subsets: ["latin"],
  style: ["normal", "italic"],
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
