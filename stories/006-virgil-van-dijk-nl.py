"""Scenes for 006-virgil-van-dijk-nl: football story with a rigged, animated cartoon player (generic player, no real likeness/logos)."""
import math, random
from toon import *

SCENES = {}
sn = math.sin
SKIN = "#c98f63"; HAIR = "#15100d"


def stands(y0, y1, seed, base="#2a3350", cols=("#e8c34a", "#e8e8f0", "#d94a4a", "#4a8ad9")):
    r = random.Random(seed)
    s = f'<rect x="0" y="{y0}" width="1350" height="{y1 - y0}" fill="{base}" {OUT}/>'
    for row in range(int((y1 - y0) / 46)):
        for k in range(30):
            s += f'<circle cx="{k * 46 + (row % 2) * 23}" cy="{y0 + 28 + row * 46}" r="14" fill="{r.choice(cols)}" opacity=".85"/>'
    return s


def floodlight(x, y, h=620):
    return (f'<g {OUT}><rect x="{x - 12}" y="{y - h}" width="24" height="{h}" fill="#3a3d49"/><rect x="{x - 90}" y="{y - h - 70}" width="180" height="80" fill="#2b2e38"/>'
            + "".join(f'<circle cx="{x - 60 + i * 40}" cy="{y - h - 30}" r="14" fill="#fff8d0" stroke-width="3"/>' for i in range(4)) + '</g>')


def pitch(y, col1="#2f8a3d", col2="#37993f"):
    s = f'<rect x="-20" y="{y}" width="1400" height="{2420 - y}" fill="{col1}" {OUT}/>'
    for i in range(8):
        s += f'<rect x="-20" y="{y + i * 120}" width="1400" height="60" fill="{col2}" opacity=".7"/>'
    s += f'<path d="M-20,{y + 260} H1370 M675,{y} V{y + 260}" stroke="#fff" stroke-width="8" fill="none" opacity=".8"/>'
    return s


def ball(x, y, r=46, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot})" {OUT}><circle r="{r}" fill="#f4f4f4"/>'
            f'<path d="M0,-18 l17,12 l-7,20 h-20 l-7,-20Z" fill="#15171c" stroke="none"/><path d="M0,-18 V-r M17,-6 L{r * .95:.0f},-14 M10,14 L{r * .6:.0f},{r * .7:.0f} M-10,14 L-{r * .6:.0f},{r * .7:.0f} M-17,-6 L-{r * .95:.0f},-14" stroke="#15171c" stroke-width="4" fill="none"/></g>')


def goal(x, y, w=420, h=280):
    s = f'<g {OUT} fill="none"><path d="M{x},{y} V{y - h} H{x + w} V{y}" stroke="#fff" stroke-width="12"/>'
    for i in range(1, 8): s += f'<path d="M{x + i * w / 8},{y - h} V{y}" stroke="#fff" stroke-width="2" opacity=".5"/>'
    for j in range(1, 6): s += f'<path d="M{x},{y - j * h / 6} H{x + w}" stroke="#fff" stroke-width="2" opacity=".5"/>'
    return s + '</g>'


def trophy(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x},{y}) scale({s}) rotate({rot})" {OUT}><path d="M-70,-190 Q-70,-70 0,-60 Q70,-70 70,-190Z" fill="#e8c34a"/>'
            '<path d="M-70,-170 Q-130,-170 -110,-110 Q-100,-90 -66,-100 M70,-170 Q130,-170 110,-110 Q100,-90 66,-100" fill="none" stroke-width="12"/>'
            '<rect x="-14" y="-62" width="28" height="70" fill="#e8c34a"/><rect x="-60" y="6" width="120" height="34" rx="6" fill="#b8922a"/>'
            '<ellipse cx="-24" cy="-150" rx="10" ry="34" fill="#fff" opacity=".35" stroke="none"/></g>')


def kit(colour):  # (shirt, shorts, socks)
    return {"red": ("#d4262c", "#d4262c", "#d4262c"), "green": ("#1f8a3c", "#f2f2f2", "#1f8a3c"),
            "orange": ("#f07a1a", "#f07a1a", "#f07a1a"), "kid": ("#3a6ac8", "#f2f2f2", "#3a6ac8")}[colour]


