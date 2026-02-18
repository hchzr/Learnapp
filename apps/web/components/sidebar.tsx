import Link from "next/link";
import type { FeatureFlags } from "@/lib/feature-flags";

const navItems = [
  ["/", "Home", null],
  ["/calendar", "Calendar", null],
  ["/study-plan", "Study Plan", "planner"],
  ["/lessons", "Lessons", null],
  ["/anki", "Anki", "anki"],
  ["/exercises", "Exercises", "exercises"],
  ["/tasks", "Tasks", null],
  ["/habits", "Habits", null],
  ["/insights", "Insights", null],
  ["/settings/integrations", "Integrations", null]
] as const;

export function Sidebar({ featureFlags }: { featureFlags: FeatureFlags }) {
  const visibleNavItems = navItems.filter(([, , featureFlag]) => {
    if (!featureFlag) {
      return true;
    }
    return featureFlags[featureFlag];
  });

  return (
    <aside className="w-64 border-r border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-950" data-testid="sidebar-nav">
      <h2 className="mb-4 text-lg font-semibold">Life & Learn</h2>
      <nav className="space-y-2">
        {visibleNavItems.map(([href, label]) => (
          <Link key={href} href={href} className="block rounded-md px-3 py-2 hover:bg-slate-200 dark:hover:bg-slate-800">
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
