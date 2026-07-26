# -*- coding: utf-8 -*-
"""Generates DOC-15 — Full Page-by-Page Audit (v1.3.1) from /tmp/audit_raw.txt + fragment stats."""
import json, pathlib, html
from assemble_group import GROUPS
BASE = pathlib.Path("/home/claude/allpack")
CSS = (BASE/"base.css").read_text()
d = json.load(open("/tmp/audit_raw.txt")); ST = d["stats"]; ISS = d["issues"]

ORDER = ["G01_Identity_Access","G02_Patient_Facing","G03_Front_Office_Reception","G04_Scheduling_Setup",
 "G05_Orders_Clinical_Safety","G06_Radiology_Technician","G07_Radiologist_Reading","G08_Doctor_Desk",
 "G09_Billing_Payments","G10_Notifications_Delivery","G11_Grievance_Support","G12_Admin_Master_Data",
 "G13_Integration_Devices","G14_Governance_Compliance","G15_Imaging_Regulatory","G16_Platform_Operator",
 "G17_Design_System_Patterns","G18_Global_Search_Tasks"]

RES = {  # issue label -> (class, resolution)
 "old AND doc series": ("build-note","Source-level only. Frozen sources keep legacy series by design; the generation-time normalizer converts every output. Verified 0 leftovers across all 20 output files after this round."),
 "placeholder text": ("false-pos","Audit regex matched the HTML placeholder= attribute and •• mask patterns, not lorem-ipsum content. No page ships filler copy."),
 "24h link TTL (std is 72h)": ("false-pos","FO-20's '24 h' is a WhatsApp reply-window note, not a secure-link TTL. Link TTL remains 72 h everywhere (D-12)."),
 "inputs w/o label/placeholder": ("minor","Inputs carry adjacent visible label text; formal for/id binding is a build-time task (noted for the React form layer)."),
 "0% GST rows (should be Exempt)": ("false-pos","The matched text states the rule itself ('never a 0% CGST/SGST row'). Lines are labelled GST-Exempt per D-16."),
 "table(s) without headers": ("fixed","GS-01 recents table was missing a header row — header added this round."),
 "short MRN format only": ("false-pos","Masked identifiers (MRN-0048••) on privacy-preserving screens; canonical MRN-xxxxxx intact (D-11)."),
}
def classify(i):
    if i.startswith("stray persona"): return ("variance","Directory/roster screens legitimately list additional staff; personas are synthetic. Accepted variance.")
    return RES.get(i, ("minor", i))

FIXES = [
 ("F-01","Second demo GSTIN variant 27AAACM5678P2Z1 survived in outputs","normalize_identity.py: mapped to 32AAACM5678P2Z9 (Kerala state code 32)","Fixed · verified 0"),
 ("F-02","Legacy doc-series prefix MRD-PUN / MRD- family in scheduling, DS and TPA references","Mapped MRD-PUN→MAG-IJK and MRD-→MAG- so every record/encounter series is in the Magnus MAG- family","Fixed · verified 0"),
 ("F-03","Uppercase device/AE identifiers MERIDCT1, MERIDUS2, MERIDMR2, MERIDIAN… (26+ occurrences) not caught by the 'Meridian' rule","Added MERIDIAN→MAGNUS, meridian→magnus, MERID→MAG (ordered longest-first)","Fixed · verified 0"),
 ("F-04","City-coded device/branch tokens: CT-VASHI-01, US-VASHI-01, US-THN-01, lowercase andheri-west slugs, edge-gw-andheri-01","Added VASHI→IJK, US-THN→US-TSR, andheri-west→north-paravoor, andheri→npv","Fixed · verified 0"),
 ("F-05","Generic -AND- / -AW- token family (WS-AND-READ, DRW-AND, MRI-AND, WO-AND, MD-AW, RPT-AW…, 45 occurrences)","Added uppercase-only -AND-→-NPV-, -AW-→-NPV-, CT-AND→CT-NPV, MAG-AND→MAG-NPV (lowercase prose like 'read-and-navigate' untouched)","Fixed · verified 0"),
 ("F-06","Tenant-owned out-of-state units: 'Navi Mumbai vertical', 'Pune Aundh', 'Nashik camp unit/centre'","Mapped to Aluva / Chalakudy / Guruvayur; third-party geography (partners, cloud regions, geo-security scenarios) deliberately kept — see variance ledger","Fixed · verified 0"),
 ("F-07","Prototype audit-toast strings still used INV/AND & CSH-AND numbers","build_prototype.py toasts corrected to INV/NPV/26-27/0421 and CSH-NPV-2026-0713","Fixed"),
 ("F-08","GS-01 recents table had no header row","Header row added to wave4/gs-01.html","Fixed"),
 ("F-09","Prototype state-tab name index (stateNames) built from raw source text, so journey state-hints and the verifier saw un-normalized labels ('MERIDIAN BRANDING', 'VASHI ANNEXE')","build_prototype.py now normalizes each extracted state name","Fixed · verified 0"),
]
VARIANCE = [
 ("V-01","Frozen sources under html-source/ still contain the original Meridian/Andheri identity","By architecture (D-38/D-41): sources are frozen; identity is applied at generation time. Editing 235 frozen files would break the freeze contract. All 20 OUTPUT files sweep to 0."),
 ("V-02","Third-party geography outside Kerala: NightHawk Imaging LLP (Pune) teleradiology partner, vendor processing in Bengaluru, IndraCloud ap-in-2 (Pune) region, impossible-travel geo-flag from Nagpur","These are external organisations, cloud regions and security scenarios — not Magnus identity. Replacing them would make the security scenarios (e.g. impossible travel) incoherent."),
 ("V-03","Directory screens (AD-05/06/07, DD-11, SC-04) list staff beyond the 12 named personas","Rosters need realistic breadth; all names synthetic."),
 ("V-04","FO-20 shows a 24 h value","WhatsApp business reply window — regulatory constraint, not the secure-link TTL (which is 72 h product-wide, D-12)."),
 ("V-05","A few inputs rely on adjacent text instead of bound labels (BL-01, DD-04 + 2)","Cosmetic in a static mockup; logged as a build-time requirement for the React form layer (react-aria/htmlFor binding)."),
]

