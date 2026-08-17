# Homtini — Farm Management System (Project Mycelium)

> An authoritative, factual overview of what this system does, how it is built, and what it has achieved. Written to be readable by both a non-technical marketing writer and another developer. Every claim below is drawn from files in this repository; where a fact cannot be verified from the code or docs, that is stated explicitly.

---

## 1. Project Purpose

This is the management system for **Homtini Farm**, a regenerative farm in Rheenendal on the Garden Route, South Africa. The farm is a living mix of cattle, ducks, blueberries, market-garden rows, cottages/rental accommodation, water infrastructure, and indigenous forest, run by a small team of staff and community members.

Internally the project is codenamed **Project Mycelium** — described in `docs/context/visionv1.md` and `docs/context/project_spec.md` as a *"local-first digital nervous system for a regenerative farm."* The problem it solves is that the farm's operational knowledge previously lived on paper lists, in WhatsApp chats, and in individuals' memories: it didn't scale, couldn't calculate ecological or financial flows, and held institutional memory hostage to whoever happened to write the note.

The system replaces that with a single place to log work, track animals and assets, reconcile money, and preserve knowledge. It is deliberately designed as an **"appliance," not a SaaS dependency**: it runs on the farm's own hardware (initially a hosted server, with a Raspberry Pi target), works offline in Wi-Fi dead zones, and is built to be "white-labelled" so any other regenerative farm can adopt and own the same software. Its stated ambition is to track three forms of capital — **financial** (did we make money?), **ecological** (did we build soil?), and **social** (did we empower the community?) — rather than optimising for yield and profit alone.

---

## 2. Current State Summary

**Production status:** Live and in daily use. The app is deployed to a production domain (`homtini.plot.org.za`) behind Nginx + Gunicorn + systemd + PostgreSQL (see `homtini/homtini_web.service`, `homtini/nginx_config`, `deploy.sh`, `docs/homtini`). A `pull_db.ps1` / `pull_prod_db.py` script exists to pull the production database down for local work, confirming a populated production database is the source of truth.

**Who uses it:** The farm manager and a small staff/community team. A generated snapshot of the live database (`docs/context/FARM_DATA.md`, dated 2026-06-28) names the farm manager (Kobus) and workers Erin, Alex, and David logging tasks, hours, and farm events.

**Application status list:**

| Status item | State (as verifiable in-repo) |
|---|---|
| **Core features complete** | Yes for the main domains — Finance (double-entry ledger, reconciliation, invoicing, cashbook, dashboard), Cattle movement/grazing, Drone mapping, Team todo/backlog (Kanban + planner + routines), plus Inventory, People/payroll, Triage/Rapid Logger, Knowledge base, Map/spatial, and Water infrastructure. See §4. |
| **DB populated** | Yes — production data is real (see the FARM_DATA snapshot) and multiple data-migration/backfill management commands exist (`seed_*`, `backfill_*`, `migrate_*`). |
| **Testing** | Extensive. ~456 Python test functions across ~94 test files, 8 Playwright end-to-end specs, 48 UAT checklists, 76 recorded UAT result JSON files, a dedicated performance-regression harness, and a custom architecture-guard linter. |
| **Deployment** | Yes — production systemd + Nginx + PostgreSQL deployment is documented, with a `deploy.sh` redeploy script. |
| **Real-world feedback** | Yes — real usage is visible in the database snapshot (56 active entities, tasks/hours/events logged by named staff), and the docs record production incidents and root-cause analyses (e.g. `docs/product/05_research/RCA-2026-03-19-git-data-loss.md`, `RCA-2026-05-01-pwa-stale-html-caching.md`, `docs/product/04_done/production-issues-april-2026.md`). |

**Completeness caveat:** The system is feature-rich but not "finished." The architecture guard's latest audit (`docs/audits/current-state.md`, 2026-06-28) reports **0 errors but 115 warnings** (N+1 query risks, view/service-boundary debt, template nesting depth). The backlog (`docs/product/01_backlog/`) lists further work. Development is active — the git history shows ~384 commits since February 2026.

---

## 3. Tech Stack

