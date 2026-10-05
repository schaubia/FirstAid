"""Simple SVG drawings shown under some steps. Keys are referenced from cards.py."""

BODY = 'fill="#E3EAE7" stroke="#51605A" stroke-width="3"'
HAND = 'fill="#11695A" fill-opacity="0.85" stroke="#0B4A3F" stroke-width="2"'
TARGET = 'fill="none" stroke="#C8102E" stroke-width="3" stroke-dasharray="6 4"'
LABEL = 'font-family="Arial, sans-serif" font-size="15" fill="#13201B"'
SMALL = 'font-family="Arial, sans-serif" font-size="13" fill="#51605A"'
CAPTION = 'font-family="Arial, sans-serif" font-size="15" fill="#51605A"'
LEADER = 'stroke="#13201B" stroke-width="1.5"'


def _svg(title, body, caption=(), h=250):
    lines = "".join(f'<text x="170" y="{h + 22 + i * 20}" text-anchor="middle" {CAPTION}>{t}</text>'
                    for i, t in enumerate(caption))
    total = h + 14 + 20 * len(caption)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 {total}" role="img">'
            f'<title>{title}</title>{body}{lines}</svg>')


# Front view of an adult torso, reused for adult / child drawings
def _torso(scale_head=26, shoulder=78):
    return f'''
  <circle cx="170" cy="36" r="{scale_head}" {BODY}/>
  <rect x="158" y="{36 + scale_head - 4}" width="24" height="16" {BODY}/>
  <path d="M{170 - shoulder} 86 Q{170 - shoulder} 70 {170 - shoulder + 22} 68 L{170 + shoulder - 22} 68
           Q{170 + shoulder} 70 {170 + shoulder} 86 L{170 + shoulder - 16} 240 L{170 - shoulder + 16} 240 Z" {BODY}/>
  <circle cx="{170 - shoulder / 2.2:.0f}" cy="118" r="4" fill="#51605A"/>
  <circle cx="{170 + shoulder / 2.2:.0f}" cy="118" r="4" fill="#51605A"/>
  <line x1="170" y1="78" x2="170" y2="160" stroke="#51605A" stroke-width="2" stroke-dasharray="3 4"/>'''


CPR_ADULT = _svg("Adult CPR hand position", _torso() + f'''
  <ellipse cx="170" cy="128" rx="28" ry="36" {HAND}/>
  <ellipse cx="170" cy="116" rx="28" ry="36" fill="#1E8C78" stroke="#0B4A3F" stroke-width="2"/>
  <path d="M152 92 L152 104 M161 88 L161 102 M170 86 L170 101 M179 88 L179 102 M188 92 L188 104"
        stroke="#0B4A3F" stroke-width="2" stroke-linecap="round"/>
  <line x1="200" y1="122" x2="262" y2="122" {LEADER}/>
  <text x="266" y="118" {LABEL}>2 hands,</text>
  <text x="266" y="136" {LABEL}>stacked</text>''',
  caption=("Centre of the chest, on the breastbone.", "Arms straight, press 5–6 cm deep."))

CPR_CHILD = _svg("Child CPR hand position", _torso(scale_head=30, shoulder=64) + f'''
  <ellipse cx="170" cy="136" rx="22" ry="30" {HAND}/>
  <line x1="194" y1="136" x2="250" y2="136" {LEADER}/>
  <text x="254" y="132" {LABEL}>Heel of</text>
  <text x="254" y="150" {LABEL}>1 hand</text>''',
  caption=("Lower half of the breastbone.", "Press about 5 cm (one third of the chest)."))

CPR_INFANT = _svg("Baby CPR and chest thrust finger position", f'''
  <circle cx="170" cy="52" r="42" {BODY}/>
  <path d="M112 116 Q112 98 132 96 L208 96 Q228 98 228 116 L220 240 L120 240 Z" {BODY}/>
  <circle cx="146" cy="128" r="3.5" fill="#51605A"/>
  <circle cx="194" cy="128" r="3.5" fill="#51605A"/>
  <line x1="116" y1="128" x2="224" y2="128" stroke="#C8102E" stroke-width="2" stroke-dasharray="5 4"/>
  <rect x="159" y="134" width="9" height="30" rx="4.5" {HAND}/>
  <rect x="171" y="134" width="9" height="30" rx="4.5" {HAND}/>
  <line x1="224" y1="128" x2="250" y2="116" {LEADER}/>
  <text x="252" y="112" {SMALL}>Nipple line</text>
  <line x1="182" y1="150" x2="250" y2="156" {LEADER}/>
  <text x="252" y="154" {LABEL}>2 fingers,</text>
  <text x="252" y="172" {LABEL}>just below</text>''',
  caption=("Press about 4 cm (one third of the chest).", "Same spot for chest thrusts when choking."))

