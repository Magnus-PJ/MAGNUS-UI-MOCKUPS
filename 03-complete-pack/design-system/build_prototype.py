"""MagnusPRO Live Prototype generator — single navigable HTML from the frozen 232-screen baseline.
Phases A+B: router, login flow, role-scoped nav, state tabs, wired primary actions, 8 guided journeys."""
import pathlib, re, json, html as H
from normalize_identity import normalize

BASE = pathlib.Path("/home/claude/allpack")
CSS = (BASE/"base.css").read_text()

# ---------------- load & split screens ----------------
WAVES = ["wave1","wave2","wave3","wave4"]
screens = {}
for w in WAVES:
    for f in sorted((BASE/w).glob("*.html")):
        src = f.read_text()
        sid = f.stem
        m = re.search(r'<span class="sid">([^<]+)</span>\s*([^<]+)</h1>', src)
        title = normalize(m.group(2).strip().replace("&amp;","&"))
        inner = normalize(src[src.find(">", src.find("<section"))+1 : src.rfind("</section>")])
        names = ["DEFAULT"] + [re.sub(r"<[^>]+>","",x).strip() for x in re.findall(r'<div class="state-tag">(.*?)</div>', src, re.S)]
        screens[sid] = dict(title=title, inner=inner, names=names)

VALID = set(screens)

# ---------------- linkify refs to router ----------------
def linkify(html_text):
    def sub(m):
        sid = f"{m.group(1)}-{m.group(2)}".lower()
        if sid in VALID:
            return f'<a href="#/{sid}" class="xref">{m.group(0)}</a>'
        return m.group(0)
    out=[]
    for part in re.split(r'(<[^>]+>)', html_text):
        out.append(part if part.startswith("<") else re.sub(r'\b([A-Z]{2})-(\d{2})\b', sub, part))
    return "".join(out)

# ---------------- role model (from DOC-03) ----------------
ROLES = {
 "frontoffice": dict(label="Front Office (D. Nair)", home="fo-01",
   groups=["fo","or","cs","nt","gr","sc","pt"], note="Reception & scheduling"),
 "technologist": dict(label="Technologist (T. Okafor)", home="tk-01", groups=["tk","or","cs","in"], note="Acquisition & safety"),
 "radiologist": dict(label="Radiologist (Dr. V. Shetty)", home="rd-01", groups=["rd","tk","cs"], note="Reading & reporting"),
 "referrer": dict(label="Referring Doctor (Dr. Meera Nair)", home="dd-01", groups=["dd"], note="Partner realm — assigned patients only"),
 "cashier": dict(label="Cashier (P. D'Souza)", home="bl-01", groups=["bl"], note="Billing & payments"),
 "branchadmin": dict(label="Branch Admin (K. Verma)", home="ad-13", groups=["ad","sc","in","au","nt","gr"], note="Branch operations"),
 "orgadmin": dict(label="Org Admin (K. Verma)", home="ad-01", groups=["ad","au","sc","in","bl","nt","gr","ir"], note="Organisation-wide"),
 "privacy": dict(label="Privacy Officer (Dr. A. Rao)", home="gv-01", groups=["gv","gr","ir","ad"], note="Governance & compliance"),
 "operator": dict(label="Platform Operator (R. Iyer)", home="pl-01", groups=["pl","in","ds"], note="NUMINACORE console"),
 "patient": dict(label="Patient (secure link)", home="pt-01", groups=["pt"], note="No account — OTP link"),
}
GROUP_NAMES = {"au":"Identity","pt":"Patient links","fo":"Front Office","sc":"Scheduling","or":"Orders","cs":"Clinical Safety",
 "tk":"Technician","rd":"Reading","dd":"Doctor Desk","bl":"Billing","nt":"Notifications","gr":"Grievance","ad":"Admin",
 "in":"Integration","gv":"Governance","ir":"Regulatory","pl":"Platform","ds":"Design System"}