| Layer | Technology |
|---|---|
| **Backend framework** | Django 5.1.x (`requirements.txt` pins `Django>=5.1,<5.2`) |
| **Language** | Python 3 (type-hinted; ~50,000 lines of non-migration Python under `src/`) |
| **API** | Django REST Framework 3.15 + SimpleJWT 5.3 (JWT + session auth) |
| **Database** | PostgreSQL in production and preferred everywhere (via `psycopg2-binary`); SQLite only as a dev fallback when no `DB_PASSWORD` is set |
| **Background tasks** | Huey (SQLite-backed `SqlHuey`) rather than Celery — chosen for low Raspberry Pi RAM footprint |
| **Templating** | Django Templates + **HTMX** (server-side rendered pages and partials) |
| **Styling** | Hand-curated CSS with a custom design-token system ("Modern Pastoralist", `src/static/css/root.css`) and Tailwind-style utility classes — **no build tooling**, no CDN (local-first); local fonts (Inter body, Playfair Display headlines) |
| **Interactivity** | HTMX + vanilla JavaScript modules; SortableJS (Kanban drag-and-drop); Chart.js (finance charts) |
| **Mapping / geospatial** | Leaflet.js + Leaflet.draw (map rendering/drawing), GeoJSON in WGS84/EPSG:4326, Turf.js (client-side area math), `tifffile` + `pyproj` (GeoTIFF bounds extraction and CRS transforms), `shapely` — **no PostGIS**; geometry stored as GeoJSON `JSONField` on entities |
| **ML / AI** | Google Gemini (via `google-genai`) for two uses: (1) receipt OCR (`src/core/receipt_ocr.py`, Gemini 2.5 Flash) and (2) AI-assisted code linting (`lint.py`, Gemini 2.0 Flash with a Moonshot Kimi fallback). Bill PDF extraction uses `pdfplumber`. The reconciliation "suggestion engine" is rule-based, not ML. |
| **Environment tooling** | `python-dotenv`, pytest + pytest-xdist + pytest-cov/coverage, Playwright (`@playwright/test`) for E2E, a custom `scripts/archguard/` static-analysis linter |

---

## 4. Completed Features

Grouped by functional domain. Each entry describes what the feature does and why it matters.

### Finance
The largest and most mature domain. Money movement flows through a **unified double-entry ledger** (`JournalEntry` / `JournalLine`) with a seeded **chart of accounts** (~40 accounts: assets, liabilities, expenses with keyword maps, income, plus one bank GL per bank account). On top of that sit:

- **Bank statement reconciliation** — CSV upload (Bank Zero/FNB format), per-line actions (purchase, quick-categorize, payment, transfer, cash withdrawal, personal, income/rental/interest/refund), a **suggestion engine** that learns from accepted matches, and support for partial payments. This turns a raw statement into a reconciled set of ledger entries.
- **Costing & margins** — the **finance dashboard** (`/finance/`) shows cash position, income vs expenses (cash-basis), income by source, expenses by category, outstanding invoices/bills, and **enterprise performance** (e.g. poultry feed-cost-vs-egg-revenue ratio, accommodation rental-vs-maintenance ratio) so an off-site owner can see which farm enterprises are healthy.
- **Invoicing** — sale, rental, service, and Umthombo-trust invoice types, recurring invoice schedules, and payment-status tracking; VAT split computed per line.
- **Actual-vs-budget / obligations** — outstanding-bill and outstanding-invoice panels, unpaid-maintenance warnings, and unreconciled-paid-invoice warnings surface what the farm owes and what hasn't been matched to the bank.
- **Cash management** — a cashbook with quick-tap categories (egg sale, salary, contractor, in/out), cash-slip scanning, **cash-count / cash-float reconciliation** (denominations + variance), vouchers with worker signatures, and audit-trail compliance.

### Cattle movement
Rotational grazing is tracked through a **"Grazing Move" farm event** with no bespoke tables: each move records from-paddock → to-paddock, updates the herd's `current_location`, and auto-relocates its map pin. Paddocks track **rest periods** (grazing/resting/ready/never-grazed statuses rendered as coloured map borders), and temporary electric-fence paddocks are supported alongside permanent ones. This gives the farmer a compliance-grade record of where the herd has been and how long each paddock has rested.

### Drone mapping
`DroneImageryOverlay` stores georeferenced drone imagery as map overlays. GeoTIFF files are processed **client-side in the browser** (geotiff.js → WebP) to keep heavy GDAL/rasterio dependencies off the Raspberry Pi; the backend extracts bounds and performs CRS transforms (`tifffile` + `pyproj`). Overlays render in Leaflet and can be **auto-linked to grazing moves** (pre-graze imagery within 7 days of a move), tying aerial imagery to management decisions.