ABDOMINAL = _svg("Abdominal thrust hand position", _torso() + f'''
  <circle cx="170" cy="212" r="4" fill="#51605A"/>
  <circle cx="170" cy="182" r="17" {HAND}/>
  <path d="M146 192 Q170 210 194 192" fill="none" stroke="#0B4A3F" stroke-width="7" stroke-linecap="round" stroke-opacity="0.7"/>
  <line x1="152" y1="178" x2="30" y2="178" {LEADER}/>
  <text x="10" y="170" {LABEL}>Fist</text>
  <line x1="166" y1="212" x2="30" y2="226" {LEADER}/>
  <text x="10" y="222" {SMALL}>Belly</text>
  <text x="10" y="237" {SMALL}>button</text>
  <path d="M272 220 L272 164" stroke="#C8102E" stroke-width="4"/>
  <path d="M262 176 L272 160 L282 176" fill="none" stroke="#C8102E" stroke-width="4" stroke-linejoin="round"/>
  <text x="286" y="194" {LABEL}>In</text>
  <text x="286" y="212" {LABEL}>and up</text>''',
  caption=("Stand behind. Fist just above the belly button,", "other hand over it. Pull sharply in and up."))

BACK_BLOWS = _svg("Back blow position", f'''
  <circle cx="170" cy="36" r="26" {BODY}/>
  <rect x="158" y="58" width="24" height="16" {BODY}/>
  <path d="M92 86 Q92 70 114 68 L226 68 Q248 70 248 86 L232 240 L108 240 Z" {BODY}/>
  <path d="M124 92 Q132 132 150 124" fill="none" stroke="#51605A" stroke-width="2.5"/>
  <path d="M216 92 Q208 132 190 124" fill="none" stroke="#51605A" stroke-width="2.5"/>
  <line x1="170" y1="76" x2="170" y2="236" stroke="#51605A" stroke-width="2" stroke-dasharray="3 4"/>
  <ellipse cx="170" cy="108" rx="24" ry="20" {HAND}/>
  <circle cx="170" cy="108" r="36" {TARGET}/>
  <line x1="206" y1="112" x2="262" y2="132" {LEADER}/>
  <text x="262" y="150" {LABEL}>Heel of</text>
  <text x="262" y="168" {LABEL}>the hand</text>''',
  caption=("Seen from behind: firm blows", "between the shoulder blades."))

LIMB = 'stroke="#7F948C" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" fill="none"'
TOP_LIMB = 'stroke="#11695A" stroke-width="18" stroke-linecap="round" stroke-linejoin="round" fill="none"'

RECOVERY = _svg("Recovery position, seen from above", f'''
  <polyline points="116,104 122,166 156,176" {LIMB}/>
  <path d="M96 76 Q150 66 214 84 L214 118 Q150 128 96 116 Z" fill="#7F948C"/>
  <polyline points="212,94 312,92" {LIMB}/>
  <polyline points="202,108 222,172 292,176" {TOP_LIMB}/>
  <polyline points="106,108 96,140 64,132" {TOP_LIMB}/>
  <circle cx="62" cy="104" r="26" fill="#7F948C"/>
  <path d="M40 116 L32 124 L44 126" fill="#7F948C"/>
  <line x1="60" y1="140" x2="44" y2="196" {LEADER}/>
  <text x="10" y="212" {SMALL}>Hand under cheek</text>
  <line x1="36" y1="126" x2="18" y2="60" {LEADER}/>
  <text x="10" y="50" {SMALL}>Mouth pointing down</text>
  <line x1="156" y1="184" x2="160" y2="212" {LEADER}/>
  <text x="122" y="228" {SMALL}>Other arm out</text>
  <line x1="236" y1="180" x2="256" y2="200" {LEADER}/>
  <text x="222" y="214" {SMALL}>Top knee bent</text>
  <text x="222" y="229" {SMALL}>stops rolling</text>''',
  caption=("Seen from above: on the side, head tilted", "back slightly so the airway stays open."))

