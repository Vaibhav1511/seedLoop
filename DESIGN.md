# SeedLoop — Design System

> A warm, editorial, agricultural design system for a farmer-owned seed commons —
> the feel of a cooperative's annual report, not a SaaS landing page.
> SeedLoop — the Midwest Biodistrict Seed Cooperative.

> **Status (2026-06-10):** This document defines the **target** design system
> (moss + barley + parchment, Fraunces + Public Sans). It supersedes the earlier
> sage/cream system. The live code (`ui.py` → `inject_theme()`, `Home.py`, and
> `pages/`) still implements the previous sage palette — re-skinning to this spec
> is a follow-up task. Until then, treat this as the source of intent, not a
> description of what currently renders.

---

## Visual Theme & Atmosphere

SeedLoop is a **farmer-owned seed commons** — an open registry and traceability
record for the Irish Midwest, governed by members rather than corporations. The
interface should read like a cooperative's well-made annual report: warm,
editorial, and unmistakably agricultural.

- **Warm** — a parchment-paper canvas, peat-brown ink, never stark white.
- **Agricultural** — colour and layout borrow from the land itself: aerial
  field-parcels, hedgerow greens, ripe barley gold.
- **Editorial** — a display serif (Fraunces) for headings paired with a clean
  humanist sans (Public Sans); generous whitespace; calm, considered hierarchy.
- **Earthy & grounded** — deep moss anchors the chrome (sidebar, quote bands,
  primary actions); barley gold is the one bright accent that points to action.

The signature motif is **the loop** — a seed travels List → Exchange → Grow →
Return and comes back to local soil. The visual language echoes this: field-strip
colour bands, a cyclical "how it works" sequence, provenance that always returns.

This is **not** a SaaS landing page and not a dark dev-tool. It is the seed
cooperative's printed report, brought to screen.

---

## Color Palette & Roles

### Core tokens

| Token | Hex | Role |
|-------|------|------|
| **Moss** | `#2E4A2C` | Deep hedgerow green — sidebar, quote band, primary buttons, step badges |
| **Leaf** | `#4F7A45` | Mid leaf green — county labels, secondary accents |
| **Barley** | `#C9A24B` | Ripe barley gold — the bright accent: solid CTA, eyebrow, arrows |
| **Peat** | `#3A2F25` | Peat-brown ink — headings and body text |
| **Parchment** | `#F7F5EC` | Paper background for the whole app |
| **Field** | `#EDEADB` | Pale field strip — subtle fills |

### Surfaces & lines

| Token | Hex | Role |
|-------|------|------|
| Card surface | `#FFFEF7` | Card fill (a touch warmer/lighter than parchment) |
| Card border | `#E3DFC9` | 1px card border |
| Dashed rule | `#C9C4AC` | Section-heading dashed rule |
| Muted meta | `#8A8268` | Small muted meta text on cards |
| Body-on-card | `#5B5345` | Card body copy |

### Field-strip stat band (farm-parcel fills)

| Strip | Background | Text |
|-------|-----------|------|
| 1 | `#33502F` | `#F1EFDF` |
| 2 | `#4F7A45` | `#F1EFDF` |
| 3 | `#7A9A57` | `#23341E` |
| 4 | `#C9A24B` | `#2A2113` |

### Text-on-colour

| Hex | Used on |
|------|---------|
| `#F7F5EC` | Cream text on moss (sidebar wordmark, ghost button, hero headline) |
| `#F1EFDF` / `#EFEEDE` | Cream text on moss/leaf bands |
| `#E4E2D2` | Hero subcopy on the photo gradient |
| `#E8E6D5` | Sidebar nav text |
| `#BFCBA8` | Sidebar sub-line (muted sage-cream) |
| `#2A2113` | Dark ink on barley (solid CTA, strip 4) |

**Role notes:**
- **Barley `#C9A24B` is the only bright accent.** Reserve it for the primary CTA,
  the eyebrow pill, the loop arrows, and the quote attribution. Do not flood it.
- **Moss `#2E4A2C` is the anchor.** It carries the sidebar, the quote band,
  primary buttons, and the loop step badges — the structural, governing colour.
- **Parchment `#F7F5EC` is the paper.** Everything sits on it; never introduce
  stark white `#fff` as a surface.

---

## Typography Rules

Two families, imported from Google Fonts:

- **Fraunces** — display serif, weights 400 / 600 / 700, optical sizing. All
  headings `h1`–`h4`.
- **Public Sans** — humanist sans, weights 400 / 500 / 600. All body, labels,
  buttons, captions.

| Element | Font / weight | Size | Notes |
|---------|---------------|------|-------|
| Hero headline | Fraunces 700 | `clamp(2.4rem, 5vw, 3.6rem)` | line-height 1.05, max-width 14ch; italic accent phrase in barley |
| Section heading | Fraunces 600 | 1.9rem | followed by a dashed rule |
| Stat number | Fraunces 600 | 2.6rem | line-height 1 |
| Card / loop title | Fraunces 600 | ~1.1rem | |
| Quote | Fraunces 400 italic | 1.5rem | max-width 32ch |
| Body | Public Sans 400 | ~1rem | line-height 1.5–1.6 |
| Labels / eyebrows | Public Sans 500/600 | ~0.72rem | UPPERCASE, letter-spacing 0.13–0.18em |

