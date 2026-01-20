# Urban Harvest Platform: Project Context

## 1. Project Overview
**Primary Goal:** To eliminate the manual data entry bottleneck for Urban Harvest by digitizing paper visit forms via AI. The system transforms a multi-hour manual transcription process into an automated, "human-in-the-loop" verification workflow, enabling scalability, accurate data tracking, and improved client retention.

**Key Features:**
*   **AI Form Extraction:** Uses Vision AI (**Current: Gemini 2.5 Flash**; **Roadmap: Gemini 3 Flash**) to extract structured data (inputs, plantings, services) from photos of handwritten forms.
*   **Verification Queue:** A split-screen UI for Admins to validate AI data against the original image.
*   **Client Portal ("Magic Link"):** A secure, time-bound mobile web interface (no login required) for clients to view summaries, rate services (1-5 stars), and submit "Wishlist" requests.
*   **Rejection Management & Audit Trail:** Client-initiated removals are "soft-deleted" (status changed to `REJECTED_BY_CLIENT`) and Admin removals to `REJECTED_BY_ADMIN`, allowing for precise source tracking and historical analysis.
*   **Operational Dashboard:** Real-time metrics on completed visits, pest incidents, and vegetable popularity, plus an **Action Center** for reviewing client additions and rejections.
*   **Client Intelligence:** A dashboard card providing historical insights: Average Visit Duration, Service Frequency, Planting Intensity (Year-over-Year), and volume-weighted "Top 5 Crops".
*   **Agronomic Intelligence (Eco-Score):** Automatically calculates the current "Active Garden" state by projecting crop lifecycles based on biological data (`days_to_maturity` and `harvest_window_days`). Includes a **Manual Removal** override to mark crops as cleared via a "scissors" action.
*   **Spatial Intelligence (Mapping):** A comprehensive geographic system using **Leaflet.js** and **Geopy (Nominatim)** to visualize and manage client locations.
    *   **Operational Map ("God Mode"):** A full-screen dashboard for visualizing client density and clusters.
    *   **Manual Pin-Drop:** An interactive map picker in the Client form to "fine-tune" locations for farms or plots where automated geocoders fail.
    *   **Scheduling Map:** A real-time visualization on the Scheduling Dashboard that color-codes daily visits by Team Leader, helping to spot geographical outliers.
*   **Scheduling Dashboard & Google Calendar Sync:** A dedicated workspace that bridges the master Google Calendar schedule with operational prep sheets. Features manual synchronization for a 14-day rolling window, auto-matching of clients, and manual linking for unmatched events.
*   **Crop Lifecycle Timeline (Gantt):** A 12-month visual representation of the garden's history and future, showing growth phases and harvest windows for every verified planting. Supports "Ground Truth" rendering where bars cut off early if a crop is manually removed.
*   **Smart Planning & Shopping:** Aggregates approved tasks from the *latest verified visits* to generate precise nursery shopping lists.

**Core Data Models:**
*   **`Client`**: The central object for contact, categorization, and **garden context**. Now includes **Spatial Metadata** (`latitude`, `longitude`, `geocoding_status`) to support mapping and route planning.
*   **`ClientAlias`**: Enables 100% accurate auto-matching by mapping alternative calendar names (e.g., "Claire Joy") to master `Client` records.
*   **`Vegetable`**: Defines biological properties including `days_to_maturity`, `harvest_window_days`, `planting_months` (ArrayField), and `category` (Leafy, Root, Fruit, etc.).
*   **`PlantedVegetable`**: Tracks what was planted. Now includes `removal_date` for manual "Ground Truth" overrides.
*   **`TeamLeader`**: Represents the head of a gardening team. Maps to Google Calendar via `gcal_calendar_id` and `gcal_color_id` for automated visit assignment.
*   **`ClientInfrastructure`**: Tracks physical garden assets (Irrigation, Composting systems) and their condition (`GOOD`, `NEEDS_REPAIR`, `BROKEN`).
*   **`Visit`**: The primary event and data container, linked to one `Client`. This model is the center of the application's universe. Statuses include `PENDING_EXTRACTION`, `PENDING_VERIFICATION`, `COMPLETE`, and `SCHEDULED` (for upcoming calendar events).
*   **`CalendarSyncLog`**: Tracks the history, status, and audit trail (created/updated/deleted counts) of every calendar synchronization attempt.
*   **`NextVisitTask`**: The "output" of a verified `Visit`. Features an **Audit Lock** (hard deletes disabled) and tracks `original_quantity` to detect and display client-side modifications (e.g., "Was 5, Now 6"). All removals must be status changes to `REJECTED_BY_ADMIN` or `REJECTED_BY_CLIENT`.