BABY = 'fill="#E3EAE7" stroke="#51605A" stroke-width="2.5"'

BACK_BLOWS_INFANT = _svg("Baby back blows: face down along the forearm", f'''
  <line x1="318" y1="206" x2="96" y2="222" stroke="#CBD5D1" stroke-width="34" stroke-linecap="round"/>
  <line x1="300" y1="126" x2="78" y2="174" stroke="#7F948C" stroke-width="30" stroke-linecap="round"/>
  <ellipse cx="192" cy="112" rx="64" ry="22" transform="rotate(-12 192 112)" {BABY}/>
  <line x1="246" y1="104" x2="268" y2="142" stroke="#E3EAE7" stroke-width="12" stroke-linecap="round"/>
  <line x1="150" y1="124" x2="146" y2="164" stroke="#E3EAE7" stroke-width="11" stroke-linecap="round"/>
  <circle cx="112" cy="134" r="25" {BABY}/>
  <polyline points="66,176 84,168 100,156" fill="none" stroke="#11695A" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <ellipse cx="160" cy="84" rx="22" ry="15" transform="rotate(-12 160 84)" {HAND}/>
  <path d="M202 30 L172 66" stroke="#C8102E" stroke-width="4"/>
  <path d="M168 52 L170 70 L187 64" fill="none" stroke="#C8102E" stroke-width="4" stroke-linejoin="round"/>
  <text x="208" y="32" {LABEL}>Heel of hand,</text>
  <text x="208" y="50" {LABEL}>between the</text>
  <text x="208" y="68" {LABEL}>shoulder blades</text>
  <line x1="96" y1="112" x2="60" y2="70" {LEADER}/>
  <text x="10" y="44" {SMALL}>Head lower</text>
  <text x="10" y="60" {SMALL}>than the body</text>
  <line x1="68" y1="182" x2="46" y2="214" {LEADER}/>
  <text x="10" y="230" {SMALL}>Fingers hold the jaw</text>
  <line x1="250" y1="226" x2="250" y2="236" {LEADER}/>
  <text x="170" y="249" {SMALL}>Rest your arm on your thigh</text>''',
  caption=("Baby face down along your forearm, head lower.", "Hold the jaw, never the soft throat."), h=252)

ILLUSTRATIONS = {
    "cpr_adult": CPR_ADULT,
    "cpr_child": CPR_CHILD,
    "cpr_infant": CPR_INFANT,
    "abdominal": ABDOMINAL,
    "back_blows": BACK_BLOWS,
    "back_blows_infant": BACK_BLOWS_INFANT,
    "recovery": RECOVERY,
}


# ---------- kinesio taping ----------
TAPE1 = 'stroke="#11695A" stroke-opacity="0.9"'   # strip 1 - teal
TAPE2 = 'stroke="#E09A12" stroke-opacity="0.95"'  # strip 2 - amber
STRETCH = 'stroke="#FFFFFF" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
BADGE_TXT = 'font-family="Arial, sans-serif" font-size="14" font-weight="700" fill="#fff" text-anchor="middle"'


def _badge(x, y, n, color):
    return (f'<circle cx="{x}" cy="{y}" r="11" fill="{color}"/>'
            f'<text x="{x}" y="{y + 5}" {BADGE_TXT}>{n}</text>')


def _lines(x, y, lines, style=SMALL, step=16):
    return "".join(f'<text x="{x}" y="{y + i * step}" {style}>{t}</text>' for i, t in enumerate(lines))


# Ankle, seen from behind
_LEG = ("M120,0 C112,35 110,70 128,100 C138,118 146,130 147,140 C139,142 136,152 143,158 "
        "C141,170 139,190 143,203 C148,215 188,215 193,203 C197,190 196,176 194,166 "
        "C201,162 201,150 191,148 C190,134 192,120 200,102 C217,70 216,35 208,0")
