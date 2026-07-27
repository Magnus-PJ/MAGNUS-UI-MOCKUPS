# Client inputs — new round (26 Jul 2026) — HOLD, more to come

Status: **ACTIONED (27 Jul 2026, v1.4 round, D-44).** Paul said "proceed and make the MVP the best" — all four Input-1 items are now designed: DS-14 (printing everywhere), DS-13 + DOC-02 Flow 17 (concurrent same-patient operators; walk-in + booked convergence), FO-06 State D + DS-12 "Priors ▸" (fast prior-history pull, ≤2 s, all branches). Further inputs, if any, start a new round in this file.

## Input 1 (received 26 Jul 2026)

1. **Printer access is available everywhere.** Every location/counter has printer access — screens can assume print capability at all points (registration, billing, token, consent, reports, Form F, counter pickup).

2. **Concurrent multi-operator use, including on the SAME patient.** Multiple operators will be working in the system at the same time, and at times on the same patient simultaneously (e.g. front office editing demographics while billing collects payment while a technician opens the same visit). Concurrency, locking/merge, and live-refresh behaviour need to be explicit.

3. **Both intake paths coexist:** walk-in patients who register and get tested on the spot, AND patients with prior appointments/bookings who arrive and get tested. Both must be first-class flows.

4. **Prior history must be pullable QUICKLY when needed:** prior bookings, prior test results, and all prior history for a patient must be available and fast to retrieve at point of need (any screen where the patient is in context).

## Awaiting

- Further inputs from Paul (he said: "I have more work and discussion to give you… I will add soon. Once you get all the info, only then react and start work.")

## Pre-analysis notes (for when work opens — NOT actioned)

- Item 1 touches: FO print points, BL receipts, NT counter pickup, IR Form F printing, DS print pattern.
- Item 2 touches: DS optimistic-locking/presence pattern, FO/BL/TK simultaneous visit access, audit (who changed what while whom), DOC-02 workflow orders, DOC-13 action contracts.
- Item 3 touches: FO-02/FO-06 (walk-in) vs SC/FO arrival flows (booked); token & queue merge rules.
- Item 4 touches: DS-12 pinned patient context bar, GS-01 omni-search, FO-06 patient 360, RD prior access (D-14), performance budget (DOC-10 annex).
