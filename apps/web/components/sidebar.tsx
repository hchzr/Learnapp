import Link from "next/link";

const navItems = [
  ["/", "Home"],
  ["/calendar", "Calendar"],
  ["/study-plan", "Study Plan"],
  ["/lessons", "Lessons"],
  ["/anki", "Anki"],
  ["/exercises", "Exercises"],
  ["/tasks", "Tasks"],
  ["/habits", "Habits"],
  ["/insights", "Insights"],
  ["/settings/integrations", "Integrations"]
] as const;

export function Sidebar() {
  return (
    <aside className="w-64 border-r border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-950" data-testid="sidebar-nav">
      <h2 className="mb-4 text-lg font-semibold">Life & Learn</h2>
      <nav className="space-y-2">
        {navItems.map(([href, label]) => (
          <Link key={href} href={href} className="block rounded-md px-3 py-2 hover:bg-slate-200 dark:hover:bg-slate-800">
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