# ---------------- wired primary actions ----------------
# sid -> [ [label_regex, target_route, toast], ... ]  target "#/sid" or "#/sid@statehint"
ACTIONS = {
 "fo-02": [["register new patient","#/fo-03","Starting registration"]],
 "fo-03": [["continue","#/fo-04","Demographics saved (draft)"]],
 "fo-04": [["create distinct|use existing","#/fo-05","Duplicate review recorded"]],
 "fo-05": [["record consent|finish","#/or-01","Consent recorded · notice v3"]],
 "fo-13": [["issue token|check in","#/fo-01","Token issued · U-018 · queue position 3"]],
 "fo-15": [["place order|pay|token|next|continue","#/bl-03","Fast-track step completed"]],
 "or-01": [["place order","#/or-02","Checking duplicates & safety…"]],
 "or-02": [["continue|create distinct|acknowledge","#/cs-01","Order placed · ACC-2026-90241"]],
 "cs-01": [["complete screening","#/tk-01","Screening decision recorded"],["request.*override|physician","#/cs-04","Override request sent to physician"]],
 "cs-04": [["grant|approve","#/tk-01","Override granted — time-boxed, audited"]],
 "cs-06": [["complete form f","#/tk-01","Form F completed · FF-2026-00341"]],
 "tk-01": [["perform","#/tk-02","Study started — identity verified"]],
 "tk-02": [["mark acquired|release","#/rd-01","Study released to reading"]],
 "tk-06": [["record|save","#/tk-02","Contrast administration recorded · lot OK"]],
 "rd-01": [["open next|resume|open in viewer","#/rd-03","Opening study in viewer"]],
 "rd-03": [["start report","#/rd-07","Report draft opened"]],
 "rd-07": [["proceed to sign|sign-off","#/rd-08","Running pre-sign checks"]],
 "rd-08": [["proceed to sign","#/rd-09","All checks reviewed"]],
 "rd-09": [["sign report|sign & finalize|final & immutable","#/rd-13","Report signed — immutable · hash stored"],["flag|critical","#/rd-10","Critical flag flow"]],
 "rd-10": [["send now|create notification","#/rd-11","Critical notification dispatched · RED tier"]],
 "rd-11": [["record acknowledgement","#/dd-02","Awaiting referrer acknowledgement"]],
 "rd-12": [["sign addendum","#/rd-13","Addendum signed · recipients re-notified"]],
 "bl-02": [["issue","#/bl-03","Invoice issued · INV/AND/26-27/0421"]],
 "bl-03": [["confirm|collect|received","#/bl-05","Payment received · receipt issued"],["upi|qr","#/bl-04","UPI initiated — awaiting confirmation"]],
 "bl-04": [["mark as received|evidence","#/bl-08","Evidence submitted — approval requested"],["check with provider","#/bl-04","Provider re-query: still pending"]],
 "bl-05": [["reprint","#/bl-05","DUPLICATE COPY printed — logged"]],
 "bl-06": [["submit|process refund","#/bl-08","Refund sent for approval"]],
 "bl-08": [["approve","#/bl-05","Approved — requester notified"]],
 "bl-09": [["sign & close|close day","#/bl-18","Day closed · CSH-AND-2026-0713"]],
 "bl-20": [["release","#/rd-13","Report released to patient channels"]],
 "nt-02": [["fix contact|resend","#/fo-07","Contact update flow (OTP-verified)"],["mark collected","#/gv-17","Pickup recorded — disclosure logged"]],
 "fo-07": [["save contact|resend","#/nt-01","Contact verified · link re-issued"]],
 "pt-01": [["continue to verify","#/pt-01@VERIF","OTP sent to ••••4821"],["view my report","#/pt-02","Code verified"]],
 "pt-02": [["pay","#/pt-06","Opening secure payment"]],
 "pt-06": [["pay ₹|upi|card","#/pt-02","Payment successful — report unlocked"]],
 "pt-09": [["submit","#/pt-10","Request submitted · DPDP-CR-00318 · 30-day clock started"]],
 "gv-04": [["execute|approve","#/gv-04@PARTIAL","Deletion executed where lawful — letter generated"]],
 "dd-02": [["acknowledge","#/rd-11","Acknowledgement recorded · loop closed"]],
 "dd-03": [["place order","#/or-02","Order sent — duplicate check running"]],
 "au-01": [["continue|sign in","#/au-03","Password accepted"]],
 "au-03": [["verify|view","#/choose","Second factor verified"]],
 "in-10": [["replay|resolve","#/in-10","Queued actions replayed — 0 conflicts"]],
 "ir-02": [["generate|validate","#/ir-03","Submission file generated"]],
 "ir-03": [["submit|record","#/ir-03","Submission recorded — awaiting acknowledgement"]],
}

