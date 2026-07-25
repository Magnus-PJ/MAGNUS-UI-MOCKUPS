# Handoff Document — MagnusPRO MVP 1

Everything a new team member, the vendor, or another AI session needs to pick this up cold.

## What this project is
Magnus Diagnostics engaged NUMINACORE to build **MagnusPRO** (working name) — an enterprise, radiology-first healthcare platform (Java 21/Spring Boot 3 modular monolith + React/TS; DPDP live, GDPR/HIPAA-ready via rulebook packs). This repo holds the **complete MVP 1 design**: 232 screens, 12 architecture docs, decision log D-01…D-37. Read `docs/VISION.md` → `docs/DECISIONS.md` → `INDEX.md`.

## Repository map
See root **`INDEX.md`** for the full classified index. Short version: `01-review/` (vendor-deck review), `02-gap-closure-pack/` (historical), `03-complete-pack/` (★ screen sources + group packs + design system), `04-architecture-docs/` (DOC-00…11), `docs/` (governance).

## Screen ID scheme (232 screens, 17 groups)
AU-01…19 Identity · PT-01…12 Patient · FO-01…22 Front Office · SC-01…10 Scheduling setup · OR-01…08 + CS-01…06 Orders & Safety · TK-01…12 Technician · RD-01…18 Radiologist · DD-01…11 Doctor Desk · BL-01…20 Billing · NT-01…08 Notifications · GR-01…06 Grievance · AD-01…21 Admin · IN-01…11 Integration · GV-01…18 Governance · IR-01…06 Regulatory · PL-01…13 Platform · DS-01…11 Design system.
Vendor deck used FO-S1-style IDs — DOC-08 maps both directions; every screen page carries its own "Baseline:" line.

## How to work with the pack
- **View:** open any `group-html/*.html` (or the Combined Volume) in a browser.
- **Edit one screen:** change its fragment in `html-source/waveN/<id>.html` (only `base.css` classes), then `python3 design-system/assemble_group.py <GroupKey>`.
- **Add a screen:** create the fragment, add its ID to GROUPS in `assemble_group.py`, add its mapping in `baseline_map.py`, run `python3 baseline_map.py inject`, rebuild the group, regenerate DOC-08.
- **Never** hand-edit `group-html/` outputs — they are generated.

## Design rules (enforce on every new screen)
1. Scope chip (MVP1-CORE / Conditional) + Baseline line. 2. 2–4 states — no happy-path-only. 3. Audit footer + step-up on money/legal/destructive actions + four-eyes on irreversible. 4. Masked identifiers where the viewer lacks purpose. 5. One SLA/overdue pattern (DS-03). 6. Synthetic data, ₹/IST formats, Aadhaar last-4, Malayalam for patient-facing Kerala content. 7. Vendor names only in AD-21/adapters — never in core screens (D-37).

## Key decisions the dev team must not re-litigate
Modular monolith (D-24) · release policy Option C via BL-20 (D-21) · critical-results tiers & closed loop (D-13) · same-org priors allow-and-audit (D-14) · Form F patient signature + monthly filing CORE (D-15) · GST-exempt labeling + credit notes (D-16) · retention-safe closure (D-18) · all-4-branch pilot (D-34) · PDFs dropped (D-35) · vendor-neutral small-file modularity (D-37). Full list: `docs/DECISIONS.md`.

## Status & pending
All design work complete and verified (see README Status). Pending (client): final legal product name, branch-4 details, UAT planning, sending the pack to NUMINACORE, rotating the GitHub token.

## Access
Repo: https://github.com/Magnus-PJ/MAGNUS-UI-MOCKUPS (fine-grained PAT held by Paul, pauljoy89@gmail.com). No other external systems wired.
