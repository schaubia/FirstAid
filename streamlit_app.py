import base64
import html

import streamlit as st

from cards import CARDS as CARDS_EN, SEV as SEV_EN
from cards_bg import CARDS as CARDS_BG, SEV as SEV_BG
from illustrations import ILLUSTRATIONS

st.set_page_config(page_title="Първа помощ · First Aid", page_icon="⛑️", layout="centered",
                   initial_sidebar_state="collapsed")

# ---------- language ----------
# Bulgarian by default; the choice is kept in the link (?lang=en) so it survives a refresh.
if "lang" not in st.session_state:
    st.session_state.lang = "en" if st.query_params.get("lang") == "en" else "bg"
LANG = st.session_state.lang

CARDS = CARDS_BG if LANG == "bg" else CARDS_EN
SEV = SEV_BG if LANG == "bg" else SEV_EN
BY_ID = {c["id"]: c for c in CARDS}

# Search finds a card by English OR Bulgarian words, whichever language is on.
SEARCH_KEYS = {c["id"]: c["keys"] for c in CARDS_EN}
for c in CARDS_BG:
    SEARCH_KEYS[c["id"]] += " " + c["keys"] + " " + c["title"] + " " + c["sub"]

UI = {
    "en": {
        "brand": "First Aid",
        "start_here": "🆘 Don't know what's wrong? Start here",
        "search": "🔍 What happened? e.g. burn, choking",
        "no_match": "Nothing matches “{q}”. If someone is in danger, call 112 now.",
        "note": "For guidance only — it doesn't replace a first aid course or the 112 operator. "
                "Follow the operator's instructions when you call.",
        "all_situations": "‹ All situations",
        "urgent": "Call 112 now, then follow the steps.",
        "call": "Call 112",
        "mode_all": "All steps",
        "mode_one": "One at a time",
        "step_of": "Step {i} of {n}",
        "back": "Back",
        "next": "Next",
        "when": "Call 112 if",
        "dont": "Don't",
        "cancel": "‹ Cancel",
        "tri_note": "Not sure? Call 112 — the operator will guide you.",
        "beat_start": "▶ Compression beat",
        "beat_stop": "■ Stop beat",
        "beat_hint": "110 per minute — push on each beat",
    },
    "bg": {
        "brand": "Първа помощ",
        "start_here": "🆘 Не знаете какво е? Започнете оттук",
        "search": "🔍 Какво се случи? напр. изгаряне, задавяне",
        "no_match": "Няма резултат за „{q}“. Ако някой е в опасност, обадете се на 112 веднага.",
        "note": "Само за ориентация — не замества курс по първа помощ или оператора на 112. "
                "Когато се обадите, следвайте указанията на оператора.",
        "all_situations": "‹ Всички ситуации",
        "urgent": "Обадете се на 112 сега, после следвайте стъпките.",
        "call": "Обаждане 112",
        "mode_all": "Всички стъпки",
        "mode_one": "Стъпка по стъпка",
        "step_of": "Стъпка {i} от {n}",
        "back": "Назад",
        "next": "Напред",
        "when": "Обадете се на 112, ако",
        "dont": "Не правете",
        "cancel": "‹ Отказ",
        "tri_note": "Не сте сигурни? Обадете се на 112 — операторът ще ви насочи.",
        "beat_start": "▶ Ритъм за натискане",
        "beat_stop": "■ Спри ритъма",
        "beat_hint": "110 в минута — натискайте при всеки удар",
    },
}
T = UI[LANG]

