import type { Metadata } from "next";
import { Inter_Tight, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const interTight = Inter_Tight({
  variable: "--font-headline",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "HydrationNarc — Drink water. Or I'm telling your kidneys.",
  description:
    "A wildly overengineered macOS sensor daemon that tracks your water intake using accelerometer data and a five-algorithm voting system. $15. Lifetime access. No mercy.",
  keywords: ["hydration tracker", "macOS app", "water intake", "sensor daemon", "accelerometer"],
  authors: [{ name: "HydrationNarc" }],
  openGraph: {
    title: "HydrationNarc — Drink water. Or I'm telling your kidneys.",
    description:
      "A wildly overengineered macOS sensor daemon that tracks your water intake using accelerometer data and a five-algorithm voting system.",
    type: "website",
    siteName: "HydrationNarc",
  },
  twitter: {
    card: "summary_large_image",
    title: "HydrationNarc — Drink water. Or I'm telling your kidneys.",
    description:
      "A wildly overengineered macOS sensor daemon. $15. Lifetime access. No mercy.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${interTight.variable} ${jetbrainsMono.variable} h-full`}>
      <body className="h-full antialiased">{children}</body>
    </html>
  );
}