**Target Users:**
*   **Admins (Timothy/Ben):** Verify data, schedule visits, and review client changes.
*   **Team Leaders/Gardeners:** Upload forms via Kiosk mode and consume the **Prep List Dossier** (which includes infrastructure alerts and budget context).
*   **Clients:** Receive email summaries, rate visits, and interact with the proposed plan.

## 2. Design Philosophies & Architectural Principles
**Guiding Principles:**
*   **Schema First:** No UI or Logic work begins until the underlying database schema is defined (e.g., `models.py` changes are the blocker for everything).
*   **Performance First:** We aggressively avoid N+1 queries. Views must use `select_related` and `prefetch_related`.
*   **Zero Friction:** Field interfaces (Kiosk) must be minimal to ensure adoption by gardeners.
*   **Progressive Disclosure:** UI elements show summaries first and reveal details/actions upon interaction.
*   **Synchronous Simplicity:** The Client Portal uses standard **Django Forms (POST)** rather than complex async JS/API calls. Stability > Flashiness.
*   **Service Layer Pattern:** Complex logic (e.g., `is_visit_link_valid`, `get_in_season_vegetables`) is encapsulated in `services.py`, keeping Views thin.

**CSS Strategy (Legacy/Hybrid):**
*   We do **not** use a Tailwind Build Step (CLI/Node) due to local environment restrictions.
*   **Approach:** We maintain a custom `styles.css` but use **AI Coding Agents** to generate and maintain utility-like classes on demand. We prioritize cleaning up existing CSS over a full rewrite.

**App Structure:**
*   `harvester/`: Configuration root (settings, WSGI).
*   `core/`: Monolithic application containing all business logic, models, and templates.

**Technology Choices:**
*   **Django:** Core framework.
*   **Celery & Redis:** Handles async AI processing and email dispatch.
*   **Gemini 2.5 / 3 Flash:** Primary LLM for OCR/Extraction (Speed & Cost focus).
*   **Leaflet.js:** Mapping engine for interactive client visualization.
*   **Geopy (Nominatim):** Backend library for automated address geocoding.
*   **PostgreSQL:** Production database.

SaaS Strategy: Instead of a complex multi-tenant architecture, we adopt a "Software Factory" model. The application is designed to be a clean "Blueprint" that can be cloned, customized, and deployed separately for different landscape companies. This prioritizes code readability and modularity over complex permission systems.

2.5 Architectural Constraints & Non-Negotiables
This section defines the technical "guardrails" for the project. All new features and user stories must adhere to these principles to avoid major refactors and maintain architectural integrity.
Data Model Constraints:
The Visit model is sacred. It is the center of the application's universe. We will avoid adding fields to it unless absolutely necessary. New, complex data related to a visit should be in its own model with a ForeignKey to Visit.
We only add, we don't break. Database migrations must be backwards-compatible. We prefer adding new, nullable fields over changing the meaning or type of existing ones.
Client data is simple. The Client model is for contact and categorization only. All operational data (what they have, what they need) must be derived from their Visit history.
Async Operations & Performance:
External API calls are forbidden in web requests. Any communication with an external service (like Gemini, Sentry, or future APIs) MUST be done in an asynchronous Celery task in core/tasks.py.
No real-time features. The application follows a request/response and asynchronous processing model. We will not implement features requiring WebSockets, live polling, or other real-time technologies.
Frontend & UI Philosophy:
Server-Side Rendering is the rule. All UI will be rendered by Django templates on the server. We will not introduce a separate JavaScript frontend framework (e.g., React, Vue, Svelte).
    Interactivity is minimal. We use vanilla JavaScript for small, targeted enhancements (like showing/hiding forms), not for managing application state on the client side.
    Formset UX: We replace standard Django 'Delete' checkboxes with intuitive 'Trash' icon buttons, using JavaScript to handle the hidden field toggling.
    CSS remains hybrid. We will continue to follow the existing strategy of using a single stylesheet and augmenting it with utility classes, avoiding a Node.js build step.SaaS Strategy ("Software Factory" Model):
No Multi-Tenancy. The application's code must remain simple and single-tenant. New clients/companies mean a new, separate deployment of the entire application "blueprint." User stories must not propose features that would require a complex, shared permission system.

## 3. Key Workflows & Business Logic