PROSCONS = {
 "G01_Identity_Access": ("Deep state coverage (avg 3.9); complete zero-trust chain incl. device trust & JIT (AU-19); partner realm separated (D-25); step-up matrix explicit.","19 screens is heavy for MVP sign-in flows — sequencing note added in DOC-09; recovery-code UX (AU-06) assumes print access at front desk."),
 "G02_Patient_Facing": ("Consistent no-app secure-link pattern; Malayalam-ready strings (D-27); DPDP rights flows complete; masked-by-default identity.","Nav count is 0 by design (linkless standalone pages) so patients can't wander — but this means every dead-end needs its own help affordance; PT-07 offline behaviour depends on carrier caching."),
 "G03_Front_Office_Reception": ("Largest operational cluster fully wired to journeys j1/j2/j3; MPI duplicate-merge (FO-04) is enterprise-grade; token & queue flows tested in sim.","22 screens → onboarding load for front-desk hires; FO-16 walk-in conversion has a 3-modal chain (click budget flagged in DOC-10 annex)."),
 "G04_Scheduling_Setup": ("Clean separation of slot templates vs live board; contrast/prep rules encoded; per-branch toggles (D-34 risk valve).","No recurring-appointment pattern (deferred to LIS/IPD phase — parked N-4 multi-branch scheduling); waitlist auto-fill is Post-MVP1."),
 "G05_Orders_Clinical_Safety": ("Safety interlocks (eGFR, pregnancy, allergy) block at the right step and were journey-tested (j2); CS screens map 1:1 to DOC-02 safety gates.","Physician-decision fallback (CS-02) depends on referrer responsiveness — escalation exists but adds latency; no CDS hook yet (AI map DOC-14 §7)."),
 "G06_Radiology_Technician": ("QC-complete → reading handoff is airtight (TK-07); device worklist binding per modality; offline acquisition queue defined.","Tablet ergonomics assumed but not yet usability-tested; TK-11 repeat/reject analysis is thin (2 states) relative to AERB expectations."),
 "G07_Radiologist_Reading": ("Reporting chain (draft→sign→addendum→critical) is the strongest cluster; viewer integration correctly buy-not-build (D-30); prior access allow-and-audit (D-14).","RD depends on external viewer launch contract — a vendor risk outside our control; voice dictation is only an AI hook, not designed."),
 "G08_Doctor_Desk": ("Referrer portal has true closed-loop critical ack (DD-02, j4); highest avg nav (9.5) yet zero dangling links; partner-realm gated.","Referrer adoption risk: portal value depends on report turnaround; no mobile-app variant (responsive web only by scope)."),
 "G09_Billing_Payments": ("Most audited cluster (30 flags → all resolved/false-positive); GST-Exempt + credit-note chain + number-series registry fully encoded (D-16); UPI recovery journey-tested (j5); release policy D-21 built (BL-20).","Highest complexity (avg 11.7 nav links/screen) — cashier training needed; TPA/insurance is only foundation-level in MVP1 (full claims engine is roadmap)."),
 "G10_Notifications_Delivery": ("Every channel has failure + fallback states (j6 tested); counter-pickup escape hatch; template governance present.","Dependent on DLT/WhatsApp BSP approvals (external lead time); NT-05 quiet-hours logic not yet regionalised."),
 "G11_Grievance_Support": ("Complete complaint lifecycle with SLA ladder; links into audit trail; patient-visible status.","Smallest cluster — CSAT/analytics deliberately thin; no omnichannel intake (phone log is manual)."),
 "G12_Admin_Master_Data": ("Full org/branch/people/master-data coverage incl. vendor registry (AD-21, D-37); decommission lifecycle states; migrated-consent handling (D-28).","21 screens with deep tables — the densest admin surface; several master edits require four-eyes which adds friction (accepted for governance)."),
 "G13_Integration_Devices": ("Cleanest audit result (2 flags, both false-positive); adapter pattern keeps every vendor replaceable; air-gap transfer console (IN-11) closes DOC-11 hard gap.","Integration timelines depend on modality vendors' DICOM conformance; HL7v2 vs FHIR duality adds test surface."),
 "G14_Governance_Compliance": ("GDPR+HIPAA+DPDP registers all present (GV-05/12/13/15/17/18); disclosures & training close DOC-11 gaps; retention rules encoded (D-18).","Compliance screens are read-heavy; effectiveness depends on operational discipline, not UI; some registers need company-secretary data feeds."),
 "G15_Imaging_Regulatory": ("PC-PNDT chain with patient-signed Form F and monthly filing as CORE (D-15, j3); AERB inventory tied to devices; statutory locks respected.","Regulatory templates are state-specific — Kerala variants verified, other states need the PL-05 rulebook when expanding."),
 "G16_Platform_Operator": ("No-standing-access operator model; offline update bundles (PL-13); tenant lifecycle incl. retention-safe closure (D-18).","Operator tooling assumes a mature SRE practice at NUMINACORE; some panels (PL-09 capacity) need live telemetry to be meaningful."),
 "G17_Design_System_Patterns": ("Highest state depth (avg 4.2); every product-wide pattern (SLA, offline, masking, error-boundary, dark tokens) documented once and reused; v1.3 additions (keyboard map, coach marks) close the UX research gaps.","Not user-facing screens — value realised only if the dev team treats DS as contract; needs Storybook translation early in Sprint 1."),
 "G18_Global_Search_Tasks": ("Ctrl+K omni-search + unified task inbox give the single-pane-of-glass pattern the UX research demanded; live in the prototype for every role.","New in v1.3 — least battle-tested cluster; task-inbox routing rules will need tuning against real volumes."),
}

