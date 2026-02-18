import type { Metadata } from "next";
import "./globals.css";
import { DarkModeToggle } from "@/components/dark-mode-toggle";
import { Sidebar } from "@/components/sidebar";
import { ThemeProvider } from "@/components/theme-provider";
import { UserHeader } from "@/components/user-header";

export const metadata: Metadata = {
  title: "Life & Learn",
  description: "Planning and learning dashboard shell"
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <div className="flex min-h-screen">
            <Sidebar />
            <main className="flex-1 p-6">
              <div className="mb-6 flex items-center justify-end gap-4">
                <UserHeader />
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
