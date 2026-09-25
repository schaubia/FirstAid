import html

import streamlit as st

from cards import CARDS, SEV

st.set_page_config(page_title="First Aid", page_icon="⛑️", layout="centered",
                   initial_sidebar_state="collapsed")

BY_ID = {c["id"]: c for c in CARDS}

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
.note { margin-top:28px; font-size:15px; color:#51605A; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="topbar">
  <div class="brand"><span class="logo">+</span>First Aid</div>
  <a class="call" href="tel:112">📞 112</a>
</div>""", unsafe_allow_html=True)

METRONOME = """
<div style="display:flex;align-items:center;gap:12px;background:#DDF0EB;border-radius:12px;
  padding:10px 14px;font-family:system-ui,sans-serif;font-size:16px;color:#13201B">
  <button id="b" style="border:0;background:#11695A;color:#fff;font-weight:700;border-radius:10px;
    padding:10px 16px;min-height:44px;font-size:16px;cursor:pointer">▶ Compression beat</button>
  <div id="d" style="width:18px;height:18px;border-radius:50%;background:#11695A;opacity:.25"></div>
  <span>110 per minute — push on each beat</span>
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
  if(t){clearInterval(t);t=null;b.textContent='▶ Compression beat';return;}
  ctx=ctx||new (window.AudioContext||window.webkitAudioContext)(); ctx.resume();
  tick(); t=setInterval(tick,60000/110); b.textContent='■ Stop beat';
};
</script>
"""


# ---------- navigation ----------
def open_card(card_id):
    st.query_params["card"] = card_id
    st.session_state.step = 0


def go_home():
    st.query_params.clear()


def box(kind, title, items):
    lis = "".join(f"<li>{html.escape(x)}</li>" for x in items)
    st.markdown(f'<div class="box {kind}"><h3>{title}</h3><ul>{lis}</ul></div>',
                unsafe_allow_html=True)


# ---------- home screen ----------
def render_home():
    q = st.text_input("Search", placeholder="🔍 What happened? e.g. burn, choking",
                      label_visibility="collapsed").strip().lower()
    found = [c for c in CARDS
             if not q or q in f'{c["title"]} {c["sub"]} {c["keys"]}'.lower()]

    if not found:
        st.warning(f"Nothing matches “{q}”. If someone is in danger, call 112 now.")

    for sev, meta in SEV.items():
        group = [c for c in found if c["sev"] == sev]
        if not group:
            continue
        st.markdown(f'<div class="group"><i style="background:{meta["color"]}"></i>'
                    f'{meta["label"]}</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, c in enumerate(group):
            cols[i % 2].button(c["title"], key=f'tile_{c["id"]}', help=c["sub"],
                               on_click=open_card, args=(c["id"],),
                               use_container_width=True)

    st.markdown('<p class="note">For guidance only — it doesn\'t replace a first aid course '
                'or the 112 operator. Follow the operator\'s instructions when you call.</p>',
                unsafe_allow_html=True)


# ---------- situation card ----------
def render_card(c):
    color = SEV[c["sev"]]["color"]
    st.button("‹ All situations", on_click=go_home)

    st.markdown(f'<div class="dhead" style="--c:{color}"><h1>{html.escape(c["title"])}</h1>'
                f'<p>{html.escape(c["recognize"])}</p></div>', unsafe_allow_html=True)

    if c.get("call"):
        st.markdown('<div class="urgent">Call 112 now, then follow the steps.'
                    '<a class="call" href="tel:112">Call 112</a></div>',
                    unsafe_allow_html=True)
    if c.get("metronome"):
        st.iframe(METRONOME, height=72)

    mode = st.radio("View", ["All steps", "One at a time"], horizontal=True,
                    label_visibility="collapsed", key="mode")

    steps = c["steps"]
    if mode == "All steps":
        for i, (title, desc) in enumerate(steps):
            with st.container(border=True):
                st.checkbox(f"**{i + 1}. {title}**", key=f'{c["id"]}_done_{i}')
                st.markdown(f'<div class="stepdesc">{html.escape(desc)}</div>',
                            unsafe_allow_html=True)
    else:
        i = min(st.session_state.get("step", 0), len(steps) - 1)
        title, desc = steps[i]
        with st.container(border=True):
            st.markdown(f'<div class="guide" style="--c:{color}">'
                        f'<div class="count">Step {i + 1} of {len(steps)}</div>'
                        f'<div class="num">{i + 1}</div>'
                        f'<div class="title">{html.escape(title)}</div>'
                        f'<div class="desc">{html.escape(desc)}</div></div>',
                        unsafe_allow_html=True)
            back, nxt = st.columns(2)
            if back.button("Back", disabled=i == 0, use_container_width=True):
                st.session_state.step = i - 1
                st.rerun()
            if nxt.button("Next", disabled=i == len(steps) - 1, type="primary",
                          use_container_width=True):
                st.session_state.step = i + 1
                st.rerun()

    box("red", "Call 112 if", c["when"])
    box("amber", "Don't", c["dont"])


card = BY_ID.get(st.query_params.get("card", ""))
if card:
    render_card(card)
else:
    render_home()
