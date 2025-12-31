import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";

// fonts
const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

// metadata
export const metadata: Metadata = {
  title: "Good-job",
  description: "All-in-one job platform",
};

// providers
import { Providers } from "@/providers/providers";
import { DevTestLoader } from "@/components/DevTestLoader";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en" suppressHydrationWarning>
        <body
          className={`${inter.variable} antialiased`}
          suppressHydrationWarning
        >
          <Providers>
            <DevTestLoader />
            {children}
          </Providers>
        </body>
      </html>
    </ClerkProvider>
  );
}
