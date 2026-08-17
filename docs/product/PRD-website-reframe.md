# PRD — Plot Website Reframe

**Product:** plot.org.za marketing site
**Status:** Approved for build
**Author:** Product owner + developer
**Date:** 2026-08-17
**Supersedes:** `design1.md` (stale Tailwind mockup — archived, not followed)

---

## 1. Overview

Reframe the Plot site from a single-niche **landscaping** pitch into a **solo practice that builds operational software for people who work the land** — agriculture, conservation, and land management. The credibility is carried by three shipped, production systems (Harvester, River, Farm), each with a summary card on the home page and a full per-project case-study page.

### Goal

A visitor leaves the site convinced: *"this person has actually shipped working systems, and can probably solve my problem."*

### Positioning (replaces current)

> **Plot** — I build the operational software that runs land-based organisations: field team planning, mapping & GIS, data capture, finances, and reporting. Proven by three production systems in agriculture, conservation, and landscaping.

Umbrella line (reusable):

> "I build the operating system for people who work the land."

---

## 2. Background

### Current state (verified in repo, 2026-08-17)

- Django 6.0 site whose real content is a single landing page: `core/templates/core/home.html` + `core/static/core/css/style.css`.
- Built with a custom-CSS design system ("Modern Pastoralist"): CSS variables (`--color-primary`, `--color-accent`, `--color-highlight`), `.section-label`, `.service-card`, `.feature-row`, `.app-mockup`, `.stat-card`, `.btn`, Material Symbols, Plus Jakarta Sans + Playfair Display.
- Two routes only: `home` and `submit_inquiry` (HTMX POST → `PilotInquiry` model). No `docs/` or `product/` directory.
- The Harvester pitch is woven through hero → methodology → "Core OS / Intelligence Stack" cards → platform section → CTA.
- `design1.md` is a stale Tailwind-CDN mockup with a different palette (forest `#1A3A17` / gold `#D4AF37`). **Do not follow it.**

### Target state

Same design system and tech stack, reorganised as: hero → methodology → case-study carousel → CTA → footer, plus three per-project pages.

---

## 3. Scope

### In scope

1. Home page restructure (hero, methodology, carousel, CTA, footer).
2. Three case-study pages: `/work/harvester/`, `/work/river/`, `/work/farm/`.
3. Copy rewrite ("we" → "I", broadened positioning).
4. Vanilla-JS case-study carousel (accessible).
5. Updated navigation links and inquiry copy.
6. Stats questionnaire appendix (to backfill real metrics later).

### Out of scope

