# MagnusPRO (working name) — UI/UX Design Pack (MVP 1)

Design review + complete MVP 1 UI/UX design pack for MagnusPRO — 231 screens, 17 groups, 12 architecture docs. Pilot: all 4 Magnus branches together. Zero-trust / air-gap / GDPR / HIPAA gap-closures built (DOC-11) (radiology-first, privacy-first HMS · Java/Spring backend · React frontend · India: DPDP / PC-PNDT / AERB / GST).

## Start here

1. **docs/VISION.md** — what Magnus HMS is and what this repo is for
2. **docs/DECISIONS.md** — every decision agreed in working sessions (D-01…D-20)
3. **docs/FUTURE_PLAN.md** — next steps, quarterly roadmap, open items
4. **docs/HANDOFF.md** — how to pick this up cold: repo map, screen IDs, how to edit/rebuild
5. **00-project-log/PROJECT_LOG.md** — chronological engagement record

## Contents
| Folder | What's inside |
|---|---|
| `01-review/` | Vendor design review & feedback document (.docx) — 20 scenario walkthroughs, P1/P2 findings, SLAs, foundation asks |
| `02-gap-closure-pack/` | 16 gap-closure screens (NS-01…NS-16) + catalogue of 10 revisions (PDF + HTML source) |
| `03-complete-pack/` | The full 225-screen MVP 1 design pack, built in 4 waves |
| `03-complete-pack/group-pdfs/` | One rendered PDF per group (G1–G17) |
| `03-complete-pack/html-source/` | Screen fragments (one HTML file per screen) |
| `03-complete-pack/design-system/` | Shared `base.css` + assembly, baseline-crosswalk and PDF-render scripts |
| `04-architecture-docs/` | DOC-00..10: HTML architecture & workflow documentation (open DOC-00_Master_Index.html first) |

## Wave status
- [x] Wave 1 — Clinical core: G3 Front Office (FO-01…22) · G5 Orders & Clinical Safety (OR-01…08, CS-01…06) · G6 Technician (TK-01…12) · G7 Radiologist (RD-01…18) — 66 screens
- [x] Wave 2 — Revenue & outreach: G9 Billing (19) · G10 Notifications (8) · G2 Patient-facing (12) · G8 Doctor Desk (11) — 50 screens
- [x] Wave 3 — Admin & governance: G12 Admin (20) · G14 Governance (16) · G15 Regulatory (6) · G11 Grievance (6) — 48 screens
- [x] Wave 4 — Identity & platform: G1 Identity (18) · G4 Scheduling setup (10) · G13 Integration (10) · G16 Platform (12) · G17 Design system (11) — 61 screens
- [x] 04-architecture-docs/: DOC-00 master index + DOC-01..10 (patient scenarios, workflow orders, roles/permissions, security layers, audit/logging, billing E2E, auth/MFA, vendor crosswalk, build blueprint, test traceability)
- [x] Baseline sync: all 226 screens carry vendor-deck references (140 extend / 86 net-new)
- [x] Combined volume (group-html/MagnusPRO_MVP1_Complete_Combined_Volume.html, 231 screens)
- [x] DOC-11 gap-closure screens built (AU-19, IN-11, PL-13, GV-17, GV-18)
- [ ] Final legal product name confirmation before UAT (working name: MagnusPRO)

Synthetic data only — no PHI. Prototype/reference, not committed product scope.
