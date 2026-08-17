# Website Reframe — UAT Checklist

**Feature:** Plot site reframe (home page + three case-study pages)
**Date:** 2026-08-17
**Pre-test setup:**
1. `python manage.py migrate`
2. `python manage.py runserver`
3. Open `http://127.0.0.1:8000/` in a desktop browser (and separately at 375px and 768px widths for the responsive scenario).

---

## Scenario 1 — Home page hero & methodology

| # | Step | Expected |
|---|---|---|
| 1.1 | Load `/` | Page renders; hero headline is in first person ("I don't just build websites…") |
| 1.2 | Check hero badge | Reads "Operational software for land-based organisations" (or equivalent) — no "landscaping" as the only frame |
| 1.3 | Check methodology stat cards | Cards show verifiable counts (3 systems / 19 templates / ~40 accounts / 456 tests) — **no percentages** |
| 1.4 | Check "See the work" button | Scrolls to `#work` |

## Scenario 2 — Carousel (happy path)

| # | Step | Expected |
|---|---|---|
| 2.1 | Locate the carousel under "The Work" | 3 slides: Harvester (01), River (02), Farm (03) |
| 2.2 | Click next arrow | Slide advances to River, then Farm, then wraps to Harvester |
| 2.3 | Click prev arrow | Slide moves back |
| 2.4 | Click each dot | Jumps to the corresponding slide; active dot is filled |
| 2.5 | Confirm each slide content | Name + domain tagline + one-line problem→solution + 4 icon bullets + stack line + "Read the full case study" link |

## Scenario 3 — Carousel accessibility

| # | Step | Expected |
|---|---|---|
| 3.1 | Focus the carousel and press ArrowRight / ArrowLeft | Slides advance/retreat via keyboard |
| 3.2 | Tab through controls | Arrows and dots are focusable `<button>` elements |
| 3.3 | Enable "prefers-reduced-motion: reduce" (OS setting or DevTools) and reload | Slide change is instant (no transition animation) |

## Scenario 4 — Case-study navigation

| # | Step | Expected |
|---|---|---|
| 4.1 | Click "Read the full case study" on the River slide | Lands on `/work/river/` with the full River case study |
| 4.2 | Repeat for Harvester and Farm | `/work/harvester/`, `/work/farm/` render correctly |
| 4.3 | On each case-study page, click the "More work" links | Cross-links navigate to the other two projects (not the current one) |
| 4.4 | Visit `/work/unknown/` | Returns a 404 page |

## Scenario 5 — Inquiry form

| # | Step | Expected |
|---|---|---|
| 5.1 | On `/` (or `/work/…/`) click "Start a project" / "Request a call" | Scrolls to the `#contact` form |
| 5.2 | Submit with name + email | Success message replaces the form (via HTMX) — "I'll be in touch soon." |
| 5.3 | Submit with empty name/email | Error message shown, no record saved |
| 5.4 | Verify DB | `PilotInquiry` row created for the valid submission only |

## Scenario 6 — Copy & factual-integrity audit

| # | Step | Expected |
|---|---|---|
| 6.1 | Grep rendered pages for " we " / " our " in site chrome (not quoted testimonials) | No first-person-plural in navigation, hero, methodology, CTA, or footer |
| 6.2 | Grep for "%" | No percentage claims anywhere |
| 6.3 | Confirm "land-based organisations / agriculture, conservation, landscaping" framing | Present; landscaping is not the sole frame |

## Scenario 7 — Responsive & visual

| # | Step | Expected |
|---|---|---|
| 7.1 | 375px width | Carousel is single-column; arrows visible; no horizontal scroll; case-study capability grid stacks to one column |
| 7.2 | 768px width | Layout remains usable |
| 7.3 | 1440px width | Case-study screenshots render in a 3-up grid (fallback SVGs show the product + screen name) |

---

## Sign-off

| Role | Name | Date | Result |
|---|---|---|---|
| Developer | | | |
| Product owner | | | |