### Team todo / backlog
- **Kanban board** — drag-and-drop columns with "personalities" (backlog / refine / queue / done) that trigger different behaviours (e.g. a scoring modal on refine, a completion modal that logs hours and optionally creates a farm event).
- **Prioritisation** — tasks carry complexity weights and metric scores; a `priority_score` is computed from role-based `ScoringScheme`s.
- **Planner / week-ahead** — a planning view with drag-to-schedule and a week-ahead partial, plus a "routine summary bar" heartbeat.
- **Routines** — recurring farm "heartbeat" tasks in two modes: **Active** (must be checked off daily) and **Passive** ("success by exception" — assumed done unless someone logs a failure), with a 7-day reliability score.
- **Triage inbox** — a catch-all where field "quick captures" (photo + note + GPS + audio) are later categorised into tasks, events, or purchases, so field friction doesn't block capture.

### Additional domains found in the codebase
- **Inventory & ledger** — purchased inputs and farm-produced stock (`InventoryItem` with behaviour tags CONSUME/RETURN/ASSIGN), entity-level holdings ("where is the 10-10-10 fertilizer?"), and task/routine consumption tracking.
- **People & payroll** — profiles with roles, skills offered/learning, contact info, payment schedules, daily/hourly rates, salary bills, and a unified payment log; a "social ledger" tracks community-contributed hours.
- **Knowledge base** — a living library of SOPs and "land stories" (Markdown entries) pinned to entities and skills.
- **Map & spatial** — a unified GeoJSON spatial model for all mappable entities (points, fences/LineStrings, paddock Polygons), with infrastructure (fences, water lines) drawn directly on the map.
- **Water infrastructure & IoT** — water tanks/pumps/outlets with connections ("pump A pumps-to tank B"), pump state and toggle, water-volume logs, and generic IoT devices with sensor readings.
- **Offline-first Rapid Logger** — a mobile PWA using IndexedDB, camera, audio recording, and a sync engine so field capture survives Wi-Fi dead zones.

---

## 5. Data Model Overview

The domain model is built on a shared `TimeStampedModel` base: every record has a **UUID primary key**, `created_at` / `updated_at`, and an `is_obsolete` soft-delete flag (no destructive deletes — history is preserved). The central concept is the **Entity**: a single source of truth for every asset, place, or biological process on the farm.

