# Decision Log — agreed in working sessions (July 2026)

Chronological record of every decision taken during the review-and-design engagement between Magnus (Paul) and the working sessions.

| # | Decision | Detail / rationale |
|---|---|---|
| D-01 | **Frontend is React, backend is Java (Spring).** | "Rust frontend" in the original brief was a typo. All technology-fit recommendations assume React SPA + Java services. |
| D-02 | **Review deliverable is vendor-facing.** | The design review (01-review/) is written as structured feedback to NUMINACORE, not an internal memo. |
| D-03 | **Dual scope lens.** | Feedback separates (a) fixes within MVP 1 limits and (b) foundation/architecture items to lock now so future modules never force a core rebuild. |
| D-04 | **Review scoring:** 20 real-world scenarios → 2 Covered / 8 Partial / 10 Gap; 7 compliance blockers (C-1…C-7), 6 safety gaps (S-1…S-6), 5 scope-tag inversions. | Basis for everything built afterwards. |
| D-05 | **Gap closure = 16 net-new screens (NS-01…NS-16) + 10 revisions (R-01…R-10).** | Delivered as pack 02; all 26 items were folded into the complete pack's screens. |
| D-06 | **Complete pack scope = 225 screens / 17 groups (Plan v2).** | Client direction: "think of this as the foundation module for the ultimate enterprise-grade system — add pages carefully, don't think about limits." Expanded from the 159-screen Plan v1. |
| D-07 | **Build in 4 waves with parallel design agents; checkpoint delivery after each wave.** | Wave 1 clinical core (66), Wave 2 revenue & outreach (50), Wave 3 admin & governance (48), Wave 4 identity/platform/foundations (61). |
| D-08 | **Delivery format: HTML packs are primary; PDFs deferred.** | A4 PDF pagination fragmented tall screens ("jumbled" pages). Fix attempted (one variable-height page per screen via Playwright) improved it, but client chose to defer PDFs entirely and work in HTML. PDFs can be regenerated later with `design-system/render_fixed.py`. |
| D-09 | **GitHub repo `Magnus-PJ/MAGNUS-UI-MOCKUPS` is the source of truth.** | Everything (review doc, gap pack, all screen sources, group packs, docs) is pushed here after every wave. |
| D-10 | **Final packaging is HELD.** | After Wave 4, the client will provide additional information; the pack will be reviewed against it, new screens/recommendations added, and only then finalised (master index + combined volume) for download. |
| D-11 | **Single canonical patient ID (MRN-xxxxxx) across all screens**, incl. billing. | Fixes the vendor deck's four conflicting ID formats. |
| D-12 | **Secure-link TTL standardised at 72 h**; report view window 15 min. | Fixes the vendor deck's 24 h vs 72 h contradiction. |
| D-13 | **Critical results:** tier RED (notify ≤15 min, ack ≤15 min) / ORANGE (≤60 min, ack ≤4 h); explicit send action; role-level owner; escalation ladder; addenda can carry the flag; in-product referrer acknowledgement (DD-02). | Closes the review's biggest safety finding. |
| D-14 | **Same-organisation priors: allow-and-audit for treatment purpose** (no deny wall mid-read); cross-org uses request lifecycle. | DPDP-compatible; reverses the vendor's access-denied viewer design. |
| D-15 | **PC-PNDT:** Form F requires the patient's signed undertaking; monthly submission is CORE (not cuttable); statutory declarations never pre-ticked; regulated template sections locked. | |
| D-16 | **Billing (India):** healthcare services labelled GST-Exempt (never 0% rows); credit-note chain for post-filing cancellations; central number-series registry; UPI pending states with UTR-evidence recovery; cash sessions + EOD close; async approvals. | |
| D-17 | **One SLA/overdue pattern product-wide** (DS-03): every countdown has a defined breach behaviour, owner, and escalation — "no silent breaches". | |
| D-18 | **Org/tenant closure is retention-safe** — never hard-deletes patient data; archive read-only through statutory retention (radiology 10y, billing 8y). | |
| D-19 | Screens carry scope chips (MVP1-CORE / Conditional / Post-MVP1-Roadmap) consistent with the signed scope checklist. | |
| D-20 | **All mockup data is synthetic; no PHI**; Aadhaar last-4 only; foetal-sex non-disclosure respected in all obstetric content. | |

