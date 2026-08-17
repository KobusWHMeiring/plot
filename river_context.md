# Plot — Portfolio Handover

**For:** the developer working on the `plot.org.za` repo
**From:** product owner / principal developer
**Date:** 2026-08-17
**Companion file:** `farm-context-prompt.md` (prompt to generate the Farm context file)

---

## 0. Purpose of this document

Plot is being reframed from a single-niche landscaping pitch into a **solo practice that builds operational software for people who work the land** — agriculture, conservation, and land management. It is proven by three shipped products:

1. **Harvester** — urban garden / landscaping operations
2. **River** — river rehabilitation field operations (this case study is written in full below)
3. **Farm** — farm management (finances, cattle movement, drone mapping, team todo/backlog)

Your job is to turn this document into the updated site. Everything you need is here — positioning, voice, site structure, a complete River case study, a Farm slot, and a Harvester migration note. The River case study is intentionally **over-comprehensive**: use the summary card on the home page, and keep the full version available for a "read more" page or a deeper slide. Trim freely — the extras are a menu, not a mandate.

---

## 1. The reframe: positioning & voice

### Current positioning (to be replaced)
> "Plot | Systems Architecture for Landscaping" — "Enterprise efficiency for the modern landscape." — "Run your garden service like a tech company."

This is too narrow. It sells *one* niche, but the actual capability is broader.

### New positioning (use this)
> **Plot** — I build the operational software that runs land-based organisations: field team planning, mapping & GIS, data capture, finances, and reporting. Proven by three production systems in agriculture, conservation, and landscaping.

One-line umbrella you can reuse:
> "I build the operating system for people who work the land."

### Voice change: "we" → "I"
The whole site currently speaks as an agency ("we", "our system", "We are accepting three new partners"). Switch to first-person singular:

| From (agency) | To (individual) |
|---|---|
| "We don't just build websites." | "I don't just build websites." |
| "Our system bridges the gap…" | "My systems bridge the gap…" |
| "We are currently accepting three new landscaping partners." | "I'm currently taking on a small number of new projects." |

**Tone:** confident, benefit-focused, technically credible. A client should finish the page thinking "this person has actually shipped working systems, and can probably solve my problem."

---

## 2. Target site structure

Keep the existing design system (CSS variables, `section-label`, `service-card`, `feature-row`, `app-mockup`, `stat-card`, `btn`, Material Symbols, Plus Jakarta Sans + Playfair Display). Reorganise the home page as:

```
Navbar (unchanged shell, updated links)
Hero                     ← rewritten: broadened, "I" voice, no landscaping-only claims
Methodology / Philosophy ← rewritten: "run your field operation like a tech company"
Case-study carousel      ← NEW: 3 slides (Harvester, River, Farm)
CTA / inquiry form       ← unchanged mechanics, updated copy
Footer                   ← unchanged shell
```

The existing Harvester-specific sections (hero flow card, "The Core OS" / "The Intelligence Stack" service cards, the app-mockup feature rows) get **distilled into the Harvester carousel slide** rather than living as separate page sections. This is what frees the page to hold three projects without becoming a wall of landscaping copy.

---

## 3. Carousel specification

