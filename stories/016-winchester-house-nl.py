"""Scenes for 016-winchester-house (Winchester Mystery House, San Jose, California, 1884-1922). Animated Sarah (human rig) and a ghost (lady rig)."""
import math
from toon import *

SCENES = {}
sn = math.sin
DARK = "#2a2a36"


def mansion(x, y, s=1.0, lit=7, seed=3):
    r = random.Random(seed)
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}>'
    g += '<rect x="-520" y="-520" width="1040" height="520" fill="#4a4258"/>'
    g += '<path d="M-560,-520 L-300,-760 L-40,-520Z M-100,-520 L200,-820 L500,-520 L560,-520 L560,-500 L-100,-500Z" fill="#2a2430"/>'
    g += '<rect x="330" y="-1000" width="150" height="500" fill="#524a62"/><path d="M310,-1000 L405,-1120 L500,-1000Z" fill="#2a2430"/>'
    g += '<rect x="-470" y="-700" width="120" height="200" fill="#524a62"/><path d="M-490,-700 L-410,-790 L-330,-700Z" fill="#2a2430"/>'
    for i in range(14):
        wx = -480 + (i % 7) * 140; wy = -460 + (i // 7) * 200 + (0 if i < 7 else -30)
        lt = r.random() < lit / 14
        g += f'<rect x="{wx}" y="{wy}" width="64" height="110" fill="{"#f3c555" if lt else "#14121a"}"/>'
    g += '<rect x="360" y="-940" width="60" height="100" fill="#f3c555"/><rect x="-60" y="-200" width="120" height="200" fill="#2a1d15"/>'
    return g + '</g>'


def beam_frame(x, y, w, h, n=5):
    g = f'<g {OUT} fill="#8a6a40">'
    g += f'<rect x="{x}" y="{y}" width="24" height="{h}"/><rect x="{x + w}" y="{y}" width="24" height="{h}"/><rect x="{x}" y="{y}" width="{w + 24}" height="24"/>'
    g += f'<rect x="{x}" y="{y + h / 2}" width="{w + 24}" height="22"/>'
    for i in range(1, n):
        g += f'<rect x="{x + w * i / n}" y="{y}" width="20" height="{h}"/>'
    g += f'<path d="M{x},{y + h} L{x + w},{y} M{x + w + 24},{y + h} L{x},{y + 24}" stroke-width="12" fill="none"/>'
    return g + '</g>'


def room(col="#2c1f2e"):
    return (f'<rect width="1350" height="2400" fill="{col}"/>'
            + "".join(f'<path d="M{x},0 V2400" stroke="#0d0f15" stroke-width="4" opacity=".35"/>' for x in range(0, 1350, 110))
            + f'<rect x="-20" y="2200" width="1400" height="300" fill="#1e1520" {OUT}/>')


def table_orb(x, y, t):
    fl = 1 + sn(t * 8) * .1
    return (f'<g transform="translate({x},{y})" {OUT}><path d="M-260,0 Q0,-50 260,0 L220,40 L-220,40Z" fill="#5a3b24"/><rect x="-30" y="40" width="60" height="260" fill="#4a3220"/>'
            f'<circle cx="0" cy="-70" r="62" fill="#a8d4ff" opacity=".85"/><path d="M-50,-4 h100 l-14,-30 h-72z" fill="#3a2a22"/>'
            f'<rect x="-190" y="-80" width="22" height="80" fill="#e8e0c8"/><path d="M-179,-80 q-10,-30 0,-50 q10,20 0,50" fill="#ffd45a" transform="scale(1,{fl:.2f})"/></g>')


# 1. Night: Sarah walks up to the huge, ever-growing mansion with a lantern
SCENES["mansion"] = dict(
    bg=sky("#0a0f20", "#403a58") + stars(61, 50, 900) + moon(1100, 420, 110) + clouds(62, "#0d1226", 4, 700, .7),
    mid=mansion(780, 1900, 1.15) + ground(1900, "#1c2620", 63, False),
    fg=fog(1850, 350, op=.25) + grass(2330, seed=64, n=10),
    glow=glow(780, 1400, 800, "#f3c555", .1),
    actor=dict(box=(0, 1500, 1350, 2330), fn=lambda ts, t: human(60 + ts * 85, 2260, 1.6, t, "walk", coat=DARK, pants=DARK, longhair=True, hold="lantern", expr="calm", look=(.9, -.3))),
)

# 2. The medium's warning: a candlelit seance, ghostly figures drift above the table
SCENES["medium"] = dict(
    bg=room("#241a2c") + f'<g {OUT}><rect x="860" y="900" width="300" height="420" fill="#14121a"/></g>',
    mid=table_orb(720, 1940, 0) + person(1100, 2000, 1.3, coat="#5a2f6a", pants="#2a1830", hair="#8a8a90"),
    fg='<rect width="1350" height="2400" fill="#0a0818" opacity=".15"/>',
    glow=glow(720, 1900, 700, "#9ad0ff", .3),
    actor=dict(box=(0, 500, 1350, 2330), fn=lambda ts, t: (
        lady(1000, 1300 + sn(t) * 20, .55, t, "glide", alpha=.55, gown="#cfd8e8")
        + lady(300, 1200 + sn(t + 2) * 20, .5, t + 1, "beckon", alpha=.5, gown="#cfd8e8", flip=True)
        + human(300, 2290, 1.6, t, "stand" if ts < 1 else "scared", coat=DARK, pants=DARK, longhair=True, expr="calm" if ts < 1 else "shocked", look=(.9, -.5)))),
)

# 3. Hammers day and night: Sarah points, a carpenter hauls timber past the open frame
SCENES["build"] = dict(
    bg=sky("#0a0f20", "#3a3550") + stars(65, 40, 900) + moon(250, 450, 100),
    mid=ground(1950, "#1c2620", 66, False) + beam_frame(180, 1100, 700, 850, 5) + beam_frame(900, 1450, 380, 500, 3)
        + f'<g {OUT}><rect x="560" y="1930" width="260" height="40" fill="#9a7a50"/><rect x="600" y="1890" width="200" height="40" fill="#8a6a40"/></g>' + lantern(250, 1500, 1.3) + lantern(820, 1300, 1.3),
    fg=fog(1950, 350, op=.2),
    glow=glow(500, 1500, 800, "#ffcf70", .25),
    actor=dict(box=(0, 1400, 1350, 2330), fn=lambda ts, t: (
        human(1050 + sn(t * .8) * 120, 2280, 1.35, t, "walk", coat="#6a5a46", hat=True, flip=(math.cos(t * .8) < 0), expr="calm")
        + human(220, 2270, 1.65, t, "point", coat=DARK, pants=DARK, longhair=True, expr="calm", look=(.9, 0)))),
)

# 4. Stairs that climb into the ceiling, a door that opens onto a wall
def _stairs():
    s = ''
    for i in range(9):
        x = 120 + i * 100; y = 2200 - i * 110
        s += f'<g {OUT}><rect x="{x}" y="{y}" width="100" height="{2260 - y}" fill="{"#6a4a30" if i % 2 else "#5a3b24"}"/><rect x="{x}" y="{y - 18}" width="100" height="22" fill="#8a6a40"/></g>'
    s += f'<g {OUT}><rect x="-20" y="1040" width="1400" height="110" fill="#1a1420"/><path d="M1000,1150 L1000,2200" stroke="#0d0f15" stroke-width="6"/></g>'
    s += f'<g {OUT}><rect x="1010" y="1300" width="230" height="420" fill="#3a2a22"/><circle cx="1210" cy="1520" r="14" fill="#e0b24a"/><rect x="1035" y="1330" width="180" height="150" fill="none" stroke-width="5"/></g>'
    return s


SCENES["stairs"] = dict(
    bg=room("#2a2030"),
    mid=_stairs(),
    fg='<rect width="1350" height="2400" fill="#0a0818" opacity=".15"/>',
    glow=glow(675, 1500, 900, "#ffcf70", .2),
    fog=False,
    actor=dict(box=(0, 1200, 1350, 2330), fn=lambda ts, t: human(110 + min(ts, 2.5) * 90, 2270, 1.5, t, "walk" if ts < 2.5 else "reach", coat=DARK, pants=DARK, longhair=True, hold=None, expr="calm" if ts < 2.5 else "shocked", look=(.9, -.6))),
)

# 5. Midnight: the great bell swings, a pale guest drifts past the tower
def _tower_bell(ts, t):
    a = sn(t * 3.2) * 24
    s = (f'<g transform="translate(675,1020) rotate({a:.1f})" {OUT}><rect x="-12" y="-80" width="24" height="90" fill="#3a2a22"/>'
         f'<path d="M-110,230 Q-100,60 0,40 Q100,60 110,230 Z" fill="#c9a43a"/><rect x="-120" y="220" width="240" height="28" rx="10" fill="#e0b24a"/>'
         f'<circle cx="0" cy="268" r="26" fill="#2a1d15"/></g>')
    return s + lady(260, 2200, 1.05, t, "glide", alpha=.6, gown="#cfd8e8", look=(.6, 0))


SCENES["bell"] = dict(
    bg=sky("#060814", "#2a2c4a") + stars(67, 70, 1200) + moon(1050, 420, 120)
       + f'<g {OUT}><rect x="360" y="800" width="630" height="1500" fill="#4a4258"/><path d="M330,800 L675,500 L1020,800Z" fill="#2a2430"/><rect x="500" y="880" width="350" height="440" fill="#14121a"/></g>',
    mid=f'<g {OUT}><circle cx="675" cy="620" r="70" fill="#e8e0d0"/><path d="M675,620 V570 M675,620 H730" stroke-width="7" fill="none"/></g>' + ground(2250, "#1c2620", 68, False),
    fg=fog(2000, 300, op=.25),
    glow=glow(675, 1100, 600, "#e0b24a", .15),
    actor=dict(box=(0, 900, 1350, 2330), fn=_tower_bell),
)

# 6. Today: a lantern-bearing visitor in the endless hallway, a ghost watching from the far end
def _hall():
    s = '<rect width="1350" height="2400" fill="#14101a"/>'
    s += f'<path d="M0,300 L500,900 L500,1500 L0,2100Z" fill="#3a2a30" {OUT}/><path d="M1350,300 L850,900 L850,1500 L1350,2100Z" fill="#3a2a30" {OUT}/>'
    s += f'<path d="M0,2100 L500,1500 L850,1500 L1350,2100 L1350,2420 L0,2420Z" fill="#241a20" {OUT}/><path d="M0,300 L500,900 L850,900 L1350,300Z" fill="#1e1822" {OUT}/><rect x="500" y="900" width="350" height="600" fill="#0a0810" {OUT}/>'
    for a, b in ((.08, .36), (.5, .72), (.82, .94)):
        for side in (0, 1):
            def pt(u, v):
                x = 500 * u; yt = 300 + 600 * u; yb = 2100 - 600 * u
                y = yt + (yb - yt) * v
                return (x if side == 0 else 1350 - x, y)
            pts = [pt(a, .22), pt(b, .22), pt(b, .9), pt(a, .9)]
            s += f'<path d="M{" L".join(f"{x:.0f},{y:.0f}" for x, y in pts)}Z" fill="#4a3220" {OUT}/>'
    return s


SCENES["end"] = dict(
    bg=_hall(),
    mid='',
    fg=fog(1300, 500, op=.2),
    glow=glow(675, 1200, 600, "#9ad0ff", .15),
    fog=False,
    actor=dict(box=(0, 700, 1350, 2330), fn=lambda ts, t: (
        lady(675, 1500, .55, t, "stand" if ts < 2 else "beckon", alpha=.45 + .2 * sn(t * 2), gown="#cfd8e8")
        + human(260 + min(ts, 3) * 30, 2290, 1.65, t, "walk" if ts < 1.5 else "scared", coat="#6a7a8a", hold="lantern" if ts < 1.5 else None, expr="calm" if ts < 1.5 else "scared", look=(.9, -.2)))),
)
