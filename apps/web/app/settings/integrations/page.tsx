import { PageShell } from "@/components/page-shell";
import { getFeatureFlags } from "@/lib/feature-flags";

export default async function IntegrationsPage() {
  const flags = await getFeatureFlags();
  const enabledIntegrations = [
    ["Notion", flags.notion_sync],
    ["Todoist", flags.todoist_sync],
    ["Google Drive ingestion", flags.drive_ingestion],
    ["Anki", flags.anki]
  ].filter(([, enabled]) => enabled);

  const description =
    enabledIntegrations.length === 0
      ? "No integrations are enabled for this environment."
      : `Enabled integrations: ${enabledIntegrations.map(([label]) => label).join(", ")}.`;

  return (
    <PageShell
      title="Integrations"
      description={description}
    />
  );
}