```
TimeStampedModel (base: UUID pk, timestamps, is_obsolete)
│
├── Entity
│   ├── category ───────→ EntityCategory (name, slug, icon, category_type, behavior tags, map styling)
│   ├── status ─────────→ EntityStatus (label, color_code)
│   ├── parent_entity ──→ Entity (self, tree hierarchy via materialized "path")
│   ├── current_location → Entity (self — e.g. cattle herd's current paddock)
│   ├── geometry (GeoJSON JSONField: Point | LineString | Polygon, WGS84)
│   ├── metadata (JSONField, validated against category schema)
│   ├── attachments ────→ MediaAttachment (GenericFK)
│   └── BiologicalEntity (multi-table-inheritance subclass: species_mix, planting_pattern, cycle_start_date)
│
├── EntityState (state_label, state_data — e.g. "JLF Barrel is Brewing")
├── EntityConnection (source/target Entity, connection_type: pumps_to | gravity_flow | feeds | …)
│
├── FarmEvent (universal polymorphic activity log)
│   ├── event_type ─────→ FarmEventType (name, slug; e.g. "grazing-move", "harvest")
│   ├── primary_actor ──→ people.Profile
│   ├── related_entity ─→ Entity   │ destination_entity ─→ Entity   │ related_entities (M2M)
│   ├── unit_used ──────→ UnitDefinition (fuzzy→metric conversion)
│   └── details/harvest_* / inventory_consumption (JSONField)
│
├── People (app `people`)
│   ├── Profile (user, role→ProfileRole, skills_offered/learning M2M→Skill, contact_info, pay rates)
│   ├── SocialLedgerAccount (total_hours_contributed)
│   └── ProfilePayment (bill FK→core.Bill, related_task FK, payment_type/method)
│
├── Finance (app `core`)
│   ├── Account (chart of accounts: code, name, account_type, keywords, default_vat_rate, default_entity)
│   ├── Purchase → Bill (vendor, due_date, recognition_account, vat split, processing_status, pdf)
│   ├── Invoice (types: SALE|RENTAL|UMTHOMBO|SERVICE|OTHER; payment_status) → InvoiceLine
│   ├── BankAccount → BankStatement → BankStatementLine (direction IN/OUT, status UNMATCHED/RECONCILED/IGNORED)
│   ├── JournalEntry (double-entry; source: MANUAL|CASHBOOK|INVOICE|PAYMENT|BILL|BANK_STATEMENT; status DRAFT→POSTED→RECONCILED)
│   │   └── JournalLine (account, debit | credit, generic entity_ref)
│   ├── Reconciliation (BankStatementLine ↔ JournalEntry)
│   ├── AccountSuggestion, SuggestionDismissal
│   ├── CashbookEntry (Source/Category incl. EGG_SALE, SALARY, CONTRACTOR; linked_bill)
│   ├── CashbookVoucher (signature_png, worker_profile, linked_bill) · CashbookScan · CashCount
│   ├── RecurringInvoice (frequency, expected_amount, window) · JournalEntryReversal
│
├── Inventory (app `core`)
│   ├── InventoryCategory (Behavior: CONSUME|RETURN|ASSIGN)
│   ├── InventoryItem (current_quantity, reorder_point, source: PURCHASED|PRODUCTION, expense_account, status)
│   ├── EntityInventoryHolding (entity, item, quantity)
│   ├── InventoryReservation (invoice_line, status RESERVED/RELEASED) · PackOption
│
├── Tasks & routines (app `core`)
│   ├── KanbanColumn (personality: BACKLOG|REFINE|QUEUE|DONE) · TaskTag
│   ├── Task (assigned_to, apprentice, entity, complexity_weight, metric_scores, priority_score, planned_date, actual_hours)
│   ├── PrioritizationMetric · ScoringScheme (role, metrics M2M)
│   ├── Routine (type ACTIVE|PASSIVE, assigned_to M2M, frequency_type WEEKLY|INTERVAL) → RoutineCompletion
│   ├── TaskInventoryRequirement · RoutineInventoryRequirement
│
├── Drone
│   └── DroneImageryOverlay (processed_image WebP, bounds N/S/E/W, entity FK, opacity)
│
├── Knowledge
│   ├── KnowledgeEntry (markdown content, entry_type, related_entities/categories/skills M2M)
│   └── PolyculturePreset (species_mix, planting_pattern)
│
├── IoT / water
│   ├── IoTDevice (device_type, host_entity, configuration) → SensorReading
│   ├── PumpState (control_mode, current_state, total_runtime_hours) · WaterVolumeLog (log_type, volume_liters)
│
└── Triage (app `triage`)
    └── TriageItem (image, note, audio_clip, gps, entity, is_purchase, ocr_data, is_processed)
```

**Field types/choices that reveal domain richness:**
- `EntityCategory.category_type` → biological | infrastructure | tool | bio_processor | general, plus boolean **behavior tags** (`is_biological`, `is_grazing_area`, `is_water_storage`, `is_water_pump`, `is_water_outlet`, `is_infrastructure_line`, `is_boundary`) that drive feature behaviour without hard-coded slugs (the "white-label" mechanism).
- `BankStatementLine.direction` → IN/OUT (auto-derived from credit/debit); `status` → UNMATCHED/RECONCILED/IGNORED with an `IgnoreReason` enum (bank fee, interest, transfer, cash withdrawal, other).
- `Invoice.InvoiceType` → SALE/RENTAL/UMTHOMBO/SERVICE/OTHER; `PaymentStatus` → UNPAID/PARTIALLY_PAID/PAID.
- `JournalEntry.Source` → MANUAL/CASHBOOK/INVOICE/PURCHASE_RECEIPT/PAYMENT/BILL/BANK_STATEMENT; status DRAFT→POSTED→RECONCILED.
- `Routine.routine_type` → ACTIVE ("trust but verify") vs PASSIVE ("success by exception").
- `KanbanColumn.personality` → BACKLOG/REFINE/QUEUE/DONE (drives modal behaviour on card drop).
- `EntityConnection.connection_type` → pumps_to | gravity_flow | feeds | can_fill | overflows_to | parallel.

---

## 6. Key UI/UX Patterns

