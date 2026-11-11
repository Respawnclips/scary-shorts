"""Scenes for 001-black-shuck. Each scene has layers bg / mid / fg / glow (SVG, 1350x2400 canvas).
Characters go in mid, picture-framing foreground in fg, lights and glowing eyes in glow."""
from toon import *

SCENES = {}

# 1. A traveller walks the coast road at night
SCENES["road"] = dict(
    bg=sky() + stars(1) + moon(960, 520, 120)
       + '<rect y="1330" width="1350" height="300" fill="#1c2b47"/>'
       + '<g stroke="#cfd6e4" stroke-width="5" opacity=".5"><path d="M860,1380 h200 M900,1430 h140 M840,1480 h230 M910,1530 h110"/></g>'
       + treeline(1400, "#2b3850", seed=4, hmin=200, hmax=380, x1=560),
    mid=fog(1150, 500) + ground(1560) + road(1570, x=700)
        + bare_tree(250, 1640, 700, "#182031", 11) + bare_tree(1180, 1620, 620, "#182031", 12)
        + person(690, 2090, 1.45, coat="#6e4a2e", back=True, hat=True, arm="hold") + lantern(876, 1912, 1.45),
    fg=trunk(-70, 210) + bush(1180, 2380, 1.5) + grass(2340, seed=3, n=14),
    glow=glow(876, 1912, 330, "#ffd76a", .75),
)

# 2. The hound, black against the moon
SCENES["hound"] = dict(
    bg=sky("#0e1530", "#4f5f7c") + stars(2, 30, 900) + moon(700, 900, 330),
    mid=treeline(1820, "#1c2740", seed=6, hmin=260, hmax=520) + fog(1500, 600, op=.5) + ground(2010, "#3c352e")
        + hound(820, 2060, 1.5),
    fg=trunk(1190, 220, lean=-30) + grass(2330, seed=5, n=22) + bush(120, 2400, 1.3),
    glow=glow(370, 1508, 200, "#ff2a1a", .9),
)

# 3. Bungay church in the storm, the hound at the doors
SCENES["church"] = dict(
    bg=sky("#0a0f20", "#37425c") + clouds(3) + bolt(1010, -40, 1.05),
    mid=treeline(1900, "#141b2c", seed=7, hmin=240, hmax=460) + ground(1960, "#39382f")
        + church(600, 1980, 1.75) + hound(470, 2010, 0.42, flip=True),
    fg=gravestone(170, 2330, 1.9) + gravestone(1160, 2360, 2.2, "#5d6473") + gravestone(820, 2400, 1.5)
       + bare_tree(60, 2420, 1500, "#0e121b", 21, 60) + grass(2360, seed=9, n=12),
    glow=glow(240, 1700, 200, "#f3c555", .6) + glow(715, 1700, 200, "#f3c555", .6) + glow(960, 1200, 200, "#f3c555", .6)
         + glow(596, 1856, 70, "#ff2a1a", .9),
)

# 4. Twelve miles to Blythburgh
SCENES["run"] = dict(
    bg=sky() + stars(4) + moon(300, 480, 100)
       + '<path d="M-20,1350 Q500,1050 1370,1250 L1370,1700 L-20,1700Z" fill="#232e45" stroke="#0d0f15" stroke-width="6"/>'
       + church(1010, 1215, 0.42),
    mid=fog(1250, 420) + ground(1560, "#3f4a36", pebbles=False)
        + '<path d="M930,1260 Q700,1500 900,1800 T500,2420 L900,2420 Q1250,2000 1010,1700 Q860,1480 980,1262Z" fill="#6a5a47" stroke="#0d0f15" stroke-width="6"/>'
        + hound(560, 1960, 0.95, flip=True) + signpost(1120, 2080, "BLYTHBURGH", 1.25),
    fg=fence(2400) + grass(2350, seed=12, n=16),
    glow=glow(845, 1610, 150, "#ff2a1a", .9) + glow(1085, 1045, 90, "#f3c555", .7),
)

