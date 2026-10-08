"""Build the installable offline phone app (PWA) from the same content as the Streamlit app.

Run:  python build_pwa.py
It reads cards.py, cards_bg.py, illustrations.py and the "Start here" questions and
interface texts from streamlit_app.py, and writes everything into the folder  pwa/ .
After changing any card or drawing, run it again and upload the new pwa/ folder.
"""
import ast
import hashlib
import json
import pathlib
import shutil

import cards
import cards_bg
import illustrations

HERE = pathlib.Path(__file__).parent
OUT = HERE / "pwa"


# ---------- read the "Start here" questions and interface texts from streamlit_app.py ----------
def _from_streamlit_app():
    tree = ast.parse((HERE / "streamlit_app.py").read_text(encoding="utf-8"))
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name == "UI":
                found["ui"] = ast.literal_eval(node.value)
            elif name == "TRIAGE":            # TRIAGE = {...}[LANG]
                value = node.value.value if isinstance(node.value, ast.Subscript) else node.value
                found["triage"] = ast.literal_eval(value)
    return found["ui"], found["triage"]


def _card(c):
    return {
        "id": c["id"], "sev": c["sev"], "title": c["title"], "sub": c["sub"],
        "recognize": c["recognize"], "call": bool(c.get("call")), "metronome": bool(c.get("metronome")),
        "steps": [[s[0], s[1], s[2] if len(s) > 2 else None] for s in c["steps"]],
        "when": c["when"], "dont": c["dont"],
    }


def build():
    ui, triage = _from_streamlit_app()
    # search finds a card by English OR Bulgarian words, whichever language is on (same as the Streamlit app)
    search = {c["id"]: c["keys"] for c in cards.CARDS}
    for c in cards_bg.CARDS:
        search[c["id"]] += " " + c["keys"] + " " + c["title"] + " " + c["sub"]
    pics_bg = {k: illustrations.ILLUSTRATIONS_BG.get(k, v) for k, v in illustrations.ILLUSTRATIONS.items()}
    data = {
        "cards": {"en": [_card(c) for c in cards.CARDS], "bg": [_card(c) for c in cards_bg.CARDS]},
        "sev": {"en": cards.SEV, "bg": cards_bg.SEV},
        "ui": ui, "triage": triage, "search": search,
        "pics": {"en": illustrations.ILLUSTRATIONS, "bg": pics_bg},
    }
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "icons").mkdir(parents=True)

    html = INDEX_HTML.replace("__DATA__", data_json)
    (OUT / "index.html").write_text(html, encoding="utf-8")
    (OUT / "README.txt").write_text(README, encoding="utf-8")
    (OUT / "manifest.webmanifest").write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=2), encoding="utf-8")
    _icons()

    # the version changes whenever the content changes, so installed apps pick up the update
    version = hashlib.sha256(html.encode()).hexdigest()[:10]
    (OUT / "sw.js").write_text(SERVICE_WORKER.replace("__VERSION__", version), encoding="utf-8")
    print(f"Built {OUT}  ({len(data['cards']['en'])} cards, version {version})")


# ---------- app icon: white cross on red (needs Pillow:  pip install pillow) ----------
def _icon(px, rounded):
    from PIL import Image, ImageDraw
    big = 512
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle((16, 16, 496, 496), radius=96, fill="#C8102E")
    else:                                   # "maskable": full square, the phone cuts its own shape
        d.rectangle((0, 0, big, big), fill="#C8102E")
    d.rounded_rectangle((216, 136, 296, 376), radius=10, fill="white")
    d.rounded_rectangle((136, 216, 376, 296), radius=10, fill="white")
    return img.resize((px, px), Image.LANCZOS)


def _icons():
    for name, px, rounded in (("icon-192.png", 192, True), ("icon-512.png", 512, True),
                              ("maskable-512.png", 512, False), ("apple-touch-icon.png", 180, False)):
        _icon(px, rounded).save(OUT / "icons" / name)