# ---------------- journeys ----------------
JOURNEYS = [
 dict(id="j1", title="Walk-in X-ray → cash → report delivered", role="frontoffice", steps=[
  ["fo-02","","Search first — no match found for this walk-in"],["fo-03","","Register demographics"],
  ["fo-05","","Capture consent (notice v3, language-aware)"],["or-01","","Create the X-ray order"],
  ["bl-03","","Collect cash — receipt from series"],["fo-13","","Check in & issue token"],
  ["tk-01","","Technologist sees gates all-clear → Perform"],["tk-02","","Acquire & release to reading"],
  ["rd-07","","Radiologist drafts the report"],["rd-09","","Sign — immutable, hash stored"],
  ["rd-13","","Signed report with distribution panel"],["nt-01","","Delivery ledger: SMS link sent ✓"]]),
 dict(id="j2", title="Contrast CT — eGFR unavailable → physician decision", role="frontoffice", steps=[
  ["or-01","","Order contrast CT"],["or-02","","Safety interception fires"],
  ["cs-01","eGFR","No eGFR on file — point-of-care or physician acceptance"],
  ["cs-04","","Physician reviews & decides (never technologist self-override)"],
  ["tk-01","","Gate now green → Perform"],["tk-06","","Contrast administration record (lot/batch)"]]),
 dict(id="j3", title="Obstetric US — Form F statutory chain", role="frontoffice", steps=[
  ["or-01","","Order obstetric ultrasound"],["cs-06","","Form F with the patient's signed undertaking"],
  ["tk-01","","Worklist shows Form F gate satisfied"],["rd-07","REGULATED","Regulated template — locked sections"],
  ["rd-09","DECLARATION","Explicit non-disclosure declaration at sign"],["ir-01","","Form F register"],
  ["ir-02","","Monthly submission prep — validation green"],["ir-03","","Submit & capture acknowledgement"]]),
 dict(id="j4", title="STAT critical bleed — closed loop", role="radiologist", steps=[
  ["rd-01","","STAT study tops the queue"],["rd-03","","Read with same-org priors loaded"],
  ["rd-09","CRITICAL","Keyword prompt: flag as critical before signing"],["rd-10","","RED tier — 15-min ack window"],
  ["rd-11","","Escalation ladder live — owner + audible"],["dd-02","","Referrer acknowledges in-product"],
  ["rd-11","CLOSED","Loop closed with full audit"]]),
 dict(id="j5", title="UPI stuck → evidence recovery", role="cashier", steps=[
  ["bl-03","UPI","UPI initiated — QR shown"],["bl-04","","Timeout: UNCONFIRMED — never retry blindly"],
  ["bl-04","EVIDENCE","UTR evidence + supervisor approval"],["bl-08","","Async approval queue"],
  ["bl-05","","Receipt issued after confirmation"]]),
 dict(id="j6", title="Report never arrived → counter pickup", role="frontoffice", steps=[
  ["nt-01","","Delivery ledger shows FAILED"],["nt-02","","Failure worklist — fix & resend or counter"],
  ["fo-07","","OTP-verified phone correction"],["nt-02","PICKUP","ID-verified counter handover"],
  ["gv-17","","Disclosure register updated"]]),
 dict(id="j7", title="DPDP deletion — partial completion", role="patient", steps=[
  ["pt-09","","Patient submits deletion request"],["pt-10","","Honest tracking with 30-day SLA"],
  ["gv-04","","Assessment: what deletes vs retention-held"],["gv-07","","Legal hold citation"],
  ["gv-04","PARTIAL","Partial-completion letter to patient"]]),
 dict(id="j8", title="Branch offline 3h → clean sync", role="frontoffice", steps=[
  ["fo-01","OFFLINE","Offline banner — actions queue locally"],["fo-15","","Walk-in continues offline"],
  ["bl-03","","Cash accepted offline — UPI blocked in offline mode (default state shows cash tender)"],["in-10","","Sync monitor: replay queued actions"],
  ["fo-01","","Back online — zero lost work"]]),
]

# ---------------- render screen templates ----------------
def render_screen(sid):
    s = screens[sid]
    return f'<div class="scr" id="scr-{sid}" style="display:none" data-sid="{sid}">{linkify(s["inner"])}</div>'

ALL = "".join(render_screen(sid) for sid in sorted(screens))

