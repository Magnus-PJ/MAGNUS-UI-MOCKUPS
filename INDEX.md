# MagnusPRO — Repository Index

> Complete classified index. Everything is HTML/Markdown — no build needed; open files in a browser.
> **Entry point:** [`04-architecture-docs/DOC-00_Master_Index.html`](04-architecture-docs/DOC-00_Master_Index.html)

## A · Governance documents (`docs/`)
| File | What it is |
|---|---|
| [docs/VISION.md](docs/VISION.md) | Vision, aims, enterprise bars, target stack |
| [docs/DECISIONS.md](docs/DECISIONS.md) | Decision log D-01…D-37 (binding design contract) |
| [docs/FUTURE_PLAN.md](docs/FUTURE_PLAN.md) | Next steps, quarterly roadmap, open items |
| [docs/HANDOFF.md](docs/HANDOFF.md) | Cold-start guide: repo map, ID scheme, how to edit/rebuild |
| [00-project-log/PROJECT_LOG.md](00-project-log/PROJECT_LOG.md) | Chronological engagement record |

## B · Architecture & workflow documentation (`04-architecture-docs/`)
| Doc | Title |
|---|---|
| DOC-00 | Master Index (linked hub) |
| DOC-01 | Patient Scenario Walkthroughs (25 end-to-end) |
| DOC-02 | Workflow Orders — screen operating sequences |
| DOC-03 | Roles, Hierarchy & Permission Model |
| DOC-04 | Security Architecture — Layers |
| DOC-05 | Audit & Logging Architecture |
| DOC-06 | Complete Billing Workflows |
| DOC-07 | Authentication & MFA — Complete Flows |
| DOC-08 | Vendor Baseline Crosswalk (232 ↔ 106) |
| DOC-09 | Build & Deployment Blueprint (Java/React, modular monolith, edge sync) |
| DOC-10 | Test Traceability + Safety-Gate Suite SG-01…12 |
| DOC-11 | Zero-Trust · Air-Gap · GDPR · HIPAA Gap Analysis (closures BUILT) |

## C · The design pack (`03-complete-pack/`)
| Path | Contents |
|---|---|
| `html-source/wave1/` | FO-01…22 · OR-01…08 · CS-01…06 · TK-01…12 · RD-01…18 (66 fragments) |
| `html-source/wave2/` | BL-01…20 · NT-01…08 · PT-01…12 · DD-01…11 (51 fragments) |
| `html-source/wave3/` | AD-01…21 · GV-01…18 · GR-01…06 · IR-01…06 (51 fragments) |
| `html-source/wave4/` | AU-01…19 · SC-01…10 · IN-01…11 · PL-01…13 · DS-01…11 (64 fragments) |
| `group-html/` | 17 browser-ready group packs + **Combined Volume (232 screens)** |
| **`MagnusPRO_Live_Prototype.html`** | **★ The app-like prototype: login → role → click through everything + 8 guided E2E journeys** |
| `design-system/` | `base.css` · `assemble_group.py` · `baseline_map.py` · `render_fixed.py` (PDF, deprecated) |
| `group-pdfs/` | DEPRECATED (D-35) — kept for history only |

## D · Historical inputs (`01-review/`, `02-gap-closure-pack/`)
| Path | Contents |
|---|---|
| `01-review/` | Review of the vendor's original 106-screen walkthrough (.docx) — findings C-x/S-x, SLAs, foundation asks |
| `02-gap-closure-pack/` | First-round gap screens NS-01…16 + revisions R-01…10 (superseded by the complete pack, kept for traceability) |

## E · Test-readiness research (`05-test-readiness/`) — DRAFT
| File | What it is |
|---|---|
| [05-test-readiness/MagnusPRO_Test_Readiness_Research.md](05-test-readiness/MagnusPRO_Test_Readiness_Research.md) | 18 demand dimensions w/ verdicts · scenarios S26–S40 · gap list N-1…N-7 (pending client decision) |
| [05-test-readiness/MagnusPRO_Screen_Inventory_232.md](05-test-readiness/MagnusPRO_Screen_Inventory_232.md) | Full organized inventory of all 232 screens |