- Any change to backend business logic, data models, or the inquiry pipeline (reused as-is).
- A CMS or admin-editable content.
- New imagery beyond the 3 screenshots per product supplied by the owner.
- Real-time features, analytics, or a JS framework.
- Redesigning the design system itself (extend, don't rewrite).

---

## 4. Information architecture & routing

| Route | Page | Notes |
|---|---|---|
| `/` | Home | hero, methodology, carousel (`#work`), CTA (`#contact`), footer |
| `/work/harvester/` | Harvester case study | distilled from existing copy |
| `/work/river/` | River case study | full long-form |
| `/work/farm/` | Farm case study | from `homtini_context.md` |
| `/submit-inquiry/` | (unchanged) | HTMX POST → `PilotInquiry` |

### Navigation (unchanged shell, updated links)

- **Methodology** → `#methodology`
- **Work** → `#work`
- **Contact** → `#contact`
- CTA button → **"Start a project"** (→ `#contact`)

### Backend changes (minimal)

- `core/urls.py`: add three `path('work/<slug>/', ...)` routes.
- `core/views.py`: one thin parameterised `work_detail(request, slug)` view (< 20 lines) rendering the matching template from a slug→template map.
- `core/templates/core/work/`: three new templates (or `work_<slug>.html` alongside `home.html` — follow existing flat layout unless it grows).
- No model changes. `PilotInquiry` and `submit_inquiry` are reused unchanged.

---

## 5. Home page spec (top → bottom)

1. **Hero** — broadened, first-person, no landscaping-only claim.
   - Badge: "Operational software for land-based organisations" (or similar).
   - Headline (draft): *"I don't just build websites. I install the operating system that runs land-based organisations."*
   - Sub: planning, mapping, field data, finances, reporting — for agriculture, conservation, and landscaping.
   - Visual: keep the existing `plot-card` workflow as a **generic** "Capture → Organize → Analyze" illustration (strip Harvester-specific wording).
2. **Methodology** (`#methodology`) — rewritten: *"run your field operation like a tech company."* Stat cards show **verifiable counts, not percentages** (see §8 factual rules).
3. **Work** (`#work`) — NEW case-study carousel (3 slides).
4. **CTA / inquiry** (`#contact`) — unchanged mechanics; copy → *"I'm currently taking on a small number of new projects."*
5. **Footer** — unchanged shell, updated links (Work, Contact, Privacy).

---

## 6. Carousel specification

- **3 slides**: Harvester, River, Farm.
- Each slide is a **summary card**, not a wall: project name + domain tagline, one-line problem → solution, 3–4 capability bullets with Material Symbols, one-line stack, and a "Read the full case study" link → `/work/<slug>/`.
- **Navigation**: prev/next arrow buttons + dots.
- **Accessibility**: keyboard-operable (arrow keys; controls are real `<button>`s, tabbable), and honours `prefers-reduced-motion` (no slide animation when set).
- **Implementation**: vanilla JS only (matches the "vanilla first" ethos — no slider library). A translate/opacity transition between slide panels.
- **CSS**: new small `.carousel`, `.carousel__arrow`, `.carousel__dot` classes in `style.css` (thin borders, muted colours — match existing visual language).

### Slide copy (drafts)

**Harvester** — urban garden / landscaping operations.
> A landscaping team's day lived on paper job cards — lost, wet, or stuck in the van — so billables leaked and clients were left in the dark.
> I built a platform that turns a photo of the paper form into verified, billable, client-ready data.
> - AI handwriting extraction,  Magic-Link client portal,  margin & job costing,  mapping & scheduling
> **Stack:** Django · Python · Celery + Redis · Gemini Vision · Leaflet

**River** — field-operations system for river rehabilitation.
> A field team planned river rehabilitation on paper, with no single view of who did what, where, or the cumulative impact.
> I built a Django platform that turns the whole operation into a planned, tracked, measurable workflow.
> - GIS mapping with lifecycle stages,  weekly / monthly / daily planners,  smart visit logging & photos,  impact dashboards & Excel export
> **Stack:** Django · Python · PostgreSQL · Leaflet · vanilla JS — in active production use.

**Farm** — farm management system for a regenerative farm.
> A regenerative farm's operational knowledge lived on paper lists, WhatsApp chats, and in people's memories.
> I built a local-first platform that tracks the work, the money, and the land — offline and on the farm's own hardware.
> - Double-entry finance & reconciliation,  cattle grazing & paddock rest,  drone mapping,  team todo, routines & offline logging
> **Stack:** Django · Python · PostgreSQL · HTMX · Leaflet — running on farm hardware.

---

## 7. Case-study page template (consistent across all three)

Each `/work/<slug>/` page follows the same structure:

1. **Hero** — project name + domain tagline + one-line problem → solution.
2. **Problem** — 2–4 sentences.
3. **Solution** — overview sentence(s).
4. **Capabilities** — feature-rows (`.feature-row` / `.feature-title` with Material Symbols), optionally grouped into a capabilities table.
5. **Engineering rigor** — the credibility section (service layer, performance, observability, testing, deployment).
6. **Outcomes** — concrete, verifiable facts (no invented ROI).
7. **Stack** — one line.
8. **Screenshot(s)** — supplied by owner (see §10).
9. **CTA** — "Start a project" → `#contact`.
10. **Cross-links** — to the other two case studies.

---

## 8. Copy & voice rules

1. Replace all plural self-references ("we", "our") with singular ("I", "my") in site chrome/copy.
2. Case studies are written **objectively** (the system, not "I"); the surrounding site copy carries the "I".
3. Replace "landscaping" as the *only* frame with **"land-based operations (agriculture, conservation, landscaping)"**.
4. Keep the premium, benefit-first tone.
5. **Factual integrity:** no invented percentages or ROI figures. Use only verifiable counts (e.g. "19 field templates", "8 river sections", "~40-account ledger", "456 tests"). Where a live number would strengthen the page but isn't yet verified, mark it and source it from the stats questionnaire (§12).

---

## 9. Design system & tech stack (unchanged, extended)

- Keep the existing custom-CSS system in `style.css` — no build step, no CDN changes, no Tailwind.
- Fonts: Plus Jakarta Sans (body) + Playfair Display (headlines); Material Symbols for icons.
- Extend `style.css` with: carousel classes, case-study page layout classes, and any small utilities needed.
- `design1.md` is superseded; archive it (do not delete outright unless owner confirms).

---

## 10. Visuals

Owner will supply screenshots (3 per product, priority-ordered). Capture guidance:

- Consistent desktop viewport (~1440px wide), browser chrome cropped out, saved as PNG or WebP.
- Avoid personally identifying/sensitive data unless the owner is happy showing it.

| Product | Priority screens |
|---|---|
| River | 1. Impact dashboard · 2. GIS section map · 3. Visit-log form · 4. Weekly planner |
| Farm | 1. Finance dashboard · 2. Farm map (paddock rest borders / drone overlay) · 3. Kanban board · 4. Grazing-move/paddock-rest view |
| Harvester | (from existing copy — verification queue / client portal / dashboard as available) |

If a screen is awkward to capture, fall back to an HTML `app-mockup` styled per product.

---

## 11. Testing & acceptance

### UAT scenarios (to be drafted as a checklist before implementation)

1. **Carousel** — navigate with arrows and dots; keyboard (arrow keys, Tab to controls); `prefers-reduced-motion` disables animation; no horizontal scroll on mobile.
2. **Case-study links** — each slide's "Read the full case study" resolves to the correct `/work/<slug>/` page; cross-links between pages work.
3. **Inquiry form** — submit with valid/invalid input; success and error states render via HTMX.
4. **Copy audit** — no remaining "we"/"our" in site chrome; no landscaping-only framing; no invented percentages.
5. **Mobile/responsive** — home and all three case-study pages at 375px and 768px.
6. **Voice/nav** — navbar links resolve to correct anchors; CTA opens the inquiry form.

### Automated (optional)

- Playwright E2E for carousel behaviour and the inquiry flow (reuse `@playwright/test` if added).

---

## 12. Stats questionnaire (appendix — to backfill real metrics)

Hand these to the River and Homtini devs; answers populate the Outcome sections and can replace the verifiable-count placeholders with live numbers.

### River

1. How many river sections are actively tracked today?
2. Cumulative totals since launch: litter bags collected (general + recyclable), plants planted, weeding sessions?
3. How many task templates ship with the system (currently 19)?
4. How many assignee roles / distinct users log in regularly?
5. Any before/after anecdote (e.g. time to produce a report, or number of logs per week)?

### Farm (Homtini)

1. Current active entity count (snapshot said 56)?
2. Open tasks and tasks completed per week (snapshot: 81 open, 16 in 7 days, 17.5 hrs logged)?
3. Number of accounts in the chart of accounts (snapshot: ~40)?
4. Number of bank-statement lines / invoices / bills reconciled or processed?
5. Paddock count and herd size?
6. Hours logged per week by the team?

---

## 13. Success criteria

- Home page holds three projects without reading as a wall of landscaping copy.
- Each case study communicates: problem → solution → capabilities → engineering rigor → outcomes.
- No fabricated metrics; verifiable counts everywhere a number appears.
- Carousel is accessible and works without a slider library.
- Inquiry form still works end-to-end after the copy/structural changes.

---

## 14. Open questions / decisions deferred

- Whether to archive or delete `design1.md`.
- Whether to add Playwright E2E (depends on whether the repo adopts a JS test harness).
- Final hero headline wording (draft provided; owner to approve exact phrasing).

---

# Website Reframe — Implementation Plan

**Goal:** Reframe the Plot site from a landscaping-only pitch into a solo-practice portfolio with a home-page carousel and three per-project case-study pages.

**Architecture:** Server-rendered Django templates. A shared `base.html` holds the navbar + footer; `home.html` and three `core/work/<slug>.html` templates extend it. A single parameterised `work_detail` view serves the three case studies. A vanilla-JS carousel animates the home page. The existing custom-CSS system is extended (no build step, no JS framework).

**Tech Stack:** Django 6.0 · Django templates · HTMX (inquiry form only) · vanilla JS · hand-curated CSS · Material Symbols · Plus Jakarta Sans + Playfair Display.

---

## Pre-Implementation UAT

**UAT file:** `tests/uat/website-reframe_uat.md` — drafted before implementation (Task 9).

---

### Task 1: Case-study routing + inquiry integrity (TDD)

**Files:**
- Test: `core/tests.py`
- Modify: `core/views.py`, `core/urls.py`
- Create: `core/templates/core/work/harvester.html`, `core/templates/core/work/river.html`, `core/templates/core/work/farm.html` (minimal placeholders)

- [ ] **Step 1 — Write the failing tests**

Replace `core/tests.py` with:

```python
from django.test import TestCase
from core.models import PilotInquiry


class CaseStudyRoutingTests(TestCase):
    def test_case_study_pages_return_200(self):
        for slug in ('harvester', 'river', 'farm'):
            with self.subTest(slug=slug):
                response = self.client.get(f'/work/{slug}/')
                self.assertEqual(response.status_code, 200)

    def test_unknown_case_study_returns_404(self):
        response = self.client.get('/work/unknown/')
        self.assertEqual(response.status_code, 404)

    def test_home_returns_200(self):
        self.assertEqual(self.client.get('/').status_code, 200)


class InquiryFlowTests(TestCase):
    def test_valid_post_creates_inquiry(self):
        response = self.client.post(
            '/submit-inquiry/',
            {'name': 'Jane', 'email': 'jane@example.com', 'message': 'Hi'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PilotInquiry.objects.filter(email='jane@example.com').exists())

    def test_missing_fields_return_400(self):
        response = self.client.post('/submit-inquiry/', {'name': '', 'email': ''})
        self.assertEqual(response.status_code, 400)
```

- [ ] **Step 2 — Run to verify they fail**

Run: `python manage.py test core -v 2`
Expected: the four routing tests fail (no `/work/…` URL; unknown slug not 404); the inquiry tests pass.

- [ ] **Step 3 — Add the view**

In `core/views.py`, after `home`, add:

```python
from django.http import Http404, HttpResponse
from django.shortcuts import render

PROJECTS = [
    {'slug': 'harvester', 'name': 'Harvester', 'tagline': 'Urban garden & landscaping operations'},
    {'slug': 'river', 'name': 'River', 'tagline': 'Field-operations system for river rehabilitation'},
    {'slug': 'farm', 'name': 'Farm', 'tagline': 'Farm management for a regenerative farm'},
]

CASE_STUDY_TEMPLATES = {
    'harvester': 'core/work/harvester.html',
    'river': 'core/work/river.html',
    'farm': 'core/work/farm.html',
}


def work_detail(request, slug):
    template = CASE_STUDY_TEMPLATES.get(slug)
    if template is None:
        raise Http404
    return render(request, template, {
        'slug': slug,
        'projects': [p for p in PROJECTS if p['slug'] != slug],
    })
```

- [ ] **Step 4 — Add the URL**

In `core/urls.py`, add:

```python
path('work/<slug:slug>/', views.work_detail, name='work_detail'),
```

- [ ] **Step 5 — Create minimal placeholder templates**

Create the three templates under `core/templates/core/work/`, each containing only `{% extends 'core/base.html' %}`… for now just a minimal `<h1>` body (base.html doesn't exist yet, so in this task use a self-contained placeholder like `<h1>River</h1>`).

- [ ] **Step 6 — Run to verify they pass**

Run: `python manage.py test core -v 2`
Expected: all tests pass.

- [ ] **Step 7 — Commit**

```bash
git add core/views.py core/urls.py core/tests.py core/templates/core/work/
git commit -m "feat(work): add case-study routing and tests"
```

---

### Task 2: Shared `base.html` + refactor home to extend it

**Files:**
- Create: `core/templates/core/base.html`
- Modify: `core/templates/core/home.html` (mechanical refactor only — content unchanged)

- [ ] **Step 1 — Create `base.html`**

Move the `<head>` (fonts, `style.css` link, favicon, htmx), navbar, and footer from `home.html` into `base.html`, with `{% block content %}{% endblock %}` between them. Navbar links become:

```html
<a class="navbar__link" href="/#methodology">Methodology</a>
<a class="navbar__link" href="/#work">Work</a>
<a class="navbar__link" href="/#contact">Contact</a>
<a href="/#contact" class="btn btn--primary">START A PROJECT</a>
```

Footer links become Work (`/#work`), Contact (`/#contact`), Privacy (`#`).

- [ ] **Step 2 — Refactor `home.html`** to `{% extends 'core/base.html' %}` + `{% block content %}` wrapping the existing sections.

- [ ] **Step 3 — Verify**

Run: `python manage.py test core -v 2` (home still 200) and `python manage.py runserver` → visually confirm the page renders unchanged.

- [ ] **Step 4 — Commit**

```bash
git add core/templates/core/base.html core/templates/core/home.html
git commit -m "refactor(templates): extract shared base.html"
```

---

### Task 3: River case-study page (full content)

**Files:**
- Rewrite: `core/templates/core/work/river.html`

- [ ] **Step 1 — Build the page**

`{% extends 'core/base.html' %}`. Follow the §7 template structure using `.section-label`, `.section-title`, `.feature-row`/`.feature-title`, `.stat-card`. Content source: `river_context.md` §4 (verbatim Problem/Solution/capabilities table/roles/stack/engineering-rigor/outcomes). Cross-links + CTA via the `projects` context (link to `{% url 'work_detail' p.slug %}`).

- [ ] **Step 2 — Verify**

Run: `python manage.py test core -v 2` and load `/work/river/` in a browser.

- [ ] **Step 3 — Commit**

```bash
git add core/templates/core/work/river.html
git commit -m "content(river): full River case-study page"
```

---

### Task 4: Harvester + Farm case-study pages

**Files:**
- Rewrite: `core/templates/core/work/harvester.html`, `core/templates/core/work/farm.html`

- [ ] **Step 1 — Harvester** — source: `project_context.md` + `plan.md` + existing `home.html` copy (AI handwriting engine, Magic-Link portal, operational intelligence, job costing, scheduling/GCal, mapping).
- [ ] **Step 2 — Farm** — source: `homtini_context.md` (finance/reconciliation, cattle grazing, drone mapping, team todo/routines, map/spatial, offline rapid logger; the "three capitals" framing; stack + engineering rigor + outcomes). No invented ROI numbers — use verifiable counts only.
- [ ] **Step 3 — Verify** (tests + browser) and **commit** each page separately.

```bash
git add core/templates/core/work/harvester.html core/templates/core/work/farm.html
git commit -m "content(work): Harvester and Farm case-study pages"
```

---

### Task 5: Home page rewrite (hero, methodology, carousel markup, CTA)

**Files:**
- Rewrite: `core/templates/core/home.html`

- [ ] **Step 1 — Hero** — new badge, broadened "I" headline (draft in PRD §5), sub-copy for agriculture/conservation/landscaping; keep the `plot-card` as a generic "Capture → Organize → Analyze" visual.
- [ ] **Step 2 — Methodology** (`id="methodology"`) — rewritten copy; stat cards use verifiable counts (e.g. "19 field templates", "8 river sections", "~40-account ledger", "456 tests"), not percentages.
- [ ] **Step 3 — Work carousel** (`id="work"`) — 3 slides from the PRD §6 slide copy, each a `service-card` summary with a "Read the full case study" link → `{% url 'work_detail' slide.slug %}`. Markup:

```html
<div class="carousel" id="work">
  <div class="carousel__viewport">
    <div class="carousel__track">
      <section class="carousel__slide">…Harvester…</section>
      <section class="carousel__slide">…River…</section>
      <section class="carousel__slide">…Farm…</section>
    </div>
  </div>
  <button class="carousel__arrow carousel__arrow--prev" aria-label="Previous">‹</button>
  <button class="carousel__arrow carousel__arrow--next" aria-label="Next">›</button>
  <div class="carousel__dots" role="tablist"></div>
</div>
```

- [ ] **Step 4 — CTA/inquiry** (`id="contact"`) — copy → "I'm currently taking on a small number of new projects." Form mechanics unchanged.
- [ ] **Step 5 — Load the carousel script** before `</body>`: `<script src="{% static 'core/js/carousel.js' %}" defer></script>`.
- [ ] **Step 6 — Verify + commit.**

```bash
git add core/templates/core/home.html
git commit -m "content(home): rewrite hero, methodology, carousel, CTA"
```

---

### Task 6: Carousel JavaScript

**Files:**
- Create: `core/static/core/js/carousel.js`

- [ ] **Step 1 — Write `carousel.js`**

```javascript
(function () {
  const carousel = document.querySelector('.carousel');
  if (!carousel) return;

  const track = carousel.querySelector('.carousel__track');
  const slides = Array.from(carousel.querySelectorAll('.carousel__slide'));
  const prev = carousel.querySelector('.carousel__arrow--prev');
  const next = carousel.querySelector('.carousel__arrow--next');
  const dotsBox = carousel.querySelector('.carousel__dots');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reduceMotion) track.classList.add('carousel__track--reduced');

  // Build dots to match slide count
  slides.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'carousel__dot';
    dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
    dot.addEventListener('click', () => goTo(i));
    dotsBox.appendChild(dot);
  });
  const dots = Array.from(dotsBox.querySelectorAll('.carousel__dot'));

  let current = 0;

  function goTo(index) {
    current = (index + slides.length) % slides.length;
    track.style.transform = `translateX(-${current * 100}%)`;
    slides.forEach((slide, i) => {
      slide.classList.toggle('carousel__slide--active', i === current);
      slide.setAttribute('aria-hidden', i === current ? 'false' : 'true');
    });
    dots.forEach((dot, i) => {
      dot.classList.toggle('carousel__dot--active', i === current);
      dot.setAttribute('aria-current', i === current ? 'true' : 'false');
    });
  }

  prev.addEventListener('click', () => goTo(current - 1));
  next.addEventListener('click', () => goTo(current + 1));

  carousel.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(current - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); goTo(current + 1); }
  });

  goTo(0);
})();
```

- [ ] **Step 2 — Verify** — load home, click arrows/dots, arrow keys, confirm no animation under reduced motion.

- [ ] **Step 3 — Commit**

```bash
git add core/static/core/js/carousel.js
git commit -m "feat(carousel): vanilla-JS accessible carousel"
```

---

### Task 7: CSS (carousel + case-study layout)

**Files:**
- Modify: `core/static/core/css/style.css` (append)

- [ ] **Step 1 — Append carousel styles**

```css
.carousel { position: relative; }
.carousel__viewport { overflow: hidden; }
.carousel__track { display: flex; transition: transform 0.4s ease; }
.carousel__track--reduced { transition: none; }
.carousel__slide { min-width: 100%; padding: 0 var(--spacing-md); box-sizing: border-box; }
.carousel__arrow {
  position: absolute; top: 50%; transform: translateY(-50%);
  width: 2.5rem; height: 2.5rem; border-radius: 50%;
  border: 1px solid var(--color-primary); background: var(--white);
  color: var(--color-primary); font-size: 1.25rem; cursor: pointer;
}
.carousel__arrow:hover { background: var(--color-primary); color: var(--white); }
.carousel__arrow--prev { left: -1.25rem; }
.carousel__arrow--next { right: -1.25rem; }
.carousel__dots { display: flex; gap: 0.5rem; justify-content: center; margin-top: var(--spacing-md); }
.carousel__dot {
  width: 10px; height: 10px; border-radius: 50%; padding: 0;
  border: 1px solid var(--color-primary); background: transparent; cursor: pointer;
}
.carousel__dot--active { background: var(--color-primary); }
```

- [ ] **Step 2 — Append case-study page styles** (`.work-hero`, `.work-section`, `.capabilities-grid`, `.stack-line`, `.outcome-list`, `.work-nav`, `.case-screenshot`), following existing tokens (thin borders, muted colours, generous whitespace).

- [ ] **Step 3 — Verify** on 375px, 768px, and 1440px.

- [ ] **Step 4 — Commit**

```bash
git add core/static/core/css/style.css
git commit -m "style: carousel and case-study layout"
```

---

### Task 8: Screenshot integration

**Files:**
- Create: `core/static/core/img/river/…`, `core/static/core/img/farm/…`, `core/static/core/img/harvester/…`
- Modify: the three case-study templates (add `<img class="case-screenshot" src="{% static 'core/img/…' %}" alt="…">`)

- [ ] **Step 1 — Add image slots** with graceful placeholders (a styled div fallback) so pages don't break before assets arrive.
- [ ] **Step 2 — Owner drops the 3 screenshots per product into the paths; compress to WebP/PNG ≤ ~200KB each.**
- [ ] **Step 3 — Verify + commit.**

---

### Task 9: UAT checklist + final verification

**Files:**
- Create: `tests/uat/website-reframe_uat.md`

- [ ] **Step 1 — Draft the UAT checklist** (scenarios from PRD §11): carousel nav/keyboard/reduced-motion, case-study links, inquiry form valid/invalid, copy audit (no "we"/"our" in chrome, no landscaping-only framing, no invented percentages), mobile 375px/768px, nav anchors.
- [ ] **Step 2 — Run `python manage.py test core -v 2`** → all green.
- [ ] **Step 3 — `python manage.py check` and `collectstatic --noinput`** → no errors.
- [ ] **Step 4 — Full manual UAT against the checklist; record results.**
- [ ] **Step 5 — Commit + push.**

```bash
git add -A
git commit -m "docs(uat): website-reframe UAT checklist"
```

---

## Notes

- Django is 6.0 (not 5.1) — see `requirements.txt`. Tests use the built-in `TestCase` runner (`python manage.py test`).
- No Playwright/pytest in this repo; carousel and visuals are verified via UAT, not automated E2E.
- `design1.md` is superseded — archive it in a final cleanup commit rather than deleting outright.
- Screenshots (Task 8) are the only externally blocked task; everything else is unblocked.