DENIAL = '''<div class="scr" id="scr-denied" style="display:none"><div class="screen-head"><h1><span class="sid">ACCESS</span> Not available to your role</h1><div class="meta"><span class="chip red">DENIED — RECORDED</span></div></div>
<div class="card" style="max-width:560px;margin:30px auto;text-align:center"><div class="card-title">🔒 Record #MRN-••••·· — no access</div>
<p style="font-size:13px">Your current role doesn't include this workspace. Nothing was shown; this attempt is recorded (DS-07 masking pattern). Request access via DD-06 / AD-05, or switch user.</p>
<p style="margin-top:10px"><a class="btn primary" href="#/choose">Switch user</a></p></div></div>'''

CHOOSER_CARDS = "".join(
 f'''<div class="card pcard" onclick="setRole('{k}')"><div class="card-title">{v["label"]}</div><p class="muted small">{v["note"]}</p><span class="chip teal">{len([s for s in screens if s.split("-")[0] in v["groups"]])} screens</span></div>'''
 for k,v in ROLES.items())
CHOOSER = f'''<div class="scr" id="scr-choose" style="display:none"><div class="screen-head"><h1><span class="sid">AU-10</span> Choose your workspace</h1><div class="meta"><span class="chip teal">SIMULATED SESSION</span><div class="cluster">Signed in · session recorded</div></div></div>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin-top:14px">{CHOOSER_CARDS}</div></div>'''

DATA = json.dumps({
 "roles": ROLES, "groups": GROUP_NAMES,
 "titles": {sid: screens[sid]["title"] for sid in screens},
 "stateNames": {sid: screens[sid]["names"] for sid in screens},
 "actions": ACTIONS, "journeys": JOURNEYS,
})