def player(x, y, s, t, mode, colour="red", **kw):
    sh, sho, so = kit(colour)
    return human(x, y, s, t, mode, coat=sh, pants=sho, socks=so, skin=SKIN, hair=HAIR, **kw)


# 1. restaurant kitchen: the teenager washes dishes
_tiles = "".join(f'<rect x="{x}" y="{y}" width="150" height="150" fill="#d8d4c4" stroke="#8a8676" stroke-width="4"/>' for x in range(0, 1350, 150) for y in range(0, 1500, 150))
SCENES["keuken"] = dict(
    bg='<rect width="1350" height="2400" fill="#d8d4c4"/>' + _tiles + '<rect y="1500" width="1350" height="900" fill="#6b5a4a"/>'
       + "".join(f'<g {OUT}><path d="M{x},420 V520" stroke-width="6"/><ellipse cx="{x}" cy="590" rx="{r}" ry="{r * .35}" fill="#7a7f8c"/></g>' for x, r in ((200, 90), (420, 70), (980, 100), (1180, 75)))
       + glow(675, 800, 800, "#fff3c0", .35),
    mid='',
    fg='<rect x="0" y="1850" width="1350" height="550" fill="#9aa0ae" stroke="#0d0f15" stroke-width="8"/><rect x="120" y="1800" width="1110" height="80" rx="20" fill="#b9bfcc" stroke="#0d0f15" stroke-width="8"/>'
       + "".join(f'<ellipse cx="{x}" cy="1790" rx="{90 - i * 6}" ry="18" fill="#f4f4f4" stroke="#0d0f15" stroke-width="5"/>' for i, x in enumerate((230, 235, 228, 233, 230)) if False)
       + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e8f6ff" opacity=".7" stroke="#8fb8d8" stroke-width="3"/>' for x, y, r in ((520, 1760, 40), (600, 1720, 26), (790, 1770, 34), (860, 1730, 22), (700, 1700, 18))),
    glow='',
    actor=dict(box=(300, 1000, 1100, 1900),
               fn=lambda ts, t: human(675, 2240, 2.15, t, "wash", coat="#f1efe6", pants="#2a2e3a", skin=SKIN, hair=HAIR, look=(sn(t) * .3, .4)),),
)
SCENES["keuken"]["focus"] = None

# 2. street pitch in Breda: boy dribbles
SCENES["veld"] = dict(
    bg=sky("#7ec8f0", "#cfeaf8") + '<g opacity=".95" fill="#fff"><ellipse cx="300" cy="500" rx="150" ry="50"/><ellipse cx="420" cy="480" rx="100" ry="44"/><ellipse cx="1000" cy="640" rx="170" ry="55"/></g>'
       + house(40, 1450, 380, 300, "#b8664a", "#6a2f2a") if False else sky("#7ec8f0", "#cfeaf8"),
    mid='', fg='', glow=glow(1000, 500, 700, "#fff6c0", .4),
    actor=dict(box=(0, 1200, 1350, 2400), fn=lambda ts, t: ""),
)


def _bg_veld():
    s = sky("#7ec8f0", "#d7eef8") + '<g fill="#fff"><ellipse cx="300" cy="500" rx="150" ry="50"/><ellipse cx="420" cy="480" rx="100" ry="44"/><ellipse cx="1000" cy="640" rx="170" ry="55"/></g>'
    for i, (x, w, h, c) in enumerate(((20, 330, 330, "#b8664a"), (400, 300, 260, "#c9b28a"), (740, 330, 340, "#9a5a4a"), (1100, 300, 300, "#c9b28a"))):
        s += f'<g {OUT}><rect x="{x}" y="{1250 - h}" width="{w}" height="{h}" fill="{c}"/><path d="M{x - 20},{1250 - h} L{x + w / 2},{1250 - h - 150} L{x + w + 20},{1250 - h}Z" fill="#6a3a34"/>' \
             + "".join(f'<rect x="{x + 40 + k * 110}" y="{1250 - h + 60}" width="60" height="80" fill="#f3d27a" stroke-width="4"/>' for k in range(2)) + '</g>'
    return s


