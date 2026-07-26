"""Build the Combined Volume (all 235 screens, one HTML) from frozen sources via the normalizer."""
import pathlib
from assemble_group import GROUPS, linkify, title_of, BASE, CSS
from normalize_identity import normalize

ORDER = ["G01_Identity_Access","G02_Patient_Facing","G03_Front_Office_Reception","G04_Scheduling_Setup",
 "G05_Orders_Clinical_Safety","G06_Radiology_Technician","G07_Radiologist_Reading","G08_Doctor_Desk",
 "G09_Billing_Payments","G10_Notifications_Delivery","G11_Grievance_Support","G12_Admin_Master_Data",
 "G13_Integration_Devices","G14_Governance_Compliance","G15_Imaging_Regulatory","G16_Platform_Operator",
 "G17_Design_System_Patterns","G18_Global_Search_Tasks"]

frags, toc_rows, n = [], [], 0
for key in ORDER:
    title, wave, ids = GROUPS[key]
    toc_rows.append(f'<tr><td colspan="2" style="background:#F0FDFA;font-weight:800;color:#0F766E">{title}</td></tr>')
    for sid in ids:
        f = BASE/wave/f"{sid}.html"
        if not f.exists(): continue
        frag = normalize(f.read_text())
        frags.append(linkify(frag, key, same_doc=True)); n += 1
        i,t = title_of(frag)
        toc_rows.append(f'<tr><td class="mono bold"><a href="#{sid}" style="color:#0F766E;text-decoration:none">{i}</a></td><td><a href="#{sid}" style="color:inherit;text-decoration:none">{t}</a></td></tr>')

cover = f'''<section class="screen" id="cover"><div style="padding-top:80px">
<div style="border-left:6px solid #0F766E;padding-left:22px">
<div style="font-size:12px;letter-spacing:.14em;font-weight:800;color:#0F766E;text-transform:uppercase;margin-bottom:10px">MagnusPRO · MVP 1 — Complete Combined Volume · v1.3.1</div>
<h1 style="font-size:36px;font-weight:800">All {n} screens · 18 groups · one document</h1>
<p style="font-size:14px;color:#64748B;margin-top:10px">Every screen with alternate states · shared design system · vendor-baseline crosswalk on every screen · synthetic data only (no PHI)</p></div>
<div class="card" style="max-width:760px;margin-top:26px;max-height:none"><div class="card-title">Table of contents ({n} screens)</div>
<table><tr><th style="width:70px">ID</th><th>Screen</th></tr>{"".join(toc_rows)}</table></div>
<p class="muted small" style="margin-top:14px">Magnus Diagnostics → NUMINACORE · July 2026 · Prototype/reference — not committed product scope.</p></div></section>'''

html = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>MagnusPRO — Complete Combined Volume (v1.3.1)</title><style>{CSS}</style></head><body>{cover}{"".join(frags)}</body></html>'
out = BASE/"out"/"MagnusPRO_MVP1_Complete_Combined_Volume.html"
out.write_text(html)
print(f"combined: {n} screens, {out.stat().st_size//1024}KB")
