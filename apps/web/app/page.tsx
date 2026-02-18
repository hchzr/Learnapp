import { Card } from "@/components/ui/card";

export default function HomePage() {
  return (
    <Card>
      <h1 className="mb-2 text-3xl font-bold">Life & Learn</h1>
      <p className="text-slate-600 dark:text-slate-300">
        Welcome to the project skeleton. Use the sidebar to explore upcoming modules.
      </p>
    </Card>
  );
}
