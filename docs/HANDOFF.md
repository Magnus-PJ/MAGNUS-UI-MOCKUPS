# Handoff Document

Everything a new team member, vendor, or another AI session needs to pick this up cold.

## What this project is

Magnus Diagnostics engaged NUMINACORE to build **Magnus HMS** (radiology-first HMS, Java/Spring + React, India compliance). The vendor produced a 107-page MVP 1 UI/UX walkthrough (106 screens) + a 209-item scope checklist. This repo contains our **review of that walkthrough** and our own **complete replacement/extension design pack** (225 screens, 17 groups) that becomes the UI/UX baseline for the 6-month MVP 1. Read `docs/VISION.md` first, then `docs/DECISIONS.md`.

## Repository map

```
00-project-log/PROJECT_LOG.md      chronological engagement record
01-review/                          vendor design review & feedback (.docx) — findings C-x/S-x/N-x, SLAs, foundation asks
02-gap-closure-pack/                first 16 gap-closure screens (NS-01…16) + catalogue (PDF + HTML)
03-complete-pack/
  html-source/wave1..wave4/         ONE HTML FRAGMENT PER SCREEN (the atomic source of truth)
  group-html/                       assembled per-group packs (self-contained, open in any browser)
  group-pdfs/                       rendered PDFs (DEPRECATED for now — see D-08; HTML is primary)
  design-system/base.css            the shared design system every screen uses
  design-system/assemble_group.py   builds per-group HTML packs (GROUPS dict = the full 17-group registry)
  design-system/render_fixed.py     one-variable-height-page-per-screen PDF renderer (Playwright) — use this, never plain A4
docs/                               VISION, DECISIONS, FUTURE_PLAN, HANDOFF (this file)
```

## Screen ID scheme (225 screens, 17 groups)

| Prefix | Group | Count | Prefix | Group | Count |
|---|---|---|---|---|---|
| AU | G1 Identity & Access | 18 | BL | G9 Billing & Payments | 19 |
| PT | G2 Patient-facing | 12 | NT | G10 Notifications & Delivery | 8 |
| FO | G3 Front Office | 22 | GR | G11 Grievance & Support | 6 |
| SC | G4 Scheduling Setup | 10 | AD | G12 Admin & Master Data | 20 |
| OR/CS | G5 Orders & Clinical Safety | 8+6 | IN | G13 Integration & Devices | 10 |
| TK | G6 Radiology Technician | 12 | GV | G14 Governance & Compliance | 16 |
| RD | G7 Radiologist | 18 | IR | G15 Imaging Regulatory | 6 |
| DD | G8 Doctor Desk | 11 | PL | G16 Platform Operator | 12 |
| | | | DS | G17 Design System & Patterns | 11 |

Vendor's original deck used different IDs (FO-S1, RR-S6…) — the review documents map between them.

## How to work with the pack

- **View:** open any `group-html/*.html` in a browser. Each screen = header (ID, title, scope chip, cluster) + purpose note + app-chrome frame + alternate states below dividers + audit footer.
- **Edit a screen:** edit its fragment in `html-source/waveN/<id>.html`, then rebuild the group: `python3 design-system/assemble_group.py <GroupKey>` (keys in the GROUPS dict).
- **Add a screen:** create the fragment following an existing one (only `base.css` classes), add its ID to GROUPS, rebuild.
- **PDFs (if re-enabled):** `python3 design-system/render_fixed.py <GroupKey>` — renders one variable-height page per screen. Never print straight to A4 (screens fragment — that was the D-08 issue).

## Design rules every screen follows (enforce on any new screen)

1. Scope chip: MVP1-CORE / Conditional / Post-MVP1.
2. 2–4 states (default + error/blocked/empty/offline/success) — no happy-path-only screens.
3. Audit footer (🔒 …recorded in the access log) + step-up identity confirm on legal/money/destructive actions + four-eyes on irreversible ones.
4. Masked identifiers wherever the viewer lacks purpose (`#MRN-••••30` pattern, DS-07).
5. One SLA/overdue pattern (DS-03): countdown → warn → BREACHED w/ owner + escalation.
6. Synthetic data only; consistent cast (Meridian Diagnostics, Andheri West, Dr. V. Shetty, K. Verma, MRN-0048xx…); ₹ Indian formats; IST; Aadhaar last-4 only.
7. India compliance surfaces: DPDP consent/rights, PC-PNDT Form F gates, AERB, GST-exempt invoicing, DLT SMS.

## Current status & the HELD gate

- Waves 1–2 complete and pushed; Waves 3–4 in production (README wave checklist is the live status).
- **Do not finalise/package**: the client (Paul, pauljoy89@gmail.com) will supply additional information after Wave 4; the pack is to be checked against it and extended before the final master index + combined volume is produced (see FUTURE_PLAN §1–3).

## Credentials & access

- Repo: https://github.com/Magnus-PJ/MAGNUS-UI-MOCKUPS (fine-grained PAT held by Paul; write access granted July 2026).
- No other external systems are wired to this project.
