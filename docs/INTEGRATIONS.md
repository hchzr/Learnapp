# Integrations (Placeholder)

This document will track scopes, sync cadence, and data mapping rules.

## Runtime gating

Integrations are now gated by feature flags in `feature_flags`:

- `notion_sync`
- `todoist_sync`
- `drive_ingestion`
- `anki`

When a flag is disabled, the frontend hides related integration UI.

## Notion
- OAuth scopes: TBD
- Sync direction: TBD

## Todoist
- OAuth scopes: TBD
- Sync direction: TBD

## Habitica
- Token/API key flow: TBD
- Sync direction: TBD

## Google
- OAuth scopes: TBD
- Drive folder ingestion flow: TBD

## Anki
- Export mode: CSV/APKG TBD
- Optional AnkiConnect bridge: TBD