- **3 slides**: Harvester, River, Farm.
- Each slide is a **summary card**, not a wall: project name + domain tagline, a one-line problem → solution, 3–4 key capability bullets with Material Symbols, a one-line tech stack, and a "read the full case study" link (point at the deeper slide or a per-project page if you add them later).
- **Navigation**: prev/next arrow buttons + dots. Keyboard-accessible (arrow keys / tab). Respect `prefers-reduced-motion`.
- **Implementation**: vanilla JS only (matches the existing "vanilla first" ethos — no slider library). A simple translate/opacity transition between slide panels is plenty.
- **If a slide feels too small**, expand it into the full case study (River's full version is in §4.2–4.5 below). The summary card → full case study is a natural progressive-disclosure path.

---

## 4. Case study 1 — River (complete)

### 4.1 Summary card (carousel slide)

> **River** — field-operations system for river rehabilitation
>
> A field team was planning river rehabilitation on paper: litter collection, weeding, planting and admin across multiple river sections, with no single view of who did what, where, or what the cumulative impact was.
>
> I built a Django platform that turns the whole operation into a planned, tracked, measurable workflow.
>
> - 🗺️ **GIS mapping** — interactive map, polygon boundaries, lifecycle stages
> - 📅 **Planning suite** — weekly/monthly/daily planners + 19 field templates
> - 📋 **Smart visit logging** — photos, litter bags, species-level weeding & planting
> - 📊 **Impact dashboards** — bags collected, plants planted, section comparisons
>
> **Stack:** Django · Python · PostgreSQL · Leaflet · vanilla JS — in active production use.

### 4.2 Full case study (long-form)

**Problem.** Rehabilitation of the Liesbeek River is coordinated by a small field team running litter collection, weeding, planting, and administrative work across many river sections. Work was planned on paper; there was no single source of truth for who did what, where, or what the cumulative impact had been. Managers couldn't see progress, and reporting was manual.

**Solution.** A purpose-built web platform that turns river rehabilitation into a planned, tracked, and measurable operation — from "which section do we work today" to "how many bags have we pulled out of the river this year".

**What it does.**

| Capability | Description |
|---|---|
| **GIS section mapping** | Interactive Leaflet map with polygon drawing. Each section holds a GeoJSON boundary and centre point; map hover syncs with the section list. Sections move through lifecycle stages (Mitigation → Clearing → Planting → Follow-up → Community). |
| **Planning suite** | Weekly planner (7-day, split by Team/Manager/Chairperson), monthly calendar, and a daily agenda with tick-to-complete. 19 real-world task templates auto-populate instructions. Tasks can span multiple days via series (`group_id`). |
| **Context-aware visit logging** | Smart forms that adapt to the task type: litter runs capture general + recyclable bag counts; weeding captures species-specific removals with quantities; planting captures species-specific counts; admin stays clean. Notes auto-fill from the task. Photos attach with descriptions. |
| **Impact dashboards** | Global metrics (total bags collected, plants planted, weeding sessions), cross-section comparisons, recent activity, and drill-down into each metric's source logs. |
| **Stage tracking** | Timestamped lifecycle history per section, with a timeline view of rehabilitation progress. |
| **Team to-do (Kanban)** | Drag-and-drop rolling to-do board (To Do / Doing / Done) with position re-indexing. |
| **Excel export** | Multi-sheet workbook export (sections, tasks, visit logs), plus planner and filtered-activity-log exports. |
| **Mobile responsive** | Every view adapts to mobile, including Kanban drag-and-drop and form controls — field-friendly on a phone at the river. |

**Roles.** Team, Manager, and Chairperson assignee types, each with their own planner rows.

**Stack.** Django 6 · Python · PostgreSQL (production) / SQLite (dev) · Django templates · Leaflet.js · vanilla JavaScript · Sentry error monitoring.

### 4.3 Engineering rigor ("spec review")

This is the section that demonstrates *capability* — how it's built, not just what it does. Use as much or as little as fits the design.

- **Service-layer architecture** — business logic lives in `services/` (e.g. `task_services.py`, `visit_log_services.py`), not in views or models. Views only route and prepare context.
- **Performance budgets** — `bulk_create`/`bulk_update` over save-in-a-loop; `select_related()` on every list view to kill N+1 queries; `.values()`/`.only()` for read-only rendering; guarded log calls. These are enforced with **automated N+1 growth tests** and performance budget tests.
- **Observability** — structured logging and Sentry for error monitoring.
- **Architecture Decision Records** — major data-flow or library changes are recorded.
- **Testing** — 20+ unit/integration test files covering planners, dashboards, Kanban, task completion/reopening, form errors, exports and search, plus a per-feature **UAT checklist process** and Playwright E2E (planned/in-progress).
- **Deployment** — Nginx + systemd + PostgreSQL, a one-command deploy script, and a production-DB sync command for safe local debugging.

### 4.4 Outcomes

- **In active production use** by a real field-operations team.
- Shipped with 19 real-world task templates and 8 river sections across 4 task types (litter run, weeding, planting, admin).
- Supported multi-day task series and three assignee roles.
- Production feedback was captured and folded back into the backlog (a real user loop, not a demo).

### 4.5 HTML skeleton (follow the existing design system)

```html
<!-- Carousel slide — River summary card -->
<div class="service-card">
    <div class="service-card__number font-serif">02</div>
    <h3 class="service-card__title font-serif">River</h3>
    <p style="color: var(--color-text-light);">
        Field-operations system for river rehabilitation.
    </p>
    <ul class="service-card__list">
        <li>GIS mapping with lifecycle stages</li>
        <li>Weekly / monthly / daily planners</li>
        <li>Smart visit logging & photos</li>
        <li>Impact dashboards & Excel export</li>
    </ul>
</div>
```

For the full case study, reuse the existing `feature-row` pattern from the current app-mockup:

```html
<div class="feature-row">
    <h4 class="feature-title font-serif">
        <span class="material-symbols-outlined" style="font-size: 1rem; vertical-align: middle;">map</span>
        GIS Section Mapping
    </h4>
    <p style="font-size: 0.9rem; color: var(--color-text-light);">
        Interactive Leaflet map with polygon drawing, GeoJSON boundaries, and lifecycle stages.
    </p>
</div>
```

### 4.6 Extra material (trim freely)

Additional facts available if a deeper "read more" page is wanted:

- **Models:** `Section`, `TaskType`, `Status`, `TaskTemplate`, `Task`, `VisitLog`, `Metric`, `Photo`, `SectionStageHistory`, `TaskCompletionHistory`.
- **Metric types:** litter general, litter recyclable, plant, weed — each with a label (e.g. species) and value.
- **Task types:** litter run, weeding, planting, admin — each with a Material Symbol icon and colour.
- **URL surface:** dashboards, section CRUD + reorder, weekly/monthly planners, daily agenda, task CRUD + search, Kanban + drag-drop API, visit logs (list/create/edit), template + task-type management, and three Excel export endpoints.
- **Tests directory:** `test_dashboard`, `test_monthly`, `test_task_series`, `test_todo_kanban`, `test_visit_log_form`, `test_weeding`, `test_chairperson`, `test_task_reopen`, `test_form_errors`, plus `performance/` (budgets, N+1 growth, discovery).
- **UAT scenarios:** dashboard metric drill-down, form validation error display, planner activity indicators, planner search, reopen completed tasks, section days worked, typeable participant counts.

---

## 5. Case study 2 — Farm (slot)

Populate this from the Farm context file generated via `farm-context-prompt.md`. Use the same structure as River's §4.1–4.5:

- **Summary card** — one-line domain tagline + problem → solution + 3–4 capability bullets + stack.
- **Full case study** — Problem / Solution / capabilities table / Stack / Engineering rigor / Outcomes.
- **Known domains to draw from:** farm finances, cattle movement, drone mapping, team todo/backlogs.

---

## 6. Case study 3 — Harvester (migration)

The current site's Harvester content is woven through the hero and capabilities sections. Distill it into a carousel slide using the same template. Suggested summary:

- **Summary card:** urban garden / landscaping operations; AI handwriting recognition, margin analysis, logistics planning; the "Core OS" + "Intelligence Stack" bullets already exist in the current service cards — reuse them.
- Keep the hero's "workflow automation" card as a *visual* on the slide if you want to retain that illustration.

---

## 7. Copy & voice guidance (we → I)

1. Replace all plural self-references with singular.
2. Replace "landscaping" as the *only* frame with "land-based operations" (agriculture, conservation, landscaping).
3. Keep the premium, benefit-first tone. Example hero rewrite:

> "I don't just build websites. I install the operational operating system that runs land-based organisations — planning, mapping, field data, finances, and reporting."

4. Case studies are written objectively (the system, not "I"), with the capability/credibility carried by the engineering-rigor section. The surrounding site copy carries the "I".

---

## 8. Integration guide (CSS classes)

| Case-study element | Existing class/pattern to reuse |
|---|---|
| Slide / project card | `service-card`, `service-card--highlight`, `service-card__number`, `service-card__title`, `service-card__list` |
| Capability feature rows | `feature-row`, `feature-title` (with `material-symbols-outlined` icons) |
| Section headers | `section-label`, `section-title font-serif` |
| Stats (e.g. "19 templates", "8 sections") | `stat-card`, `stat-card__icon`, `stat-card__label` |
| Buttons / CTAs | `btn btn--primary`, `btn btn--outline` |
| App screenshot mockup | `app-mockup`, `app-mockup__screen` |
| Icons | Material Symbols (`map`, `calendar_today`, `analytics`, `view_kanban`, `download`, `smartphone`, `timeline`, `edit_note`) |
| Carousel controls | new small `.carousel` / `.carousel__arrow` / `.carousel__dot` classes in `style.css` (keep visual language: thin borders, muted colours) |