def _veld_actor(ts, t):
    x = 220 + ts * 190; ph = t * 9
    bx = x + 150 + 45 * sn(ph)
    return player(x, 2230, 2.0, t, "run", "kid", num=None) + ball(bx, 2215 - abs(sn(ph * .5)) * 14, 38, t * 400)


SCENES["veld"] = dict(
    bg=_bg_veld(),
    mid=f'<rect x="-20" y="1250" width="1400" height="1200" fill="#7a7f88" {OUT}/><rect x="-20" y="1250" width="1400" height="60" fill="#5a5f68"/>' + goal(900, 1650, 380, 250),
    fg='', glow=glow(1000, 500, 700, "#fff6c0", .4),
    actor=dict(box=(0, 1300, 1350, 2400), fn=_veld_actor),
)

# 3. no contract: the boy, a coach with a letter
SCENES["contract"] = dict(
    bg='<rect width="1350" height="2400" fill="#cfd4dc"/><rect y="1600" width="1350" height="800" fill="#7b6a5a"/>'
       + f'<rect x="170" y="500" width="500" height="380" fill="#b9d8f0" {OUT}/><path d="M420,500 V880 M170,690 H670" stroke="#0d0f15" stroke-width="8"/>',
    mid=person(1000, 2250, 2.1, coat="#3a3f52", hat=False, arm="reach", skin="#e2c29a"),
    fg='<rect x="500" y="1960" width="800" height="440" fill="#8a6a4a" stroke="#0d0f15" stroke-width="8"/><rect x="740" y="1920" width="320" height="50" fill="#f4f4f4" stroke="#0d0f15" stroke-width="5" transform="rotate(-4 900 1940)"/>',
    glow=glow(430, 700, 600, "#fff3c0", .3),
    actor=dict(box=(100, 1000, 900, 2400),
               fn=lambda ts, t: human(430, 2250, 2.15, t, "stand", coat="#3a6ac8", pants="#f2f2f2", skin=SKIN, hair=HAIR, expr="sad", look=(.6, .8), hr_bias=0) if False
               else player(430, 2250, 2.15, t, "stand", "kid", expr="sad", look=(.4, .9))),
)

# 4. Groningen: stadium, player runs with ball
SCENES["groningen"] = dict(
    bg=sky("#2a4a8a", "#e8a36a") + stands(780, 1250, 3, "#34406a") + floodlight(160, 1250) + floodlight(1190, 1250),
    mid=pitch(1250, "#2f8a3d", "#37993f") + goal(80, 1700, 420, 280),
    fg='<rect x="0" y="2330" width="1350" height="70" fill="#1d2a1d" opacity=".5"/>',
    glow=glow(160, 600, 500, "#fff8d0", .4) + glow(1190, 600, 500, "#fff8d0", .4),
    actor=dict(box=(0, 1300, 1350, 2400),
               fn=lambda ts, t: player(200 + ts * 190, 2240, 2.1, t, "run", "green") + ball(200 + ts * 190 + 150 + 45 * sn(t * 9), 2222 - abs(sn(t * 4.5)) * 14, 38, t * 400)),
)

# 5. hospital: he is seriously ill, lying in bed, heart monitor
def _hosp(ts, t):
    p = f'<g transform="translate(330,2000) rotate(90)">{human(0, 0, 2.0, t, "stand", coat="#e8eef5", pants="#e8eef5", skin=SKIN, hair=HAIR, expr="sad", look=(0, .5))}</g>'
    pts = "".join(f'{860 + i * 8},{1200 - (180 * math.exp(-(((i * 8 - (t * 220) % 400) / 14) ** 2)) if True else 0):.0f} ' for i in range(0, 50))
    mon = f'<rect x="820" y="1000" width="440" height="300" rx="20" fill="#0d1a14" stroke="#0d0f15" stroke-width="8"/><polyline points="{pts}" fill="none" stroke="#38ff8a" stroke-width="6"/>'
    return p + mon