- **"Modern Pastoralist" design system** (`docs/product/redesign/DESIGN.md` + `src/static/css/root.css`): earth-tone palette (forest green `#526b4a`, terracotta `#9d4e30`, butter-sand background `#fdffda`), a strict **"no-line" rule** (boundaries expressed through background/surface tonal shifts rather than 1px borders), soft pill-shaped buttons, ambient low-opacity shadows, and generous whitespace ("fallow fields" of UI). All tokens are CSS variables (`--m-*`), with local fonts and no CDNs.
- **Map/list sync** — a Leaflet farm map with a sidebar of "mapped" and "unmapped" entities; clicking one highlights the other. Paddocks render as hollow polygons with status-coloured borders so drone imagery stays visible underneath.
- **Progressive disclosure via HTMX modals** — nearly every list (entities, purchases, bills, invoices, inventory, tasks) opens a detail/edit modal as an HTMX partial rather than a full page, with a documented modal-and-list-refresh pattern to avoid race conditions.
- **High information density** — the finance dashboard is a "bento grid" of cards (cash position, income/expenses chart, breakdowns, outstanding items) with click-to-drill-down into inline HTMX detail panels.
- **Mobile responsiveness + offline-first** — the Rapid Logger is a PWA (manifest + service worker + IndexedDB) that captures photos, audio, and GPS offline and syncs later; client-side image compression and WebM/Opus audio keep storage small.
- **Zero-friction field input** — cascading dropdowns, "fast-tap" category buttons (e.g. cashbook quick categories), and "fuzzy units" (buckets, wheelbarrows) captured at the speed of life and converted to metric values in the background.
- **Success-by-exception** — passive routines appear as static badges (no check-off burden); only failures are logged, keeping daily friction minimal.

---

## 7. Recent Learnings & Best Practices

Drawn from `docs/engineering/prompts/dev/LEARNINGS.md` and `docs/context/build_principles.md`:

- **"Prefetch or Perish" / N+1 is a system killer** — on a Raspberry Pi one bad query locks the DB. `select_related`/`prefetch_related` are mandatory; `@property` methods that do filtered aggregation must be documented and replaced with **subquery annotations** for list contexts (e.g. `InventoryItem.available_quantity`). The ArchGuard rule RU-012 catches these structurally.
- **Coordinate systems** — everything is stored as GeoJSON in **WGS84/EPSG:4326**; projected CRS (UTM) GeoTIFFs are transformed via `pyproj`. No PostGIS — geometry is a `JSONField`, centroids are auto-calculated on save, area math is client-side (Turf.js).
- **Ground-truth geospatial reality** — browser GPS is useless for sub-metre work (~3–5 m error on consumer phones); precision comes from measuring-rope offsets against the mapped paddock boundary, and consumer drone orthomosaics need ground control points (GCPs) + RTK correction to reach centimetre accuracy.
- **HTMX lifecycle management** — third-party libs (SortableJS) need explicit destroy-before-swap cleanup; shared modals must never target page-specific DOM elements (use event-driven refresh via `htmx.trigger()`); check `document.contains()` before destroying.
- **`bulk_update`/`bulk_create` skip `auto_now`** — `updated_at` must be set manually; ArchGuard's atomic-context detection has known AST limitations that require a redundant inner `with transaction.atomic()` (savepoint) per loop iteration.
- **Service layer over model methods** — complex logic (routine completion with transactions, permissions, idempotency) lives in service classes, not models or views; cross-service imports are lazy/local to avoid circular imports.
- **Idempotency patterns** — client-generated UUIDs (return 200 "already captured" for offline sync retries) and daily `last_completed_at` checks (return 409 + current state for double-taps).
- **Migration ordering & data fixes** — data migrations (`RunSQL`/`RunPython`) must run *before* the schema change that removes an enum value; `managed=False → managed=True` requires running `makemigrations` twice.
- **Migration-before-removal** — never reference models in uninstalled apps (Django validates lazy FK references at check time).

---

## 8. File Structure Overview

