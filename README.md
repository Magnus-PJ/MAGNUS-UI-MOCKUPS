# MagnusPRO — Complete MVP 1 UI/UX Design & Architecture Pack

**MagnusPRO** (working name; final legal name confirmed before UAT) is a privacy-first, radiology-first, multi-tenant healthcare platform — the **foundation module** for a complete enterprise healthcare system (future: LIS, IPD, OT, ICU, ER, IVF, nuclear medicine, pharmacy, CRM, portals, ABDM, international, AI) built so the core is **never rebuilt**.

**This repository is the single source of truth** for the MVP 1 design: **232 production-grade screens** across **17 groups**, **12 architecture documents**, the full decision log, and the vendor-baseline crosswalk — everything the development team (NUMINACORE, Java 21/Spring Boot 3 + React/TypeScript) needs to start Sprint 1 with zero ambiguity.

## Quick start

| You are… | Start here |
|---|---|
| **Anyone** | `04-architecture-docs/DOC-00_Master_Index.html` — the linked index of everything |
| **Leadership / client** | `docs/VISION.md` → `docs/DECISIONS.md` (D-01…D-37) |
| **The dev team** | `DOC-09` build blueprint → `DOC-11` gap analysis → `DOC-08` crosswalk → group packs |
| **Anyone wanting to FEEL the product** | `03-complete-pack/MagnusPRO_Live_Prototype.html` — open, sign in, click through everything |
| **Designers** | `03-complete-pack/group-html/` (one browser-ready pack per group) + `DS` group (design system) |
| **QA / UAT** | `DOC-10` test traceability + safety-gate suite SG-01…SG-12 · `DOC-01` 25 scenarios |
| **New joiner / another AI session** | `docs/HANDOFF.md` |

## Repository map

```
00-project-log/            Chronological engagement record
01-review/                 Review of the vendor's original 106-screen walkthrough (.docx)
02-gap-closure-pack/       First 16 gap-closure screens (NS-01…16) + 10 revisions (historical)
03-complete-pack/
  html-source/wave1..4/    ★ ONE SMALL FILE PER SCREEN (232 fragments) — edit one screen
                             without touching anything else; IDs like fo-01.html, rd-09.html
  group-html/              17 assembled group packs + the Combined Volume (232 screens, one file)
  design-system/           base.css (shared design system) · assemble_group.py (rebuild packs)
                           · baseline_map.py (vendor crosswalk, regenerates DOC-08)
  group-pdfs/              DEPRECATED (D-35: PDFs dropped; HTML is the deliverable)
04-architecture-docs/      DOC-00 Master Index · 01 Patient Scenarios (25) · 02 Workflow Orders
                           · 03 Roles & Permissions · 04 Security Layers · 05 Audit & Logging
                           · 06 Billing E2E · 07 Auth & MFA · 08 Vendor Crosswalk
                           · 09 Build & Deployment Blueprint · 10 Test Traceability
                           · 11 Zero-Trust/Air-Gap/GDPR/HIPAA Gap Analysis (closures BUILT)
docs/                      VISION · DECISIONS (D-01…D-37) · FUTURE_PLAN · HANDOFF
```

## The 17 groups (232 screens)

| G | Group | IDs | # | G | Group | IDs | # |
|---|---|---|---|---|---|---|---|
| G1 | Identity & Access | AU-01…19 | 19 | G10 | Notifications & Delivery | NT-01…08 | 8 |
| G2 | Patient-facing (secure links) | PT-01…12 | 12 | G11 | Grievance & Support | GR-01…06 | 6 |
| G3 | Front Office & Reception | FO-01…22 | 22 | G12 | Admin & Master Data | AD-01…21 | 21 |
| G4 | Scheduling & Resource Setup | SC-01…10 | 10 | G13 | Integration & Devices | IN-01…11 | 11 |
| G5 | Orders & Clinical Safety | OR-01…08, CS-01…06 | 14 | G14 | Governance & Compliance | GV-01…18 | 18 |
| G6 | Radiology Technician | TK-01…12 | 12 | G15 | Imaging Regulatory (PC-PNDT/AERB) | IR-01…06 | 6 |
| G7 | Radiologist Reading & Reporting | RD-01…18 | 18 | G16 | Platform Operator | PL-01…13 | 13 |
| G8 | Doctor Desk (referrers) | DD-01…11 | 11 | G17 | Design System & Patterns | DS-01…11 | 11 |
| G9 | Billing & Payments | BL-01…20 | 20 | | | | |

Every screen: scope chip (MVP1-CORE / Conditional) · **Baseline line** tracing it to the vendor deck or the finding that created it (140 extend / 92 net-new) · 2–4 states (error/blocked/empty/offline) · audit microcopy · synthetic data only (no PHI).

## Enterprise bars (all designed-in, DOC-11)

- **Zero-trust:** device trust & conditional access (AU-19), JIT elevation, step-up bound tokens, masked-by-default, DLP thresholds (GV-15), no standing operator access.
- **Air-gap capable:** signed-bundle transfer console (IN-11), offline update bundles (PL-13), edge sync with idempotent replay (IN-10, DS-04).
- **GDPR + HIPAA ready (beyond DPDP):** processing restriction & FHIR portability (GV-05), lawful-basis register (GV-12), BAA/SCC coverage (GV-13), disclosures register (GV-17), training & attestation (GV-18), jurisdiction policy packs in the regional rulebook (PL-05). Certification/BAAs are per-tenant commercial steps.
- **Vendor-neutral & white-label:** no vendor names in core screens/models — vendors live in the per-centre registry (AD-21) and replaceable adapters (DOC-09 §9); tenant branding via theme tokens (DS-01, AD-14).
- **Small-file modularity:** one fragment per screen, bounded-context modules in the backend blueprint — a change to any one item never ripples through the system.

## Pilot (per decision D-34)

All **4 Magnus branches go live together** (North Paravoor, Irinjalakuda, Pullur, + branch 4 TBC) — cloud control plane + 4 edge data planes, remote reading across sites, per-branch readiness tracked on AD-21. Staged go-live within the window; per-branch feature toggles (AD-17) as the risk valve. **UAT planning: deferred by client** (DOC-10 is ready when it starts).

## How to change things

1. Edit the single screen fragment in `03-complete-pack/html-source/waveN/<id>.html` (only `base.css` classes).
2. Rebuild its group: `python3 design-system/assemble_group.py <GroupKey>`.
3. New screen? Add the file + its GROUPS entry + its `baseline_map.py` mapping, re-run the map's `inject`, rebuild, and regenerate DOC-08.
4. Commit and push — this repo is the source of truth.

## Status

- [x] Vendor-deck review (20 scenarios, C/S findings) · [x] Gap-closure pack (NS/R)
- [x] Waves 1–4: all 17 groups built · [x] Vendor-baseline sync on every screen
- [x] Architecture docs DOC-00…11 · [x] DOC-11 closures built (AU-19, IN-11, PL-13, GV-17, GV-18, AD-21 + 7 state additions)
- [x] Combined Volume (232 screens, one HTML) · [x] MagnusPRO naming applied · [x] Verification: ALL CHECKS PASSED
- [ ] Final legal product name (client, before UAT) · [ ] Branch-4 details (client) · [ ] UAT planning (deferred)

*Prototype/reference — not committed product scope. All data synthetic. July 2026.*
