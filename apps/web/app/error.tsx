"use client";

import { ErrorAlert } from "@/components/ui/alert";

export default function GlobalError({ error }: { error: Error & { digest?: string } }) {
  return (
    <div className="max-w-2xl">
      <ErrorAlert title="Something went wrong" description={error.message || "Please refresh and try again."} />
    </div>
  );
}