**Rules:**
- Headings are **always Fraunces**; body, labels, and UI are **always Public Sans**.
- Hierarchy is carried by the serif/sans contrast and weight, not by many colours.
- Eyebrows and labels are uppercase with wide tracking; body is sentence case.

---

## Component Stylings

### Card (`#FFFEF7`)
The base surface for the loop and featured-seed grids.
```css
background-color: #FFFEF7;
border: 1px solid #E3DFC9;
border-radius: 14px;
padding: 24px 22px 20px;        /* loop card; seed card uses 18–20px */
```

### Buttons
```css
/* Solid (primary CTA) */
.btn-solid {
    background: #C9A24B;          /* barley */
    color: #2A2113;              /* dark ink */
    border-radius: 10px;
    padding: 13px 26px;
    font: 600 0.95rem 'Public Sans';
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
}
/* Ghost (secondary) */
.btn-ghost {
    background: transparent;
    color: #F7F5EC;
    border: 1.5px solid rgba(247,245,236,0.7);
    border-radius: 10px;
    padding: 13px 26px;
}
.btn:hover { transform: translateY(-2px); }   /* both lift 2px */
```

### Eyebrow pill
```css
color: #C9A24B;                   /* barley */
border: 1px solid rgba(201,162,75,0.6);
border-radius: 999px;             /* fully rounded */
padding: 5px 14px;
font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.18em;
```

### Field-strip stat band
One horizontal band, `14px` radius, subtle shadow, divided into four equal strips
(see palette). Number (Fraunces 600, 2.6rem) above an uppercase label
(letter-spacing 0.13em). Reads as farm parcels seen from the air. Stacks
vertically below 880px.

### Loop card (signature element)
```css
/* 34px circular step badge */
.step {
    width: 34px; height: 34px; border-radius: 50%;
    background: #2E4A2C; color: #F7F5EC;          /* moss / cream */
    font: 600 0.95rem 'Fraunces';                  /* numeral */
    display: flex; align-items: center; justify-content: center;
}
```
Between cards a **barley `→` arrow** floats on the card's right edge. The **fourth
card shows a `↺` glyph** in its top-right corner instead, signalling the cycle
closing. Below 880px the grid becomes 2×2 and arrows are hidden.

### Featured seed card
A full-width **8px colour swatch bar** across the top, then padding 18–20px:
an uppercase county label in leaf `#4F7A45`, the variety name (Fraunces ~1.08rem),
a one-line description, and a muted meta line `#8A8268`. Hover: lift 3px with a
soft shadow.

### Quote band
```css
background: #2E4A2C;              /* moss */
border-radius: 16px;
padding: 46px 52px;
/* blockquote: Fraunces italic 1.5rem, #F4F2E4, max-width 32ch */
/* attribution: barley #C9A24B, uppercase, ~0.85rem, letter-spacing 0.1em */
```

### Section heading pattern
Every section heading is the title (Fraunces 600, 1.9rem) followed by a horizontal
**dashed rule** (`1px dashed #C9C4AC`) that fills the remaining row width.

### Sidebar
Background **moss `#2E4A2C`**, no border. Top to bottom: brand wordmark "SeedLoop"
(Fraunces 700, 1.6rem, `#F7F5EC`); sub-line "MIDWEST BIODISTRICT SEED COOPERATIVE"
(0.72rem uppercase, letter-spacing 0.14em, `#BFCBA8`); a thin divider
(`1px solid rgba(247,245,236,0.25)`); the nav radio (text `#E8E6D5`, ~0.98rem,
active highlighted); another divider; a member-counties caption.

---

## Layout Principles

- **Parchment canvas.** The whole app sits on `#F7F5EC`; the main content column is
  centred at `max-width: 1080px`.
- **Quiet chrome.** Hide Streamlit's default header, footer, and main menu. Custom
  HTML is injected via `st.markdown(..., unsafe_allow_html=True)`; native widgets
  are used only where interactivity is required (nav radio, trace input/button).
- **Field-parcel motif.** Horizontal colour bands (the stat strips) and the loop
  grid echo aerial farmland — structure drawn from the land.
- **Dashed-rule sections.** Every section opens with a title + dashed rule, giving
  a consistent, report-like rhythm down the page.

### Spacing scale (in use)
| Token | Value | Used for |
|-------|-------|----------|
| Hero padding | `72px 56px 64px` | Hero interior (→ `48px 28px` ≤880px) |
| Quote padding | `46px 52px` | Quote band interior |
| Loop card padding | `24px 22px 20px` | Loop cards |
| Seed card padding | `18–20px` | Featured seed cards |
| Stat strip padding | `26px` | Stat strips |
| Button padding | `13px 26px` | Buttons |
| Eyebrow padding | `5px 14px` | Eyebrow pill |
| Content max-width | `1080px` | Main column |

