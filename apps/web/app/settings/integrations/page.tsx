import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

type IntegrationStatus = {
  provider: string;
  connected: boolean;
};

const providerLabels: Record<string, string> = {
  notion: "Notion",
  todoist: "Todoist",
  google_drive: "Google Drive",
  habitica: "Habitica",
  anki: "Anki",
};

const fallbackProviders: IntegrationStatus[] = [
  { provider: "notion", connected: false },
  { provider: "todoist", connected: false },
  { provider: "google_drive", connected: false },
  { provider: "habitica", connected: false },
  { provider: "anki", connected: false },
];

async function getIntegrationStatuses(): Promise<IntegrationStatus[]> {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

  try {
    const response = await fetch(`${apiBaseUrl}/v1/integrations/status`, {
      cache: "no-store",
    });

    if (!response.ok) {
      return fallbackProviders;
    }

    const data = (await response.json()) as { providers?: IntegrationStatus[] };
    if (!data.providers || data.providers.length === 0) {
      return fallbackProviders;
    }

    return data.providers;
  } catch {
    return fallbackProviders;
  }
}

export default async function IntegrationsPage() {
  const providers = await getIntegrationStatuses();

  return (
    <section className="space-y-4">
      <div>
        <h1 className="text-2xl font-semibold">Integrations</h1>
        <p className="text-slate-600 dark:text-slate-300">Manage your external services and connection status.</p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {providers.map((item) => {
          const providerLabel = providerLabels[item.provider] ?? item.provider;
          const statusLabel = item.connected ? "Connected" : "Not Connected";

          return (
            <Card key={item.provider} className="space-y-3">
              <h2 className="text-lg font-medium">{providerLabel}</h2>
              <p className="text-sm text-slate-600 dark:text-slate-300">Status: {statusLabel}</p>
              <Button disabled variant="outline">
                Connect
              </Button>
            </Card>
          );
        })}
      </div>
    </section>
  );
}
