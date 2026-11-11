"""Scenes for 003-axeman-new-orleans (New Orleans, 1918-1919). Gore-free: shadows, a letter, music."""
import random
from toon import *

SCENES = {}


def rowhouses(y, seed=1, lit=.35, cols=("#5b4452", "#44536b", "#6b5a44"), n=3, w=520, h=1100):
    r = random.Random(seed); g = ""
    for k in range(n):
        x = k * (w + 6) - 60; col = cols[k % len(cols)]
        g += f'<g {OUT}><rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{col}"/><rect x="{x - 14}" y="{y - h - 30}" width="{w + 28}" height="38" fill="#2a2430"/>'
        for row in range(3):
            for c in range(2):
                wx, wy = x + 80 + c * 220, y - h + 100 + row * 300
                on = r.random() < lit
                g += f'<rect x="{wx}" y="{wy}" width="110" height="180" rx="8" fill="{"#f3c555" if on else "#12141d"}"/><path d="M{wx + 55},{wy} v180 M{wx},{wy + 90} h110" fill="none" stroke-width="3"/>'
            by = y - h + 300 + row * 300
            g += f'<path d="M{x + 20},{by} h{w - 40}" stroke-width="10" fill="none"/>' + "".join(f'<path d="M{x + 30 + j * 32},{by} v-52" stroke-width="5" fill="none"/>' for j in range((w - 60) // 32 + 1))
        g += f'<rect x="{x + w // 2 - 50}" y="{y - 220}" width="100" height="220" rx="10" fill="#2a1d15"/></g>'
    return g


def gaslamp(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-10" y="-520" width="20" height="520" fill="#1a1d27"/>'
            '<path d="M-34,-520 h68 l-12,-60 h-44Z" fill="#1a1d27"/><rect x="-24" y="-600" width="48" height="84" rx="8" fill="#ffd76a"/></g>')


def notes(seed, n=14, col="#ffd76a"):
    r = random.Random(seed)
    return "".join(f'<text x="{r.randint(60, 1250)}" y="{r.randint(500, 2200)}" font-size="{r.randint(70, 130)}" fill="{col}" '
                   f'stroke="#0d0f15" stroke-width="4" opacity=".85" transform="rotate({r.randint(-25, 25)} 600 1000)">{r.choice("♪♫")}</text>' for _ in range(n))


# 1. New Orleans, a gas-lit street at night
SCENES["street"] = dict(
    bg=sky("#0d1226", "#4a4560") + stars(41, 30, 700) + moon(1080, 380, 90),
    mid=rowhouses(1900, 3, .3) + fog(1750, 450, op=.4) + '<rect y="1900" width="1350" height="500" fill="#2d2a30"/>'
        + "".join(f'<path d="M{x},1900 q80,60 0,120" fill="none" stroke="#1a171d" stroke-width="5" opacity=".6"/>' for x in range(0, 1400, 110)),
    fg=gaslamp(1150, 2400, 1.9),
    glow=glow(1150 - 40, 1230, 520, "#ffd76a", .6),
)

# 2. The letter
_scrawl = "".join(f'<path d="M{330},{y} q60,-40 120,0 t120,0 t120,0 t120,0" fill="none" stroke="#1c1612" stroke-width="7"/>' for y in range(1000, 1900, 120))
SCENES["letter"] = dict(
    bg='<rect width="1350" height="2400" fill="#2a1c14"/>' + "".join(f'<path d="M0,{y} H1350" stroke="#0d0f15" stroke-width="5" opacity=".5"/>' for y in range(0, 2400, 190)),
    mid='<g transform="rotate(-4 675 1400)" stroke="#0d0f15" stroke-width="8"><rect x="230" y="760" width="900" height="1300" fill="#e9dcb8"/></g>'
        '<g transform="rotate(-4 675 1400)">' + _scrawl + '<text x="300" y="900" font-size="90" font-style="italic" fill="#1c1612">March 13, 1919</text></g>',
    fg='<rect width="1350" height="2400" fill="#05060a" opacity=".3"/>',
    glow=glow(1100, 600, 800, "#ff9a3a", .55),
)

# 3. A shadow at the window
SCENES["shadow"] = dict(
    bg='<rect width="1350" height="2400" fill="#3a3140"/>' + "".join(f'<path d="M0,{y} H1350" stroke="#0d0f15" stroke-width="4" opacity=".4"/>' for y in range(60, 2400, 150)),
    mid='<rect x="250" y="600" width="850" height="1300" rx="20" fill="#f3c555" stroke="#0d0f15" stroke-width="10"/><path d="M675,600 V1900 M250,1250 H1100" stroke="#0d0f15" stroke-width="10"/>'
        '<g fill="#0a0a10"><circle cx="620" cy="1070" r="70"/><path d="M520,1000 q100,-120 200,0 l20,6 h-240Z"/><path d="M540,1140 h160 l60,520 h-280Z"/>'
        '<path d="M760,1200 L900,860" stroke="#0a0a10" stroke-width="26"/><path d="M880,820 q70,-40 100,20 q-10,60 -80,70Z"/></g>'
        '<path d="M170,1900 H1180 V2000 H170Z" fill="#2a1d15" stroke="#0d0f15" stroke-width="8"/>',
    fg=bush(90, 2400, 1.6) + bush(1250, 2400, 1.5),
    glow=glow(675, 1250, 700, "#ffb347", .45),
)

# 4. A jazz band in a parlour
def _horn(x, y, flip=1):
    return (f'<g transform="translate({x},{y}) scale({flip},1)" {OUT}><path d="M0,0 h140 l70,-40 v100 l-70,-40 h-140Z" fill="#e8b84a"/><circle cx="210" cy="10" r="14" fill="#fff0b0" stroke="none"/></g>')


SCENES["jazz"] = dict(
    bg='<rect width="1350" height="2400" fill="#5a2f3c"/>' + "".join(f'<path d="M{x},0 V1700" stroke="#3a1c26" stroke-width="30" opacity=".5"/>' for x in range(40, 1350, 120))
       + '<rect y="1700" width="1350" height="700" fill="#33211a" stroke="#0d0f15" stroke-width="6"/>',
    mid=person(300, 2200, 1.7, coat="#2f4a6e", hat=True, arm="hold") + _horn(520, 1890)
        + person(1000, 2200, 1.7, coat="#6e2f3a", arm="hold", flip=True) + _horn(780, 1890, -1)
        + '<g stroke="#0d0f15" stroke-width="8"><rect x="450" y="1900" width="460" height="260" fill="#2a1d15"/><path d="M470,1900 h420" stroke="#f1efe6" stroke-width="30"/></g>',
    fg=notes(4, 12),
    glow=glow(675, 1500, 900, "#ffb347", .5),
)

# 5. Every window is lit and the whole street is playing
SCENES["party"] = dict(
    bg=sky("#0d1226", "#6a4a68") + stars(42, 25, 600),
    mid=rowhouses(1900, 5, .95) + '<rect y="1900" width="1350" height="500" fill="#2d2a30"/>' + fog(1950, 250, op=.3),
    fg=notes(7, 16),
    glow=glow(675, 1300, 1000, "#ffb347", .5),
)

# 6. Dawn, everyone safe
SCENES["dawn"] = dict(
    bg=sky("#f0a86a", "#ffe3a8") + '<circle cx="675" cy="1550" r="210" fill="#fff3c0"/>',
    mid=rowhouses(1900, 8, .1, cols=("#7a5a62", "#5a6a84", "#8a7656")) + '<rect y="1900" width="1350" height="500" fill="#5a4f50"/>',
    fg=gaslamp(200, 2400, 1.8),
    glow=glow(675, 1550, 800, "#ffd9a0", .6),
)

# 7. The man who was never found
SCENES["alley"] = dict(
    bg=sky("#05060d", "#1c2033"),
    mid='<path d="M0,0 L420,900 H930 L1350,0Z" fill="#14161f" stroke="#0d0f15" stroke-width="6"/><path d="M0,2400 L420,1500 H930 L1350,2400Z" fill="#2a2630" stroke="#0d0f15" stroke-width="6"/>'
        '<path d="M0,0 L420,900 V1500 L0,2400Z" fill="#242634" stroke="#0d0f15" stroke-width="6"/><path d="M1350,0 L930,900 V1500 L1350,2400Z" fill="#242634" stroke="#0d0f15" stroke-width="6"/>'
        '<rect x="420" y="900" width="510" height="600" fill="#0b0c12"/>' + fog(1300, 450, op=.45)
        + person(675, 1500, .62, coat="#14151c", pants="#0a0a10", back=True, hat=True),
    fg='<rect width="1350" height="2400" fill="#02030a" opacity=".25"/>',
    glow=glow(675, 1300, 600, "#cfd6e4", .3),
)