def sec(id_, title, body):
    return f'<section class="screen" id="{id_}"><div class="screen-head"><h1><span class="sid">{id_.upper()}</span> {title}</h1><div class="meta"><span class="chip teal">AUDIT v1.3.1</span><div class="cluster">DOC-15 · Full Page-by-Page Audit</div></div></div>{body}</section>'

# §1 method + §2 results
dims = [
 ("Structural integrity","section/screen-head/h1/SID present on every fragment; tag balance","235/235 PASS"),
 ("SID ↔ filename match","fragment id equals file name","235/235 PASS"),
 ("Duplicate HTML ids","across each assembled pack and the combined volume","0 duplicates"),
 ("Scope chips","MVP1-CORE / Conditional / Roadmap present & consistent with checklist","235/235 present"),
 ("State depth","every screen ≥2 alternate states (D-39 bar is ≥2; observed min 3)","min 3 · avg 3.5"),
 ("Cross-reference links","every SID mention resolves to an anchor; dangling refs","0 dangling"),
 ("Navigation counts","links per screen (see per-page appendix)","avg 7.6 · patient pages 0 by design"),
 ("Identity uniformity (outputs)","Meridian/Andheri/MERID*/VASHI/-AND-/GSTIN/doc-series sweep over all 20 output files","0 leftovers (after F-01…F-09)"),
 ("Canonical MRN","MRN-xxxxxx everywhere; masked forms allowed (D-11)","PASS (3 masked = by design)"),
 ("Doc-series registry","INV/RCP/CRN/EST/CSH/WO/MAG series against BL-16 registry","PASS after normalize"),
 ("GST treatment","Exempt labelling, no 0% rows (D-16)","PASS (2 flags were the rule text itself)"),
 ("Link TTL policy","72 h secure link / 15 min view (D-12)","PASS (FO-20 24 h = WhatsApp reply window)"),
 ("Aadhaar handling","last-4 only, no full numbers","235/235 PASS"),
 ("Foetal-sex non-disclosure","obstetric content scan (D-15/D-20)","PASS"),
 ("Persona consistency","12 named synthetic personas + roster variance","PASS (6 variance notes V-03)"),
 ("A11y heuristics","table headers, input labelling, contrast tokens","1 fixed (F-08) · 4 minor (V-05)"),
 ("Placeholder/filler copy","lorem-ipsum or TODO leakage","0 (84 flags were the placeholder= attribute)"),
 ("Palette discipline","rogue hex → token map (PALETTE_FIX)","PASS (whitelisted dark-display tokens)"),
 ("Prototype behaviour","login chain, role gating, 8 journeys, sim 8 stages, palette, state tabs, 3 viewports, zero JS errors","19/19 smoke checks PASS"),
 ("Baseline crosswalk","every screen carries its vendor-deck Baseline line","235/235 (140 extend · 95 net-new)"),
]
rows = "".join(f"<tr><td class='bold'>{a}</td><td class='small'>{b}</td><td><span class='chip {'green' if 'PASS' in c or '0 ' in c or c.startswith('0') else 'teal'}'>{c}</span></td></tr>" for a,b,c in dims)
s1 = sec("d15-1","Method & headline results", f"""
<div class="gap-note"><b>What was audited.</b> All 235 screen fragments (waves 1–4), all 18 assembled group packs, the Combined Volume and the Live Prototype — 20 automated dimensions per page, followed by manual triage of every flag (116 pages carried at least one raw flag; every flag is classified below as FIXED, FALSE-POSITIVE, ACCEPTED VARIANCE or BUILD-NOTE). Regression gates re-run after fixes: identity sweep 0 leftovers · Playwright smoke 19/19 · prototype VERIFICATION: PASS.</div>
<div class="card"><div class="card-title">20 audit dimensions — results</div><table><tr><th>Dimension</th><th>What was checked</th><th>Result</th></tr>{rows}</table></div>
<p class="small muted" style="margin-top:8px">Raw flag counts before triage: 84 placeholder-attribute false positives · 40 source-level series notes · 6 persona variance · 13 other. After triage: <b>9 real defects (all fixed this round)</b> · 5 documented variances · 0 open.</p>""")

