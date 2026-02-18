# Life & Learn — V2 Acceptance Criteria (Definition of Done)

This document is the single source of truth for what "V2" means.
A release is considered **V2-complete** only when all items below are satisfied.

---

## 0) Global Quality Bar

### 0.1 Product requirements
- The webapp provides a coherent, student-friendly dashboard for a Terminale student:
  - merges calendar events, tasks, study sessions, habits
  - syncs external services (Notion, Todoist, Habitica, Google Drive)
  - supports Anki workflows (export + optional push)
  - supports lesson ingestion → flashcards → fiches → exercises → planning loop
- UX is sleek, fast, and stable:
  - consistent layout and design system across pages
  - good empty states, loading states, error states
  - no broken navigation paths

### 0.2 Engineering requirements
- CI is green on main:
  - lint, typecheck, unit tests
  - at least one integration test suite for sync logic (mocked APIs)
  - at least minimal E2E tests for core flows
- All background jobs are:
  - idempotent
  - retry-safe with backoff
  - observable (job status + logs)
- All AI outputs written to DB are validated against schemas.
- No secrets are committed. `.env.example` is complete.

### 0.3 Security & privacy requirements
- OAuth tokens and API secrets stored encrypted-at-rest.
- PII/tokens are never logged. Logs are redacted by default.
- Least-privilege OAuth scopes are used (Drive limited to selected folder if possible).
- Users can disconnect integrations and delete their data (including derived data).
- Rate limiting exists on auth + AI endpoints + sync triggers.

---

## 1) Onboarding & Integrations

### 1.1 Authentication
- Users can sign up / sign in.
- Google OAuth is supported (required for Drive integration).
- Sessions are secure (HTTP-only cookies or equivalent).
- Logout works across the app.

**Acceptance test**
- A new user can create an account, sign in, and reach the dashboard.

### 1.2 Integration connections (Settings → Integrations)
The app supports connecting and showing status for:
- Notion (OAuth)
- Todoist (OAuth)
- Google Drive (OAuth)
- Habitica (API token)
- Anki integration mode (choose one or more):
  - Export-only (CSV / APKG)
  - Optional: AnkiConnect push workflow (requires user-side bridge)

**Acceptance tests**
- Each integration shows: Disconnected → Connecting → Connected status.
- Connected integrations can be disconnected cleanly (revocation when available).
- No integration blocks app usage if unconnected (feature flags + graceful degradation).

---

## 2) Canonical Data Model (Unified Source of Truth)

### 2.1 Canonical entities exist and are used across the app
Minimum canonical entities for V2:
- User
- ExternalAccount (per integration)
- AuditLog
- Event (calendar items + time blocks)
- Task (from Todoist/Notion + internal)
- Habit, HabitLog (from Habitica + internal)
- LessonDocument (Drive file metadata)
- LessonUnit (structured content chunks)
- Deck, Flashcard (generated and/or imported/exported)
- Exercise, Attempt (generated + curated)
- Objective, Exam, StudyPlan, StudySession
- Mastery signal per concept/topic

**Acceptance**
- External objects are always mapped into canonical objects and displayed from canonical objects.
- External IDs and sync cursors are stored to support incremental sync and dedupe.

### 2.2 Sync correctness rules
- Sync is incremental where supported (delta cursors / updated_since).
- Dedupe rules exist (external_source + external_id uniqueness).
- Conflict strategy is documented and implemented:
  - External services remain authoritative for their native fields unless explicit bidirectional support exists.
  - The app may enrich canonical objects with internal metadata (duration, difficulty, tags).
  - When a field is editable internally and mapped externally, pushes are explicit and logged.

**Acceptance tests**
- Sync can be run repeatedly without duplicating items.
- Failures are logged, retried, and do not corrupt state.

---

## 3) Dashboard & Core UX

