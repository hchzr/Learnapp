"use client";

import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";

export function DarkModeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  const isDark = resolvedTheme === "dark";

  return (
    <Button variant="outline" size="sm" onClick={() => setTheme(isDark ? "light" : "dark")}>
      {isDark ? "Light mode" : "Dark mode"}
    </Button>
  );
}
