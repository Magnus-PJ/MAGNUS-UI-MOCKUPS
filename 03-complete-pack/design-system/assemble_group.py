import pathlib, sys, re, subprocess

BASE = pathlib.Path("/home/claude/allpack")
CSS = (BASE/"base.css").read_text()

GROUPS = {
 "G03_Front_Office_Reception": ("G3 · Front Office & Reception", "wave1", ["fo-%02d"%i for i in range(1,23)]),
 "G05_Orders_Clinical_Safety": ("G5 · Orders & Clinical Safety", "wave1", ["or-%02d"%i for i in range(1,9)]+["cs-%02d"%i for i in range(1,7)]),
 "G06_Radiology_Technician":   ("G6 · Radiology Technician", "wave1", ["tk-%02d"%i for i in range(1,13)]),
 "G07_Radiologist_Reading":    ("G7 · Radiologist — Reading & Reporting", "wave1", ["rd-%02d"%i for i in range(1,19)]),
 # wave2
 "G09_Billing_Payments":       ("G9 · Billing & Payments", "wave2", ["bl-%02d"%i for i in range(1,21)]),
 "G10_Notifications_Delivery": ("G10 · Notifications & Delivery", "wave2", ["nt-%02d"%i for i in range(1,9)]),
 "G02_Patient_Facing":         ("G2 · Patient-Facing (Secure Links)", "wave2", ["pt-%02d"%i for i in range(1,13)]),
 "G08_Doctor_Desk":            ("G8 · Doctor Desk (Referrers)", "wave2", ["dd-%02d"%i for i in range(1,12)]),
 # wave3
 "G12_Admin_Master_Data":      ("G12 · Admin — Org, People & Master Data", "wave3", ["ad-%02d"%i for i in range(1,21)]),
 "G14_Governance_Compliance":  ("G14 · Governance & Compliance", "wave3", ["gv-%02d"%i for i in range(1,17)]),
 "G15_Imaging_Regulatory":     ("G15 · Imaging Regulatory (PC-PNDT / AERB)", "wave3", ["ir-%02d"%i for i in range(1,7)]),
 "G11_Grievance_Support":      ("G11 · Grievance & Support", "wave3", ["gr-%02d"%i for i in range(1,7)]),
 # wave4
 "G01_Identity_Access":        ("G1 · Identity & Access", "wave4", ["au-%02d"%i for i in range(1,19)]),
 "G04_Scheduling_Setup":       ("G4 · Scheduling & Resource Setup", "wave4", ["sc-%02d"%i for i in range(1,11)]),
 "G13_Integration_Devices":    ("G13 · Integration & Devices", "wave4", ["in-%02d"%i for i in range(1,11)]),
 "G16_Platform_Operator":      ("G16 · Platform Operator", "wave4", ["pl-%02d"%i for i in range(1,13)]),
 "G17_Design_System_Patterns": ("G17 · Design System & Patterns", "wave4", ["ds-%02d"%i for i in range(1,12)]),
}

def title_of(frag):
    m = re.search(r'<h1><span class="sid">([^<]+)</span>\s*([^<]+)</h1>', frag)
    return (m.group(1), m.group(2).strip()) if m else ("?","?")

def build(key):
    title, wave, ids = GROUPS[key]
    outdir = BASE/"out"; outdir.mkdir(exist_ok=True)
    frags, toc = [], []
    missing = []
    for sid in ids:
        f = BASE/wave/f"{sid}.html"
        if not f.exists(): missing.append(sid); continue
        frag = f.read_text()
        frags.append(frag)
        i,t = title_of(frag)
        toc.append(f'<tr><td class="mono bold" style="color:#0F766E">{i}</td><td>{t}</td></tr>')
    cover = f'''<section class="screen" id="cover">
<div style="padding-top:120px"><div style="border-left:6px solid #0F766E;padding-left:22px">
<div style="font-size:12px;letter-spacing:.14em;font-weight:800;color:#0F766E;text-transform:uppercase;margin-bottom:10px">Magnus HMS · MVP 1 Complete Design Pack</div>
<h1 style="font-size:36px;font-weight:800">{title}</h1>
<p style="font-size:14px;color:#64748B;margin-top:10px">{len(frags)} screens · every screen with alternate states · shared design system · synthetic data only (no PHI)</p></div>
<div class="card" style="max-width:700px;margin-top:26px"><div class="card-title">Screens in this group</div>
<table><tr><th style="width:70px">ID</th><th>Screen</th></tr>{"".join(toc)}</table></div>
<p class="muted small" style="margin-top:14px">Magnus Diagnostics → NUMINACORE · July 2026 · Prototype/reference — not committed product scope.</p></div></section>'''
    html = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Magnus HMS — {title}</title><style>{CSS}\n@page{{size:A4;margin:0}}@media print{{body{{background:#fff}}}}</style></head><body>{cover}{"".join(frags)}</body></html>'
    hf = outdir/f"Magnus_HMS_{key}.html"; hf.write_text(html)
    print(f"{key}: {len(frags)} screens, missing={missing}, html={hf.stat().st_size//1024}KB")
    import os
    if os.environ.get("MAKE_PDF"):
        pf = outdir/f"Magnus_HMS_{key}.pdf"
        subprocess.run(["/opt/pw-browsers/chromium","--headless","--disable-gpu","--no-sandbox",f"--print-to-pdf={pf}","--no-pdf-header-footer",str(hf)],capture_output=True)

for k in sys.argv[1:]: build(k)