# ---------- quick triage ("Don't know what's wrong?") ----------
# Each question: (question, hint, [(answer label, target), ...])
# target = another question id, "card:<card id>", or "list" (close and show all cards)
TRIAGE = {
    "en": {
        "start": ("Does the person respond when you shout and tap their shoulders?", "",
                  [("Yes, they respond", "talk"),
                   ("No response", "breath")]),
        "breath": ("Are they breathing normally?",
                   "Tilt the head back, lift the chin, and watch the chest for up to 10 seconds. "
                   "Gasping doesn't count.",
                   [("Yes, breathing normally", "card:unconscious"),
                    ("No, or only gasping", "age_cpr")]),
        "age_cpr": ("How old are they?", "Call 112 now if you haven't — put the phone on speaker.",
                    [("Adult or teenager", "card:cpr"),
                     ("Child (1 year to puberty)", "card:cpr-child"),
                     ("Baby (under 1 year)", "card:cpr-infant")]),
        "talk": ("Can they breathe, speak or cough?", "",
                 [("Yes — show me all situations", "list"),
                  ("No — can't breathe, speak or cough", "age_choke"),
                  ("Wheezing, struggling to breathe — has asthma", "card:asthma"),
                  ("Swollen lips or throat after food, a sting or medicine", "card:allergy")]),
        "age_choke": ("How old are they?", "",
                      [("Adult or teenager", "card:choking"),
                       ("Child (1 year to puberty)", "card:choking-child"),
                       ("Baby (under 1 year)", "card:choking-infant")]),
    },
    "bg": {
        "start": ("Реагира ли човекът, когато го викате и го потупвате по раменете?", "",
                  [("Да, реагира", "talk"),
                   ("Не реагира", "breath")]),
        "breath": ("Диша ли нормално?",
                   "Наклонете главата назад, повдигнете брадичката и гледайте гърдите до 10 секунди. "
                   "Редките хрипливи вдишвания не се броят.",
                   [("Да, диша нормално", "card:unconscious"),
                    ("Не, или само хрипти на пресекулки", "age_cpr")]),
        "age_cpr": ("На каква възраст е?", "Обадете се на 112, ако още не сте — включете високоговорителя.",
                    [("Възрастен или тийнейджър", "card:cpr"),
                     ("Дете (от 1 година до пубертета)", "card:cpr-child"),
                     ("Бебе (под 1 година)", "card:cpr-infant")]),
        "talk": ("Може ли да диша, да говори или да кашля?", "",
                 [("Да — покажи всички ситуации", "list"),
                  ("Не — не може да диша, да говори или да кашля", "age_choke"),
                  ("Свирене в гърдите, трудно диша — има астма", "card:asthma"),
                  ("Подути устни или гърло след храна, ужилване или лекарство", "card:allergy")]),
        "age_choke": ("На каква възраст е?", "",
                      [("Възрастен или тийнейджър", "card:choking"),
                       ("Дете (от 1 година до пубертета)", "card:choking-child"),
                       ("Бебе (под 1 година)", "card:choking-infant")]),
    },
}[LANG]

# ---------- styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap');
html, body, .stApp, .stApp * { font-family: "Atkinson Hyperlegible", system-ui, sans-serif; }
.block-container { padding-top: 1.2rem; max-width: 760px; }
header[data-testid="stHeader"], footer { display: none; }

.topbar { display:flex; align-items:center; gap:12px; margin-bottom:8px; }
.topbar .brand { flex:1; font-weight:700; font-size:22px; display:flex; align-items:center; gap:10px; }
.topbar .logo { width:30px; height:30px; border-radius:7px; background:#C8102E; color:#fff;
  display:grid; place-items:center; font-size:22px; font-weight:700; line-height:1; }
a.call { background:#C8102E; color:#fff !important; text-decoration:none !important; font-weight:700;
  font-size:20px; padding:10px 20px; border-radius:999px; display:inline-block; }