README = """FIRST AID / ПЪРВА ПОМОЩ - phone app (works offline)

WHAT IS IN THIS FOLDER
  index.html            the whole app (all cards, drawings, both languages)
  manifest.webmanifest  name and icon for the phone's home screen
  sw.js                 keeps the app on the phone so it works without internet
  icons/                app icons

PUT IT ONLINE (free, GitHub Pages)
  1. On github.com: New repository, e.g. "first-aid", set to Public.
  2. "Add file" > "Upload files". Upload EVERYTHING inside this folder
     (index.html must be at the top level, not inside another folder). Commit.
  3. Settings > Pages > Source: "Deploy from a branch", Branch: main, folder: / (root) > Save.
  4. After about a minute the app is at:  https://YOUR-USERNAME.github.io/first-aid/

INSTALL ON A PHONE (open the link once with internet)
  Android (Chrome):  menu (three dots) > "Install app" or "Add to Home screen".
  iPhone (Safari):   Share button > "Add to Home Screen".  (Must be Safari.)
  After that it opens from the home screen, also with no signal.

UPDATE THE CONTENT
  1. Edit cards.py / cards_bg.py / illustrations.py as before.
  2. Run:  python build_pwa.py      (in the folder with cards.py; needs Pillow: pip install pillow)
  3. Upload the new files from the pwa folder to the same repository, replacing the old ones.
  Phones get the update the next time the app is opened with internet
  (sometimes it needs to be closed and opened once more).
"""

MANIFEST = {
    "name": "Първа помощ · First Aid",
    "short_name": "Първа помощ",
    "description": "Първа помощ стъпка по стъпка, работи и без интернет. Step-by-step first aid that works offline.",
    "lang": "bg",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#FFFFFF",
    "theme_color": "#C8102E",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}

SERVICE_WORKER = """// Keeps the whole app on the phone so it opens without internet.
const CACHE = 'first-aid-__VERSION__';
const FILES = ['./', 'index.html', 'manifest.webmanifest',
               'icons/icon-192.png', 'icons/icon-512.png', 'icons/maskable-512.png', 'icons/apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(
    caches.match(e.request, {ignoreSearch: true}).then(hit => hit ||
      fetch(e.request).catch(() => e.request.mode === 'navigate' ? caches.match('index.html') : undefined))
  );
});
"""

