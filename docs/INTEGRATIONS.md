# Integrations

This document tracks integration providers, current connectivity behavior, and future sync scope.

## Current status surface

- Frontend dashboard: `/settings/integrations`.
- Backend status endpoint: `GET /v1/integrations/status`.
- Current providers and defaults:
  - Notion: `connected=false`
  - Todoist: `connected=false`
  - Google Drive: `connected=false`
  - Habitica: `connected=false`
  - Anki: `connected=false`
- The UI currently renders each provider as **Not Connected** with a disabled **Connect** button while auth flows are not yet implemented.

## Planned scope (next iterations)

## Notion
- OAuth scopes: TBD
- Sync direction: TBD

## Todoist
- OAuth scopes: TBD
- Sync direction: TBD

## Habitica
- Token/API key flow: TBD
- Sync direction: TBD

## Google Drive
- OAuth scopes: TBD
- Drive folder ingestion flow: TBD

## Anki
- Export mode: CSV/APKG TBD
- Optional AnkiConnect bridge: TBD