## Expert-panel round (post-Wave-4, July 25)

| # | Decision | Detail |
|---|---|---|
| D-21 | Report release policy = **Option C** (org-configurable, clinical override, full audit); pilot default withhold-until-payment; critical results ALWAYS bypass the hold. | New screen BL-20; Report status separates signed vs released; `release_without_payment` permission. Resolves open question Q1. |
| D-22 | Pilot topology = **Option A**: one operational branch + remote radiologists; cloud control-plane / branch edge data-plane (local Docker + Orthanc). | DOC-09 §7. |
| D-23 | Offline = **Option A practical MVP**: registration/billing-cash/consent/token offline with queued sync; UPI blocked offline; reporting cloud-only. | DS-04 + DOC-09 §8; ConnectionStatusProvider + IndexedDB queue + idempotent sync endpoints. |
| D-24 | Build = **modular monolith** (Java 21/Spring Boot 3, bounded contexts, transactional outbox, adapters); Kubernetes deferred. | DOC-09 §1–2. |
| D-25 | External referrers get a **separate partner identity realm** (attribute-restricted), distinct portal pages. | AU-16 updated; DD cluster. |
| D-26 | Sign-off = **authenticated clinical sign-off** (reg no. + content hash + immutable audit), risk-based step-up (not per-report); migration batch approval added to step-up matrix. | RD-09/AU-09 updated. |
| D-27 | Patient-facing languages = **English + Malayalam** (Kerala pilot: N. Paravoor / Irinjalakuda / Pullur); react-i18next from Sprint 1. | PT-11, CS-03, DS-10 updated. |
| D-28 | Migrated patients carry `consent_status=IMPORTED_LEGACY_UNVERIFIED`, visible and restricting external sharing until fresh consent. | AD-12; front-desk prompt at next visit. |
| D-29 | SLA engine = `sla_deadline`/`sla_status` fields + scheduled sweep with auto-escalation; 99.5% uptime allows planned Sunday-night window. | DOC-09 §11. |
| D-30 | Viewer = integrate (OHIF embedded / external launch), never build; prior-selection contract: accession + prior UIDs (same patient/modality/24 months) in launch URL. | RD-05 updated; DOC-09 §7. |
| D-31 | Branding: synthetic tenant names to be replaced with final product name **before UAT** (name TBD by Magnus). | Pending client. |
| D-32 | **Working product name = MagnusPRO** (applied across all 226 screens and pack covers; final legal name confirmed at UAT per D-31). | Synthetic tenant names (Meridian etc.) remain as demo tenants. |
| D-33 | **Enterprise bars adopted:** zero-trust, air-gap capable, GDPR + HIPAA ready (in addition to DPDP). Gap audit published as DOC-11: 4 hard gaps (AU-19 device trust/JIT, IN-11 air-gap transfer, PL-13 offline updates, GV-17 disclosures + GV-18 training), 12 state-level partials, 0 foundation-breaking defects. | Backfill placement per DOC-11 §6. |
| D-34 | **Pilot deploys to ALL 4 Magnus branches together** (N. Paravoor, Irinjalakuda, Pullur, + 4th), superseding the single-branch part of D-22; cloud control-plane + 4 edge data-planes; remote reading across sites. | Raises rollout risk — mitigations: staged go-live within the window, per-branch feature toggles (AD-17), branch-scoped worklists, 4× edge monitoring (IN-10). |
| D-35 | **PDFs permanently dropped.** HTML is the sole deliverable format. | render_fixed.py kept in repo for the record only. |
| D-36 | **DOC-11 backfills built:** AU-19, IN-11, PL-13, GV-17, GV-18 + 7 state additions (GV-01/05/12/13/15, PL-05). Pack = 231 screens. | Zero-trust, air-gap, GDPR, HIPAA closures in place at design level. |
| D-37 | **Vendor-neutral + small-file modularity mandated:** no vendor names in core screens/data model — vendors live in the per-centre registry (AD-21) + replaceable adapters; every screen is one small standalone file so any item can be changed without touching the rest; white-label via theme tokens. | New screen AD-21 centre details & vendor registry; README rewritten around these rules. |