SCENES["ziekenhuis"] = dict(
    bg='<rect width="1350" height="2400" fill="#cfe6dc"/><rect y="1650" width="1350" height="750" fill="#9fb8ae"/>'
       + f'<rect x="900" y="420" width="360" height="460" fill="#b9d8f0" {OUT}/><path d="M1080,420 V880 M900,650 H1260" stroke="#0d0f15" stroke-width="8"/>'
       + f'<g {OUT}><rect x="140" y="1980" width="900" height="60" fill="#8a96a6"/><rect x="140" y="2040" width="30" height="200" fill="#8a96a6"/><rect x="1010" y="2040" width="30" height="200" fill="#8a96a6"/></g>',
    mid='',
    fg=f'<g {OUT}><path d="M300,1930 Q680,1840 1030,1930 V2010 H300Z" fill="#f4f4f4"/><path d="M300,1960 H1030" stroke="#c4cad8" stroke-width="8"/></g>'
       + f'<g {OUT}><rect x="1130" y="1300" width="14" height="900" fill="#8a96a6"/><rect x="1090" y="1300" width="100" height="14" fill="#8a96a6"/><rect x="1100" y="1350" width="60" height="100" rx="14" fill="#e8f6ff" opacity=".85"/></g>',
    glow=glow(1050, 700, 600, "#fff8d0", .3),
    actor=dict(box=(100, 900, 1300, 2200), fn=_hosp),
)

# 6. Liverpool: 75 million, big stadium, he celebrates
SCENES["liverpool"] = dict(
    bg=sky("#2a1030", "#b8403a") + stands(700, 1250, 8, "#4a1f2a", ("#d4262c", "#f2f2f2", "#e8c34a")) + floodlight(150, 1250, 700) + floodlight(1200, 1250, 700)
       + f'<rect x="340" y="330" width="670" height="250" rx="24" fill="#10141c" {OUT}/><text x="675" y="500" font-size="120" font-weight="bold" fill="#ffd400" stroke="none" text-anchor="middle" font-family="DejaVu Sans">£75.000.000</text>',
    mid=pitch(1250, "#2f8a3d", "#37993f"), fg='',
    glow=glow(675, 450, 700, "#ffd400", .3) + glow(150, 500, 500, "#fff8d0", .4) + glow(1200, 500, 500, "#fff8d0", .4),
    actor=dict(box=(250, 1100, 1100, 2400), fn=lambda ts, t: player(675, 2250, 2.2, t, "cheer", "red", num=4)),
)


# 7. Champions League trophy, confetti
def _cl(ts, t):
    rr = random.Random(5); conf = ""
    for i in range(70):
        x0 = rr.random() * 1350; sp = 220 + rr.random() * 260; ph = rr.random() * 6
        y = (rr.random() * 2400 + t * sp) % 2400; x = x0 + sn(t * 2 + ph) * 40
        conf += f'<rect x="{x:.0f}" y="{y:.0f}" width="16" height="28" fill="{rr.choice(["#ffd400", "#d4262c", "#ffffff", "#2f7be8"])}" transform="rotate({(t * 200 + i * 40) % 360:.0f} {x:.0f} {y:.0f})" stroke="none"/>'
    bob = -abs(sn(t * 6)) * 38 * 2.2
    return player(675, 2250, 2.2, t, "cheer", "red", num=4) + trophy(675, 1130 + bob, 2.0, sn(t * 3) * 6) + conf


SCENES["cl"] = dict(
    bg=sky("#0a1030", "#2a3a8a") + stars(9, 60, 800) + stands(900, 1250, 11, "#1f2a5a") + floodlight(150, 1250, 700) + floodlight(1200, 1250, 700),
    mid=pitch(1250, "#287a36", "#2f8a3d"), fg='',
    glow=glow(675, 800, 900, "#ffe08a", .35),
    actor=dict(box=(0, 0, 1350, 2400), fn=_cl),
)

# 8. finale: player stands, looks at the viewer
SCENES["finale"] = dict(
    bg=sky("#2a3a7a", "#f0a060") + '<circle cx="1000" cy="900" r="200" fill="#ffd89a" opacity=".9"/>' + stands(1000, 1300, 15, "#33406a"),
    mid=pitch(1300, "#2f8a3d", "#37993f"), fg='',
    glow=glow(1000, 900, 800, "#ffb060", .4),
    actor=dict(box=(250, 1100, 1100, 2400),
               fn=lambda ts, t: player(600, 2250, 2.2, t, "stand", "red", num=4, expr="grin", look=(sn(t) * .2, 0)) + ball(830, 2232, 40, 0)),
)
