# Future Plan & Roadmap — MagnusPRO

## Immediate (client actions — nothing blocks on the design side)
1. **Final legal product name** → one sweep replaces the MagnusPRO working name across screens/docs (pre-UAT, D-31/D-32).
2. **Branch-4 details** for AD-21 (name, code, modalities, edge hardware).
3. **Hand the pack to NUMINACORE**: repo link + `01-review/` docx; walk DECISIONS D-11…D-37 as the design contract; DOC-09 defines Sprint-1 readiness.
4. **UAT planning** (deferred): derive scripts from DOC-10 (25 scenario chains + safety gates SG-01…12 + statutory set); assign acceptance owners.
5. Rotate/revoke the shared GitHub token.

## MVP 1 build phase (6 months, all-4-branch pilot per D-34)
- Phase 0 artifacts to demand: data model (FHIR-aligned), ID scheme, encounter spine, event catalogue, authz policy model, audit schema, offline/sync contract, OpenAPI per screen action (DOC-09).
- SLA matrix mirrored into the SoW (report TAT, critical tiers, RPO 15m/RTO 4h, Sunday maintenance window).
- Staged go-live inside the window across the 4 branches; per-branch feature toggles (AD-17) as the risk valve; readiness tracked on AD-21.

## Post-MVP quarterly releases (scope checklist)
| Theme | Contents |
|---|---|
| Diagnostics & LIS | Test catalog, samples, barcodes, analyzers, lab reports (#87–95) |
| Portals & network | Patient PWA, referrer portal expansion, teleradiology at scale (#104–117) |
| SaaS & white-label | Tenant onboarding, entitlements, metering, subscription billing (#118–129) |
| Interop | FHIR APIs, ABDM/ABHA, DICOMweb expansion, integration engine (#84–86, #147–161) |
| IPD & hospital | ADT, beds, nursing, MAR, OT, discharge, IPD billing (#162–173) — encounter spine is pre-built |
| International | Activate EU-GDPR / US-HIPAA rulebook packs (PL-05) + BAA/SCC execution per tenant |
| AI (governed, parallel) | Governance, de-identification, data lake, triage, reporting assist (#174–203) |

## Watch list
- Vendor deck data errors (review §10) must be fixed before UAT scripts are generated.
- OHIF vs commercial viewer decision before build start (RD-03/04, DOC-09 §7).
- Air-gap screens (IN-11, PL-13) activate only when an air-gapped site is contracted.
- DOC-10 acceptance-owner column to be filled at UAT planning.