INDEX_HTML = r"""<!doctype html>
<html lang="bg">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#C8102E">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Първа помощ">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>Първа помощ · First Aid</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<style>
  :root { --ink:#13201B; --muted:#51605A; --line:#CBD5D1; --red:#C8102E; --teal:#11695A; }
  * { box-sizing: border-box; }
  html, body { margin: 0; background: #FFFFFF; color: var(--ink);
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; }
  body { padding: env(safe-area-inset-top) 0 env(safe-area-inset-bottom); }
  main { max-width: 760px; margin: 0 auto; padding: 12px 16px 40px; }
  button { font: inherit; color: inherit; }

  .topbar { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
  .brand { flex:1; font-weight:700; font-size:22px; display:flex; align-items:center; gap:10px; }
  .logo { width:30px; height:30px; border-radius:7px; background:var(--red); color:#fff;
    display:grid; place-items:center; font-size:22px; font-weight:700; line-height:1; }
  a.call { background:var(--red); color:#fff; text-decoration:none; font-weight:700;
    font-size:20px; padding:10px 18px; border-radius:999px; white-space:nowrap; }
  .lang { display:flex; gap:6px; margin-bottom:12px; }
  .lang button { border:1px solid var(--line); background:#fff; border-radius:999px; padding:6px 14px; font-size:15px; }
  .lang button.on { background:var(--ink); color:#fff; border-color:var(--ink); }

  .big { display:block; width:100%; min-height:64px; font-size:19px; font-weight:700; text-align:left;
    border:1px solid var(--line); border-radius:10px; background:#fff; padding:12px 14px; margin:0 0 8px; cursor:pointer; }
  .big:active { background:#EEF2F0; }
  .big.primary { background:var(--red); border-color:var(--red); color:#fff; }
  .back { min-height:48px; font-size:17px; width:auto; padding:8px 14px; }

  input.search { width:100%; font-size:18px; padding:12px 14px; border:1px solid var(--line); border-radius:10px; margin:4px 0 4px; }
  .warn { background:#FCEFD9; border-radius:10px; padding:12px 14px; margin-top:10px; font-size:17px; }
  .group { font-size:16px; font-weight:700; color:var(--muted); margin:22px 0 8px; display:flex; align-items:center; gap:8px; }
  .group i { width:10px; height:10px; border-radius:50%; display:inline-block; }
  .tiles { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
  .tiles .big { margin:0; font-size:17px; min-height:64px; }
  @media (max-width: 340px) { .tiles { grid-template-columns:1fr; } }

  .tq { font-size:26px; font-weight:700; line-height:1.25; margin:10px 0 6px; }
  .tq-hint { font-size:18px; color:var(--muted); margin-bottom:12px; }

  .dhead { border-left:8px solid var(--c); padding:4px 0 4px 14px; margin:8px 0 16px; }
  .dhead h1 { font-size:30px; line-height:1.15; margin:0; }
  .dhead p { margin:6px 0 0; color:var(--muted); font-size:18px; }
  .urgent { display:flex; gap:12px; align-items:center; background:#FBE7EA; border-radius:12px;
    padding:12px 14px; margin-bottom:12px; font-weight:700; font-size:18px; }
  .urgent a.call { margin-left:auto; font-size:17px; padding:8px 14px; }
  .beat { display:flex; align-items:center; gap:12px; background:#DDF0EB; border-radius:12px; padding:10px 14px; margin-bottom:12px; font-size:16px; }
  .beat button { border:0; background:var(--teal); color:#fff; font-weight:700; border-radius:10px; padding:10px 16px; min-height:44px; font-size:16px; }
  .beat .dot { width:18px; height:18px; border-radius:50%; background:var(--teal); opacity:.25; flex:none; }
  .modes { display:flex; gap:8px; margin:4px 0 12px; }
  .modes button { flex:1; border:1px solid var(--line); background:#fff; border-radius:10px; padding:10px; font-size:16px; font-weight:700; }
  .modes button.on { background:var(--ink); color:#fff; border-color:var(--ink); }

  .step { border:1px solid var(--line); border-radius:12px; padding:12px 14px; margin-bottom:10px; }
  .step label { display:flex; gap:10px; align-items:flex-start; font-size:20px; font-weight:700; cursor:pointer; }
  .step input { width:24px; height:24px; margin-top:2px; flex:none; accent-color:var(--teal); }
  .step.done label { color:var(--muted); text-decoration:line-through; }
  .stepdesc { color:var(--muted); font-size:17px; margin:6px 0 0 34px; line-height:1.4; }
  .pic img { width:100%; max-width:340px; display:block; margin:8px 0 2px; }
  .guide .count { color:var(--muted); font-weight:700; }
  .guide .num { font-size:72px; font-weight:700; line-height:1; color:var(--c); margin:8px 0; }
  .guide .title { font-size:26px; font-weight:700; line-height:1.25; }
  .guide .desc { font-size:18px; color:var(--muted); margin-top:10px; line-height:1.4; }
  .nav { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:12px; }
  .nav button { min-height:56px; font-size:18px; font-weight:700; border-radius:10px; border:1px solid var(--line); background:#fff; }
  .nav button.primary { background:var(--red); border-color:var(--red); color:#fff; }
  .nav button:disabled { opacity:.35; }

  .box { border-radius:12px; padding:14px 16px; margin-top:14px; font-size:17px; line-height:1.4; }
  .box h3 { margin:0 0 6px; font-size:18px; }
  .box ul { margin:0; padding-left:20px; }
  .box.red { background:#FBE7EA; }
  .box.amber { background:#FCEFD9; }
  .note { margin-top:28px; font-size:15px; color:var(--muted); line-height:1.4; }
</style>
</head>
<body>
<main id="app"></main>
<script id="data" type="application/json">__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const app = document.getElementById('app');
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

let lang = 'bg';
try { lang = localStorage.getItem('lang') || 'bg'; } catch (e) {}
let query = '', mode = 'all', step = 0, done = {};

const T = () => D.ui[lang];
const cardsNow = () => D.cards[lang];
const cardById = id => cardsNow().find(c => c.id === id);

function setLang(l) {
  lang = l;
  try { localStorage.setItem('lang', l); } catch (e) {}
  render();
}

// ---------- navigation: the address (#...) changes, so the phone's Back button works ----------
function go(hash) { if (location.hash === hash) render(); else location.hash = hash; }
function openCard(id) { step = 0; go('#/card/' + id); }
function triageGo(target) {
  if (target.startsWith('card:')) openCard(target.slice(5));
  else if (target === 'list') go('#');
  else go('#/triage/' + target);
}
window.addEventListener('hashchange', render);

function topbar() {
  return `<div class="topbar"><div class="brand"><span class="logo">+</span>${esc(T().brand)}</div>
    <a class="call" href="tel:112">📞 112</a></div>
    <div class="lang"><button data-lang="bg" class="${lang === 'bg' ? 'on' : ''}">Български</button>
    <button data-lang="en" class="${lang === 'en' ? 'on' : ''}">English</button></div>`;
}

// ---------- home ----------
function tilesHTML() {
  const q = query.trim().toLowerCase();
  const found = cardsNow().filter(c => !q || (c.title + ' ' + c.sub + ' ' + D.search[c.id]).toLowerCase().includes(q));
  let out = found.length ? '' : `<div class="warn">${esc(T().no_match.replace('{q}', query.trim()))}</div>`;
  for (const [sev, meta] of Object.entries(D.sev[lang])) {
    const group = found.filter(c => c.sev === sev);
    if (!group.length) continue;
    out += `<div class="group"><i style="background:${meta.color}"></i>${esc(meta.label)}</div><div class="tiles">` +
      group.map(c => `<button class="big" data-card="${c.id}" title="${esc(c.sub)}">${esc(c.title)}</button>`).join('') + '</div>';
  }
  return out;
}

function renderHome() {
  app.innerHTML = topbar() +
    `<button class="big primary" data-tri="start">${esc(T().start_here)}</button>
     <input class="search" type="search" placeholder="${esc(T().search)}" value="${esc(query)}" aria-label="Search">
     <div id="tiles">${tilesHTML()}</div>
     <p class="note">${esc(T().note)}</p>`;
  app.querySelector('.search').addEventListener('input', e => {
    query = e.target.value;
    document.getElementById('tiles').innerHTML = tilesHTML();
  });
}

// ---------- start here ----------
function renderTriage(node) {
  const [question, hint, answers] = D.triage[lang][node];
  app.innerHTML = topbar() +
    `<button class="big back" data-tri="list">${esc(T().cancel)}</button>
     <div class="tq">${esc(question)}</div>${hint ? `<div class="tq-hint">${esc(hint)}</div>` : ''}` +
    answers.map(([label, target]) => `<button class="big" data-tri="${esc(target)}">${esc(label)}</button>`).join('') +
    `<p class="note">${esc(T().tri_note)}</p>`;
}

// ---------- situation card ----------
function pic(key) {
  const svg = key && D.pics[lang][key];
  return svg ? `<div class="pic"><img alt="" src="data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}"></div>` : '';
}

function renderCard(c) {
  const color = D.sev[lang][c.sev].color;
  const ink = D.sev[lang][c.sev].ink || color;       // darker shade for the big step number
  const d = done[c.id] = done[c.id] || {};
  let html = topbar() +
    `<button class="big back" data-tri="list">${esc(T().all_situations)}</button>
     <div class="dhead" style="--c:${color}"><h1>${esc(c.title)}</h1><p>${esc(c.recognize)}</p></div>`;
  if (c.call) html += `<div class="urgent">${esc(T().urgent)}<a class="call" href="tel:112">${esc(T().call)}</a></div>`;
  if (c.metronome) html += `<div class="beat"><button id="beat">${esc(beatOn ? T().beat_stop : T().beat_start)}</button>
      <div class="dot" id="dot"></div><span>${esc(T().beat_hint)}</span></div>`;
  html += `<div class="modes"><button data-mode="all" class="${mode === 'all' ? 'on' : ''}">${esc(T().mode_all)}</button>
      <button data-mode="one" class="${mode === 'one' ? 'on' : ''}">${esc(T().mode_one)}</button></div>`;
  if (mode === 'all') {
    html += c.steps.map(([title, desc, key], i) =>
      `<div class="step ${d[i] ? 'done' : ''}"><label><input type="checkbox" data-done="${i}" ${d[i] ? 'checked' : ''}>
        <span>${i + 1}. ${esc(title)}</span></label><div class="stepdesc">${esc(desc)}</div>${pic(key)}</div>`).join('');
  } else {
    const i = Math.min(step, c.steps.length - 1), [title, desc, key] = c.steps[i];
    html += `<div class="step guide" style="--c:${ink}"><div class="count">${esc(T().step_of.replace('{i}', i + 1).replace('{n}', c.steps.length))}</div>
      <div class="num">${i + 1}</div><div class="title">${esc(title)}</div><div class="desc">${esc(desc)}</div>${pic(key)}
      <div class="nav"><button data-step="-1" ${i === 0 ? 'disabled' : ''}>${esc(T().back)}</button>
      <button class="primary" data-step="1" ${i === c.steps.length - 1 ? 'disabled' : ''}>${esc(T().next)}</button></div></div>`;
  }
  html += box('red', T().when, c.when) + box('amber', T().dont, c.dont);
  app.innerHTML = html;
  const b = document.getElementById('beat');
  if (b) b.addEventListener('click', toggleBeat);
}
const box = (kind, title, items) =>
  `<div class="box ${kind}"><h3>${esc(title)}</h3><ul>${items.map(x => `<li>${esc(x)}</li>`).join('')}</ul></div>`;

// ---------- CPR beat: 110 per minute ----------
let beatOn = null, ctx = null;
function tick() {
  const dot = document.getElementById('dot');
  if (dot) { dot.style.opacity = 1; setTimeout(() => dot.style.opacity = .25, 120); }
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.frequency.value = 880; g.gain.setValueAtTime(.25, ctx.currentTime);
  g.gain.exponentialRampToValueAtTime(.001, ctx.currentTime + .08);
  o.connect(g).connect(ctx.destination); o.start(); o.stop(ctx.currentTime + .09);
}
function toggleBeat() {
  if (beatOn) { stopBeat(); } else {
    ctx = ctx || new (window.AudioContext || window.webkitAudioContext)(); ctx.resume();
    tick(); beatOn = setInterval(tick, 60000 / 110);
  }
  const b = document.getElementById('beat');
  if (b) b.textContent = beatOn ? T().beat_stop : T().beat_start;
}
function stopBeat() { if (beatOn) { clearInterval(beatOn); beatOn = null; } }

// keep the screen on while a card is open (helps during CPR); quietly skipped where unsupported
let wake = null;
async function keepAwake(on) {
  try {
    if (on && !wake && navigator.wakeLock) { wake = await navigator.wakeLock.request('screen'); wake.addEventListener('release', () => wake = null); }
    if (!on && wake) { await wake.release(); wake = null; }
  } catch (e) {}
}
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && location.hash.startsWith('#/card/')) keepAwake(true); });

// ---------- one click handler for everything ----------
app.addEventListener('click', e => {
  const t = e.target.closest('button, input[type=checkbox]');
  if (!t) return;
  if (t.dataset.lang) return setLang(t.dataset.lang);
  if (t.dataset.card) return openCard(t.dataset.card);
  if (t.dataset.tri) return triageGo(t.dataset.tri);
  if (t.dataset.mode) { mode = t.dataset.mode; return render(); }
  if (t.dataset.step) { step = Math.max(0, step + Number(t.dataset.step)); render(); return window.scrollTo(0, 0); }
  if (t.dataset.done !== undefined) {
    const id = location.hash.split('/')[2];
    done[id][t.dataset.done] = t.checked;
    t.closest('.step').classList.toggle('done', t.checked);
  }
});

function render() {
  document.documentElement.lang = lang;
  const [, view, arg] = location.hash.split('/');
  const card = view === 'card' && cardById(arg);
  if (!card) stopBeat();
  keepAwake(!!card);
  if (card) renderCard(card);
  else if (view === 'triage' && D.triage[lang][arg]) renderTriage(arg);
  else renderHome();
}
render();

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
