export const FEATURE_FLAG_NAMES = [
  "notion_sync",
  "todoist_sync",
  "drive_ingestion",
  "anki",
  "exercises",
  "planner"
] as const;

export type FeatureFlagName = (typeof FEATURE_FLAG_NAMES)[number];
export type FeatureFlags = Record<FeatureFlagName, boolean>;

export const DEFAULT_FEATURE_FLAGS: FeatureFlags = {
  notion_sync: false,
  todoist_sync: false,
  drive_ingestion: false,
  anki: false,
  exercises: false,
  planner: false
};

function sanitizeFeatureFlags(input: Partial<Record<string, unknown>> | null | undefined): FeatureFlags {
  const flags = { ...DEFAULT_FEATURE_FLAGS };
  for (const name of FEATURE_FLAG_NAMES) {
    if (typeof input?.[name] === "boolean") {
      flags[name] = input[name] as boolean;
    }
  }
  return flags;
}

export async function getFeatureFlags(): Promise<FeatureFlags> {
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!apiBaseUrl) {
    return DEFAULT_FEATURE_FLAGS;
  }

  try {
    const response = await fetch(`${apiBaseUrl}/v1/feature-flags`, {
      cache: "no-store"
    });

    if (!response.ok) {
      return DEFAULT_FEATURE_FLAGS;
    }

    const payload: { flags?: Partial<Record<string, unknown>> } = await response.json();
    return sanitizeFeatureFlags(payload.flags);
  } catch {
    return DEFAULT_FEATURE_FLAGS;
  }
}
