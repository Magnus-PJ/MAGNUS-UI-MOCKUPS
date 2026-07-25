# Magnus HMS — Vision & Aim

## The vision

Build **Magnus HMS** as a privacy-first, radiology-first, multi-tenant, multi-organization, multi-branch, multi-region healthcare management platform — serving Magnus Diagnostics' own clinic and diagnostic chain first, and designed from day one for **white-label deployment** to other clinic chains, diagnostic centres, and multi-branch healthcare organisations.

## The aim of this repository

This repo is the **UI/UX source of truth for MVP 1** — the first six-month, radiology-first pilot release — produced as a complete, enterprise-grade design pack:

1. **MVP 1 is the foundation module.** Everything designed here must carry the *entire* future roadmap (LIS, patient/referrer portals, full multi-branch, IPD/hospital workflows, SaaS tenant platform, AI) **without ever rebuilding the core**. Foundation-grade decisions (identifiers, encounter spine, event model, consent/audit patterns, design system) are locked now.
2. **Complete, not minimal.** The pack covers every screen a real Indian radiology diagnostics chain needs to operate the MVP 1 scope end-to-end — 225 screens across 17 groups, each with alternate states (error / blocked / empty / offline / success). No workflow dead-ends.
3. **Compliance is designed in, not bolted on.** DPDP Act (consent, rights, DPB), PC-PNDT (Form F with patient signature, monthly filing), AERB (licences, dose), GST (exempt healthcare invoicing, credit notes), CERT-In breach clocks, DLT SMS — every statutory obligation has an owning screen and enforcement states.
4. **Patient safety is a design requirement.** Closed-loop critical results (tiered, escalated, acknowledged), safety gates visible at the point of acquisition, physician-only overrides, duplicate/wrong-patient/wrong-side defences, partial-study hard blocks.

## Target build stack (context for these designs)

- **Backend:** Java (Spring Boot), event backbone (Kafka/RabbitMQ), Keycloak identity, policy-service authorization, FHIR-R4-aligned domain model, dcm4che imaging gateway.
- **Frontend:** React SPA consuming the same OpenAPI contracts that future portals/PWA will use; OHIF-based DICOM viewer integration recommended over building from scratch.
- **Deployment:** cloud control-plane + branch data-plane, offline-first branch operations with sync (India region pinning; DPDP data-residency).

## Pilot context

Meridian Diagnostics (synthetic tenant) · Andheri West branch pilot · radiology-first (CT/MRI/US/X-ray) · India (IST, ₹, DPDP/PC-PNDT/AERB/GST). **All data in every mockup is synthetic — no PHI anywhere.**
