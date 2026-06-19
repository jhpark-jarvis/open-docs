import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OpenDocs",
  description: "AI-powered MapleStory event documentation platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
