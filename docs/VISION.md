# MagnusPRO — Vision & Aim

## The vision

Build **MagnusPRO** (working name; final legal name before UAT) as a **true enterprise healthcare operating platform**: privacy-first, radiology-first at launch, multi-tenant, multi-organization, multi-branch, multi-region — serving Magnus Diagnostics' four Kerala centres first, and designed from day one for **white-label deployment** to other clinic chains, diagnostic centres and hospitals.

MVP 1 is not a small product — it is the **foundation module** of the complete platform. Every future module in every section of healthcare — **LIS, IPD, OT, ICU, ER, IVF, nuclear medicine, pharmacy & inventory, CRM, patient & referrer portals, telehealth, ABDM & international interop, and governed AI** — must attach to the patient, encounter, order, billing, consent, identity and audit foundations built now, **without ever rebuilding the core**.

## The five enterprise bars (all designed-in — audited in DOC-11)

1. **Production-grade** — every screen ships with its error/blocked/empty/offline states, SLA breach behaviour, and audit trail; nothing is happy-path-only.
2. **Zero-trust** — identity-centric access, MFA, device trust & conditional access (AU-19), JIT elevation, object-bound step-up tokens, masked-by-default data, DLP thresholds, no standing privileged access anywhere (including the platform operator).
3. **Air-gap capable & highly secure** — offline-first branches with idempotent sync (IN-10), and true air-gapped operation via signed-bundle transfer (IN-11) and offline update bundles (PL-13).
4. **Multi-jurisdiction compliance** — DPDP live for the pilot; **GDPR and HIPAA readiness built as regional rulebook policy packs** (PL-05) with the supporting surfaces (disclosures register GV-17, processing restriction & portability GV-05, lawful-basis register GV-12, BAA/SCC coverage GV-13, training & attestation GV-18) — compliance is rulebook content, not code forks.
5. **Vendor-neutral & white-label** — no vendor names in core screens or the data model; every external dependency (PACS, viewer, SMS, WhatsApp, payments, edge hardware) is a replaceable adapter registered per centre (AD-21); tenant branding via theme tokens (DS-01, AD-14). Swapping a vendor is a registry + config change, never a rebuild.

## What this repository is

The **UI/UX and architecture source of truth for MVP 1**: 232 production-grade screens (17 groups), 12 architecture documents, the decision log (D-01…D-37) and the crosswalk proving the pack is a faithful **extension of the vendor's baseline deck** (140 screens extend it; 92 net-new, each justified by a review finding or scope item).

## Build & pilot context

- **Stack:** Java 21 / Spring Boot 3 **modular monolith** (bounded contexts, transactional outbox, replaceable adapters) · React + TypeScript · Keycloak · PostgreSQL · OHIF-class viewer integration · Docker (K8s deferred) — full blueprint in DOC-09.
- **Pilot (D-34):** all **4 Magnus branches together** — cloud control plane + 4 edge data planes, remote reading across sites, per-centre readiness on AD-21.
- **Languages:** staff English; patient-facing English + **Malayalam** (Kerala), i18n-ready for more.
- **Data:** every mockup uses synthetic data — no PHI anywhere.
