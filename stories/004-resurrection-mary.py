"""Scenes for 004-resurrection-mary (Chicago ghost legend)."""
from toon import *

SCENES = {}


def ghost(x, y, s=1.0, back=False):
    """Pale girl in a long white dress, long dark hair; feet at (x, y)."""
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}>'
    g += '<path d="M-40,-300 Q-120,-120 -150,0 H150 Q120,-120 40,-300Z" fill="#e9eef7"/>'
    g += '<path d="M-52,-300 Q-70,-190 -48,-110 L-30,-290Z M52,-300 Q70,-190 48,-110 L30,-290Z" fill="#cfd8ea"/>'
    g += '<rect x="-14" y="-336" width="28" height="40" fill="#dfe6f2"/>'
    g += '<circle cx="0" cy="-376" r="48" fill="#dfe6f2"/>'
    g += '<path d="M-56,-380 Q-60,-440 0,-444 Q60,-440 56,-380 L66,-250 L40,-300 Q0,-330 -40,-300 L-66,-250Z" fill="#14141c"/>'
    if not back:
        g += '<path d="M-48,-372 Q0,-420 48,-372 Q30,-345 0,-343 Q-30,-345 -48,-372Z" fill="#dfe6f2" stroke="none"/>'
        g += '<circle cx="-17" cy="-370" r="7" fill="#0d0f15" stroke="none"/><circle cx="17" cy="-370" r="7" fill="#0d0f15" stroke="none"/><path d="M-9,-352 q9,5 18,0" fill="none" stroke-width="3"/>'
    return g + '</g>'


# 1. A dark road at night, a girl in white by the roadside
SCENES["road"] = dict(
    bg=sky("#080c1c", "#3c4258") + stars(51, 40, 900) + moon(300, 440, 100)
       + treeline(1500, "#151b2c", seed=52, hmin=200, hmax=420),
    mid=fog(1450, 420, op=.45) + ground(1600, "#2b3028") + road(1610, x=675, far=60, near=700)
        + ghost(1010, 1900, 1.15),
    fg=grass(2350, seed=53, n=14) + bush(110, 2400, 1.4),
    glow=glow(1010, 1650, 380, "#cfe0ff", .45),
)

# 2. The ballroom dance
SCENES["ballroom"] = dict(
    bg='<rect width="1350" height="2400" fill="#2d1f33"/>'
       + "".join(f'<rect x="{x}" y="0" width="60" height="2000" fill="#3e2c46" stroke="#0d0f15" stroke-width="5"/>' for x in (60, 1230))
       + '<path d="M0,420 Q675,720 1350,420" fill="none" stroke="#0d0f15" stroke-width="8"/>'
       + "".join(f'<circle cx="{x}" cy="{int(420 + 300 * (1 - ((x - 675) / 675) ** 2))}" r="26" fill="#ffd76a" stroke="#0d0f15" stroke-width="4"/>' for x in range(50, 1350, 100)),
    mid='<rect y="1900" width="1350" height="500" fill="#3a2a22" stroke="#0d0f15" stroke-width="6"/>'
        + person(470, 2250, 1.9, coat="#3c4f73", hat=False, arm="reach")
        + ghost(820, 2260, 2.0),
    fg='<rect width="1350" height="2400" fill="#05060a" opacity=".18"/>',
    glow=glow(675, 700, 1000, "#ffb347", .45) + glow(820, 1700, 420, "#cfe0ff", .4),
)

# 3. In the car, the passenger seat
SCENES["ride"] = dict(
    bg=sky("#05070f", "#232a3d") + '<path d="M0,1350 L560,1000 H790 L1350,1350 V2400 H0Z" fill="#14161d"/>'
       + '<path d="M600,1000 L650,2400 M750,1000 L700,2400" stroke="#cfd6e4" stroke-width="10" opacity=".35"/>'
       + stars(54, 30, 800),
    mid='<rect y="1850" width="1350" height="550" fill="#1b1a20" stroke="#0d0f15" stroke-width="8"/>'
        '<circle cx="450" cy="2150" r="210" fill="none" stroke="#0d0f15" stroke-width="40"/>'
        + person(350, 2480, 2.2, coat="#6e4a2e", back=True, hat=True)
        + ghost(1010, 2480, 2.0, back=False),
    fg='<path d="M0,0 H1350 V240 H0Z" fill="#0d0f15"/><path d="M0,0 V2400 M1350,0 V2400" stroke="#0d0f15" stroke-width="60"/>',
    glow=glow(1010, 1700, 520, "#cfe0ff", .4),
)

# 4. The cemetery gate
_bars = "".join(f'<path d="M{x},700 V2200" stroke="#0d0f15" stroke-width="40"/><path d="M{x},700 V2200" stroke="#3a3d49" stroke-width="22"/>'
                f'<path d="M{x - 22},700 l22,-70 l22,70Z" fill="#3a3d49" stroke="#0d0f15" stroke-width="5"/>' for x in range(160, 1250, 130))
SCENES["gate"] = dict(
    bg=sky("#080c1c", "#454c66") + stars(55, 40, 800) + moon(1000, 420, 110) + treeline(1450, "#161c2e", seed=56, hmin=250, hmax=500),
    mid=ground(1900, "#2b2f2b") + gravestone(300, 1900, 1.5) + gravestone(1000, 1900, 1.8) + fog(1800, 450, op=.5)
        + ghost(675, 2250, 1.7),
    fg=_bars + '<path d="M120,1100 H1230 M120,1900 H1230" stroke="#0d0f15" stroke-width="30"/><path d="M120,1100 H1230 M120,1900 H1230" stroke="#3a3d49" stroke-width="14"/>',
    glow=glow(675, 1750, 500, "#cfe0ff", .5),
)

# 5. Scorch marks on the iron bars
_scorch = "".join(f'<ellipse cx="{x}" cy="{y}" rx="54" ry="120" fill="#ff7a2a" opacity=".85" stroke="#0d0f15" stroke-width="5"/><ellipse cx="{x}" cy="{y}" rx="26" ry="70" fill="#1a0f0a"/>' for x, y in ((520, 1720), (680, 1780), (840, 1720)))
SCENES["bars"] = dict(
    bg='<rect width="1350" height="2400" fill="#0b0d14"/>',
    mid="".join(f'<rect x="{x}" y="0" width="150" height="2400" fill="#3a3d49" stroke="#0d0f15" stroke-width="10"/><path d="M{x + 30},0 V2400" stroke="#5a5e6e" stroke-width="12"/>' for x in (330, 610, 890)),
    fg=_scorch,
    glow=glow(680, 1750, 700, "#ff6a1a", .55),
)

# 6. An empty road and headlights
SCENES["end"] = dict(
    bg=sky("#05070f", "#2a3047") + stars(57, 40, 900) + treeline(1500, "#10151f", seed=58, hmin=220, hmax=480),
    mid=fog(1500, 420, op=.5) + ground(1600, "#222620") + road(1610, x=675, far=70, near=720),
    fg=grass(2350, seed=59, n=12),
    glow=glow(675, 1560, 600, "#fff2c0", .5),
)
