import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "TaelioAI - Your AI Storytelling Companion",
  description: "Generate, write, and edit stories effortlessly with AI-powered assistance",
  keywords: ["AI", "story writing", "creative writing", "storytelling", "fiction"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
            {children}
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}