# 5. The scorch marks on the church door
_planks = "".join(f'<path d="M{x},700 V2420" stroke="#0d0f15" stroke-width="5" opacity=".7"/>' for x in range(330, 1100, 130))
_claws = "".join(f'<path d="M{x},{y} q-70,300 -150,560" fill="none" stroke="{c}" stroke-width="{w}"/>'
                 for c, w in (("#ff7a2a", 46), ("#0b0706", 30))
                 for x, y in ((620, 900), (740, 870), (860, 900), (980, 950)))
SCENES["door"] = dict(
    bg='<rect width="1350" height="2400" fill="#4c5361"/>'
       + "".join(f'<path d="M{(r % 2) * 110 + c * 220 - 110},{r * 130} h200 v110 h-200Z" fill="none" stroke="#0d0f15" stroke-width="4" opacity=".5"/>'
                 for r in range(19) for c in range(8)),
    mid='<path d="M190,2420 V900 A485,485 0 0 1 1160,900 V2420Z" fill="#2a2e38" stroke="#0d0f15" stroke-width="8"/>'
        '<path d="M250,2420 V910 A425,425 0 0 1 1100,910 V2420Z" fill="#553c29" stroke="#0d0f15" stroke-width="8"/>'
        + _planks + _claws
        + '<g fill="#23262d" stroke="#0d0f15" stroke-width="6"><rect x="250" y="1050" width="330" height="44" rx="10"/><rect x="250" y="1950" width="330" height="44" rx="10"/><circle cx="1010" cy="1620" r="40"/></g>',
    fg=person(430, 2470, 2.1, coat="#3f5a78", back=True, arm="reach")
       + '<rect width="1350" height="2400" fill="#05060a" opacity=".25"/>',
    glow=glow(720, 1180, 520, "#ff6a1a", .5),
)

# 6. Paws behind you - don't turn around
SCENES["behind"] = dict(
    bg=sky("#0d142b", "#48587a") + stars(6, 30, 900) + moon(1040, 420, 90),
    mid=treeline(1500, "#1d2942", seed=9, hmin=320, hmax=640, x1=520) + treeline(1500, "#1d2942", seed=10, hmin=320, hmax=640, x0=860)
        + fog(1150, 520, op=.55) + ground(1520, "#40392f") + road(1530, x=690, far=40, near=520)
        + hound(880, 1600, 0.45)
        + person(560, 2330, 2.0, coat="#6e4a2e", hat=True, scared=True, arm="hold") + lantern(816, 2040, 2.0),
    fg=trunk(1160, 240, lean=-40) + bush(60, 2420, 1.4) + grass(2350, seed=14, n=10),
    glow=glow(745, 1434, 110, "#ff2a1a", 1) + glow(816, 2040, 380, "#ffd76a", .7),
)

# 7. Two eyes in the dark
_teeth = "".join(f'<path d="M{300 + k * 76},1500 l38,130 l38,-130Z"/><path d="M{338 + k * 76},1800 l38,-120 l38,120Z"/>' for k in range(10))
SCENES["eyes"] = dict(
    bg=sky("#020307", "#150a0d"),
    mid=f'<g fill="#ece8da" stroke="#0d0f15" stroke-width="5">{_teeth}</g>'
        '<g stroke="#0d0f15" stroke-width="8"><path d="M250,1150 Q430,980 600,1180 Q430,1280 250,1150Z" fill="#ff2a1a"/>'
        '<path d="M1100,1150 Q920,980 750,1180 Q920,1280 1100,1150Z" fill="#ff2a1a"/>'
        '<ellipse cx="440" cy="1150" rx="22" ry="70" fill="#1a0504"/><ellipse cx="910" cy="1150" rx="22" ry="70" fill="#1a0504"/></g>',
    fg=bare_tree(120, 2420, 1300, "#000", 31, 50) + bare_tree(1250, 2420, 1500, "#000", 32, 56),
    glow=glow(430, 1150, 420, "#ff2a1a", .7) + glow(920, 1150, 420, "#ff2a1a", .7),
)
