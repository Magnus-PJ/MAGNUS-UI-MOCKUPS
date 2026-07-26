# MagnusPRO — Test-Readiness & Capability Research (DRAFT for client review)

**Purpose:** before any next build step — (1) list every demand/test dimension (yours + extensions), with an honest verdict on the current 232-screen design; (2) list new real-world scenarios beyond the existing 25; (3) list the genuine gaps found; (4) the full organized inventory of built pages. Nothing here is built yet — this is the research you asked to review first.

---

## PART A — Demand dimensions & verdicts

Verdicts: ✅ DESIGNED (surface + states exist) · 🟡 PARTIAL (foundation exists, surface or test missing) · 🔴 GAP (needs new pages/concept)

| # | Demand | Verdict | Evidence & what's missing |
|---|---|---|---|
| A1 | Clinical-scenario completeness testing of current pages | ✅ | DOC-01 (25 scenario chains) + DOC-10 (84 test cases, safety gates SG-01…12). Method ready: walk each chain against group packs. |
| A2 | Each role sees ONLY the data it needs | ✅ design / 🟡 test | DOC-03 role×group matrix, ABAC (care-team, own-branch, purpose), masking DS-07, referrer realm. **Missing: a negative-access test suite** (deny-cases per role, e.g. cashier must NOT open a report body) — needs adding to DOC-10 as RB-xx tests. |
| A3 | Role-based viewing alterable when need arises | ✅ | AD-04 custom roles + editable matrix (approval + versioning + simulate-user), ABAC condition editor, JIT elevation (AU-19), delegation (DD-10), branch feature toggles (AD-17). Runtime-configurable, change-controlled — never a code change. |
| A4 | Core strong enough for quarterly modules, added seamlessly | ✅ design / 🟡 drill | Encounter spine, generic ServiceRequest/Report model, event backbone, adapters, entitlements (PL-04), toggles (AD-17), release rings (PL-08). **Missing: a "module-addition drill"** — enable a sandbox LIS module for one branch in staging, prove zero core migration. |
| A5 | Changes pushed without affecting regular work | ✅ design / 🟡 drill | Release rings + rollback (PL-08), blast-radius previews (AD-17/PL-04), effective-dated configs (price lists BL-10, letterheads AD-14, calendars SC-06), versioned templates, Sunday window (D-29). **Missing: explicit change-drill tests** (price change mid-day with invoices open; template change with drafts open; rulebook update mid-month). |
| A6 | Seamless user experience | 🟡 | One design system (DS-01…11), consistent patterns, i18n, offline banners. **Missing: a usability test protocol** — task-completion time targets per persona (register ≤90s, check-in ≤30s, sign report ≤4 clicks), kiosk accessibility test. |
| A7 | Accounting integrity | 🟡 | Strong per-branch: invoices→receipts→refunds→CRN→ledger→day book→GST export→cash sessions. **Gaps: (a) org-level financial consolidation across the 4 branches (BL-18 is branch-scoped); (b) accounting period close/lock at org level (only GST export locks today); (c) cross-branch payments & inter-branch settlement** (pay/advance at branch A for a scan at branch B). |
| A8 | Multi-site, multi-user (same organisation) | ✅ mostly | MPI (FO-08/09), cross-branch priors (RD-03), floating staff (AD-03), branch-scoped worklists, org dashboard (AD-13), 4-edge sync (IN-10), centre registry (AD-21). **Gap: central/multi-branch scheduling view** (call-centre books any branch — FO-10 is single-branch today). |
| A9 | Different organisations, multi-user (multi-tenant) | ✅ isolation / 🔵 roadmap | Tenant isolation, plans, metering, operator dual-control (PL cluster). Cross-ORG workflows (tenant-A referring to tenant-B, teleradiology marketplace) = deliberate roadmap, not MVP. |
| A10 | Same organisation, DIFFERENT BRAND per branch | 🔴 | Branding today is org-level (AD-14) and tenant-level (white-label). A "brands" layer between org and branch (e.g. "Magnus Diagnostics" + "Magnus Scans Pullur") does not exist: needs brand entity + per-brand letterheads, SMS sender/DLT headers, patient-page branding, report headers, receipts. **Candidate: AD-22 Brand management + states in AD-14 / NT-04 / PT pages / DS-09.** |
| A11 | Concurrency safety (multi-user same object) | ✅ | Draft lock + takeover (RD-07), slot-conflict rejection (FO-10), same-study concurrent-reader warning (RD-04), queue accept/steal rules (RD-01), idempotency keys. |
| A12 | Performance & scale (1000+ users, checklist #29) | 🟡 | Non-UI: needs load-test plan (morning-rush 100 concurrent, 4-branch sync fan-in). Propose as acceptance drill. |
| A13 | Resilience: DR / failover / offline | ✅ design / 🟡 drill | RPO 15m/RTO 4h + restore-test register (PL-09), edge offline (DS-04/IN-10). Drills to schedule: DR failover during a reporting session; branch offline 4h during rush. |
| A14 | Security assurance | ✅ design / 🟡 drill | DOC-04 layers, DOC-11 closures. Drills: penetration test, breach tabletop (GV-09), access-review campaign dry-run. |
| A15 | Statutory audit readiness | ✅ | PC-PNDT inspector simulation: IR register + submissions + Form F evidence pull ≤30 min; AERB (IR-05); DPDP evidence (GV-14/GV-15). Add as drill ST-05. |
| A16 | Data migration rehearsal | ✅ design / 🟡 drill | AD-12 dry-run/rollback designed; needs a full rehearsal with real legacy exports before go-live. |
| A17 | Accessibility & devices | 🟡 | WCAG intent + DS specs; needs an audit pass + device/browser/print-hardware matrix test (thermal slips, label printers, kiosk touch). |
| A18 | Comms deliverability | 🟡 | NT designs complete; needs live DLT/WhatsApp sandbox delivery test per template variant (NT-08) before go-live. |

---

## PART B — New real-world scenarios (beyond the existing 25 in DOC-01)

| # | Scenario | Exercises | Current status |
|---|---|---|---|
| S26 | Advance paid at N. Paravoor; scan done at Irinjalakuda; partial refund at Pullur | Cross-branch money movement, org ledger | 🔴 needs A7(c) design |
| S27 | Org month-end close: 4 branches reconciled, consolidated P&L extract, GST filing | Org finance consolidation + period lock | 🔴 needs A7(a,b) |
| S28 | Central call-centre books/reschedules across all 4 branches from one screen | Multi-branch scheduling view | 🔴 needs A8 gap |
| S29 | Same patient books same-day slots at two branches | MPI + cross-branch conflict warning | 🟡 partial (MPI exists; conflict rule undefined) |
| S30 | Patient at a differently-branded branch gets brand-correct SMS, receipt, report letterhead | Brand layer | 🔴 needs A10 |
| S31 | Price list v2 published at 14:00 while invoices are open at all branches | Effective-dating under load | ✅ designed (BL-10 versions) — add change-drill test |
| S32 | Report template updated while 3 radiologists have open drafts | Template versioning + draft pinning | ✅ designed (RD-18 guards) — add drill |
| S33 | LIS sandbox module enabled for one branch via toggles, mid-week, zero downtime | Module-addition seam | 🟡 drill needed (A4) |
| S34 | Cashier gets supervisor rights for 2h via JIT, then auto-revoked | Alterable RBAC | ✅ designed (AU-19) |
| S35 | Monday 08:00 rush: ~100 concurrent staff, 4 branches + remote reading | Performance | 🟡 load-test plan |
| S36 | Cloud region failover while a radiologist is mid-report | DR + draft preservation | 🟡 drill (RD-04 restore + PL-09) |
| S37 | PC-PNDT inspector arrives unannounced; evidence pack in 30 minutes | Statutory readiness | ✅ designed (IR cluster) — add drill ST-05 |
| S38 | Patient withdraws notification consent mid-visit; report ready 2h later | Consent propagation to delivery | ✅ designed (NT-05/GV-11) |
| S39 | Referrer abroad; locum delegate acknowledges a RED critical result | Delegation + critical loop | ✅ designed (DD-10 + DD-02) |
| S40 | Second organisation onboarded onto the platform while Magnus runs live | Tenant isolation proof | ✅ designed (PL-02) — add isolation test |

## PART C — Consolidated gap list (what would actually be built next — pending your go)

| # | Item | Type | Closes |
|---|---|---|---|
| N-1 | **AD-22 Brand management** (org → brands → branches; per-brand letterhead, DLT sender, patient-page & report branding) | New screen + states in AD-14/NT-04/DS-09/PT | A10, S30 |
| N-2 | **BL-21 Org finance consolidation & period close** (4-branch roll-up, month-end lock, variance) | New screen | A7(a,b), S27 |
| N-3 | **BL-22 Inter-branch transactions & settlement** (pay-anywhere, advance-anywhere, internal settlement register) | New screen + states in BL-03/14 | A7(c), S26 |
| N-4 | **FO-23 Multi-branch scheduling view** (call-centre booking across branches; same-day cross-branch conflict warning) | New screen | A8, S28, S29 |
| N-5 | **RB-xx negative-access test suite** added to DOC-10 (per-role deny cases) | Doc addition | A2 |
| N-6 | **Acceptance drills annex** in DOC-10: module-addition, change-push, DR-failover, load, migration rehearsal, DLT live test, PNDT inspection, tenant-isolation | Doc addition | A4, A5, A12–A18 |
| N-7 | **Usability test protocol** (persona task-time targets) | Doc addition | A6 |

## PART D — Current page inventory (232 screens, organized)

See `inventory.md` (attached) — every screen ID, title and scope chip, grouped G1–G17. Spot-verified during this research: all 232 fragments valid, baseline-tagged, MagnusPRO-branded; scope chips consistent (CONDITIONAL screens: FO-19, FO-22, SC-08, TK-11, RD-02, RD-06, RD-16, DD-08, DD-10, DD-11, NT-08, GR-06, AD-19, GV-12, GV-18, AU-19, IN-11, PL-13).

## Suggested next steps (for your decision — nothing started)
1. Approve/edit the gap list N-1…N-7 (N-1…N-4 are the only new screens; N-5…N-7 are document additions).
2. I build approved items, re-verify, update crosswalk/docs, push.
3. Then (optionally) run the paper test-pass: every scenario S01–S40 walked against the packs with pass/fail noted per screen — producing the completeness certificate you want before handing to NUMINACORE.