```
.
├── src/                          # Django project root (manage.py lives here)
│   ├── mycelium/                 # Project config
│   │   ├── settings.py           # Django 5.1, DRF+JWT, Huey, OCR, email, Postgres settings
│   │   └── urls.py               # ~290 URL patterns: pages, HTMX partials, JSON APIs
│   ├── core/                     # Main domain app (the bulk of the system)
│   │   ├── models/               # Partitioned: entities, finance, inventory, tasks, routines, drone, iot, cashbook_*, knowledge, attachments, base
│   │   ├── services/             # ~60 service modules (finance, reconciliation, bill, invoice, cashbook, grazing, spatial, routine, task, payroll, VAT…)
│   │   ├── serializers/          # DRF serializers, partitioned by domain
│   │   ├── views/                # Views partitioned by domain (banking, bills, cashbook, entities, finance, inventory, purchases, tasks, routines…)
│   │   ├── migrations/           # 109 migrations (schema evolution history)
│   │   ├── management/commands/  # ~30 backfill/seed/import/repair commands
│   │   └── receipt_ocr.py        # Gemini-based receipt OCR
│   ├── people/                   # Profiles, roles, skills, payroll, social ledger
│   ├── triage/                   # Offline field capture (TriageItem) + Rapid Logger
│   ├── templates/                # base.html + core/ (pages) + core/partials/ (HTMX fragments) + people/ + triage/
│   └── static/                   # css/ (root.css design tokens + per-feature css), js/ (HTMX, Leaflet, Chart.js, app modules), pwa/ (service worker, IndexedDB app), img/
├── docs/                         # The documentation hub
│   ├── context/                  # vision, charter, project_spec, build_principles, FARM_DATA snapshot
│   ├── engineering/              # prompts (dev/PO/PM), LEARNINGS, state (MODELS/VIEWS/LOGIC/STRUCTURE), systems overviews, runbooks, ADRs
│   ├── product/                  # 00_implemented, 01_backlog, 03_ready, 04_done (archive), 05_research, 06_flows, redesign/
│   └── audits/                   # architecture-guard outputs + performance baselines
├── homtini/                      # Deployment config: systemd unit, nginx config, psql setup, STEPS
├── scripts/archguard/            # Custom static-analysis linter (RU-* rules)
├── tests/                        # core/ (Python), e2e/ (Playwright), uat/ (checklists), performance/, fixtures/
├── deploy.sh                     # Production redeploy script
├── requirements.txt / package.json / playwright.config.js / pytest.ini
└── utilities_knysna/             # Sample municipal utility-bill PDFs used for bill-ingestion testing
```

---

## 9. Outcomes & Metrics (important for the portfolio)

**Verifiable numbers found in-repo:**

- **Codebase size:** ~50,000 lines of Python under `src/` (excluding migrations); 109 migrations in `core` alone (119 across all apps); ~384 git commits since the first commit in February 2026.
- **Testing coverage of the work:** ~456 Python test functions across ~94 test files; 8 Playwright end-to-end specs (`tests/e2e/*.spec.js`); 48 UAT checklists (`tests/uat/*.md`); 76 recorded UAT result JSON files (`docs/product/04_done/*-uat-results.json`).
- **Code quality:** the architecture guard's latest audit (`docs/audits/current-state.md`, 2026-06-28) reports **0 errors / 115 warnings**.
- **Performance discipline:** a query-budget harness (`tests/performance/`, `docs/audits/perf-baseline-2026-08-09.md`) measures per-endpoint query counts against budgets. The baseline recorded 6 endpoints passing budget, 4 marginally over, and one regression (finance dashboard: 88 queries vs a 22 budget) — documented as a known issue to investigate. A separate **bulk-save remediation** (`docs/product/00_implemented/bulk-save-pi-performance.md`) targeted `.save()`-in-loop patterns for Raspberry Pi performance.
- **Live data snapshot** (`docs/context/FARM_DATA.md`, generated 2026-06-28 from the production database): **56 active entities**, **81 open tasks**, **16 tasks completed in the prior 7 days (17.5 hours logged)**, 16 farm events in 7 days, 0 routine failures; a chart of accounts with ~40 accounts; recent purchases totalling several thousand ZAR. *(Note: this is a point-in-time snapshot of a single farm's data, not an aggregate statistic.)*
- **Deployment:** a single production instance at `homtini.plot.org.za`.

**Screenshots & design mockups in the repo:**

- `docs/product/redesign/done/` — `kanban_design.html`, `logger_design.html`, `triage.html`, `inventory_redesign.html`, `inventory_modal_redesign.html`
- `docs/product/redesign/finance_dash_redesign.html`, `docs/product/redesign/stitch-prompt-dashboard.md`
- `docs/product/05_research/eggs-widget-mockup.html`, `docs/product/05_research/abseil-vs-build-principles-comparison.html`
- `src/static/img/farm_map.jpg` (farm map image), `src/static/img/entity-icons/` (cattle, building, pump, water-tank, water-tap), plus PWA icons (`icon-192.png`, `icon-512.png`)
- Root-level images: `login-failure.png`, `farm_map.jpg`, `water-tank.png`, `water-tap.png`, `pump.png`, `cottage-icon-8213839-512.png`, `cow_2395746.png`, `duck.png`

**What is *not* quantified in-repo:** There are **no documented quantitative business-outcome metrics** — no formal "hours saved per week," return-on-investment figure, user-count beyond the named staff in the snapshot, or revenue-growth numbers. **No quantitative business outcomes are documented in-repo**; any such figures would be guesswork. The strongest evidence of impact is the live production database and the breadth of shipped, UAT-tested functionality listed in §4.