_FOOT = ("M128,214 C128,204 139,200 150,202 L186,202 C197,200 208,204 208,214 "
         "C208,220 199,222 168,222 C137,222 128,220 128,214 Z")

ANKLE_TEXT = {
    "en": dict(title="Kinesio tape on the ankle, seen from behind",
               start=["Start on the", "inner side"],
               stretch=["Half stretch", "over the outer", "ankle bone"],
               back=["Around the", "back of the heel"],
               caption=("Seen from behind, foot at a right angle.",
                        "Stick the ends on without stretch.")),
    "bg": dict(title="Кинезио тейп на глезена, изглед отзад",
               start=["Начало от", "вътрешната", "страна"],
               stretch=["Половин", "опъване над", "външния глезен"],
               back=["Около петата", "отзад"],
               caption=("Изглед отзад, стъпалото под прав ъгъл.",
                        "Краищата се залепват без опъване.")),
}


def tape_ankle(lang="en"):
    t = ANKLE_TEXT[lang]
    body = f'''
  <line x1="40" y1="223" x2="300" y2="223" stroke="#CBD5D1" stroke-width="3" stroke-linecap="round"/>
  <path d="{_FOOT}" fill="#D3DDD9" stroke="#51605A" stroke-width="2.5"/>
  <path d="{_LEG} Z" fill="#E3EAE7"/>
  <path d="{_LEG}" fill="none" stroke="#51605A" stroke-width="3" stroke-linejoin="round"/>
  <path d="M160,110 C161,138 162,160 162,178 M174,110 C173,138 172,160 172,178"
        fill="none" stroke="#9AACA5" stroke-width="2" stroke-linecap="round"/>

  <path d="M125,45 C126,72 134,95 141,112 C148,126 151,136 151,146 C149,160 148,178 150,194
           C153,210 183,210 186,194 C188,178 187,166 186,156 C185,140 185,128 190,112 C197,95 204,72 204,45"
        fill="none" {TAPE1} stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
  <g {STRETCH}>
    <line x1="186" y1="140" x2="186" y2="172"/>
    <polyline points="182,145 186,139 190,145"/>
    <polyline points="182,167 186,173 190,167"/>
  </g>
  <path d="M145,176 C156,184 180,184 191,176" fill="none" {TAPE2} stroke-width="12" stroke-linecap="round"/>

  {_badge(104, 46, 1, "#11695A")}
  <line x1="62" y1="68" x2="95" y2="53" {LEADER}/>
  {_lines(10, 82, t["start"])}
  <line x1="196" y1="156" x2="230" y2="132" {LEADER}/>
  {_lines(234, 112, t["stretch"])}
  {_badge(216, 188, 2, "#E09A12")}
  {_lines(234, 186, t["back"])}'''
    return _svg(t["title"], body, caption=t["caption"])


# Knee: front view + side view with the knee bent
TAPE3 = 'stroke="#4F7FA8" stroke-opacity="0.9"'   # side X - blue-grey, goes on first

KNEE_TEXT = {
    "en": dict(title="Kinesio tape on the knee, front and side",
               front="Front", side="From the side",
               caption=("Y-strip: base above the kneecap, tails around",
                        "both sides with light stretch. Knee bent.",
                        "Strip 2 is optional: half stretch below it.",
                        "X: if the side hurts, put it on first, under the Y.")),
    "bg": dict(title="Кинезио тейп на коляното, отпред и отстрани",
               front="Отпред", side="Отстрани",
               caption=("Y-лента: основата над капачката, опашките",
                        "от двете ѝ страни с леко опъване.",
                        "Коляно свито. Лента 2 е по желание.",
                        "X при болка отстрани: слага се първа, под Y.")),
}

_F_FILL = ("M48,0 C50,60 52,95 54,118 C54,135 58,150 60,170 C62,200 62,220 62,232 "
           "L108,232 C108,220 108,200 110,170 C112,150 116,135 116,118 C118,95 120,60 122,0 Z")