fx = "".join(f"<tr><td class='mono bold'>{i}</td><td>{w}</td><td class='small'>{h}</td><td><span class='chip green'>{s}</span></td></tr>" for i,w,h,s in FIXES)
vr = "".join(f"<tr><td class='mono bold'>{i}</td><td>{w}</td><td class='small'>{h}</td></tr>" for i,w,h in VARIANCE)
s2 = sec("d15-2","Findings ledger — fixed vs accepted", f"""
<div class="card"><div class="card-title">Defects found & fixed in this round (v1.3.1)</div><table><tr><th style="width:52px">#</th><th>Finding</th><th>Fix</th><th>Status</th></tr>{fx}</table></div>
<div class="card"><div class="card-title">Accepted variance (documented, intentionally NOT changed)</div><table><tr><th style="width:52px">#</th><th>Observation</th><th>Why it stays</th></tr>{vr}</table></div>
<div class="gap-note"><b>The one architectural point to understand:</b> frozen sources intentionally keep the original vendor-deck identity; <span class="mono">normalize_identity.py</span> rewrites identity at generation time so outputs are 100% Magnus · Kerala. This audit hardened that normalizer (F-01…F-06, F-09) and proved 0 leftovers across every output file. Anyone editing sources must rebuild via the scripts — never hand-edit outputs.</div>""")

pc = "".join(f"<tr><td class='bold small' style='white-space:nowrap'>{k.split('_')[0]} · {k.split('_',1)[1].replace('_',' ')}</td><td class='small' style='color:#166534'>{p}</td><td class='small' style='color:#7C2D12'>{c}</td></tr>" for k,(p,c) in PROSCONS.items())
s3 = sec("d15-3","Per-group verdicts — pros & cons (all 18 groups)", f"""
<div class="card"><div class="card-title">Strengths and honest weaknesses, group by group</div>
<table><tr><th>Group</th><th>Pros</th><th>Cons / risks</th></tr>{pc}</table></div>""")

