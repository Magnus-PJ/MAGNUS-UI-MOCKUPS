"""Render group packs as one variable-height PDF page per screen (no mid-screen breaks)."""
import pathlib, re, sys, io
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader

BASE = pathlib.Path("/home/claude/allpack")
CSS = (BASE/"base.css").read_text()
from assemble_group import GROUPS, title_of  # reuse definitions

PAGE_W = 1340  # px

def wrap(fragment_html, title):
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>{title}</title>
<style>{CSS}
body{{background:#fff;width:{PAGE_W}px;margin:0}}
.screen{{page-break-after:auto;min-height:0;padding:26px 34px}}
.frame{{overflow:visible}}
td,th{{word-break:break-word}}
</style></head><body>{fragment_html}</body></html>'''

def cover_html(title, toc_rows, n):
    return wrap(f'''<section class="screen"><div style="padding-top:60px">
<div style="border-left:6px solid #0F766E;padding-left:22px">
<div style="font-size:12px;letter-spacing:.14em;font-weight:800;color:#0F766E;text-transform:uppercase;margin-bottom:10px">Magnus HMS · MVP 1 Complete Design Pack</div>
<h1 style="font-size:36px;font-weight:800">{title}</h1>
<p style="font-size:14px;color:#64748B;margin-top:10px">{n} screens · one page per screen · alternate states included · synthetic data only (no PHI)</p></div>
<div class="card" style="max-width:720px;margin-top:26px"><div class="card-title">Screens in this group</div>
<table><tr><th style="width:80px">ID</th><th>Screen</th></tr>{toc_rows}</table></div>
<p class="muted small" style="margin-top:14px">Magnus Diagnostics → NUMINACORE · July 2026 · Prototype/reference — not committed product scope.</p>
</div></section>''', title)

def render_group(pw, key):
    title, wave, ids = GROUPS[key]
    outdir = BASE/"out"; outdir.mkdir(exist_ok=True)
    browser = pw.chromium.launch(args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": PAGE_W, "height": 1000})
    writer = PdfWriter()
    frags, toc = [], []
    for sid in ids:
        f = BASE/wave/f"{sid}.html"
        if not f.exists(): continue
        frag = f.read_text()
        i, t = title_of(frag)
        toc.append(f'<tr><td class="mono bold" style="color:#0F766E">{i}</td><td>{t}</td></tr>')
        frags.append((sid, frag, t))
    # cover
    page.set_content(cover_html(title, "".join(toc), len(frags)), wait_until="load")
    h = page.evaluate("document.body.scrollHeight")
    pdf = page.pdf(width=f"{PAGE_W}px", height=f"{max(h,900)+20}px", print_background=True)
    for p in PdfReader(io.BytesIO(pdf)).pages: writer.add_page(p)
    # screens — one variable-height page each
    for sid, frag, t in frags:
        page.set_content(wrap(frag, t), wait_until="load")
        h = page.evaluate("document.body.scrollHeight")
        pdf = page.pdf(width=f"{PAGE_W}px", height=f"{h+20}px", print_background=True)
        r = PdfReader(io.BytesIO(pdf))
        # keep only first page (content fits by construction; guard anyway)
        writer.add_page(r.pages[0])
        if len(r.pages) > 1:  # unexpectedly tall — append remainder too
            for p in r.pages[1:]: writer.add_page(p)
    out = outdir/f"Magnus_HMS_{key}.pdf"
    with open(out, "wb") as fh: writer.write(fh)
    browser.close()
    print(f"{key}: {len(frags)} screens -> {len(writer.pages)} pages, {out.stat().st_size//1024}KB")

with sync_playwright() as pw:
    for k in sys.argv[1:]:
        render_group(pw, k)