**Visit Data Processing:**
1.  **Upload:** Image uploaded via `VisitUploadForm`.
2.  **Extraction (Async):** Celery task sends image to Gemini; returns JSON.
3.  **Draft:** JSON populates a `Visit` record with status `PENDING_VERIFICATION`.
4.  **Verification:** Admin reviews data in `verification_queue_view`.
5.  **Completion:** Admin clicks "Approve". Status -> `COMPLETE`.
6.  **Triggers:** Generates `NextVisitTask` items, AI Narrative Summary, and Client Email.

**Scheduling & Google Calendar Sync:**
1.  **Trigger:** Admin clicks "Sync Calendar" on the Scheduling Dashboard.
2.  **Auth:** Service uses `GOOGLE_SERVICE_ACCOUNT_JSON` to access shared calendars.
3.  **Fetch:** Retrieves events for a rolling 14-day window from multiple calendars.
4.  **Match:** 
    *   **Automated:** Maps event titles to `Client` records using smart prefix extraction and `ClientAlias` mapping.
    *   **Logistical Filtering:** Filters out non-visit events (e.g., "Lunch", "Leave For").
    *   **Manual:** Unmatched events appear in an "Action Required" list for manual linking by Admin.
5.  **Upsert:** Creates or updates `Visit` records with status `SCHEDULED` and mapped `TeamLeader`.
6.  **Print:** Admin filters scheduled visits by date/team and generates the nursery-ready **Prep Pack PDF**.

**Client Engagement (The Feedback Loop):**
*   **The Magic Link:** A token-signed URL sent via email, valid for **5 days** post-visit.
*   **The Portal:** A simple, scrolling page showing the Summary and Homework. Uses **Input-to-Action Masking** (`get_client_display_plan`) to simplify the UX (e.g., "Pesticide" input is displayed as "Do Pest Control").
*   **Interaction:** A **single form** allows the client to:
    *   Rate the visit (1-5 stars).
    *   Leave a comment.
    *   Select "Wishlist" items (Checkboxes filtered by Season). Items are grouped into simplified categories: **Vegetables**, **Herbs**, and **Flowers**.
    *   Remove suggested items (Sets status to `REJECTED_BY_CLIENT`).
*   **Submission:** Standard POST request. Creates/Updates `NextVisitTask` items with `source='CLIENT'` and `is_archived=False`.

**Operational Planning (The Shopping Run):**
*   **Review (Action Center):** Admin reviews additions and rejections on the Dashboard. Displays comparison of `original_quantity` vs client requested quantity.
    *   **Accept All Changes:** Approves additions and archives rejections in one click.
    *   **Restore Item:** Overrides a client rejection, moving it back to `APPROVED` and setting source to `GARDENER`.
*   **Prep List Dossier:** Gardeners receive a "Dossier" view containing budget context and **Infrastructure Alerts** (items marked `NEEDS_REPAIR` or `BROKEN`).
*   **Aggregation:** Admin selects a batch of clients for the upcoming week.
*   **Logic:** The system identifies the **Latest Verified Visit** for each selected client, pulls all `APPROVED` tasks, and sums them up.
*   **Output:** An Excel Shopping List organized by Unit (Tray vs. Pot) and Item Name.

**Client Intelligence (Stats & Scoring):**
*   **Aggregation:** `ClientStatsService` aggregates historical data (Frequency, Duration, Intensity).
*   **Rhythm:** Calculates **Average Visit Duration** (filtered for visits with start/end times) and **Visit Frequency**.
*   **Top Crops:** Ranked by **Total Volume** (not frequency). Volume is calculated using heuristic multipliers: 128 plants for full Trays and a 200x multiplier for fractional trays (quantity < 1).
*   **Intensity:** Averages planting quantities (Trays vs 6-Packs) across all verified visits to gauge garden activity levels.

**Agronomic Intelligence (Lifecycle Projections):**
*   **Active Status:** Determined by comparing the current date to `visit_date + (days_to_maturity + harvest_window_days)`, provided `removal_date` is null.
*   **Ground Truth:** Allows manual termination of a crop lifecycle via the UI, which immediately removes it from "Active" calculations and truncates its Gantt bar.
*   **Cross-DB Reliability:** To avoid PostgreSQL interval casting errors (`bigint to interval`), lifecycle arithmetic is performed in the **Python Service Layer** (`AgronomicService`) rather than raw SQL.
*   **Gantt Grid:** Uses a percentage-based layout where 100% = 365 days. Growth and harvest bars are clipped to the visible 12-month window.