JS = r"""
const D = __DATA__;
let role=null, journey=null, jstep=0, auditN=88214;
const $=q=>document.querySelector(q), $$=q=>document.querySelectorAll(q);
function toast(msg){const t=document.createElement('div');t.className='toastx';t.innerHTML='🔒 '+msg+' · <span class="mono">AUTH-'+(auditN++)+'</span>';document.body.appendChild(t);setTimeout(()=>t.remove(),3200);}
function allowed(sid){if(!role)return false;if(role&&D.roles[role].groups.includes(sid.split('-')[0]))return true;return false;}
function show(id){$$('.scr').forEach(e=>e.style.display='none');const el=document.getElementById(id);if(el){el.style.display='block';const sid=el.dataset&&el.dataset.sid;if(sid){hydrate(sid);simInject(sid);}}window.scrollTo(0,0);}
const hydrated={};
function hydrate(sid){if(hydrated[sid])return;const scr=document.getElementById('scr-'+sid);const kids=[...scr.children];
 const groups=[[]];const names=['Default'];
 for(const el of kids){
  if(el.classList&&el.classList.contains('divider-label')){el.style.display='none';continue;}
  if(el.classList&&el.classList.contains('state-tag')){el.style.display='none';groups.push([]);names.push(el.textContent.trim());continue;}
  groups[groups.length-1].push(el);}
 scr._groups=groups;
 const hasDefault=groups[0].some(el=>!isPinned(el));
 scr._first=hasDefault?0:(groups.length>1?1:0);
 if(groups.length>1){const bar=document.createElement('div');bar.className='stabs';
  names.forEach((n,i)=>{if(i===0&&!hasDefault)return;const b=document.createElement('button');b.className='stab';b.dataset.gi=i;b.textContent=(i===0?'Default':n.slice(0,52));b.onclick=()=>setState(sid,i);bar.appendChild(b);});
  const anchor=scr.querySelector('.gap-note')||scr.querySelector('.screen-head');
  if(anchor){anchor.after(bar);}else{scr.prepend(bar);}scr._bar=bar;}
 hydrated[sid]=true;setState(sid,scr._first);}
function isPinned(el){return el.classList&&(el.classList.contains('screen-head')||el.classList.contains('gap-note')||el.classList.contains('stabs')||(el.tagName==='P'&&el.classList.contains('audit')));}
function setState(sid,i){const scr=document.getElementById('scr-'+sid);if(!scr._groups)return;
 scr._groups.forEach((g,gi)=>g.forEach(el=>{el.style.display=(isPinned(el)||gi===i)?'':'none';}));
 if(scr._bar)scr._bar.querySelectorAll('.stab').forEach(b=>b.classList.toggle('on',+b.dataset.gi===i));}
function stateByHint(sid,hint){if(!hint)return -1;const names=D.stateNames[sid]||[];const i=names.findIndex(n=>n.toUpperCase().includes(hint.toUpperCase()));return i<0?0:i;}
function route(){let h=location.hash||'#/login';h=h.slice(2);
 if(h==='login'){show('scr-au-01');paintChrome('Sign in');return;}
 if(h==='choose'){show('scr-choose');paintChrome('Choose workspace');return;}
 let [sid,hint]=h.split('@');
 if(!D.titles[sid]){toast('Unknown screen '+sid);return;}
 const preauth=['au-01','au-02','au-03','au-06','au-07','pt-01'];
 if(!role&&!preauth.includes(sid)){location.hash='#/login';return;}
 if(!role&&preauth.includes(sid)){show('scr-'+sid);const _si0=stateByHint(sid,hint);const _s0=document.getElementById('scr-'+sid);setState(sid,_si0<0?(_s0._first||0):_si0);paintChrome(sid.toUpperCase()+' · '+D.titles[sid]);return;}
 if(!allowed(sid)&&role!=='__all'){show('scr-denied');paintChrome('Access denied');return;}
 show('scr-'+sid);const _si=stateByHint(sid,hint);const _scr=document.getElementById('scr-'+sid);setState(sid,_si<0?(_scr._first||0):_si);paintChrome(sid.toUpperCase()+' · '+D.titles[sid]);paintNav(sid);}
function paintChrome(t){$('#hdr-title').textContent=t;$('#hdr-role').textContent=role?D.roles[role].label:'not signed in';}
function paintNav(cur){const nav=$('#sidenav');if(!role){nav.innerHTML='';return;}
 let html='';const gs=D.roles[role].groups;gs.forEach(g=>{const items=Object.keys(D.titles).filter(s=>s.split('-')[0]===g).sort();if(!items.length)return;
 html+='<div class="sec-label">'+ (D.groups[g]||g) +'</div>'+items.map(s=>'<a class="nav-item'+(s===cur?' active':'')+'" href="#/'+s+'">'+s.toUpperCase()+' · '+D.titles[s].slice(0,26)+'</a>').join('');});
 nav.innerHTML=html;}
function setRole(r){role=r;toast('Signed in as '+D.roles[r].label);location.hash='#/'+D.roles[r].home;if(('#/'+D.roles[r].home)===location.hash)route();}
function actionClick(sid,label){const rules=D.actions[sid]||[];for(const [pat,target,msg] of rules){if(new RegExp(pat,'i').test(label)){toast(msg);const [ts,th]=target.slice(2).split('@');if(ts==='choose'){location.hash='#/choose';return;}if(journey===null){location.hash='#/'+ts+(th?('@'+th):'');}else{location.hash=target;}return;}}
 toast('“'+label.slice(0,40)+'” recorded in the access log (simulated)');}
document.addEventListener('click',e=>{const b=e.target.closest('.btn');if(b&&!b.closest('#jbar')&&!b.getAttribute('href')){const scr=b.closest('.scr');if(scr&&scr.dataset.sid){e.preventDefault();actionClick(scr.dataset.sid,b.textContent.trim());}}});
/* journeys */
function startJourney(id){journey=D.journeys.find(j=>j.id===id);jstep=0;role=journey.role;jgo();$('#jbar').style.display='flex';}
function jgo(){const st=journey.steps[jstep];role=journey.role; // role follows tour context
 // auto-switch role so the step is visible
 const pre=st[0].split('-')[0];for(const[k,v]of Object.entries(D.roles)){if(v.groups.includes(pre)){role=k;break;}}
 location.hash='#/'+st[0]+(st[1]?('@'+st[1]):'');route();
 $('#jinfo').innerHTML='<b>'+journey.title+'</b> — step '+(jstep+1)+'/'+journey.steps.length+' · '+st[2]+' <span class="muted small">(acting as '+D.roles[role].label+')</span>';}
function jnext(d){jstep=Math.min(Math.max(jstep+d,0),journey.steps.length-1);jgo();}
function jexit(){journey=null;$('#jbar').style.display='none';toast('Journey ended — free roam');}
function jumpTo(v){const sid=v.split(' ')[0].toLowerCase();if(D.titles[sid]){role=role||'__all';if(role==='__all'){/*explorer*/}location.hash='#/'+sid;}}

/* ---------- Phase C: live data simulation ---------- */
const SIM = {active:false, stage:0,
 stages:[
  {n:'Registered', view:'fo-02', act:'Register at front desk'},
  {n:'Consent recorded (v3, en+ml)', view:'fo-06', act:'Capture consent'},
  {n:'Order placed — XR Chest PA · ACC-2026-90900', view:'or-04', act:'Place the order'},
  {n:'Invoice paid ₹800 — INV/NPV/26-27/0900', view:'bl-01', act:'Collect cash'},
  {n:'Token X-012 issued · queue pos 2', view:'fo-01', act:'Check in & issue token'},
  {n:'Study acquired & released to reading', view:'rd-01', act:'Perform & acquire'},
  {n:'Report signed — Dr. V. Shetty', view:'rd-14', act:'Sign the report'},
  {n:'Delivered — SMS secure link ✓', view:'nt-01', act:'Deliver'}]};
const SIMROWS = {
 'fo-02':[1,'Asha Varma · MRN-004900 · 29y F · +91 98470 ••210 · EXACT MATCH — registered today 10:41, North Paravoor'],
 'fo-06':[1,'Asha Varma · MRN-004900 — record ACTIVE · consent v3 (en+ml) recorded'],
 'or-04':[3,'ACC-2026-90900 · Asha Varma · X-ray Chest PA · Routine · Dr. Meera Nair — LIVE STATUS follows the demo'],
 'bl-01':[4,'INV/NPV/26-27/0900 · Asha Varma · ₹800 · Exempt (healthcare) · PAID — cash, receipt RCP/NPV/26-27/0900'],
 'fo-01':[5,'Token X-012 · Asha Varma · X-ray · WAITING (2nd) — issued 10:58'],
 'tk-01':[5,'X-012 · Asha Varma · MRN-004900 · XR Chest PA · gates: screening n/a · consent ✓ · READY → Perform'],
 'rd-01':[6,'ACC-2026-90900 · Asha Varma · XR Chest PA · ROUTINE · SLA 24h — unreported, assigned Dr. V. Shetty'],
 'rd-14':[7,'ACC-2026-90900 · Asha Varma · XR Chest PA — SIGNED 12:02 by Dr. V. Shetty · hash stored'],
 'nt-01':[8,'ACC-2026-90900 → Asha Varma · SMS secure link · DELIVERED ✓ 12:05 IST · opened 12:11']};
function simPaint(){const b=$('#simbody');if(!b)return;let h='';
 if(!SIM.active){h='<p class="muted">Watch one record flow through the whole product: register → consent → order → pay → token → acquire → sign → deliver. Rows appear live in search, queues, worklists, billing and delivery.</p><span class="btn primary small" onclick="simStart()">▶ Start live demo</span>';}
 else{SIM.stages.forEach((s,i)=>{const st=i<SIM.stage?'done':(i===SIM.stage?'cur':'');h+='<div class="sstage '+st+'"><span class="sdot">'+(i<SIM.stage?'✓':(i+1))+'</span><span>'+s.n+'</span></div>';});
  h+='<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap">';
  if(SIM.stage<SIM.stages.length)h+='<span class="btn primary small" onclick="simAdvance()">'+SIM.stages[SIM.stage].act+' ›</span>';
  else h+='<span class="chip green">E2E complete — Asha delivered ✓</span>';
  h+='<span class="btn small" onclick="simReset()">Reset</span></div>';}
 b.innerHTML=h;}
function simStart(){SIM.active=true;SIM.stage=0;toast('Live demo started — new patient Asha Varma');simAdvance();}
function simAdvance(){if(SIM.stage>=SIM.stages.length)return;const s=SIM.stages[SIM.stage];SIM.stage++;toast('LIVE DEMO · '+s.n);
 const pre=s.view.split('-')[0];for(const[k,v]of Object.entries(D.roles)){if(v.groups.includes(pre)){role=k;break;}}
 if(('#/'+s.view)===location.hash){route();}else{location.hash='#/'+s.view;}
 simPaint();}
function simReset(){SIM.active=false;SIM.stage=0;$$('.simrow').forEach(e=>e.remove());simPaint();toast('Demo reset');}
function simInject(sid){const scr=document.getElementById('scr-'+sid);if(!scr)return;
 scr.querySelectorAll('.simrow').forEach(e=>e.remove());
 if(!SIM.active)return;const conf=SIMROWS[sid];if(!conf||SIM.stage<conf[0])return;
 const tables=[...scr.querySelectorAll('table')].filter(tb=>tb.offsetParent!==null||true);
 const tb=tables.find(x=>x.querySelector('th'));if(!tb)return;
 const tr=document.createElement('tr');tr.className='simrow';
 tr.innerHTML='<td colspan="99">● LIVE DEMO — '+conf[1]+'</td>';
 const body=tb.querySelector('tbody')||tb; const hd=tb.querySelector('tr');
 hd&&hd.parentNode===body?body.insertBefore(tr,hd.nextSibling):body.insertBefore(tr,body.firstChild);}

window.addEventListener('hashchange',route);
window.addEventListener('load',()=>{const dl=$('#jumplist');dl.innerHTML=Object.keys(D.titles).sort().map(s=>'<option value="'+s.toUpperCase()+' — '+D.titles[s]+'">').join('');
 simPaint();const jm=$('#jmenu');jm.innerHTML='<option value="">▶ Run a journey…</option>'+D.journeys.map(j=>'<option value="'+j.id+'">'+j.title+'</option>').join('');route();});
"""

