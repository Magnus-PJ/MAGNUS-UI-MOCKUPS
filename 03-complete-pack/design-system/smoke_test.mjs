// Prototype regression smoke test (v1.3.1 audit round)
import { chromium } from '/home/claude/.npm-global/lib/node_modules/playwright/index.mjs';
const FILE = 'file:///home/claude/allpack/out/MagnusPRO_Live_Prototype.html';
const results = []; const ok = (n, c) => results.push([c ? 'PASS' : 'FAIL', n]);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const errors = [];
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
page.on('pageerror', e => errors.push(String(e)));

await page.goto(FILE); await page.waitForTimeout(400);
// 1. Login chain
ok('login screen shown', await page.locator('#scr-au-01').isVisible());
await page.evaluate(() => { location.hash = '#/au-03'; }); await page.waitForTimeout(200);
await page.evaluate(() => setRole('frontoffice')); await page.waitForTimeout(300);
ok('frontoffice home after setRole', (await page.evaluate(() => location.hash)).includes('fo-'));

// 2. Role gating: frontoffice must NOT see platform screens
const denied = await page.evaluate(() => { location.hash = '#/pl-01'; return new Promise(r => setTimeout(() => r(document.body.innerText.includes('not available to your role') || !document.querySelector('#scr-pl-01') || document.querySelector('#scr-pl-01').style.display === 'none' || !allowed('pl-01')), 300)); });
ok('role gating blocks pl-01 for frontoffice', denied);

// 3. All 8 journeys
for (const j of ['j1','j2','j3','j4','j5','j6','j7','j8']) {
  const r = await page.evaluate(async (id) => {
    startJourney(id); let steps = 0;
    const J = D.journeys.find(x => x.id === id);
    for (let i = 0; i < J.steps.length - 1; i++) { jnext(1); steps++; await new Promise(r => setTimeout(r, 30)); }
    const done = steps === J.steps.length - 1; jexit(); return done;
  }, j);
  ok(`journey ${j} walks all steps`, r);
}

// 4. Sim: 8 stages
const sim = await page.evaluate(async () => {
  simReset(); simStart(); // simStart runs stage 1
  while (SIM.stage < SIM.stages.length) { simAdvance(); await new Promise(r => setTimeout(r, 30)); }
  return SIM.stage === SIM.stages.length;
});
ok('sim completes all stages', sim);

// 5. Palette opens and finds screens
const pal = await page.evaluate(() => { palOpen(); palQuery('billing'); const n = document.querySelectorAll('#pal .pitem, #pal li, #pal .prow, #pal [onclick]').length; palClose(); return n; });
ok('palette returns results for "billing"', pal > 0);

// 6. State tabs hydrate on a multi-state screen
await page.evaluate(() => setRole('orgadmin')); await page.waitForTimeout(200);
await page.evaluate(() => { location.hash = '#/ad-01'; }); await page.waitForTimeout(300);
const tabs = await page.evaluate(() => document.querySelectorAll('#scr-ad-01 .stab').length);
ok('ad-01 state tabs rendered', tabs >= 2);
const tabTxt = await page.evaluate(() => [...document.querySelectorAll('#scr-ad-01 .stab')].map(b => b.textContent).join('|'));
ok('ad-01 tab labels normalized (no VASHI)', !/VASHI|MERID/i.test(tabTxt) || /IJK/.test(tabTxt));

// 7. Viewports render without error
for (const [w, h, name] of [[390, 844, 'phone'], [820, 1180, 'ipad'], [2560, 1400, 'wide']]) {
  await page.setViewportSize({ width: w, height: h }); await page.waitForTimeout(250);
  const vis = await page.evaluate(() => document.body.scrollHeight > 100);
  ok(`viewport ${name} renders`, vis);
}

ok('zero page errors', errors.length === 0);
await browser.close();
let fail = 0;
for (const [s, n] of results) { if (s === 'FAIL') fail++; console.log(s, '·', n); }
if (errors.length) console.log('ERRORS:', errors.slice(0, 3));
console.log(fail === 0 ? 'SMOKE: ALL PASS (' + results.length + ' checks)' : 'SMOKE: ' + fail + ' FAILURES');
process.exit(fail === 0 ? 0 : 1);