### 3.1 Home Dashboard ("Today")
Dashboard includes:
- Today timeline: events + time blocks + study sessions
- Top tasks (from unified tasks)
- Anki: due count summary (even if export-only, show planned review queue)
- Habits snapshot (streaks / today's completion)
- "Start next session" CTA that launches the guided study flow (see §7)
- Quick add: task, event/time-block, habit log (optional), study session

**Acceptance**
- Dashboard loads in <2s on normal connection after initial sync.
- All cards handle empty states gracefully (no integrations connected, etc.).

### 3.2 Navigation
Left nav includes:
- Home
- Calendar
- Study Plan
- Lessons
- Anki
- Exercises
- Tasks
- Habits
- Insights
- Settings (Integrations)

**Acceptance**
- Every nav item routes to a working page with at least V2 functionality described here.

---

## 4) Calendar & Planning

### 4.1 Unified calendar view
- Day / week / month views
- Shows:
  - imported events if available (or internal events at minimum)
  - internal time blocks (study, sport, free time)
  - planned study sessions

### 4.2 Time blocking
- Users can create/edit/delete time blocks (study/sport/free time/custom).
- Drag-and-drop rescheduling
- Conflict detection (visual + warning)

**Acceptance tests**
- A user can plan a day with study + sport + free time blocks.
- Rescheduling updates the canonical DB and persists on reload.

---

## 5) Tasks & Projects

### 5.1 Unified task list
- Pull tasks from Todoist and/or Notion (when connected).
- Internal tasks also supported.
- Canonical tasks support:
  - title, description, due date
  - project/area
  - tags (subject/chapter)
  - estimated duration
  - priority / load (light/medium/heavy)

### 5.2 Task → Plan integration
- A user can turn tasks into planned study sessions (manual or assisted).
- Planner can schedule tasks into available time blocks.

**Acceptance**
- User sees merged task list without duplicates.
- Completion status updates in canonical DB; optional push-back is explicit and audited.

---

## 6) Habits & Health (Habitica + internal)

### 6.1 Habit tracking
- Pull habits/dailies from Habitica (if connected) and show status/streak.
- User can log completion for the day.
- Internal habits supported if Habitica not connected.

### 6.2 Insights (basic)
- At least one insights view:
  - habit streaks
  - time spent vs planned
  - study completion rate by week

**Acceptance**
- Habits module works with Habitica connected and in internal-only mode.

---

## 7) Lessons Library (Google Drive) & Knowledge System

### 7.1 Drive ingestion
- User selects a Drive folder as “Lessons folder”.
- App detects new/updated files in that folder (polling acceptable for V2).
- Supported file types:
  - PDF
  - DOCX
  - Google Docs (export)
  - Images (OCR fallback)

### 7.2 Structured LessonUnits
- Ingested text is split into LessonUnits:
  - subject, chapter, title
  - extracted text chunks with stable IDs
  - source pointers to file + page ranges where possible

### 7.3 Search
- Full-text search at minimum.
- Prefer semantic search if implemented.

**Acceptance tests**
- Upload a PDF into Drive folder → appears in Lessons within a reasonable time.
- Lesson can be opened and searched.

---

## 8) Anki & Flashcards (V2)

### 8.1 Flashcard generation
- From a selected LessonDocument or LessonUnit:
  - generate a set of flashcards
  - each card has: question, answer (or cloze), tags, deck suggestion, provenance link
- Must pass validation:
  - no empty fields
  - not overly long (configurable)
  - avoids multi-fact cards (card-lint)

### 8.2 Review queue UI
- Generated cards appear in a “Review & Approve” queue:
  - user can edit, delete, approve
  - bulk approve supported

### 8.3 Export / Push
At least one export method must be fully functional:
- CSV export compatible with Anki import

Optional V2+:
- APKG export
- AnkiConnect push mode via user-side bridge

**Acceptance**
- User can generate cards from a lesson, approve them, export CSV, import into Anki successfully.
- No duplicate exports unless user requests duplication (deck versioning).

---

## 9) Fiches de révision (V2)

### 9.1 Fiche generator
From a lesson:
- produce a structured fiche with:
  - key definitions
  - methods / techniques
  - essential formulas
  - typical bac-style question types
  - common traps/mistakes
  - short recap checklist

### 9.2 Export targets
- In-app viewer
- PDF export
- Optional: Export to Notion page (if Notion connected)

**Acceptance**
- A user can generate a fiche from a lesson and export to PDF.
- If Notion connected, a user can export a fiche to a Notion page and re-export updates that page.

---

## 10) Exercises & Socratic Tutor (V2)

### 10.1 Exercise sources
- Generated exercises aligned to lesson concepts:
  - multi-difficulty ladder (easy → medium → hard)
  - full solutions and marking scheme
- Curated exercises from the internet:
  - store title, URL, source, difficulty, concept tags
  - no heavy scraping required by default (links are acceptable)

### 10.2 Socratic tutoring
- Step-by-step attempt flow:
  - user submits a step or partial reasoning
  - tutor responds with hint, question, or correction
- The tutor avoids giving full solutions immediately unless user asks explicitly.
- Attempts are saved and used to update mastery signals.

**Acceptance**
- A user can complete an exercise with hints, see a correction, and have the attempt recorded.

---

## 11) Planner Engine (V2)

### 11.1 Inputs
- Exam dates and weights (user-defined)
- Objectives (e.g., “master chapter X by date Y”)
- Availability constraints:
  - sleep window
  - fixed commitments (events)
  - sport and free time blocks
- Workload signals:
  - Anki due load
  - mastery weaknesses from exercises/flashcards

### 11.2 Outputs
- Auto-generated weekly plan:
  - distribution across subjects
  - scheduled study sessions in available time blocks
- Auto-generated daily plan:
  - specific sessions with:
    - lesson units to study
    - anki review block
    - exercises to do
- Replanning:
  - if user misses sessions, plan adjusts without overpacking

**Acceptance**
- A user can set exams/objectives and generate a weekly plan.
- The plan updates after missed sessions and after new mastery signals appear.

---

## 12) Notifications & Coach (V2)

### 12.1 Notifications
- In-app notifications at minimum.
- Optional: email notifications for:
  - upcoming planned sessions
  - overdue tasks
  - Anki due spikes

### 12.2 Coach chat (Orchestrator)
- A chat assistant inside the app that can:
  - “Plan my week”
  - “Generate flashcards from this lesson”
  - “Give me exercises on topic X”
  - “Create a fiche for chapter Y”
- The assistant triggers internal pipelines and returns results + links.

**Acceptance**
- Coach can successfully run at least 3 multi-step flows end-to-end and persist outputs.

---

## 13) Data deletion & Portability

### 13.1 Disconnect integrations
- Users can disconnect each integration (revoking tokens when possible).
- Disconnection behavior is explicit:
  - keeps canonical data (optional) or deletes associated data (user choice).

### 13.2 Delete account
- Delete all user data:
  - canonical objects
  - derived AI outputs
  - stored tokens
  - files/caches

**Acceptance**
- Delete account fully removes user’s data from DB and storage.

---

## 14) Release Checklist (V2)

- All acceptance criteria above pass.
- E2E tests cover at least:
  - onboarding + connect Drive
  - ingest lesson
  - generate cards
  - export CSV
  - create weekly plan
  - complete one exercise with tutor
- Documentation includes:
  - ARCHITECTURE.md
  - INTEGRATIONS.md (scopes, tokens, sync limits)
  - RUNBOOK.md (jobs, troubleshooting)
- No high severity security issues open.
