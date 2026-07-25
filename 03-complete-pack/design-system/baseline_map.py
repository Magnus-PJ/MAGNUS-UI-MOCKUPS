"""Vendor-baseline crosswalk: our screen ID -> relation to vendor deck (MVP1UIUXDESIGN.pdf, 106 screens)
and review refs (C-x/S-x/N-x from Magnus_HMS_MVP1_UIUX_Design_Review_Feedback.docx).
Injects a 'Baseline' line into each fragment's screen-head and can emit the crosswalk table."""
import pathlib, re, sys

# our-id : (relation, vendor/ref text)
M = {
 # G3 Front Office
 "fo-01":("EXTENDS","FO-S1 Reception dashboard"), "fo-02":("EXTENDS","FO-S2 Patient search"),
 "fo-03":("EXTENDS","FO-S3 Registration — demographics step"), "fo-04":("EXTENDS","FO-S3 Registration — duplicate review step"),
 "fo-05":("EXTENDS","FO-S3 Registration — consent step"), "fo-06":("EXTENDS","FO-S7 Patient record"),
 "fo-07":("NET-NEW","closes review §5 delivery-hijack guard (relates FO-S7)"), "fo-08":("NET-NEW","closes S-6 / N-2 patient merge (no vendor screen)"),
 "fo-09":("NET-NEW","closes S-6 / N-2 merge resolve (no vendor screen)"), "fo-10":("EXTENDS","FO-S4 Appointment scheduling"),
 "fo-11":("EXTENDS","FO-S6 Reschedule / cancel"), "fo-12":("EXTENDS","FO-S10 Appointments"),
 "fo-13":("EXTENDS","FO-S5 Check-in & token issuance"), "fo-14":("EXTENDS","FO-S5 queue control + FO-S9 display rules"),
 "fo-15":("NET-NEW","walk-in fast-track (scope item #51)"), "fo-16":("NET-NEW","N-7 visit/encounter spine (checklist #15/#16)"),
 "fo-17":("EXTENDS","FO-S1 no-show reconcile → full EOD close"), "fo-18":("NET-NEW","referred/paper intake (scope item #51)"),
 "fo-19":("NET-NEW","waitlist (Conditional)"), "fo-20":("EXTENDS","FO-S7 representatives section"),
 "fo-21":("NET-NEW","shift handover (ops continuity)"), "fo-22":("NET-NEW","kiosk self check-in (Conditional)"),
 # G5 Orders & Clinical Safety
 "or-01":("EXTENDS","RT-S3 + DD-S2 shared order path"), "or-02":("NET-NEW","closes S-5 / N-9 duplicate & laterality (vendor DD-S2 demoed the failure)"),
 "or-03":("EXTENDS","RT-S3 order confirmation → full timeline"), "or-04":("NET-NEW","orders worklist (dept view)"),
 "or-05":("NET-NEW","closes RT-S2 cancellation-visibility gap"), "or-06":("NET-NEW","prep protocols (scope item #61/#63)"),
 "or-07":("NET-NEW","closes S-5 STAT-inflation governance"), "or-08":("NET-NEW","paper referral digitisation"),
 "cs-01":("EXTENDS","CS-S1 contrast screening + R-01 eGFR pathway"), "cs-02":("NET-NEW","MR safety (closes DD-S2 deferred-safety gap)"),
 "cs-03":("EXTENDS","CS-S2 consent + R-02 refusal/vernacular"), "cs-04":("NET-NEW","closes S-2 physician-only override (was CS-S1 self-override)"),
 "cs-05":("NET-NEW","adverse reaction record (clinical safety)"), "cs-06":("EXTENDS","IR-S1 Form F + C-1 patient signature (NS-10)"),
 # G6 Technician
 "tk-01":("EXTENDS","RT-S1 worklist + S-2 safety gates (NS-05)"), "tk-02":("EXTENDS","RT-S2 acquisition + S-3 partial-study block"),
 "tk-03":("EXTENDS","RT-S4 exception queues (re-tagged CORE)"), "tk-04":("EXTENDS","RT-S2 hold/cancel → visible terminal states"),
 "tk-05":("NET-NEW","closes RT-S2 flag-retake dead-end"), "tk-06":("NET-NEW","contrast administration record (lot/batch)"),
 "tk-07":("NET-NEW","closes R-07 device-down alerting (relates IN-S1)"), "tk-08":("EXTENDS","IN-S1 modality sync detail"),
 "tk-09":("NET-NEW","room & prep checklist (protocol-driven)"), "tk-10":("EXTENDS","RT-S2 dose block → registry + DRL flags"),
 "tk-11":("NET-NEW","QC & calibration log (Conditional)"), "tk-12":("NET-NEW","technician daily summary & handover"),
 # G7 Radiologist
 "rd-01":("EXTENDS","RR-S1 reading worklist"), "rd-02":("EXTENDS","RR-S1 teleradiology action (Conditional)"),
 "rd-03":("EXTENDS","RR-S2 viewer + S-4 same-org priors fix"), "rd-04":("EXTENDS","RR-S2 degraded/edge states"),
 "rd-05":("EXTENDS","RR-S2 prior-comparison layout"), "rd-06":("NET-NEW","hanging protocols (Conditional)"),
 "rd-07":("EXTENDS","RR-S3 authoring + R-03 uncoded escape"), "rd-08":("NET-NEW","pre-sign quality checklist"),
 "rd-09":("EXTENDS","RR-S4 sign-off + C-3 explicit declaration"), "rd-10":("EXTENDS","RR-S4 critical toggle → full flag/tier/send (NS-01, S-1)"),
 "rd-11":("EXTENDS","RR-S6 critical queue + S-1 send/owner/escalation"), "rd-12":("EXTENDS","RR-S5 addendum + S-1c critical flag & re-notify"),
 "rd-13":("EXTENDS","RR-S7 signed report + R-04 distribution status"), "rd-14":("NET-NEW","report registry & governed search"),
 "rd-15":("EXTENDS","RR-S5 chain → version diff view"), "rd-16":("NET-NEW","second opinion (Conditional)"),
 "rd-17":("EXTENDS","AD-S6 KPIs → radiologist personal dashboard"), "rd-18":("EXTENDS","RR-S8 templates + C-3 locked statutory sections"),
 # G9 Billing
 "bl-01":("EXTENDS","BL-S1 worklist (single MRN identity, D-11)"), "bl-02":("EXTENDS","BL-S2 invoice + C-5 GST fixes"),
 "bl-03":("EXTENDS","BL-S3 payment collection + cash UI"), "bl-04":("EXTENDS","BL-S3 pending → NS-09 UPI recovery"),
 "bl-05":("EXTENDS","BL-S4 receipts + duplicate watermark"), "bl-06":("EXTENDS","BL-S5 refunds + failure state"),
 "bl-07":("EXTENDS","BL-S6 cancel + R-05 credit notes"), "bl-08":("EXTENDS","BL-S2/S5 approvals → NS-06 async queue"),
 "bl-09":("NET-NEW","NS-08 cash session & EOD close"), "bl-10":("EXTENDS","BL-S7 catalog & price lists"),
 "bl-11":("EXTENDS","BL-S9 payers (re-scoped minimal into MVP1)"), "bl-12":("EXTENDS","BL-S2 discounts → rules & limits"),
 "bl-13":("EXTENDS","BL-S8 setup + C-5c/d numbering & tax"), "bl-14":("NET-NEW","advances & deposits"),
 "bl-15":("EXTENDS","FO-S7 history → full patient ledger"), "bl-16":("NET-NEW","estimates/quotes"),
 "bl-17":("NET-NEW","write-off & bad debt"), "bl-18":("NET-NEW","day book & collections"),
 "bl-19":("NET-NEW","C-5e GST summary export"),
 "bl-20":("NET-NEW","resolves open question Q1: report release policy Option C (signed vs released, clinical override, critical bypass)"),
 # G10 Notifications
 "nt-01":("EXTENDS","NT-S1 delivery ledger"), "nt-02":("EXTENDS","NT-S1 failures → NS-07 recovery worklist"),
 "nt-03":("EXTENDS","NT-S2 templates & DLT"), "nt-04":("EXTENDS","IN-S3 + NT-S3 channels & senders"),
 "nt-05":("EXTENDS","NT-S1 suppressions → consent cross-view"), "nt-06":("NET-NEW","per-patient message log"),
 "nt-07":("NET-NEW","quiet hours & TRAI rules"), "nt-08":("EXTENDS","NT-S2 preview → test harness (Conditional)"),
 # G2 Patient
 "pt-01":("EXTENDS","PT-S1 secure link & OTP"), "pt-02":("EXTENDS","PT-S2 report view"),
 "pt-03":("EXTENDS","PT-S1 expired/renew + D-12 TTL standardised"), "pt-04":("EXTENDS","BL-S4 receipt → patient link view"),
 "pt-05":("EXTENDS","FO-S4 prep instructions → patient page"), "pt-06":("EXTENDS","BL-S3 → patient online payment page"),
 "pt-07":("EXTENDS","PT-S4 consent view"), "pt-08":("EXTENDS","PT-S4 privacy & rights"),
 "pt-09":("EXTENDS","PT-S4 'how to make a request' → digital submission"), "pt-10":("EXTENDS","GR-S3 → patient tracking page"),
 "pt-11":("NET-NEW","language & accessibility"), "pt-12":("EXTENDS","GR-S2 → patient help & troubleshooting"),
 # G8 Doctor Desk
 "dd-01":("EXTENDS","DD-S1 patient summary"), "dd-02":("EXTENDS","DD-S1 'Results inbox — SOON' → built (NS-02, S-1g)"),
 "dd-03":("EXTENDS","DD-S2 order + S-5 interception"), "dd-04":("EXTENDS","DD-S1 orders → status tracking"),
 "dd-05":("EXTENDS","DD-S1 break-glass + R-08 auto-expiry"), "dd-06":("EXTENDS","AZ-S2 + C-7 masked denial (NS-14)"),
 "dd-07":("NET-NEW","my patients list"), "dd-08":("NET-NEW","referral analytics (Conditional)"),
 "dd-09":("NET-NEW","delivery preferences & profile"), "dd-10":("NET-NEW","delegation/locum (Conditional)"),
 "dd-11":("NET-NEW","SOAP & prescription (scope items #74/#76, Conditional)"),
 # G12 Admin
 "ad-01":("EXTENDS","AD-S1 org & branches + decommission lifecycle"), "ad-02":("EXTENDS","FO-S9 service points → master data"),
 "ad-03":("EXTENDS","AD-S2 users + R-10 multi-branch & dependency guards"), "ad-04":("EXTENDS","AD-S3 roles & permissions"),
 "ad-05":("EXTENDS","AD-S7 approvals + access-review campaigns"), "ad-06":("EXTENDS","AD-S9 practitioners + C-6 mandatory registrations"),
 "ad-07":("EXTENDS","RT-S3 referring-doctor directory → admin surface"), "ad-08":("EXTENDS","AD-S11 equipment + C-6 PNDT machine field"),
 "ad-09":("EXTENDS","AD-S11 validity data → NS-13 expiry enforcement"), "ad-10":("EXTENDS","AD-S4 consent admin + notice versions"),
 "ad-11":("EXTENDS","AD-S12 terminology + version pinning"), "ad-12":("EXTENDS","AD-S5 import + rollback & consent state"),
 "ad-13":("EXTENDS","AD-S6 dashboard + governed drill-through"), "ad-14":("EXTENDS","AD-S8 branding + effective-dated letterheads"),
 "ad-15":("EXTENDS","AD-S8 → document templates registry"), "ad-16":("EXTENDS","BL-S8 series → central number registry (C-5c)"),
 "ad-17":("EXTENDS","PL-S3 features → branch-level toggles"), "ad-18":("NET-NEW","scheduled jobs monitor"),
 "ad-19":("NET-NEW","staff announcements (Conditional)"), "ad-21":("NET-NEW","pilot ops: centre details & vendor registry (vendor-neutral adapters, D-37)"),
 "ad-20":("EXTENDS","GV-S2 audit stream → branch-admin viewer"),
 # G14 Governance
 "gv-01":("NET-NEW","compliance calendar (statutory obligations)"), "gv-02":("EXTENDS","GV-S2 access log review"),
 "gv-03":("EXTENDS","GV-S1 emergency access review"), "gv-04":("EXTENDS","GV-S3 deletion pipeline + failure states"),
 "gv-05":("EXTENDS","GV-S3/PT-S4 → copy/correction/nominee execution"), "gv-06":("EXTENDS","GV-S5 retention (re-tagged CORE)"),
 "gv-07":("NET-NEW","NS-11 legal holds"), "gv-08":("EXTENDS","GV-S4 → NS-15 incident front door"),
 "gv-09":("EXTENDS","GV-S4 breach runbook + overdue states"), "gv-10":("EXTENDS","AD-S4 notices → governance versioning"),
 "gv-11":("NET-NEW","consent registry & analytics"), "gv-12":("NET-NEW","DPIA-lite register (Conditional)"),
 "gv-13":("NET-NEW","processor/vendor register (DPAs)"), "gv-14":("EXTENDS","PL-S4 residency → evidence page"),
 "gv-15":("NET-NEW","audit export governance"), "gv-16":("EXTENDS","GV cluster PO/DPO roles (fixes title inconsistency finding)"),
 "gv-17":("NET-NEW","DOC-11 HP-1: HIPAA accounting of disclosures / DPDP sharing summary"),
 "gv-18":("NET-NEW","DOC-11 HP-3: workforce training & attestation (HIPAA 164.308, NABH)"),
 # G11 Grievance
 "gr-01":("EXTENDS","GR-S1 queue + care-safety dual escalation"), "gr-02":("EXTENDS","GR-S2 wizard + anonymous channel"),
 "gr-03":("EXTENDS","GR-S3 resolution + reopen state"), "gr-04":("NET-NEW","privacy handoff queue (GR↔GV bridge)"),
 "gr-05":("EXTENDS","GR-S3 → patient tracking page"), "gr-06":("NET-NEW","root-cause analytics (Conditional)"),
 # G15 Regulatory
 "ir-01":("EXTENDS","IR-S1 → Form F register"), "ir-02":("EXTENDS","IR-S2 + C-2 validation & cutoff"),
 "ir-03":("EXTENDS","IR-S2 + C-2 receipts & immutability"), "ir-04":("NET-NEW","C-2 corrections/resubmission"),
 "ir-05":("EXTENDS","AD-S11 → AERB compliance register"), "ir-06":("NET-NEW","regulatory calendar"),
 # G1 Identity
 "au-01":("EXTENDS","AU-S7…S13 entry doors → one templated sign-in"), "au-02":("EXTENDS","AU-S1/S4 failure & lockout states"),
 "au-03":("EXTENDS","AU-S2 → 2FA verify step (P2 auth gap)"), "au-04":("EXTENDS","AU-S2 enrolment + backup codes"),
 "au-05":("NET-NEW","P2 lost-authenticator recovery"), "au-06":("EXTENDS","AU-S5 reset + policy"),
 "au-07":("EXTENDS","AU cluster activation flow"), "au-08":("NET-NEW","P2 session lock & shared-terminal switch"),
 "au-09":("EXTENDS","AU-S6 step-up + action matrix"), "au-10":("NET-NEW","workspace chooser & context switch"),
 "au-11":("NET-NEW","my profile, sessions & access history"), "au-12":("NET-NEW","policy re-acceptance gate"),
 "au-13":("NET-NEW","P2 IdP-unreachable degraded mode"), "au-14":("NET-NEW","P2 admin unlock & recovery approvals"),
 "au-15":("NET-NEW","password & MFA policy admin"), "au-16":("EXTENDS","AU-S13 realms → SSO settings"),
 "au-17":("NET-NEW","org-wide sessions & devices"), "au-18":("NET-NEW","service accounts & API keys (foundation)"),
 "au-19":("NET-NEW","DOC-11 ZT-1/ZT-2: device trust, conditional access, JIT elevation"),
 # G4 Scheduling setup
 "sc-01":("EXTENDS","FO-S8 working hours"), "sc-02":("EXTENDS","FO-S8 holidays & closures"),
 "sc-03":("EXTENDS","FO-S8 slot templates"), "sc-04":("EXTENDS","FO-S8 doctor availability"),
 "sc-05":("EXTENDS","FO-S8 equipment availability + maintenance"), "sc-06":("NET-NEW","calendar publish/versioning"),
 "sc-07":("EXTENDS","FO-S8 template flags → overbook/walk-in rules"), "sc-08":("NET-NEW","block booking & camps (Conditional)"),
 "sc-09":("EXTENDS","FO-S9 tokens & queue rules"), "sc-10":("EXTENDS","FO-S9 public display settings"),
 # G13 Integration
 "in-01":("EXTENDS","IN-S1 → connector health board"), "in-02":("EXTENDS","IN-S1 + AD-S11 single-write-surface fix"),
 "in-03":("EXTENDS","RT-S4 unknown-AE → quarantine queue"), "in-04":("NET-NEW","PACS/archive config (scope item #66)"),
 "in-05":("NET-NEW","message browser (scope item #103 baseline)"), "in-06":("NET-NEW","retry/replay console (scope item #103)"),
 "in-07":("EXTENDS","IN-S3 comms providers + expiry alerting"), "in-08":("EXTENDS","IN-S2 printers & peripherals"),
 "in-09":("NET-NEW","webhooks & API clients (Conditional, foundation)"), "in-10":("NET-NEW","edge/offline sync monitor (checklist #12–14)"),
 "in-11":("NET-NEW","DOC-11 AG-1/AG-4: air-gap transfer console (checklist #8)"),
 # G16 Platform
 "pl-01":("EXTENDS","PL cluster → operator home & tenant health"), "pl-02":("EXTENDS","PL-S1 orgs & onboarding"),
 "pl-03":("EXTENDS","PL-S2 + C-4 retention-safe close"), "pl-04":("EXTENDS","PL-S3 plans + impact preview"),
 "pl-05":("EXTENDS","PL-S4 rulebook + diff & rings"), "pl-06":("EXTENDS","PL-S5/S7 support access + revoke"),
 "pl-07":("NET-NEW","platform audit log (tenant-visible mirror)"), "pl-08":("NET-NEW","release & ring management (scope item #143)"),
 "pl-09":("EXTENDS","PL-S6 → backup/DR evidence (RPO/RTO)"), "pl-10":("EXTENDS","PL-S6 → incidents & status page"),
 "pl-11":("NET-NEW","usage metering (scope item #123 minimal)"), "pl-12":("EXTENDS","PL-S5 → operator break-glass dual control"),
 "pl-13":("NET-NEW","DOC-11 AG-3: offline signed update bundles"),
 # G17 Design system
 "ds-01":("NET-NEW","codifies the vendor deck's implicit design system — tokens"), "ds-02":("NET-NEW","component gallery & rules"),
 "ds-03":("NET-NEW","NS-16 SLA/escalation pattern (product-wide)"), "ds-04":("NET-NEW","offline/degraded/sync pattern (checklist #13/#14)"),
 "ds-05":("NET-NEW","empty/loading/error pattern (review §5 gap)"), "ds-06":("NET-NEW","audit & step-up pattern"),
 "ds-07":("NET-NEW","masked identity & privacy pattern (C-7)"), "ds-08":("NET-NEW","form validation & Indian formats"),
 "ds-09":("NET-NEW","print/document template pattern"), "ds-10":("NET-NEW","i18n & localisation pattern"),
 "ds-11":("NET-NEW","navigation & IA map of the full product"),
}

WAVES = {"wave1":["fo","or","cs","tk","rd"],"wave2":["bl","nt","pt","dd"],"wave3":["ad","gv","gr","ir"],"wave4":["au","sc","in","pl","ds"]}
BASE = pathlib.Path("/home/claude/allpack")

def inject():
    done=miss=0
    for wave, prefixes in WAVES.items():
        for f in sorted((BASE/wave).glob("*.html")):
            sid = f.stem
            if sid not in M: print("NO MAP:", sid); miss+=1; continue
            rel, txt = M[sid]
            frag = f.read_text()
            if "Baseline:" in frag: continue  # idempotent
            color = "#0F766E" if rel=="EXTENDS" else "#B45309"
            tag = f'<div class="cluster" style="margin-top:3px;font-weight:700;color:{color}">Baseline: {rel} · {txt}</div>'
            new, n = re.subn(r'(<div class="cluster">[^<]*</div>)', r'\1'+tag, frag, count=1)
            if n: f.write_text(new); done+=1
            else: print("NO ANCHOR:", sid); miss+=1
    print(f"injected {done}, issues {miss}")

if __name__=="__main__" and "inject" in sys.argv: inject()