SHELL_CSS = """
body{margin:0;padding-top:52px}
#hdr{position:fixed;top:0;left:0;right:0;height:52px;background:#0F766E;color:#fff;display:flex;align-items:center;gap:14px;padding:0 16px;z-index:50;font-size:13px}
#hdr b{font-size:15px}
#hdr select,#hdr input{border:none;border-radius:6px;padding:6px 8px;font-size:12.5px}
#hdr .rolechip{background:#134E4A;border-radius:14px;padding:4px 12px}
#layout{display:flex;min-height:calc(100vh - 52px)}
#sidenav{width:230px;background:#fff;border-right:1px solid #E2E8F0;padding:10px 0;overflow-y:auto;position:sticky;top:52px;height:calc(100vh - 52px);flex-shrink:0}
#sidenav .nav-item{display:block;text-decoration:none;font-size:11.5px;padding:5px 14px}
#stage{flex:1;padding:20px 26px;min-width:0;max-width:1400px}
.scr{background:#fff;border-radius:12px;padding:22px 28px;box-shadow:0 1px 5px rgba(15,23,42,.07)}
.stabs{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0;border-bottom:2px solid #E2E8F0;padding-bottom:8px}
.stab{border:1px solid #CBD5E1;background:#F8FAFC;border-radius:16px;padding:4px 12px;font-size:11.5px;font-weight:700;cursor:pointer;color:#475569}
.stab.on{background:#0F766E;border-color:#0F766E;color:#fff}
.xref{color:#0F766E;text-decoration:none;border-bottom:1px dotted #99F6E4}
.toastx{position:fixed;bottom:76px;right:20px;background:#1E293B;color:#fff;padding:10px 16px;border-radius:9px;font-size:12.5px;z-index:99;box-shadow:0 6px 20px rgba(0,0,0,.3);animation:fadein .2s}
@keyframes fadein{from{opacity:0;transform:translateY(8px)}to{opacity:1}}
#jbar{position:fixed;bottom:0;left:0;right:0;background:#134E4A;color:#fff;display:none;align-items:center;gap:14px;padding:10px 18px;z-index:60;font-size:13px}
#jbar .btn{background:#fff;color:#134E4A;border:none}
.pcard{cursor:pointer;transition:box-shadow .15s}.pcard:hover{box-shadow:0 4px 16px rgba(15,118,110,.25)}
.btn{cursor:pointer}
/* ---------- responsive ---------- */
#burger{display:none;background:#134E4A;color:#fff;border:none;border-radius:6px;padding:6px 10px;font-size:16px;cursor:pointer}
@media (max-width:1024px){
 #sidenav{width:190px}
 .kpi-row{flex-wrap:wrap}.kpi{min-width:44%}
 .split{grid-template-columns:1fr !important}
 .row{flex-wrap:wrap}
}
@media (max-width:768px){
 #burger{display:block}
 #sidenav{position:fixed;left:0;top:52px;bottom:0;transform:translateX(-100%);transition:transform .2s;z-index:70;box-shadow:4px 0 20px rgba(0,0,0,.2)}
 #sidenav.open{transform:none}
 #stage{padding:10px}
 .scr{padding:12px}
 #jump,#hdr .muted{display:none}
 #jmenu{max-width:130px}
 .frame .sidebar{display:none}
 .kpi{min-width:100%}
 .kv{grid-template-columns:1fr !important}
 table{display:block;overflow-x:auto;white-space:nowrap}
 .screen-head{flex-direction:column;gap:6px}
 .screen-head .meta{text-align:left}
 body{font-size:13px}
}
@media (min-width:1700px){
 #stage{max-width:1500px;margin:0 auto}
 body{font-size:15px}
}
/* ---------- sim panel ---------- */
#simpanel{position:fixed;right:14px;bottom:64px;width:280px;background:#fff;border:1.5px solid #0F766E;border-radius:12px;box-shadow:0 8px 30px rgba(15,23,42,.25);z-index:65;font-size:12px}
#simpanel .sph{background:#0F766E;color:#fff;padding:8px 12px;border-radius:10px 10px 0 0;font-weight:800;display:flex;justify-content:space-between;cursor:pointer}
#simpanel .spb{padding:10px 12px;max-height:44vh;overflow-y:auto}
.sstage{display:flex;gap:8px;align-items:center;padding:3px 0}
.sdot{width:14px;height:14px;border-radius:50%;background:#E2E8F0;color:#fff;font-size:9px;text-align:center;line-height:14px;font-weight:800;flex-shrink:0}
.sstage.done .sdot{background:#15803D}.sstage.cur .sdot{background:#0F766E;box-shadow:0 0 0 3px #CCFBF1}
.sstage.cur{font-weight:800}
tr.simrow td{background:#CCFBF1 !important;border-left:4px solid #0F766E;font-weight:700}
@media (max-width:768px){#simpanel{width:calc(100vw - 20px);right:10px;bottom:58px}}
"""