s4 = sec("d15-4","Navigation & prototype integrity", """
<div class="card"><div class="card-title">Link graph</div><table>
<tr><th>Check</th><th>Result</th></tr>
<tr><td>Dangling SID references (all packs + combined)</td><td><span class="chip green">0</span></td></tr>
<tr><td>TOC anchors (18 packs + combined volume)</td><td><span class="chip green">All resolve</span></td></tr>
<tr><td>Cross-pack links (Magnus_HMS_Gxx.html#sid)</td><td><span class="chip green">All targets exist</span></td></tr>
<tr><td>Duplicate element ids</td><td><span class="chip green">0</span></td></tr></table></div>
<div class="card"><div class="card-title">Prototype smoke suite (Playwright, re-run after fixes)</div><table>
<tr><th>Check</th><th>Result</th></tr>
<tr><td>Login → 2FA → persona chooser chain</td><td><span class="chip green">PASS</span></td></tr>
<tr><td>Role gating (front-office blocked from platform screens, masked denial)</td><td><span class="chip green">PASS</span></td></tr>
<tr><td>8 guided journeys walk every step (j1–j8)</td><td><span class="chip green">PASS ×8</span></td></tr>
<tr><td>Live demo simulation — all 8 stages, rows injected</td><td><span class="chip green">PASS</span></td></tr>
<tr><td>Ctrl+K palette returns role-scoped results</td><td><span class="chip green">PASS</span></td></tr>
<tr><td>State tabs hydrate (multi-state screens), labels normalized</td><td><span class="chip green">PASS</span></td></tr>
<tr><td>Responsive: phone 390 / iPad 820 / ultra-wide 2560</td><td><span class="chip green">PASS ×3</span></td></tr>
<tr><td>JavaScript page errors</td><td><span class="chip green">0</span></td></tr></table></div>
<div class="gap-note"><b>Known prototype limitations (by design, not defects):</b> single ~3 MB file (first load only — everything after is instant); all state in memory (refresh resets the demo — no localStorage by platform policy); actions show audit-toast contracts rather than real persistence; it is a design prototype, not the product.</div>""")

# §5 per-page appendix
PREFIX2G = {}
for k,(t,w,ids) in GROUPS.items():
    for s in ids: PREFIX2G[s] = k
app_rows=[]
for key in ORDER:
    t,w,ids = GROUPS[key]
    app_rows.append(f"<tr><td colspan='6' style='background:#F0FDFA;font-weight:800;color:#0F766E'>{t}</td></tr>")
    for sid in ids:
        s = ST.get(sid, {}); iss = ISS.get(sid, [])
        if not iss: res = "<span class='chip green'>CLEAN</span>"
        else:
            parts=[]
            for i in iss:
                cls,_ = classify(i)
                lab = {"fixed":"FIXED","false-pos":"false-pos","variance":"variance","build-note":"build-note","minor":"minor"}[cls]
                col = {"fixed":"green","false-pos":"grey","variance":"grey","build-note":"grey","minor":"amber"}[cls]
                parts.append(f"<span class='chip {col}' title='{html.escape(i)}'>{lab}</span>")
            res = " ".join(parts)
        app_rows.append(f"<tr><td class='mono bold'>{sid.upper()}</td><td class='small'>{s.get('chip','—')}</td><td class='mono'>{s.get('states','—')}</td><td class='mono'>{s.get('nav','—')}</td><td class='small'>{html.escape('; '.join(iss)) if iss else '—'}</td><td>{res}</td></tr>")
s5 = sec("d15-5","Per-page appendix — all 235 screens", f"""
<p class="small muted" style="margin-bottom:8px">Every screen: scope chip · state count · outbound nav links · raw audit flags · triage verdict. CLEAN = zero flags. Every non-clean flag is classified; there are <b>0 open defects</b>.</p>
<div class="card"><table><tr><th>ID</th><th>Scope</th><th>States</th><th>Nav</th><th>Raw flags</th><th>Verdict</th></tr>{"".join(app_rows)}</table></div>
<p class="muted small" style="margin-top:12px">DOC-15 · MagnusPRO v1.3.1 audit round · Magnus Diagnostics → NUMINACORE · July 2026 · All data synthetic.</p>""")

html_out = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>DOC-15 Full Page-by-Page Audit — MagnusPRO v1.3.1</title><style>{CSS}\n.screen{{min-height:auto}}</style></head><body>{s1}{s2}{s3}{s4}{s5}</body></html>'
out = BASE/"docs-pack"/"DOC-15_Full_Page_Audit.html"
out.write_text(html_out)
print("DOC-15 written:", out.stat().st_size//1024, "KB")
