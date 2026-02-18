import Link from "next/link";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Typography } from "@/components/ui/typography";

export function PageShell({ title, description, home = false }: { title: string; description: string; home?: boolean }) {
  return (
    <Card className="max-w-2xl">
      <CardHeader className="page-stack">
        <Typography as="h1" variant="h1">
          {title}
        </Typography>
        <Typography variant="lead">{description}</Typography>
      </CardHeader>
      {!home && (
        <CardContent>
          <Link href="/" className="text-sm text-blue-600 underline underline-offset-2 dark:text-blue-400">
            Back to home
          </Link>
        </CardContent>
      )}
      {home && (
        <CardFooter>
          <Typography variant="body">Use the sidebar to explore upcoming modules.</Typography>
        </CardFooter>
      )}
    </Card>
  );
}