/* big tap targets for situation buttons */
div.stButton > button { min-height:64px; font-size:19px; font-weight:700; border-radius:10px;
  justify-content:flex-start; text-align:left; border:1px solid #CBD5D1; }
div.stButton > button p { font-size:19px; font-weight:700; }
div.stButton > button[kind="primary"] { background:#C8102E; border-color:#C8102E; color:#fff; }

.tq { font-size:26px; font-weight:700; line-height:1.25; margin:10px 0 6px; }
.tq-hint { font-size:18px; color:#51605A; margin-bottom:12px; }

.group { font-size:16px; font-weight:700; color:#51605A; margin:22px 0 8px;
  display:flex; align-items:center; gap:8px; }
.group i { width:10px; height:10px; border-radius:50%; display:inline-block; }

.dhead { border-left:8px solid var(--c); padding:4px 0 4px 14px; margin:4px 0 16px; }
.dhead h1 { font-size:32px; line-height:1.15; margin:0; padding:0; }
.dhead p { margin:6px 0 0; color:#51605A; font-size:18px; }
.urgent { display:flex; gap:12px; align-items:center; background:#FBE7EA; border-radius:12px;
  padding:12px 14px; margin-bottom:12px; font-weight:700; font-size:18px; }
.urgent a.call { margin-left:auto; font-size:17px; padding:8px 14px; }

.stepdesc { color:#51605A; font-size:17px; margin:-6px 0 4px 32px; }
div[data-testid="stCheckbox"] label p { font-size:20px; }

.guide .count { color:#51605A; font-weight:700; }
.guide .num { font-size:72px; font-weight:700; line-height:1; color:var(--c); margin:8px 0; }
.guide .title { font-size:26px; font-weight:700; line-height:1.25; }
.guide .desc { font-size:18px; color:#51605A; margin-top:10px; }

.box { border-radius:12px; padding:14px 16px; margin-top:14px; font-size:17px; }
.box h3 { margin:0 0 6px; font-size:18px; padding:0; }
.box ul { margin:0; padding-left:20px; }
.box.red { background:#FBE7EA; }
.box.amber { background:#FCEFD9; }
.pic img { width:100%; max-width:340px; display:block; margin:6px 0 4px; }
.note { margin-top:28px; font-size:15px; color:#51605A; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="topbar">
  <div class="brand"><span class="logo">+</span>{T["brand"]}</div>
  <a class="call" href="tel:112">📞 112</a>
</div>""", unsafe_allow_html=True)


def set_lang():
    st.query_params["lang"] = st.session_state.lang


st.radio("Language", ["bg", "en"], key="lang", horizontal=True, on_change=set_lang,
         format_func=lambda x: {"bg": "Български", "en": "English"}[x],
         label_visibility="collapsed")

METRONOME = """
<div style="display:flex;align-items:center;gap:12px;background:#DDF0EB;border-radius:12px;
  padding:10px 14px;font-family:system-ui,sans-serif;font-size:16px;color:#13201B">
  <button id="b" style="border:0;background:#11695A;color:#fff;font-weight:700;border-radius:10px;
    padding:10px 16px;min-height:44px;font-size:16px;cursor:pointer">__START__</button>
  <div id="d" style="width:18px;height:18px;border-radius:50%;background:#11695A;opacity:.25"></div>
  <span>__HINT__</span>
</div>
<script>
let t=null, ctx=null;
const b=document.getElementById('b'), d=document.getElementById('d');
function tick(){
  d.style.opacity=1; setTimeout(()=>d.style.opacity=.25,120);
  const o=ctx.createOscillator(), g=ctx.createGain();
  o.frequency.value=880; g.gain.setValueAtTime(.25,ctx.currentTime);
  g.gain.exponentialRampToValueAtTime(.001,ctx.currentTime+.08);
  o.connect(g).connect(ctx.destination); o.start(); o.stop(ctx.currentTime+.09);
}
b.onclick=()=>{
  if(t){clearInterval(t);t=null;b.textContent='__START__';return;}
  ctx=ctx||new (window.AudioContext||window.webkitAudioContext)(); ctx.resume();
  tick(); t=setInterval(tick,60000/110); b.textContent='__STOP__';
};
</script>
""".replace("__START__", T["beat_start"]).replace("__STOP__", T["beat_stop"]) \
   .replace("__HINT__", T["beat_hint"])


# ---------- navigation ----------
def open_card(card_id):
    st.query_params["card"] = card_id
    st.session_state.step = 0
    st.session_state.tri = None


def go_home():
    if "card" in st.query_params:
        del st.query_params["card"]   # keep ?lang= so the language stays
    st.session_state.tri = None


def triage_go(target):
    """Move to the next triage question, open a card, or close the triage."""
    if target.startswith("card:"):
        open_card(target[5:])
    elif target == "list":
        st.session_state.tri = None
    else:
        st.session_state.tri = target


def picture(step):
    """Show the step's illustration, if it has one."""
    if len(step) > 2 and step[2] in ILLUSTRATIONS:
        data = base64.b64encode(ILLUSTRATIONS[step[2]].encode()).decode()
        st.markdown(f'<div class="pic"><img src="data:image/svg+xml;base64,{data}" alt=""></div>',
                    unsafe_allow_html=True)


def box(kind, title, items):
    lis = "".join(f"<li>{html.escape(x)}</li>" for x in items)
    st.markdown(f'<div class="box {kind}"><h3>{html.escape(title)}</h3><ul>{lis}</ul></div>',
                unsafe_allow_html=True)


# ---------- triage screen ----------
def render_triage(node):
    question, hint, answers = TRIAGE[node]
    st.button(T["cancel"], key="tri_cancel", on_click=triage_go, args=("list",))
    st.markdown(f'<div class="tq">{html.escape(question)}</div>', unsafe_allow_html=True)
    if hint:
        st.markdown(f'<div class="tq-hint">{html.escape(hint)}</div>', unsafe_allow_html=True)
    for label, target in answers:
        st.button(label, key=f"tri_{node}_{target}", on_click=triage_go, args=(target,),
                  use_container_width=True)
    st.markdown(f'<p class="note">{html.escape(T["tri_note"])}</p>', unsafe_allow_html=True)


# ---------- home screen ----------
def render_home():
    node = st.session_state.get("tri")
    if node in TRIAGE:
        render_triage(node)
        return

    st.button(T["start_here"], key="tri_open", type="primary",
              on_click=triage_go, args=("start",), use_container_width=True)

    q = st.text_input("Search", placeholder=T["search"],
                      label_visibility="collapsed").strip().lower()
    found = [c for c in CARDS
             if not q or q in f'{c["title"]} {c["sub"]} {SEARCH_KEYS[c["id"]]}'.lower()]

    if not found:
        st.warning(T["no_match"].format(q=q))

    for sev, meta in SEV.items():
        group = [c for c in found if c["sev"] == sev]
        if not group:
            continue
        st.markdown(f'<div class="group"><i style="background:{meta["color"]}"></i>'
                    f'{html.escape(meta["label"])}</div>', unsafe_allow_html=True)
        for i, c in enumerate(group):
            if i % 2 == 0:              # new row every 2 tiles, so phones keep the same order
                cols = st.columns(2)
            cols[i % 2].button(c["title"], key=f'tile_{c["id"]}', help=c["sub"],
                               on_click=open_card, args=(c["id"],),
                               use_container_width=True)

    st.markdown(f'<p class="note">{html.escape(T["note"])}</p>', unsafe_allow_html=True)


# ---------- situation card ----------
def render_card(c):
    color = SEV[c["sev"]]["color"]
    st.button(T["all_situations"], on_click=go_home)

    st.markdown(f'<div class="dhead" style="--c:{color}"><h1>{html.escape(c["title"])}</h1>'
                f'<p>{html.escape(c["recognize"])}</p></div>', unsafe_allow_html=True)

    if c.get("call"):
        st.markdown(f'<div class="urgent">{html.escape(T["urgent"])}'
                    f'<a class="call" href="tel:112">{html.escape(T["call"])}</a></div>',
                    unsafe_allow_html=True)
    if c.get("metronome"):
        st.iframe(METRONOME, height=72)

    mode = st.radio("View", ["all", "one"], horizontal=True, key="mode",
                    format_func=lambda m: T["mode_all"] if m == "all" else T["mode_one"],
                    label_visibility="collapsed")

    steps = c["steps"]
    if mode == "all":
        for i, step in enumerate(steps):
            title, desc = step[0], step[1]
            with st.container(border=True):
                st.checkbox(f"**{i + 1}. {title}**", key=f'{c["id"]}_done_{i}')
                st.markdown(f'<div class="stepdesc">{html.escape(desc)}</div>',
                            unsafe_allow_html=True)
                picture(step)
    else:
        i = min(st.session_state.get("step", 0), len(steps) - 1)
        title, desc = steps[i][0], steps[i][1]
        with st.container(border=True):
            ink = SEV[c["sev"]].get("ink", color)   # darker shade for the big number, if set
            st.markdown(f'<div class="guide" style="--c:{ink}">'
                        f'<div class="count">{T["step_of"].format(i=i + 1, n=len(steps))}</div>'
                        f'<div class="num">{i + 1}</div>'
                        f'<div class="title">{html.escape(title)}</div>'
                        f'<div class="desc">{html.escape(desc)}</div></div>',
                        unsafe_allow_html=True)
            picture(steps[i])
            back, nxt = st.columns(2)
            if back.button(T["back"], disabled=i == 0, use_container_width=True):
                st.session_state.step = i - 1
                st.rerun()
            if nxt.button(T["next"], disabled=i == len(steps) - 1, type="primary",
                          use_container_width=True):
                st.session_state.step = i + 1
                st.rerun()

    box("red", T["when"], c["when"])
    box("amber", T["dont"], c["dont"])


card = BY_ID.get(st.query_params.get("card", ""))
if card:
    render_card(card)
else:
    render_home()
