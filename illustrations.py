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