_F_LEFT = "M48,0 C50,60 52,95 54,118 C54,135 58,150 60,170 C62,200 62,220 62,232"
_F_RIGHT = "M122,0 C120,60 118,95 116,118 C116,135 112,150 110,170 C108,200 108,220 108,232"
_S_FILL = ("M178,58 L280,58 C300,58 312,70 312,92 C312,110 306,130 304,150 C302,180 300,210 298,232 "
           "L268,232 C266,210 252,185 252,160 C252,138 258,124 256,114 L178,112 Z")
_S_TOP = "M178,58 L280,58 C300,58 312,70 312,92 C312,110 306,130 304,150 C302,180 300,210 298,232"
_S_BACK = "M178,112 L256,114 C258,124 252,138 252,160 C252,185 266,210 268,232"


def tape_knee(lang="en"):
    t = KNEE_TEXT[lang]
    body = f'''
  <line x1="170" y1="8" x2="170" y2="236" stroke="#CBD5D1" stroke-width="2" stroke-dasharray="4 5"/>

  <path d="{_F_FILL}" fill="#E3EAE7"/>
  <path d="{_F_LEFT}" fill="none" stroke="#51605A" stroke-width="3"/>
  <path d="{_F_RIGHT}" fill="none" stroke="#51605A" stroke-width="3"/>
  <ellipse cx="85" cy="118" rx="17" ry="20" fill="#D3DDD9" stroke="#51605A" stroke-width="2.5"/>
  <line x1="85" y1="30" x2="85" y2="84" {TAPE1} stroke-width="15" stroke-linecap="round"/>
  <path d="M85,80 C66,88 60,108 62,126 C64,144 70,158 76,172" fill="none" {TAPE1} stroke-width="8" stroke-linecap="round"/>
  <path d="M85,80 C104,88 110,108 108,126 C106,144 100,158 94,172" fill="none" {TAPE1} stroke-width="8" stroke-linecap="round"/>
  <path d="M66,151 C76,156 94,156 104,151" fill="none" {TAPE2} stroke-width="10" stroke-linecap="round"/>
  <g {STRETCH}>
    <line x1="78" y1="154.5" x2="92" y2="154.5"/>
    <polyline points="82,151 77,154.5 82,158"/>
    <polyline points="88,151 93,154.5 88,158"/>
  </g>
  {_badge(63, 34, 1, "#11695A")}
  {_badge(127, 152, 2, "#E09A12")}
  <text x="85" y="250" text-anchor="middle" {SMALL}>{t["front"]}</text>

  <path d="{_S_FILL}" fill="#E3EAE7"/>
  <path d="{_S_TOP}" fill="none" stroke="#51605A" stroke-width="3" stroke-linejoin="round"/>
  <path d="{_S_BACK}" fill="none" stroke="#51605A" stroke-width="3" stroke-linejoin="round"/>
  <ellipse cx="302" cy="88" rx="9" ry="17" fill="#D3DDD9" stroke="#51605A" stroke-width="2.5"/>
  <line x1="265" y1="80" x2="293" y2="108" {TAPE3} stroke-width="9" stroke-linecap="round"/>
  <line x1="293" y1="80" x2="265" y2="108" {TAPE3} stroke-width="9" stroke-linecap="round"/>
  <line x1="206" y1="67" x2="262" y2="67" {TAPE1} stroke-width="12" stroke-linecap="round"/>
  <path d="M260,67 C280,67 289,78 289,92 C289,108 291,122 295,140" fill="none" {TAPE1} stroke-width="8" stroke-linecap="round"/>
  <path d="M290,121 C296,124 302,124 306,121" fill="none" {TAPE2} stroke-width="9" stroke-linecap="round"/>
  {_badge(206, 42, 1, "#11695A")}
  {_badge(322, 124, 2, "#E09A12")}
  {_badge(246, 124, "X", "#4F7FA8")}
  <text x="255" y="250" text-anchor="middle" {SMALL}>{t["side"]}</text>'''
    return _svg(t["title"], body, caption=t["caption"], h=256)


ILLUSTRATIONS["tape_ankle"] = tape_ankle("en")
ILLUSTRATIONS["tape_knee"] = tape_knee("en")

# Bulgarian versions. A drawing missing here falls back to the English one above.
ILLUSTRATIONS_BG = {
    "tape_ankle": tape_ankle("bg"),
    "tape_knee": tape_knee("bg"),
}
