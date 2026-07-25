# 03 · The complete design pack (source of truth)
- **`html-source/`** — one small standalone HTML fragment per screen (232 files). Edit one file, rebuild its group; nothing else is touched (D-37 modularity rule).
- **`group-html/`** — assembled per-group packs + the Combined Volume; open in any browser.
- **`design-system/`** — `base.css` (all screens use only these classes) · `assemble_group.py` (GROUPS registry + pack builder) · `baseline_map.py` (vendor crosswalk source; regenerates DOC-08).
- **`group-pdfs/`** — deprecated (D-35).
Screen conventions: scope chip · Baseline line · 2–4 states · audit footer · synthetic data only.
