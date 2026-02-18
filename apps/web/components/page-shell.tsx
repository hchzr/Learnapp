import Link from "next/link";
import { Card } from "@/components/ui/card";

export function PageShell({ title, description }: { title: string; description: string }) {
  return (
    <Card className="max-w-2xl">
      <h1 className="mb-2 text-2xl font-semibold">{title}</h1>
      <p className="mb-4 text-slate-600 dark:text-slate-300">{description}</p>
      <Link href="/" className="text-sm text-blue-600 underline">
        Back to home
      </Link>
    </Card>
  );
}