**Job Costing & Profitability:**
*   **Fee Normalization:** To prevent profit inflation, fixed monthly budgets are divided by the client's `frequency` (e.g., 4 visits/mo) to calculate a "Per-Visit Fee" for financial reporting.
*   **Cost Allocation:**
    *   **Direct Materials:** Derived from master prices in `Input` and `Vegetable` (weighted by unit type: Tray vs. Plug).
    *   **Overheads:** Daily labor and transport rates are split across all visits for a specific team/day. If start/end times are available, overheads are weighted by visit duration.
*   **Reporting:** A dedicated Costing Dashboard and Excel Export provide Timothy (Finance) with actual-vs-budget visibility.

## 4. "Finnicky Bits" & Known Issues
*   **AI Hallucination:** The AI is a "Drafting Tool." We use **Gemini Flash** prompts tuned to extract "Homework" into bullet points.
*   **Unit Normalization:** `tasks.py` maps chaotic inputs (e.g., "2 bgs") to Database Enums.
*   **Timezones:** Server is UTC; South Africa is UTC+2. `services.py` accounts for this to prevent premature link expiry.
*   **Email Styling:** Gmail/Outlook strip external CSS. We must use **Inline CSS** for email templates.
*   **Seasonality:** Defined by an `ArrayField` of integers (1-12) on the `Vegetable` model. New vegetables must have this populated.
*   **Database Constraints:** The `is_archived` field on `NextVisitTask` is NOT NULL. All creation logic (AI, Manual, Client) must explicitly set it to `False` to avoid extraction failures.
*   **AI Re-processing Risk:** The background task `_sync_next_tasks` uses a hard `.delete()` on all tasks. If AI re-processes a form after a client has made requests, those requests (`source='CLIENT'`) will currently be lost.
*   **Copy List Scraping:** The "Copy List" logic in `visit_detail.html` relies on DOM scraping. It is "Status Aware" (ignores rejections) but remains vulnerable to HTML structure changes.
*   **Dashboard Lifecycle:** The Dashboard Action Center modal replaces content with a success message when empty. It currently requires a page refresh to detect new requests that arrive while the user is on the dashboard.
*   **Heuristic Multipliers:** Top Crop scoring uses hardcoded weights (e.g., 200 plants for fractional trays, 128 for full trays) in `services.py`. These are based on industry standards but are currently immutable without code changes.
*   **Unit Assumptions:** The "Fractional Rule" (quantity < 1 triggers a 200x multiplier) assumes that any decimal planting record represents a tray percentage. This logic resides in the intelligence service layer.
*   **Database Casting (PostgreSQL vs SQLite):** Direct SQL date arithmetic using integers (days) fails on PostgreSQL without explicit interval casting. We prioritize performing these calculations in **Python** to ensure the code remains database-agnostic.
*   **Gantt Temporal Alignment:** The timeline uses a 30.4-day month approximation to align a 12-month grid with a 365-day percentage-based layout.
*   **CSS Utility Reliance:** Since we don't use a Tailwind JIT compiler, "arbitrary value" utilities (like `bg-green-50/50`) or specific sizing (`w-48`) must be manually added to `utilities.css`. Missing classes will result in zero-size elements.
*   **Frequency Divisor:** Costing logic defaults to `frequency=1` if not specified to ensure divisions never fail, though the model enforces a `MinValueValidator(1)`.
Safe Migration Strategy: We strictly follow a "Safe Enrichment" pattern for migrations. We use qs.filter().update() to apply metadata (Categories/Seasons) to existing rows. We avoid update_or_create or get_or_create in migrations to prevent accidental generation of "Ghost Vegetables" that differ only by capitalization or spacing.


## 5. Development & Deployment
**Environment:**

 **Local Development:** Standard Django (`python manage.py runserver`). **No Docker.** Requires a `.env` file in the project root with the following keys:
    ```
    SECRET_KEY=...
    DEBUG=True
    GOOGLE_API_KEY=...
    GOOGLE_SERVICE_ACCOUNT_JSON=...
    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0
    TURBOSMTP_KEY=...
    TURBOSMTP_SECRET=...
    SENTRY_DSN=...
    ```
*   **Production:** **Dockerized.** Uses `docker-compose.yml`. Nginx proxies to Gunicorn.
Testing Strategy: We prioritize Integration Tests (Business Logic Flows) over granular Unit Tests.
Critical Path: The "Golden Flow" (Upload -> Extract -> Verify -> Wishlist -> Shopping List) must be covered by automated tests to prevent regression as the system evolves.
Logic Tests: Complex parsers (e.g., parse_quantity_unit) require unit tests covering edge cases.
**Dependencies:**
*   **Primary AI:** Google Gemini 2.5 Flash (Targeting Upgrade to Gemini 3 Flash).
*   **Redis:** Essential for the Celery queue.


