"""Scenes for 002-murder-castle (H. H. Holmes' Chicago hotel, 1893). Gore-free: shows the building, never the victims."""
from toon import *

SCENES = {}

# 1. Chicago 1893, the hotel across from the fairgrounds
SCENES["castle"] = dict(
    bg=sky("#0e1428", "#5a5f78") + stars(21, 40, 800) + moon(240, 420, 90)
       + treeline(1500, "#1d2437", seed=22, hmin=120, hmax=260),
    mid=fog(1500, 400, op=.4) + ground(1900, "#33302c") + road(1910, x=675, far=120, near=700)
        + hotel(675, 1900, 1.15),
    fg=fence(2400) + grass(2350, seed=23, n=12),
    glow=glow(675, 1750, 600, "#f3c555", .35),
)

# 2. The charming doctor
SCENES["doctor"] = dict(
    bg=sky("#1a1424", "#4a3f55") + '<rect y="1300" width="1350" height="1100" fill="#2b2230"/>'
       + '<g stroke="#0d0f15" stroke-width="4" opacity=".4">' + "".join(f'<path d="M{x},0 V1300"/>' for x in range(60, 1350, 150)) + '</g>',
    mid='<path d="M120,2400 V1000 A555,555 0 0 1 1230,1000 V2400Z" fill="#241a1c" stroke="#0d0f15" stroke-width="8"/>'
        + person(675, 2330, 2.5, coat="#3a3640", pants="#1c1d24", hat=True, arm="hold"),
    fg='<rect width="1350" height="2400" fill="#05060a" opacity=".2"/>',
    glow=glow(675, 1400, 700, "#f3c555", .35),
)

# 3. The hallway with too many doors
_doors = "".join(
    f'<path d="M{x - 90 * k},{1480 - 80 * k} v{-420 + 160 * k} h{180 * k} v{420 - 160 * k}Z" fill="{c}" stroke="#0d0f15" stroke-width="6"/>'
    for x, k, c in ((250, 1.0, "#4b3329"), (1100, 1.0, "#4b3329"), (420, .7, "#3d2a22"), (930, .7, "#3d2a22"), (540, .45, "#31221c"), (810, .45, "#31221c")))
SCENES["hall"] = dict(
    bg='<rect width="1350" height="2400" fill="#2a2024"/>'
       '<path d="M0,0 L560,900 H790 L1350,0Z" fill="#1c1519" stroke="#0d0f15" stroke-width="6"/>'
       '<path d="M0,2400 L560,1500 H790 L1350,2400Z" fill="#3a2d2a" stroke="#0d0f15" stroke-width="6"/>'
       '<path d="M0,0 L560,900 V1500 L0,2400Z" fill="#34262b" stroke="#0d0f15" stroke-width="6"/>'
       '<path d="M1350,0 L790,900 V1500 L1350,2400Z" fill="#34262b" stroke="#0d0f15" stroke-width="6"/>'
       '<rect x="560" y="900" width="230" height="600" fill="#0b090c" stroke="#0d0f15" stroke-width="6"/>',
    mid=_doors,
    fg=person(300, 2420, 1.9, coat="#4a5d78", back=True, hat=True, arm="hold") + lantern(468, 2160, 1.9),
    glow=glow(468, 2160, 420, "#ffd76a", .75),
)

# 4. A room-rate sign and the hotel behind it
SCENES["sign"] = dict(
    bg=sky("#0d1226", "#4c5470") + stars(24, 35, 900) + moon(1050, 520, 100),
    mid=fog(1700, 500, op=.4) + ground(2000, "#35302b") + hotel(300, 1990, .8, seed=9)
        + signpost(940, 2200, "ROOMS TO LET", 1.6),
    fg=bush(120, 2400, 1.5) + grass(2350, seed=25, n=14),
    glow=glow(300, 1700, 400, "#f3c555", .3),
)

# 5. A secret chute and stairs down into the dark
_steps = "".join(f'<path d="M{300 + k * 30},{1250 + k * 150} H{1050 - k * 30} V{1400 + k * 150} H{300 + k * 30}Z" fill="{c}" stroke="#0d0f15" stroke-width="6"/>'
                 for k, c in enumerate(["#5b4a40", "#4b3b33", "#3b2e28", "#2c221e", "#1c1614", "#100c0b"]))
SCENES["chute"] = dict(
    bg='<rect width="1350" height="2400" fill="#1b1517"/>'
       + "".join(f'<path d="M0,{y} H1350" stroke="#0d0f15" stroke-width="4" opacity=".5"/>' for y in range(100, 1200, 130)),
    mid='<rect y="1200" width="1350" height="1200" fill="#3a2d2a" stroke="#0d0f15" stroke-width="6"/>'
        '<path d="M250,1200 H1100 V2150 H250Z" fill="#070508" stroke="#0d0f15" stroke-width="8"/>'
        + _steps
        + '<path d="M150,1200 L250,1100 H1100 L1200,1200Z" fill="#5a4636" stroke="#0d0f15" stroke-width="6"/>',
    fg=person(1180, 2420, 1.6, coat="#6e4a2e", back=True, hat=True, scared=False, flip=True),
    glow=glow(675, 1900, 700, "#ff6a1a", .35),
)

# 6. The detective and the jail
SCENES["caught"] = dict(
    bg='<rect width="1350" height="2400" fill="#3a3f4b"/>'
       + "".join(f'<path d="M{(r % 2) * 110 + c * 220 - 110},{r * 130} h200 v110 h-200Z" fill="none" stroke="#0d0f15" stroke-width="4" opacity=".4"/>'
                 for r in range(19) for c in range(8)),
    mid='<rect x="200" y="700" width="950" height="1500" fill="#14161c" stroke="#0d0f15" stroke-width="8"/>'
        + person(675, 2150, 1.7, coat="#c08a3a", pants="#2a2a30", arm="down", scared=False),
    fg="".join(f'<rect x="{x}" y="500" width="34" height="1900" fill="#23262d" stroke="#0d0f15" stroke-width="6"/>' for x in range(150, 1250, 130))
       + '<rect x="100" y="620" width="1150" height="40" fill="#23262d" stroke="#0d0f15" stroke-width="6"/>',
    glow=glow(675, 900, 600, "#cfd6e4", .3),
)

# 7. The hotel burns
SCENES["fire"] = dict(
    bg=sky("#1a0a0a", "#7a2e1a") + stars(26, 20, 600),
    mid=ground(2000, "#2d2623") + hotel(675, 1990, 1.1, lit="#ff7a2a", wall="#3a2c2a", seed=5)
        + "".join(f'<path d="M{x},{y} q-60,-160 0,-300 q30,100 90,60 q20,120 -90,240Z" fill="#ff7a2a" stroke="#0d0f15" stroke-width="5"/>'
                  for x, y in ((380, 1500), (620, 1250), (860, 1450), (1020, 1650), (500, 1800))),
    fg=fence(2400, "#1d1613") + grass(2350, seed=27, n=10),
    glow=glow(675, 1500, 900, "#ff6a1a", .6),
)
