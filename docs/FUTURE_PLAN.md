# Future Plan & Roadmap

## Immediate next steps (this engagement)

1. **Finish Wave 3 & Wave 4** screen production (in progress; status in README).
2. **Client's additional information review (HELD gate).** Paul will provide further inputs after Wave 4. We then: check the pack against them → add new screens / issue recommendations → only after that finalise.
3. **Final packaging** (after the gate): master index + IA map refresh (DS-11), combined single-volume pack, per-group packs, and download bundle. PDFs regenerated (one-page-per-screen renderer) only if the client re-enables them.
4. **Vendor handoff:** send NUMINACORE the review docx (01), the gap-closure pack (02), and this complete pack (03) as the UI/UX baseline for Phase 0 sign-off; walk through DECISIONS.md D-11…D-18 as design contract items.

## MVP 1 build phase (6 months, NUMINACORE)

- Phase 0 sign-off artifacts to demand: FHIR-aligned data model, ID scheme, encounter spine, event catalogue, authz policy model, audit schema, offline/sync contract, OpenAPI contracts per screen action (see review §9).
- SLA matrix (review §8) mirrored into the SoW: TAT targets, critical-result windows, delivery retries, RPO 15 min / RTO 4 h, support severities.
- UAT scripts should be generated from the 20 scenario walkthroughs in the review — they are the acceptance backbone.

## Post-MVP quarterly releases (from the scope checklist)

| Quarter theme | Contents (checklist refs) |
|---|---|
| Diagnostics & LIS | Test catalog, samples, barcodes, analyzers (HL7/ASTM), lab reports (#87–95) |
| Multi-branch expansion | Branch rollout, MPI at scale, longitudinal record, patient timeline, dashboards (#79–83, #100–101) |
| Patient/referrer network | Patient PWA portal, referrer portal, online payments at scale, teleradiology (#104–117) |
| SaaS & white-label | Tenant onboarding, branding, entitlements, metering, subscription billing (#118–129) |
| Interop & exchange | FHIR APIs, ABDM/ABHA, DICOMweb expansion, integration engine (#84–86, #147–161) |
| IPD (extended roadmap) | ADT, beds/wards, nursing, MAR, OT, discharge, IPD billing (#162–173) — the encounter spine (FO-16/NS-12) is the pre-built foundation |
| AI roadmap (parallel, governed) | AI governance, de-identification, data lake, triage, reporting assist (#174–203) — consent + human-in-the-loop patterns already present in vendor RA screens |

## Open items / watch list

- GitHub token is fine-grained and repo-scoped; rotate before expiry.
- Vendor deck data errors (review §10) must be fixed before UAT script generation.
- Q1 policy question still unanswered by Magnus: **is a signed report withheld until payment?** Needs an explicit org-level policy either way (affects BL/NT/PT screens' release logic).
- Decide OHIF vs commercial viewer before build start (RD-03/04 assume OHIF-class capability).