### Radius scale (in use)
| Token | Value | Used for |
|-------|-------|----------|
| Hero | `18px` | Hero banner |
| Quote band | `16px` | Quote block |
| Stat band | `14px` | Stat band |
| Card | `14px` | Cards |
| Button | `10px` | Buttons |
| Step badge | `50%` | Loop step circle |
| Pill | `999px` | Eyebrow pill |

---

## Depth & Elevation

Depth is restrained and earthy — printed-paper, not glossy glass.

- **Cards** rest on a `1px #E3DFC9` border with a soft shadow on hover
  (lift 3px). The border and warm fill do most of the separating work.
- **The solid CTA** carries a single soft shadow `0 6px 18px rgba(0,0,0,0.25)`;
  the stat band a subtle `0 2px 10px rgba(58,47,37,0.08)`.
- **Moss bands** (sidebar, quote) are flat solid blocks — colour, not shadow,
  gives them weight.
- **Interaction** is a gentle 2–3px lift on buttons and cards; no glows, no
  neon, no layered z-stacks.

---

## Do's and Don'ts

### Do
- ✅ Use **Fraunces** for every heading and **Public Sans** for everything else.
- ✅ Keep the canvas **parchment `#F7F5EC`** and ink **peat `#3A2F25`**.
- ✅ Anchor structure in **moss** (sidebar, quote, primary buttons, step badges).
- ✅ Reserve **barley `#C9A24B`** as the single bright accent — CTA, eyebrow, arrows.
- ✅ Lean on the **field-parcel motif** — colour-band strips, the cyclical loop.
- ✅ Open every section with a title + **dashed rule**.
- ✅ Keep the feel of a **cooperative's annual report** — warm, editorial, agricultural.

### Don't
- ❌ **Don't substitute your own palette, fonts, or copy** — every token here is intentional.
- ❌ Don't introduce stark white `#fff` surfaces — use card `#FFFEF7` on parchment.
- ❌ Don't let barley gold flood — it points to action, it isn't a background.
- ❌ Don't mix in extra typefaces or use the serif for body text.
- ❌ Don't add heavy shadows, glows, or a glassy/SaaS sheen.
- ❌ Don't make it read like a tech landing page — this is a seed cooperative.

---

## Responsive Behavior

- **≤880px:** the stat band **stacks vertically**; the loop grid becomes **2×2**
  with the connecting arrows hidden; hero padding shrinks to `~48px 28px`; the
  quote band padding eases to `~34px 26px`.
- **Cards reflow** to fewer columns but keep their `14px` radius and padding.
- **Type scales by the hero `clamp()`** and the serif/sans hierarchy; avoid
  shrinking label sizes so tracking stays legible.
- **Touch targets** stay comfortable — buttons keep `13px 26px` padding.

---

## Agent Prompt Guide

Use this block when prompting an AI tool (Stitch, v0, etc.) to generate on-brand
SeedLoop UI:

> Design a screen for **SeedLoop — the Midwest Biodistrict Seed Cooperative**, a
> farmer-owned seed registry and traceability commons for the Irish Midwest.
>
> **Atmosphere:** warm, editorial, agricultural — a cooperative's annual report,
> NOT a SaaS landing page, NOT a dark dev-tool. The motif is "the loop": a seed
> travels List → Exchange → Grow → Return and comes back to local soil.
>
> **Colours:** parchment `#F7F5EC` canvas; peat-brown `#3A2F25` ink; deep moss
> `#2E4A2C` for the sidebar, quote bands, primary buttons and step badges; leaf
> `#4F7A45` for county labels/accents; barley gold `#C9A24B` as the single bright
> accent (solid CTA, eyebrow pill, loop arrows). Cards are `#FFFEF7` with a
> `1px #E3DFC9` border. Field-strip stat band uses `#33502F / #4F7A45 / #7A9A57 /
> #C9A24B`. Never use stark white surfaces.
>
> **Typography:** Fraunces (display serif, 400/600/700) for all headings; Public
> Sans (400/500/600) for body, labels and buttons. Hero headline Fraunces 700
> `clamp(2.4rem,5vw,3.6rem)` with an italic accent phrase in barley. Eyebrows and
> labels uppercase, letter-spacing 0.13–0.18em.
>
> **Components:** rounded hero (18px) with a left-to-right dark-green photo
> gradient; a four-strip field-parcel stat band (14px); a 4-card "loop" with 34px
> moss step badges and barley arrows (the 4th card shows a `↺`); featured seed
> cards with an 8px colour swatch bar; a moss quote band (16px) with Fraunces
> italic and a barley attribution; section headings each followed by a dashed
> rule. Solid barley CTA + ghost (cream-outline) button, both lifting 2px on hover.
>
> **Layout:** parchment background, content max-width 1080px, quiet chrome, the
> field-parcel motif, generous editorial whitespace. Responsive: stat band stacks
> and the loop becomes 2×2 (no arrows) below 880px.

---

*Target spec for SeedLoop. When the app is re-skinned to this system, update
`ui.py` → `inject_theme()` to match, and restore the "Source of truth: ui.py"
footer here.*
