# Magnus HMS — UI/UX Project Log

Chronological record of everything produced in this engagement (July 2026).

## 1. Design review (input: vendor's 107-page MVP 1 walkthrough + scope checklist)
- Reviewed all 106 vendor screens (18 clusters) + 209-item scope checklist.
- Tested 20 real-world radiology-clinic scenarios → 2 Covered / 8 Partial / 10 Gap.
- Findings: 7 statutory/compliance blockers (C-1…C-7), 6 patient-safety gaps (S-1…S-6),
  5 scope-tag inversions, ~14 workflow dead-ends, 14 prototype data errors, 12 vendor questions.
- SLA matrix proposed (TAT, critical-result ack tiers, delivery retries, RPO/RTO 15min/4h).
- Foundation asks: FHIR-R4-aligned domain model, one canonical ID scheme, encounter spine,
  event backbone (Kafka/RabbitMQ), policy-service authz (Keycloak+OPA), hash-chained audit,
  terminology versioning, OHIF viewer integration, offline/sync contract. Stack: Java (Spring Boot) + React.
- Deliverable: `01-review/Magnus_HMS_MVP1_UIUX_Design_Review_Feedback.docx`

## 2. Gap-closure design pack (16 new screens NS-01…NS-16 + 10 revisions R-01…R-10)
- Deliverable: `02-gap-closure-pack/` (PDF re-rendered one-page-per-screen + HTML source)

## 3. Complete MVP 1 design pack — 225 screens / 17 groups / 4 waves
- Plan v2 approved: enterprise-foundation completeness, unlimited page budget.
- Groups G1–G17 (see README). One HTML fragment per screen; shared design system `base.css`.
- Waves: 1 Clinical core (66) ✅ · 2 Revenue & outreach (50) 🔄 · 3 Admin & governance (48) · 4 Identity/platform/foundations (61).
- PDF rendering: one variable-height page per screen (Playwright) after A4 fragmentation issue was found and fixed.
- Final packaging intentionally HELD until client provides additional inputs after Wave 4.

## Key design decisions carried through every screen
- Critical-results closed loop: tiers (RED 15m / ORANGE 4h), explicit send, escalation ladder, in-product referrer ack.
- Safety gates visible at point of acquisition; physician-only overrides; partial-study hard block.
- Same-org priors: allow-and-audit (treatment purpose); masked identifiers on all denial screens.
- PC-PNDT: patient signature on Form F, centre-specific registration checks, monthly submission = CORE.
- Billing: GST-exempt labeling, credit-note chain, UPI pending/UTR-evidence recovery, cash sessions, async approvals.
- One SLA/overdue pattern product-wide; DPDP microcopy + audit line on every screen; synthetic data only.