html_out = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MagnusPRO — Live Prototype (232 screens, navigable E2E)</title>
<style>{CSS}\n{SHELL_CSS}</style></head><body>
<div id="hdr"><button id="burger" onclick="document.getElementById('sidenav').classList.toggle('open')">☰</button><b>◎ MagnusPRO</b><span class="muted" style="color:#99F6E4">Live Prototype · v1.1 · synthetic data</span>
<span id="hdr-title" style="flex:1;text-align:center;font-weight:700"></span>
<select id="jmenu" onchange="if(this.value)startJourney(this.value);this.selectedIndex=0"></select>
<input list="jumplist" id="jump" placeholder="Jump to screen…" size="22" onchange="jumpTo(this.value);this.value=''"><datalist id="jumplist"></datalist>
<span class="rolechip" id="hdr-role"></span>
<a class="btn small" style="background:#fff" href="#/choose">Switch user</a></div>
<div id="layout"><nav id="sidenav"></nav><main id="stage">
{ALL}
{CHOOSER}
{DENIAL}
</main></div>
<div id="simpanel"><div class="sph" onclick="document.querySelector('#simpanel .spb').classList.toggle('hide');this.querySelector('i').textContent=document.querySelector('#simpanel .spb').classList.contains('hide')?'▲':'▼'"><span>● Live demo — Asha Varma</span><i style="font-style:normal">▼</i></div><div class="spb" id="simbody"></div></div>
<div id="jbar"><span id="jinfo" style="flex:1"></span><span class="btn small" onclick="jnext(-1)">‹ Prev</span><span class="btn small primary" onclick="jnext(1)">Next step ›</span><span class="btn small" onclick="jexit()">Exit tour</span></div>
<script>{JS.replace("__DATA__", DATA)}</script></body></html>"""

out = BASE/"out/MagnusPRO_Live_Prototype.html"
out.write_text(html_out)
print("prototype written:", out.stat().st_size//1024, "KB ·", len(screens), "screens ·", len(JOURNEYS), "journeys ·", sum(len(v) for v in ACTIONS.values()), "wired actions")
# verification: journey targets + states resolve
errs=[]
for j in JOURNEYS:
    for sid,hint,_ in j["steps"]:
        if sid not in screens: errs.append(f"{j['id']}: missing {sid}")
        elif hint and not any(hint.upper() in n.upper() for n in screens[sid]['names']): errs.append(f"{j['id']}: {sid} no state ~'{hint}'")
for sid in ACTIONS:
    if sid not in screens: errs.append(f"action map: missing {sid}")
print("VERIFICATION:", "PASS" if not errs else errs)
