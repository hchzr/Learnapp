import type { Metadata } from "next";
import "./globals.css";
import { DarkModeToggle } from "@/components/dark-mode-toggle";
import { Sidebar } from "@/components/sidebar";
import { ThemeProvider } from "@/components/theme-provider";
import { getFeatureFlags } from "@/lib/feature-flags";

export const metadata: Metadata = {
  title: "Life & Learn",
  description: "Planning and learning dashboard shell"
};

export default async function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const featureFlags = await getFeatureFlags();

  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <div className="flex min-h-screen">
            <Sidebar featureFlags={featureFlags} />
            <main className="flex-1 p-6">
              <div className="mb-6 flex justify-end">
                <DarkModeToggle />
              </div>
              {children}
            </main>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
