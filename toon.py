"""Cartoon drawing helpers: every function returns an SVG fragment for a 1350x2400 canvas.
Characters stand with their feet at (x, y). Thick dark outlines, muted night palette."""
import random, itertools

_n = itertools.count()
OUT = 'stroke="#0d0f15" stroke-width="6"'


def uid():
    return f"g{next(_n)}"


def sky(top="#141d36", bot="#5d6f8a"):
    i = uid()
    return (f'<defs><linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bot}"/></linearGradient></defs><rect width="1350" height="2400" fill="url(#{i})"/>')


def stars(seed=1, n=45, ymax=1100):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.randint(0, 1350)}" cy="{r.randint(0, ymax)}" r="{r.choice([2, 2, 3, 4])}" '
                   f'fill="#dfe6f5" opacity="{r.uniform(.35, .9):.2f}"/>' for _ in range(n))


def glow(x, y, r, col, op=0.8):
    i = uid()
    return (f'<defs><radialGradient id="{i}"><stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{i})"/>')


def moon(x, y, r=110, col="#ebe6d0"):
    return (glow(x, y, r * 3.2, col, 0.38) + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" {OUT}/>'
            f'<circle cx="{x - r * .3}" cy="{y - r * .2}" r="{r * .18}" fill="#cfc9b0"/>'
            f'<circle cx="{x + r * .32}" cy="{y + r * .3}" r="{r * .12}" fill="#cfc9b0"/>'
            f'<circle cx="{x + r * .1}" cy="{y - r * .5}" r="{r * .08}" fill="#cfc9b0"/>')


def clouds(seed=3, col="#0c1122", n=7, ymax=900, op=.85):
    r = random.Random(seed); s = f'<g fill="{col}" opacity="{op}">'
    for _ in range(n):
        x, y = r.randint(-100, 1350), r.randint(0, ymax)
        for k in range(5):
            s += f'<ellipse cx="{x + k * 110}" cy="{y + r.randint(-30, 30)}" rx="{r.randint(120, 200)}" ry="{r.randint(60, 100)}"/>'
    return s + '</g>'


def fog(y, h, col="#93a3bb", op=.45):
    i = uid()
    return (f'<defs><linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{col}" stop-opacity="{op}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/>'
            f'</linearGradient></defs><rect x="0" y="{y}" width="1350" height="{h}" fill="url(#{i})"/>')


def bare_tree(x, y, h, col="#1a2233", seed=None, w=None):
    r = random.Random(seed if seed is not None else int(x)); w = w or max(8, h / 20)
    tx = x + r.randint(-15, 15)
    s = f'<g fill="none" stroke="{col}"><path d="M{x},{y} L{tx},{y - h}" stroke-width="{w:.0f}"/>'
    for k in range(6):
        f = r.uniform(.35, .95); bx = x + (tx - x) * f; by = y - h * f
        d = 1 if k % 2 else -1; L = h * r.uniform(.2, .36)
        ex, ey = bx + d * L, by - L * r.uniform(.5, 1.0)
        s += f'<path d="M{bx:.0f},{by:.0f} Q{bx + d * L * .5:.0f},{by - L * .1:.0f} {ex:.0f},{ey:.0f}" stroke-width="{w * .45:.0f}"/>'
        s += f'<path d="M{(bx + ex) / 2 + d * L * .1:.0f},{(by + ey) / 2:.0f} l{d * L * .3:.0f},{-L * .38:.0f}" stroke-width="{max(3, w * .26):.0f}"/>'
    return s + '</g>'


def treeline(y, col="#27344a", seed=2, hmin=280, hmax=560, step=95, x0=-40, x1=1400):
    r = random.Random(seed)
    return "".join(bare_tree(x + r.randint(-25, 25), y, r.randint(hmin, hmax), col, seed * 100 + x)
                   for x in range(x0, x1, step))


def ground(y, col="#4a4035", seed=5, pebbles=True):
    r = random.Random(seed)
    s = f'<path d="M-20,{y} Q340,{y - 34} 675,{y} T1370,{y - 12} L1370,2420 L-20,2420Z" fill="{col}" {OUT}/>'
    if pebbles:
        for _ in range(22):
            px, py = r.randint(0, 1350), r.randint(y + 40, 2380)
            s += f'<ellipse cx="{px}" cy="{py}" rx="{r.randint(10, 22)}" ry="{r.randint(5, 9)}" fill="none" stroke="#0d0f15" stroke-width="3" opacity=".55"/>'
    return s


def road(y, col="#6a5a47", x=675, far=50, near=440):
    return (f'<path d="M{x - far},{y} L{x + far},{y} L{x + near},2420 L{x - near},2420Z" fill="{col}" {OUT}/>'
            f'<path d="M{x - far * .3},{y + 40} L{x - near * .35},2420 M{x + far * .3},{y + 40} L{x + near * .35},2420" stroke="#0d0f15" stroke-width="3" opacity=".3" fill="none"/>')


def trunk(x, w=190, col="#2a2320", lean=30):
    """Big framing tree at the edge of the picture."""
    return (f'<path d="M{x},2420 L{x + lean},-20 L{x + lean + w * .8},-20 L{x + w},2420Z" fill="{col}" {OUT}/>'
            f'<path d="M{x + w * .35},2300 Q{x + w * .45},1500 {x + lean + w * .3},600 M{x + w * .7},2000 Q{x + w * .72},1400 {x + lean + w * .6},900 '
            f'M{x + w * .5},700 q-10,-200 10,-420" fill="none" stroke="#0d0f15" stroke-width="4" opacity=".7"/>'
            f'<path d="M{x + w * .55},1250 q20,-18 44,-4 q-22,22 -44,4z" fill="#0d0f15"/>')


def bush(x, y, s=1, col="#2b4534"):
    b = f'<g transform="translate({x},{y}) scale({s})" {OUT} fill="{col}">'
    for cx, cy, r in ((-110, -40, 70), (-40, -90, 85), (50, -80, 90), (125, -35, 72), (0, -30, 80)):
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
    return b + f'<rect x="-190" y="-20" width="390" height="140" stroke="none"/></g>'


def grass(y=2330, col="#24382b", seed=8, n=26):
    r = random.Random(seed); s = f'<g fill="{col}" {OUT}>'
    for _ in range(n):
        x = r.randint(-20, 1350); h = r.randint(60, 150)
        s += f'<path d="M{x},{y + 90} L{x + 14},{y - h} L{x + 34},{y + 90} L{x + 56},{y - h * .7:.0f} L{x + 74},{y + 90}Z"/>'
    return s + '</g>'


def person(x, y, s=1.0, coat="#7c2f2b", pants="#22252d", skin="#e2c29a", hair="#17181d",
           flip=False, back=False, hat=False, scared=False, arm="down"):
    """arm: down | hold (forearm out, e.g. lantern) | reach (hand up and forward)."""
    f = -1 if flip else 1
    p = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    p += '<ellipse cx="-24" cy="-4" rx="30" ry="14" fill="#14161b"/><ellipse cx="28" cy="-4" rx="30" ry="14" fill="#14161b"/>'
    p += f'<path d="M-44,-150 L-42,-8 L-8,-8 L-2,-120 L6,-8 L42,-8 L44,-150Z" fill="{pants}"/>'
    p += f'<path d="M-50,-262 Q-76,-200 -64,-140 L-40,-144 Q-46,-200 -30,-250Z" fill="{coat}"/><circle cx="-53" cy="-134" r="15" fill="{skin}"/>'
    p += f'<path d="M-54,-268 Q0,-292 54,-268 L62,-120 Q0,-104 -62,-120Z" fill="{coat}"/>'
    if arm == "hold":
        p += f'<path d="M50,-262 Q82,-220 72,-192 L122,-182 L120,-156 L50,-160 Q30,-200 30,-250Z" fill="{coat}"/><circle cx="128" cy="-168" r="15" fill="{skin}"/>'
    elif arm == "reach":
        p += f'<path d="M50,-262 L132,-332 L150,-310 L62,-222Z" fill="{coat}"/><circle cx="148" cy="-328" r="15" fill="{skin}"/>'
    else:
        p += f'<path d="M50,-262 Q76,-200 64,-140 L40,-144 Q46,-200 30,-250Z" fill="{coat}"/><circle cx="53" cy="-134" r="15" fill="{skin}"/>'
    p += f'<rect x="-12" y="-298" width="24" height="28" fill="{skin}"/><circle cx="0" cy="-332" r="46" fill="{skin}"/>'
    if back:
        p += f'<path d="M-46,-336 A46,46 0 0 1 46,-336 L44,-306 Q0,-284 -44,-306Z" fill="{hair}"/>'
    else:
        p += f'<path d="M-46,-338 A46,46 0 0 1 46,-338 Q22,-362 2,-350 Q-20,-364 -46,-338Z" fill="{hair}"/>'
        er = 11 if scared else 7
        for ex in (-15, 19):
            p += f'<circle cx="{ex}" cy="-328" r="{er}" fill="#fff" stroke-width="3"/><circle cx="{ex + 1}" cy="-328" r="3.5" fill="#0d0f15" stroke="none"/>'
        if scared:
            p += '<ellipse cx="3" cy="-300" rx="9" ry="12" fill="#2a1014" stroke-width="3"/><path d="M-28,-348 l16,-8 M32,-348 l-16,-8" fill="none" stroke-width="4"/>'
        else:
            p += '<path d="M-8,-302 q10,6 22,0" fill="none" stroke-width="4"/>'
    if hat:
        p += '<ellipse cx="0" cy="-366" rx="68" ry="15" fill="#2a2622"/><path d="M-36,-368 Q-34,-424 0,-426 Q34,-424 36,-368Z" fill="#2a2622"/>'
    return p + '</g>'


def lantern(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M0,-52 v18" fill="none"/>'
            f'<rect x="-18" y="-34" width="36" height="52" rx="6" fill="#f7d76e"/><path d="M-22,-34 h44 M-22,18 h44" fill="none"/></g>')


def hound(x, y, s=1.0, flip=False, outline="#3b4356"):
    """Huge black dog, side view, facing left (flip=True faces right). Eye is at (-300,-368)*s."""
    f = -1 if flip else 1
    i = uid()
    shapes = ('<ellipse cx="60" cy="-250" rx="235" ry="112"/><ellipse cx="-120" cy="-275" rx="135" ry="135"/>'
              '<ellipse cx="-250" cy="-362" rx="92" ry="82"/><path d="M-310,-395 L-436,-352 L-430,-312 L-300,-300Z"/>'
              '<path d="M-300,-306 L-412,-288 L-330,-266Z"/><path d="M-242,-430 L-214,-528 L-188,-424Z"/><path d="M-290,-424 L-278,-506 L-244,-430Z"/>'
              '<path d="M-172,-200 L-192,0 L-138,0 L-110,-200Z"/><path d="M-92,-200 L-102,0 L-48,0 L-30,-200Z"/>'
              '<path d="M170,-222 L212,-110 L190,0 L244,0 L264,-120 L252,-242Z"/><path d="M108,-200 L128,0 L182,0 L172,-200Z"/>'
              '<path d="M280,-292 Q402,-332 424,-436 Q382,-340 270,-250Z"/>'
              '<path d="M-60,-372 l30,-56 l26,50 l34,-48 l22,52 l36,-40 l18,50Z"/>')
    return (f'<g transform="translate({x},{y}) scale({f * s},{s})"><defs><g id="{i}">{shapes}</g></defs>'
            f'<use href="#{i}" stroke="{outline}" stroke-width="16" fill="{outline}"/><use href="#{i}" fill="#07080c"/>'
            '<path d="M-420,-312 l12,22 l12,-22 l12,20 l12,-22 l12,20 l12,-22 l12,20 l12,-20Z" fill="#f1efe6" stroke="#0d0f15" stroke-width="2"/>'
            '<ellipse cx="-300" cy="-368" rx="17" ry="12" fill="#ff2a1a"/><circle cx="-303" cy="-369" r="5" fill="#ffd9a0"/></g>')


def church(x, y, s=1.0, lit="#f3c555", stone="#59606e", dark="#343946"):
    c = f'<g transform="translate({x},{y}) scale({s})" {OUT}>'
    c += f'<rect x="-270" y="-330" width="400" height="330" fill="{stone}"/><path d="M-292,-330 L-70,-505 L150,-330Z" fill="{dark}"/>'
    c += f'<rect x="120" y="-640" width="172" height="640" fill="#626978"/><path d="M106,-640 L206,-840 L306,-640Z" fill="{dark}"/>'
    c += '<path d="M206,-840 v-70 M184,-884 h44" fill="none" stroke-width="8"/>'
    c += '<path d="M-125,0 L-125,-150 A55,55 0 0 1 -15,-150 L-15,0Z" fill="#3b2a1f"/><path d="M-70,-200 V0" fill="none" stroke-width="4"/>'
    for wx, wy in ((-232, -110), (40, -110), (180, -400)):
        c += f'<path d="M{wx},{wy} v-92 a26,26 0 0 1 52,0 v92Z" fill="{lit}"/>'
    c += '<g fill="none" stroke-width="3" opacity=".6"><path d="M-240,-280 h50 M-150,-250 h60 M0,-270 h44 M150,-560 h50 M220,-260 h50 M160,-120 h46 M-200,-30 h40 M40,-40 h50"/></g>'
    return c + '</g>'


def gravestone(x, y, s=1.0, col="#69707f"):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-44,0 v-96 a44,44 0 0 1 88,0 v96Z" fill="{col}"/>'
            '<path d="M0,-108 v52 M-18,-90 h36" fill="none" stroke-width="5"/></g>')


def bolt(x, y, s=1.0):
    pts = "0,0 -70,330 -10,320 -110,700 -30,690 -150,1080 60,600 -10,610 90,290 20,300 80,0"
    return (f'<g transform="translate({x},{y}) scale({s})"><polygon points="{pts}" fill="#fff8c9" stroke="#ffffff" stroke-width="10"/></g>'
            + glow(x - 30 * s, y + 500 * s, 520 * s, "#dfe6ff", .55))


def signpost(x, y, text, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-12" y="-330" width="24" height="330" fill="#4b3a2b"/>'
            f'<path d="M-170,-320 h300 l50,42 l-50,42 h-300Z" fill="#8a6f4e"/>'
            f'<text x="-158" y="-264" font-size="38" font-weight="bold" fill="#17120d" stroke="none">{text}</text></g>')


def fence(y, col="#3a2f26", step=170):
    s = f'<g {OUT} fill="{col}"><rect x="-20" y="{y - 120}" width="1400" height="20"/><rect x="-20" y="{y - 60}" width="1400" height="20"/>'
    for x in range(40, 1400, step):
        s += f'<path d="M{x - 16},{y} v-170 l16,-22 l16,22 v170Z"/>'
    return s + '</g>'


def hotel(x, y, s=1.0, lit="#f3c555", wall="#5a4a42", roof="#2d2623", rows=6, cols=5, seed=3):
    """Tall Victorian hotel, front view, centred on x, feet at y. Some windows lit, some dark."""
    r = random.Random(seed)
    w, h = 150 * cols + 60, 170 * rows + 80
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}>'
    g += f'<rect x="{-w // 2}" y="{-h}" width="{w}" height="{h}" fill="{wall}"/>'
    g += f'<path d="M{-w // 2 - 24},{-h} L{-w // 2 + 40},{-h - 90} H{w // 2 - 40} L{w // 2 + 24},{-h}Z" fill="{roof}"/>'
    g += f'<rect x="{-w // 2 - 24}" y="{-h - 16}" width="{w + 48}" height="26" fill="{roof}"/>'
    for ry in range(rows):
        for cx in range(cols):
            wx = -w // 2 + 50 + cx * 150
            wy = -h + 50 + ry * 170
            on = r.random() < .42
            g += f'<rect x="{wx}" y="{wy}" width="64" height="104" rx="10" fill="{lit if on else "#14161f"}"/>'
            g += f'<path d="M{wx + 32},{wy} v104 M{wx},{wy + 48} h64" fill="none" stroke-width="3"/>'
    g += '<path d="M-60,0 V-120 A60,60 0 0 1 60,-120 V0Z" fill="#2a1d15"/>'
    return g + '</g>'


def tallhat(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><ellipse cx="0" cy="0" rx="68" ry="15" fill="#17181d"/>'
            '<path d="M-38,-2 Q-36,-70 0,-72 Q36,-70 38,-2Z" fill="#17181d"/></g>')


# ---------------------------------------------------------------- animated clown (rigged, for "actor" scenes)
import math as _m


def clown(x, y, s=1.0, t=0.0, mode="walk", flip=False, look=(0.0, 0.0), mouth=None, head_rot=None,
          bust=False, balloon=True, candy=True):
    """Rigged clown, feet at (x, y), ~700 units tall, drawn for time t (seconds).
    mode: walk | wave | stand | face (head only, centred at x,y).  bust=True hides everything below the chest.
    Nested transforms = a real skeleton: hips -> knees -> shoes, shoulders -> elbows -> hands, neck -> head."""
    sn = _m.sin
    blink = 0.12 if (t % 3.3) < 0.13 else 1.0
    if mode == "walk":
        ph = t * 5.2
        la, ra = sn(ph) * 27, -sn(ph) * 27
        lk, rk = max(0, sn(ph + 1.3)) * 38, max(0, sn(ph + 1.3 + _m.pi)) * 38
        bob = -abs(sn(ph)) * 16; lean = 5 + sn(ph * 2) * 1.2
        arm_l, el_l = -sn(ph) * 24 + 8, -14
        arm_r, el_r = sn(ph) * 24 - 8, -14 - 8 * sn(ph)
        hr = sn(ph) * 3 + (0 if head_rot is None else head_rot)
        mo = 0.18 + 0.06 * sn(t * 2) if mouth is None else mouth
    elif mode == "wave":
        bob = sn(t * 2.2) * 5; lean = sn(t * 1.7) * 2.5
        la = ra = lk = rk = 0
        arm_l, el_l = 8 + sn(t * 1.5) * 3, -20
        arm_r, el_r = -152 + sn(t * 9) * 4, 28 + sn(t * 9) * 30          # raised arm, waving forearm
        hr = sn(t * 1.3) * 6 + (0 if head_rot is None else head_rot)
        mo = 0.3 + 0.2 * (sn(t * 3) > 0.4) if mouth is None else mouth
    else:                                                                # stand / face
        bob = sn(t * 1.6) * 4; lean = sn(t * 1.1) * 1.5
        la = ra = lk = rk = 0; arm_l, el_l, arm_r, el_r = 4, -10, -4, -10
        hr = sn(t * 0.8) * 5 + (0 if head_rot is None else head_rot)
        mo = 0.25 if mouth is None else mouth
    lx, ly = look
    SUIT, DOTS, SKIN, RED = "#d8a935", "#2f5aa8", "#efe8dc", "#cf2430"

    def sleeve(a, e, hold=None):
        g = f'<g transform="rotate({a})"><path d="M-27,-16 Q-34,50 -22,112 L22,112 Q34,50 27,-16Z" fill="{SUIT}"/>'
        g += f'<circle cx="-4" cy="40" r="9" fill="{DOTS}" stroke="none"/><circle cx="8" cy="82" r="8" fill="{DOTS}" stroke="none"/>'
        g += f'<g transform="translate(0,104) rotate({e})"><path d="M-23,-6 Q-26,40 -18,92 L18,92 Q26,40 23,-6Z" fill="{SUIT}"/>'
        g += f'<path d="M-24,80 h48 l-4,20 h-40Z" fill="#fff" />'
        g += '<g transform="translate(0,104)"><circle r="24" fill="#f6f6f6"/><circle cx="-20" cy="6" r="10" fill="#f6f6f6"/><circle cx="19" cy="8" r="10" fill="#f6f6f6"/>'
        up = -(a + e + lean)
        if hold == "balloon":
            sw = sn(t * 2.4) * 9
            g += (f'<g transform="rotate({up + sw * .6:.1f})"><path d="M0,0 Q{20 + sw:.1f},-300 {10 + sw * 2:.1f},-560" stroke="#e8e2d0" stroke-width="4" fill="none"/>'
                  f'<g transform="translate({10 + sw * 2:.1f},-630)"><ellipse rx="64" ry="78" fill="{RED}"/><path d="M-14,78 l14,22 l14,-22Z" fill="{RED}"/>'
                  f'<ellipse cx="-22" cy="-30" rx="14" ry="22" fill="#fff" opacity=".35" stroke="none"/></g></g>')
        if hold == "lolly":
            g += (f'<g transform="rotate({up:.1f})"><path d="M0,0 V-170" stroke="#e8e2d0" stroke-width="9"/><g transform="translate(0,-196)">'
                  f'<circle r="46" fill="#fff"/><path d="M0,0 m0,-38 a38,38 0 1 1 -2,0 M0,-22 a22,22 0 1 0 2,0 M0,-8 a8,8 0 1 1 -1,0" fill="none" stroke="#e23a56" stroke-width="9"/></g></g>')
        g += '</g></g></g>'
        return g

    def leg(a, k):
        return (f'<g transform="rotate({a})"><path d="M-44,-8 Q-52,60 -36,132 L36,132 Q52,60 44,-8Z" fill="{SUIT}"/>'
                f'<path d="M-44,40 h88 M-40,86 h80" stroke="{DOTS}" stroke-width="10" fill="none"/>'
                f'<g transform="translate(0,128) rotate({k})"><path d="M-34,0 L34,0 L29,100 L-29,100Z" fill="#7a2c80"/>'
                f'<g transform="translate(0,96)"><path d="M-40,-6 Q-30,40 0,38 Q86,40 96,16 Q96,-8 52,-10 L36,-14Z" fill="{RED}"/>'
                f'<circle cx="86" cy="12" r="20" fill="#e8c43a" stroke="none"/><path d="M-40,-6 h76" stroke="#0d0f15" stroke-width="6"/></g></g></g>')

    def head(rot):
        eyes = ""
        for ex in (-30, 30):
            eyes += (f'<g transform="translate({ex},-98)"><path d="M-22,-34 L0,-48 L22,-34 L0,-22Z" fill="#2c64c8" stroke-width="4"/>'
                     f'<ellipse rx="18" ry="{22 * blink:.1f}" fill="#fff" stroke-width="4"/>'
                     f'<circle cx="{lx * 9:.1f}" cy="{ly * 8:.1f}" r="{6.5 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/></g>')
        brow = f'<path d="M-52,-132 L-12,-118 M52,-132 L12,-118" stroke="#8a1a22" stroke-width="9" fill="none"/>'
        open_ = 16 + 44 * mo
        mouth_ = (f'<path d="M-62,-62 Q0,-30 62,-62 Q0,{-30 + open_ - 6:.1f} -62,-62Z" fill="#1a0509" stroke-width="5"/>')
        teeth = ""
        for i in range(8):
            u = (i + .5) / 8; px = -62 + 124 * u; py = -62 + 2 * 32 * u * (1 - u) * 1.0
            teeth += f'<path d="M{px - 8:.1f},{py:.1f} l8,{10 + 10 * mo:.1f} l8,-{10 + 10 * mo:.1f}Z" fill="#f4efe2" stroke-width="2"/>'
        smile = (f'<path d="M-84,-108 Q-96,-40 -62,-62 Q0,-30 62,-62 Q96,-40 84,-108" fill="none" stroke="{RED}" stroke-width="22"/>')
        return (f'<g transform="rotate({rot})">'
                + f'<g fill="#c9481f"><circle cx="-76" cy="-120" r="34"/><circle cx="-90" cy="-84" r="30"/><circle cx="76" cy="-120" r="34"/><circle cx="90" cy="-84" r="30"/><circle cx="-48" cy="-170" r="30"/><circle cx="48" cy="-170" r="30"/></g>'
                + f'<path d="M-36,-176 L10,-262 L50,-174Z" fill="{DOTS}"/><circle cx="10" cy="-266" r="16" fill="{RED}"/>'
                + f'<ellipse cx="0" cy="-92" rx="76" ry="84" fill="{SKIN}"/>'
                + eyes + brow + smile + mouth_ + teeth
                + f'<circle cx="0" cy="-74" r="24" fill="{RED}"/><circle cx="-7" cy="-82" r="7" fill="#ff8a8a" stroke="none"/></g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + f'<g transform="translate(0,0)">{head(hr)}</g></g>'
    out += f'<g transform="translate(0,{bob:.1f})">'
    if not bust:
        out += f'<g transform="translate(-40,-250)">{leg(la, lk)}</g><g transform="translate(40,-250)">{leg(ra, rk)}</g>'
    out += f'<g transform="translate(0,-250) rotate({lean})">'
    out += f'<g transform="translate(-76,-228)">{sleeve(arm_l, el_l, "lolly" if candy and mode == "walk" else None)}</g>' if mode != "wave" else f'<g transform="translate(-76,-228)">{sleeve(arm_l, el_l, "lolly" if candy else None)}</g>'
    out += (f'<path d="M-80,0 Q-112,-120 -70,-250 L70,-250 Q112,-120 80,0Z" fill="{SUIT}"/>'
            f'<circle cx="-40" cy="-60" r="14" fill="{DOTS}" stroke="none"/><circle cx="44" cy="-130" r="14" fill="{DOTS}" stroke="none"/><circle cx="-30" cy="-190" r="12" fill="{DOTS}" stroke="none"/>'
            f'<g fill="{RED}"><circle cx="0" cy="-60" r="15"/><circle cx="0" cy="-120" r="15"/><circle cx="0" cy="-180" r="15"/></g>')
    out += f'<path d="M-62,-250 l12,24 l16,-24 l16,24 l16,-24 l16,24 l16,-24 l16,24 l12,-24 l-6,-20 h-98Z" fill="#fafafa"/>'
    out += f'<g transform="translate(0,-262)">{head(hr)}</g>'
    out += f'<g transform="translate(76,-228)">{sleeve(arm_r, el_r, "balloon" if balloon and mode == "walk" else None)}</g>'
    out += '</g></g></g>'
    return out


def human(x, y, s=1.0, t=0.0, mode="stand", coat="#7c2f2b", pants="#22252d", skin="#e2c29a", hair="#17181d",
          hat=False, flip=False, expr="calm", look=(0.0, 0.0), back=False, hold=None, num=None, socks=None, longhair=False, horns=False):
    """Rigged, animated person (feet at (x, y), ~430 units tall), drawn for time t. Use inside an "actor" scene
    (SCENES[name]["actor"] = dict(box=(x0, y0, x1, y1), fn=lambda ts, t: human(...))) so the main character really moves.
    mode: stand (breathing, looking around) | walk | dance (wild jerky dancing) | run | cheer (jumping, arms up) | wash (scrubbing at a sink) | scared (trembling, hands up) | reach (arm out) | point | back (stand, seen from behind).
    expr: calm | scared | shocked | grin.   hold: None | lantern (hand holds a lantern that swings).   back=True hides the face."""
    sn = _m.sin
    ph = t * (5.0 if mode == "walk" else 9.0 if mode == "run" else 0)
    bob = lean = 0.0; la = ra = lk = rk = 0.0
    al, el, ar, er = 4 + sn(t * 1.4) * 2, -8, -4 - sn(t * 1.4) * 2, -8
    hr = sn(t * 0.9) * 4 + look[0] * 6
    if mode in ("walk", "run"):
        amp = 26 if mode == "walk" else 42
        la, ra = sn(ph) * amp, -sn(ph) * amp
        lk, rk = max(0, sn(ph + 1.3)) * (34 if mode == "walk" else 60), max(0, sn(ph + 1.3 + _m.pi)) * (34 if mode == "walk" else 60)
        bob = -abs(sn(ph)) * (10 if mode == "walk" else 18); lean = 4 if mode == "walk" else 12
        al, ar = -sn(ph) * amp * .9 + 6, sn(ph) * amp * .9 - 6; el = er = -18 if mode == "walk" else -70
    elif mode == "scared":
        tr = sn(t * 38) * 2.2
        bob = tr * .6; lean = -4 + tr; al, el, ar, er = 150 + sn(t * 30) * 3, 30, -150 - sn(t * 31) * 3, -30
        hr = tr * 2; expr = "scared" if expr == "calm" else expr
    elif mode == "cheer":
        bob = -abs(sn(t * 6)) * 38; al, ar = 148 + sn(t * 7) * 9, -148 - sn(t * 7) * 9; el, er = 8, -8
        la, ra = sn(t * 6) * 9, -sn(t * 6) * 9; expr = "grin"
    elif mode == "wash":
        bob = sn(t * 1.8) * 2; al, ar = -10 + sn(t * 8) * 5, 10 - sn(t * 8 + 1) * 5; el, er = -38 + sn(t * 8) * 8, 38 - sn(t * 8 + 1) * 8
    elif mode == "bow":
        lean = 40 * max(0.0, min(1.0, (t % 6) / 1.0)) if False else 42; al, el, ar, er = 20, -6, -20, -6; hr = 8; bob = 0
    elif mode == "dance":
        ph = t * 7.0
        bob = -abs(sn(ph)) * 22; lean = sn(ph * .5) * 9
        la, ra = sn(ph) * 30, -sn(ph) * 30
        lk, rk = max(0, sn(ph + 1.5)) * 50, max(0, sn(ph + 1.5 + _m.pi)) * 50
        al, el = 100 + sn(ph) * 45, 30 + sn(ph * 2) * 25
        ar, er = -100 - sn(ph + 1.2) * 45, -30 - sn(ph * 2 + 1) * 25
        hr = sn(ph * .5) * 14
    elif mode == "reach":
        ar, er = -92 + sn(t * 3) * 3, -6; bob = sn(t * 1.6) * 2
    elif mode == "point":
        ar, er = -88, 0; lean = 2; bob = sn(t * 1.6) * 2
    else:
        bob = sn(t * 1.8) * 3
    if hold == "lantern" and mode in ("stand", "walk", "back"):
        ar, er = -75, -35
    lx, ly = look
    blink = 0.12 if (t % 3.7) < 0.12 else 1.0
    f = -1 if flip else 1
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(0,{bob:.1f})">'

    def arm(a, e, item):
        g = (f'<g transform="rotate({a:.1f})"><path d="M-22,-10 Q-30,50 -20,104 L20,104 Q30,50 22,-10Z" fill="{coat}"/>'
             f'<g transform="translate(0,100) rotate({e:.1f})"><path d="M-19,-4 Q-22,40 -15,84 L15,84 Q22,40 19,-4Z" fill="{coat}"/>'
             f'<circle cx="0" cy="92" r="17" fill="{skin}"/>')
        if item == "hook":
            g += ('<g transform="translate(0,96)"><path d="M0,0 V34 Q0,96 -46,78 L-38,62 Q-20,72 -14,36 V0Z" fill="#b8c0cc" stroke-width="5"/></g>')
        if item == "musket":
            g += ('<g transform="translate(0,92)"><rect x="-9" y="-70" width="18" height="120" rx="6" fill="#5a3a22"/>'
                  '<rect x="-5" y="40" width="10" height="170" fill="#2b2f3a"/></g>')
        if item == "lantern":
            sw = sn(t * 2.1) * 6
            g += (f'<g transform="translate(0,92) rotate({-(a + e + lean) * .9 + sw:.1f})"><path d="M0,0 V30" stroke="#0d0f15" stroke-width="5"/>'
                  f'<rect x="-18" y="30" width="36" height="52" rx="6" fill="#f3c555"/><rect x="-22" y="26" width="44" height="10" fill="#3a3d49"/>'
                  f'<rect x="-22" y="78" width="44" height="10" fill="#3a3d49"/></g>')
        return g + '</g></g>'

    def leg(a, k):
        return (f'<g transform="rotate({a:.1f})"><path d="M-30,-6 L30,-6 L26,100 L-26,100Z" fill="{pants}"/>'
                f'<g transform="translate(0,96) rotate({k:.1f})"><path d="M-25,0 L25,0 L22,88 L-22,88Z" fill="{socks or pants}"/>'
                f'<path d="M-24,84 Q-26,106 -4,106 Q40,106 46,96 Q44,86 22,84Z" fill="#14161b"/></g></g>')

    o += f'<g transform="translate(-24,-170)">{leg(la, lk)}</g><g transform="translate(24,-170)">{leg(ra, rk)}</g>'
    o += f'<g transform="translate(0,-170) rotate({lean:.1f})">'
    o += f'<g transform="translate(-52,-150)">{arm(al, el, None)}</g>'
    o += f'<path d="M-58,0 Q-70,-80 -54,-160 Q0,-186 54,-160 Q70,-80 58,0Z" fill="{coat}"/><path d="M0,-170 V-6" stroke="#0d0f15" stroke-width="3" opacity=".5" fill="none"/>' + (f'<text x="0" y="-70" font-size="64" font-weight="bold" fill="#fff" stroke="none" text-anchor="middle" font-family="DejaVu Sans">{num}</text>' if num else "")
    o += f'<rect x="-11" y="-190" width="22" height="26" fill="{skin}"/>'
    # head
    o += f'<g transform="translate(0,-196) rotate({hr:.1f})">' + (f'<path d="M-48,-40 Q-52,30 -36,56 L40,56 Q54,30 48,-40Z" fill="{hair}"/>' if longhair else "") + f'<circle cx="0" cy="-36" r="42" fill="{skin}"/>'
    if back:
        o += f'<path d="M-44,-38 A44,44 0 0 1 44,-38 L42,-8 Q0,10 -42,-8Z" fill="{hair}"/>'
    else:
        o += f'<path d="M-43,-40 A43,43 0 0 1 43,-40 Q20,-64 0,-54 Q-22,-66 -43,-40Z" fill="{hair}"/>'
        er_ = {"calm": 7, "scared": 11, "shocked": 13, "grin": 7, "sad": 6}[expr]
        for ex in (-15, 15):
            o += (f'<ellipse cx="{ex}" cy="-34" rx="{er_}" ry="{er_ * blink:.1f}" fill="#fff" stroke-width="3"/>'
                  f'<circle cx="{ex + lx * 4:.1f}" cy="{-34 + ly * 3:.1f}" r="{3.4 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/>')
        if expr in ("scared", "shocked"):
            o += ('<ellipse cx="0" cy="-10" rx="8" ry="11" fill="#2a1014" stroke-width="3"/>'
                  '<path d="M-26,-52 l16,-8 M26,-52 l-16,-8" fill="none" stroke-width="4"/>')
        elif expr == "sad":
            o += '<path d="M-9,-8 q9,-7 18,0" fill="none" stroke-width="4"/><path d="M-26,-54 l16,7 M26,-54 l-16,7" fill="none" stroke-width="4"/>'
        elif expr == "grin":
            o += '<path d="M-14,-14 q14,14 28,0Z" fill="#fff" stroke-width="3"/>'
        else:
            o += '<path d="M-9,-12 q9,5 18,0" fill="none" stroke-width="4"/>'
    if hat:
        o += '<ellipse cx="0" cy="-66" rx="62" ry="13" fill="#2a2622"/><path d="M-34,-68 Q-32,-118 0,-120 Q32,-118 34,-68Z" fill="#2a2622"/>'
    if horns:
        o += '<path d="M-34,-68 L-52,-128 L-12,-76Z M34,-68 L52,-128 L12,-76Z" fill="#2a1014" stroke-width="5"/>'
    o += '</g>'
    o += f'<g transform="translate(52,-150)">{arm(ar, er, hold)}</g>'
    return o + '</g></g></g>'


# ---------------------------------------------------------------- Jersey Devil rig (horse head, bat wings, hooves, forked tail)
def devil(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(0.0, 0.0), shriek=None, body="#3a2b33"):
    """Rigged, animated Jersey Devil, feet at (x, y), ~620 units tall, faces LEFT (flip=True faces right).
    mode: stand (breathing, wings folded-ish, tail swaying) | fly (hovering, big wing flaps, legs dangling) | face (head only, centred at x,y).
    shriek: mouth opening 0-1 (None = automatic)."""
    sn = _m.sin
    fly = mode == "fly"
    fl = sn(t * (7.5 if fly else 2.0))
    wa = (-8 + fl * 40) if fly else (-4 + fl * 7)
    hov = (-sn(t * 3.7) * 34 - 120) if fly else sn(t * 1.7) * 3
    sway = sn(t * 2.6) * 18
    nr = sn(t * .9) * 4 + look[0] * 6
    blink = 0.12 if (t % 3.1) < 0.12 else 1.0
    mo = (0.15 + 0.1 * sn(t * 2)) if shriek is None else shriek
    MEM, BELLY, EYE = "#2a1d2e", "#5a4048", "#ff3a22"

    def wing(side):
        a = wa * side
        g = (f'<g transform="rotate({-(30 * side) + a * side * -1:.1f})"><g transform="scale({side},1)">'
             f'<path d="M0,0 L-130,-310 L-360,-290 L-290,-190 L-340,-100 L-200,-110 L-120,-20Z" fill="{MEM}"/>'
             f'<path d="M0,0 L-130,-310 L-8,-30" fill="{body}"/>'
             f'<path d="M-130,-310 L-290,-190 M-130,-310 L-200,-110" fill="none" stroke-width="5"/>'
             f'<path d="M-130,-310 L-170,-352 L-146,-320" fill="{body}"/></g></g>')
        return g

    def hind(sd, ph):
        a = (-30 + sn(t * 3.7 + ph) * 12) if fly else sd * 3
        k = (50 + sn(t * 3.7 + ph) * 10) if fly else 0
        return (f'<g transform="rotate({a:.1f})"><path d="M-30,-10 Q-60,60 -30,130 L26,120 Q30,50 28,-10Z" fill="{body}"/>'
                f'<g transform="translate(0,124) rotate({k:.1f})"><path d="M-24,-6 L-34,60 L-26,92 L24,92 L22,60 L26,-6Z" fill="{body}"/>'
                f'<path d="M-30,88 L-44,126 L38,126 L26,88Z" fill="#17101a"/></g></g>')

    def head():
        eyes = ""
        for ex, ey in ((-52, -22), (4, -34)):
            eyes += (f'<ellipse cx="{ex}" cy="{ey}" rx="13" ry="{11 * blink:.1f}" fill="{EYE}" stroke-width="4"/>'
                     f'<circle cx="{ex + look[0] * 4:.1f}" cy="{ey + look[1] * 3:.1f}" r="{4 * (1 if blink > .5 else .1):.1f}" fill="#ffe9a0" stroke="none"/>')
        op = 12 + 56 * mo
        teeth = "".join(f'<path d="M{-150 + i * 22},{14 + i * 0.6:.1f} l8,{14:.0f} l8,-14Z" fill="#f4efe2" stroke-width="2"/>' for i in range(5))
        return (f'<g transform="rotate({nr:.1f})">'
                f'<path d="M-14,-70 L-6,-176 L30,-76Z M-46,-72 L-62,-170 L-12,-84Z" fill="#17101a"/>'          # ears + horns
                f'<path d="M20,-70 q60,-90 14,-150 q-6,70 -40,100Z" fill="#17101a"/>'
                f'<ellipse cx="0" cy="-20" rx="64" ry="62" fill="{body}"/>'
                f'<path d="M-40,-50 Q-150,-30 -200,18 Q-204,44 -176,44 L-60,{34 + op * .1:.1f}Z" fill="{body}"/>'  # snout (top)
                f'<path d="M-60,{34 + op * .1:.1f} L-176,{44}  L-190,{44 + op:.1f} Q-150,{58 + op:.1f} -50,{52 + op:.1f}Z" fill="#241823"/>'
                f'<path d="M-176,{44} L-190,{44 + op:.1f}" stroke-width="5" fill="none"/>'
                + eyes + f'<g transform="translate(0,{op * .15:.1f})">{teeth}</g>'
                f'<circle cx="-186" cy="12" r="6" fill="#0d0f15" stroke="none"/>'
                f'<path d="M-30,-62 q20,-26 54,-8 M-50,-52 q-20,-14 -28,-34" fill="none" stroke-width="4" opacity=".5"/></g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + head() + '</g>'
    out += f'<g transform="translate(0,{hov:.1f})">'
    out += f'<g transform="translate(70,-260) rotate({sway - 10:.1f})"><path d="M0,-12 Q150,-30 190,80 Q210,150 170,200 L196,214 L214,178 L226,214 L240,196 L214,120 Q196,40 0,18Z" fill="{body}"/>'
    out += f'<path d="M176,198 l-28,38 l44,-18 l36,26 l-6,-44Z" fill="#17101a"/></g>'
    out += f'<g transform="translate(20,-380)">{wing(-1)}</g><g transform="translate(-20,-380)">{wing(1)}</g>'
    out += f'<g transform="translate(-36,-230)">{hind(-1, 0)}</g><g transform="translate(40,-230)">{hind(1, 2.2)}</g>'
    out += (f'<g transform="rotate({sn(t * 1.5) * 2:.1f})"><path d="M-84,-230 Q-110,-330 -60,-430 L60,-430 Q110,-330 84,-230Z" fill="{body}"/>'
            f'<path d="M-50,-250 Q0,-210 50,-250 Q56,-330 0,-400 Q-56,-330 -50,-250Z" fill="{BELLY}" stroke="none"/>')
    arm = -20 + sn(t * 2.2) * 8 if not fly else -40 + sn(t * 7.5) * 14
    out += (f'<g transform="translate(-60,-380) rotate({arm:.1f})"><path d="M-14,0 Q-26,60 -12,110 L16,106 Q22,50 14,0Z" fill="{body}"/>'
            f'<path d="M-14,108 l-6,26 M0,110 l0,28 M12,108 l8,26" stroke="#e8e0d0" stroke-width="6" fill="none"/></g>')
    out += (f'<g transform="translate(-20,-420) rotate({-12 + nr * .5:.1f})"><path d="M-30,10 Q-70,-60 -40,-130 L10,-120 Q-10,-60 30,10Z" fill="{body}"/>'
            f'<g transform="translate(-24,-146)">{head()}</g></g></g>')
    return out + '</g></g>'


# ---------------------------------------------------------------- the Brown Lady (floating ghost woman rig)
def lady(x, y, s=1.0, t=0.0, mode="glide", flip=False, look=(0.0, 0.0), alpha=0.92, gown="#6b4a34", face_only=False):
    """Rigged, animated ghost woman in an old brown gown, ~620 units tall, feet (hem) at (x, y). She floats.
    mode: glide (drifting, arms swaying) | beckon (one arm waves toward you) | stand (still, breathing) | face (head only, centred at x,y)."""
    sn = _m.sin
    hov = -26 - sn(t * 1.6) * 16
    lean = sn(t * 1.1) * 3
    hr = sn(t * .7) * 5 + look[0] * 6
    blink = 0.12 if (t % 4.1) < 0.14 else 1.0
    if mode == "beckon":
        a1, e1 = -120 + sn(t * 3) * 10, 40 + sn(t * 3) * 25
        a2, e2 = 10, -10
    elif mode == "stand":
        a1, e1, a2, e2 = 6, -10, -6, -10
    else:
        a1, e1 = 14 + sn(t * 1.4) * 8, -16 + sn(t * 1.9) * 8
        a2, e2 = -14 - sn(t * 1.3 + 1) * 8, -16 - sn(t * 1.7) * 8
    HAIR, SKIN = "#2a2020", "#e3dccd"

    def sleeve(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-20,-10 Q-30,60 -18,118 L18,118 Q30,60 20,-10Z" fill="{gown}"/>'
                f'<g transform="translate(0,114) rotate({e:.1f})"><path d="M-17,-4 Q-24,50 -14,96 L14,96 Q24,50 17,-4Z" fill="{gown}"/>'
                f'<path d="M-20,86 q20,22 40,0 l0,16 q-20,16 -40,0Z" fill="#e8e2d2"/><circle cx="0" cy="110" r="15" fill="{SKIN}"/></g></g>')

    def head():
        eyes = "".join(f'<ellipse cx="{ex}" cy="-8" rx="10" ry="{14 * blink:.1f}" fill="#06070b" stroke-width="3"/>'
                       f'<circle cx="{ex + look[0] * 3:.1f}" cy="{-8 + look[1] * 3:.1f}" r="3" fill="#cfe8ff" stroke="none"/>' for ex in (-17, 17))
        return (f'<g transform="rotate({hr:.1f})"><path d="M-48,-30 Q-60,60 -34,92 L38,92 Q60,60 48,-30Z" fill="{HAIR}"/>'
                f'<ellipse cx="0" cy="-2" rx="44" ry="54" fill="{SKIN}"/>'
                f'<path d="M-46,-14 Q-40,-72 0,-70 Q40,-72 46,-14 Q20,-46 0,-44 Q-20,-46 -46,-14Z" fill="{HAIR}"/>'
                f'<circle cx="0" cy="-86" r="26" fill="{HAIR}"/>'
                + eyes + f'<path d="M-9,30 q9,-6 18,0" fill="none" stroke-width="4"/>'
                f'<path d="M-26,-26 l14,-4 M26,-26 l-14,-4" fill="none" stroke-width="3" opacity=".6"/></g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if face_only or mode == "face":
        return out + head() + '</g>'
    out += f'<g opacity="{alpha}" transform="translate(0,{hov:.1f})">'
    # skirt with a waving hem
    w1, w2, w3 = sn(t * 2.2) * 22, sn(t * 2.2 + 1.6) * 26, sn(t * 2.2 + 3.1) * 22
    out += (f'<path d="M-70,-300 Q-150,-140 {-190 + w1:.1f},0 Q{-110 + w1:.1f},{26 + w2 * .3:.1f} {-60 + w2:.1f},8 Q0,{30 - w2 * .3:.1f} {60 + w3:.1f},8 '
            f'Q{110 + w3:.1f},{26 + w3 * .3:.1f} {190 + w3:.1f},0 Q150,-140 70,-300Z" fill="{gown}"/>'
            f'<path d="M-30,-250 Q-50,-120 {-60 + w1:.1f},-20 M30,-250 Q50,-120 {60 + w3:.1f},-20 M0,-260 Q0,-120 {w2:.1f},-10" fill="none" stroke-width="4" opacity=".4"/>')
    out += f'<g transform="translate(0,-300) rotate({lean:.1f})">'
    out += f'<g transform="translate(-60,-196)">{sleeve(a1, e1)}</g>'
    out += (f'<path d="M-62,0 Q-76,-100 -56,-214 Q0,-236 56,-214 Q76,-100 62,0Z" fill="{gown}"/>'
            f'<path d="M-40,-214 Q0,-170 40,-214" fill="#e8e2d2" stroke-width="5"/>')
    out += f'<rect x="-12" y="-244" width="24" height="34" fill="{SKIN}"/><g transform="translate(0,-292)">{head()}</g>'
    out += f'<g transform="translate(60,-196)">{sleeve(a2, e2)}</g>'
    return out + '</g></g></g>'


# ---------------------------------------------------------------- shared set pieces for the 2026-11-12 stories
def pine(x, y, h, col="#14241f", seed=None):
    r = random.Random(seed if seed is not None else int(x))
    s = f'<g fill="{col}"><rect x="{x - 8}" y="{y - h * .2:.0f}" width="16" height="{h * .2:.0f}"/>'
    for i in range(5):
        w = h * (.34 - i * .05); yy = y - h * .12 - i * h * .19
        s += f'<path d="M{x - w:.0f},{yy:.0f} L{x + r.randint(-6, 6)},{yy - h * .3:.0f} L{x + w:.0f},{yy:.0f}Z"/>'
    return s + '</g>'


def pineline(y, col="#101c1a", seed=3, hmin=380, hmax=700, step=110, x0=-40, x1=1400):
    r = random.Random(seed)
    return "".join(pine(x + r.randint(-30, 30), y, r.randint(hmin, hmax), col, seed * 31 + x) for x in range(x0, x1, step))


def waves(y, col="#1d3552", seed=4, rows=9, hi=34, line="#0d0f15"):
    r = random.Random(seed); s = ''
    for k in range(rows):
        yy = y + k * 110; ph = r.randint(0, 90)
        d = f'M-20,{yy} '
        for xx in range(-20, 1400, 130):
            d += f'q65,{-hi - k * 6 + (ph % 20)} 130,0 '
        s += f'<path d="{d} L1400,2420 L-20,2420Z" fill="{col}" stroke="{line}" stroke-width="5" opacity="{.75 + k * .03:.2f}"/>'
    return s


def snow(y, col="#cfd9e6"):
    return (f'<path d="M-20,{y} Q340,{y - 40} 675,{y} T1370,{y - 14} L1370,2420 L-20,2420Z" fill="{col}" {OUT}/>'
            f'<path d="M100,{y + 80} q80,-30 190,0 M700,{y + 140} q100,-34 230,0 M300,{y + 260} q80,-26 170,0" fill="none" stroke="#9fb0c8" stroke-width="6"/>')


def hoofprints(x0, y0, x1, y1, n=9, col="#7f8fa8"):
    s = ''
    for i in range(n):
        u = i / (n - 1); px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u + (14 if i % 2 else -14)
        s += (f'<g transform="translate({px:.0f},{py:.0f})" fill="{col}" stroke="#0d0f15" stroke-width="3"><path d="M-14,-18 Q-4,-6 -4,18 L-16,18 Q-26,0 -14,-18Z"/>'
              f'<path d="M14,-18 Q4,-6 4,18 L16,18 Q26,0 14,-18Z"/></g>')
    return s


def ship(x, y, s=1.0, hull="#4a3a2e", sail="#d6cfb8", lean=0.0):
    """Old two-masted sailing ship, side view, centred on x, waterline at y."""
    g = f'<g transform="translate({x},{y}) rotate({lean}) scale({s})" {OUT}>'
    g += f'<path d="M-420,-110 L420,-110 L340,40 L-340,40Z" fill="{hull}"/><path d="M-420,-110 H420 v-26 H-420Z" fill="#2b2119"/>'
    g += '<rect x="-12" y="-760" width="24" height="650" fill="#3a2b1f"/><rect x="-250" y="-640" width="24" height="530" fill="#3a2b1f"/><rect x="190" y="-560" width="24" height="450" fill="#3a2b1f"/>'
    g += (f'<path d="M-170,-720 Q-60,-620 -170,-340 H150 Q60,-620 150,-720Z" fill="{sail}"/><path d="M-120,-340 Q0,-300 120,-340 V-160 H-120Z" fill="{sail}"/>'
          f'<path d="M-244,-600 Q-340,-480 -420,-200 L-240,-200Z" fill="{sail}"/><path d="M210,-520 Q330,-400 390,-210 L214,-210Z" fill="{sail}"/>')
    g += '<path d="M-12,-760 L-12,-800 l70,16 l-70,16" fill="#8c2a2a"/>'
    return g + '</g>'


def window(x, y, w, h, lit="#f3c555"):
    return (f'<g {OUT}><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{lit}"/><path d="M{x + w / 2},{y} v{h} M{x},{y + h / 2} h{w}" fill="none"/></g>')


# ---------------------------------------------------------------- Spring-heeled Jack rig (cloak, helmet, glowing eyes, spring boots)
def jack(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(0.0, 0.0), flame=None, cloak="#14151f"):
    """Rigged, animated Spring-heeled Jack, ~600 units tall, feet at (x, y). Faces RIGHT (flip=True faces left).
    mode: stand (cloak swaying, breathing) | leap (bounces high on spring boots, legs tucking, cloak flaring) | claw (arm reaches out at you) | face (head only, centred at x,y).
    flame: 0-1 size of the blue fire from his mouth (None = automatic flicker in leap/claw)."""
    sn = _m.sin
    ph = (t * 1.25) % 1.0
    air = max(0.0, sn(ph * _m.pi)) if mode == "leap" else 0.0
    up = -air * 330
    sq = (1 - air) * (max(0, sn(ph * _m.pi * 2 + 2.2)) * 0 + 0)      # placeholder (no squash)
    tuck = air * 70
    fl = flame if flame is not None else (0.5 + 0.5 * sn(t * 9) if mode in ("leap", "claw") else 0.0)
    fl = max(0.0, fl)
    br = sn(t * 1.8) * 3
    flap = sn(t * 3.1) * 8 + (air * 30 if mode == "leap" else 0)
    hr = sn(t * .8) * 3 + look[0] * 5
    blink = 0.15 if (t % 3.3) < .12 else 1.0
    a1, e1, a2, e2 = 8 + sn(t * 1.5) * 4, -20, -8 - sn(t * 1.4) * 4, -20
    if mode == "leap":
        a1, e1, a2, e2 = 130 - air * 30, 20, 40 + air * 40, 30
    elif mode == "claw":
        a1, e1 = -95 + sn(t * 3) * 6, -10 + sn(t * 4) * 8
    SK, EYE = "#232733", "#ff7a1a"

    def arm(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-16,-8 Q-22,50 -12,104 L12,104 Q22,50 16,-8Z" fill="{cloak}"/>'
                f'<g transform="translate(0,100) rotate({e:.1f})"><path d="M-14,-4 Q-18,40 -10,84 L10,84 Q18,40 14,-4Z" fill="{cloak}"/>'
                f'<path d="M-12,82 l-10,38 M0,86 l0,44 M12,82 l12,36" stroke="#c9ccd6" stroke-width="6" stroke-linecap="round" fill="none"/>'
                f'<circle cx="0" cy="88" r="14" fill="#2b2f3d"/></g></g>')

    def leg(a, k):
        coil = "".join(f'<path d="M-22,{60 + i * 15} h44" stroke="#e0b24a" stroke-width="5" fill="none"/>' for i in range(3))
        return (f'<g transform="rotate({a:.1f})"><path d="M-24,-6 L24,-6 L20,96 L-20,96Z" fill="#1a1c27"/>'
                f'<g transform="translate(0,92) rotate({k:.1f})"><path d="M-20,0 L20,0 L16,96 L-16,96Z" fill="#1a1c27"/>{coil}'
                f'<path d="M-20,92 Q-24,114 0,114 Q44,114 50,102 Q46,92 18,92Z" fill="#8a6a2a"/></g></g>')

    def head():
        eyes = "".join(f'<path d="M{ex - 15},-20 Q{ex},{-34 * blink - 4:.1f} {ex + 15},-20 Q{ex},{-8 + 12 * (1 - blink):.1f} {ex - 15},-20Z" fill="{EYE}" stroke-width="3"/>' for ex in (-18, 18))
        mouth = ""
        if fl > .05:
            mouth = (f'<path d="M-10,12 Q0,{34 + fl * 20:.0f} 10,12Z" fill="#06070b" stroke-width="3"/>'
                     f'<path d="M10,16 Q{50 + fl * 70:.0f},{10 + sn(t * 12) * 8:.0f} {60 + fl * 110:.0f},{20 + sn(t * 9) * 12:.0f} Q{40 + fl * 50:.0f},{36} 8,24Z" fill="#7fc8ff" stroke="#e8f6ff" stroke-width="3"/>'
                     f'<path d="M14,20 Q{40 + fl * 40:.0f},18 {50 + fl * 70:.0f},22" fill="none" stroke="#fff" stroke-width="4"/>')
        else:
            mouth = '<path d="M-12,14 q12,8 24,0" fill="none" stroke-width="4"/>'
        return (f'<g transform="rotate({hr:.1f})"><path d="M-44,-30 Q-50,-100 0,-130 Q50,-100 44,-30Z" fill="#2a2c38"/>'
                f'<path d="M-20,-110 L0,-190 L20,-110Z" fill="#2a2c38"/>'      # pointed helmet spike
                f'<ellipse cx="0" cy="0" rx="40" ry="46" fill="{SK}"/>'
                f'<path d="M-46,-26 Q0,-50 46,-26 L46,-12 Q0,-30 -46,-12Z" fill="#14151f"/>' + eyes + mouth +
                f'<path d="M-34,24 L-10,60 L0,30 L12,60 L34,24Z" fill="#0b0c12" opacity=".0"/></g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + head() + '</g>'
    out += f'<g transform="translate(0,{up:.1f})">'
    # cloak behind
    out += (f'<g transform="translate(0,-340)"><path d="M-40,-150 Q{-150 - flap * 3:.0f},0 {-190 - flap * 4:.0f},{190 - air * 60:.0f} Q{-110 - flap:.0f},{150 - air * 40:.0f} {-60},{190 - air * 50:.0f} '
            f'Q-10,{140 - air * 30:.0f} 30,{196 - air * 50:.0f} L50,-150Z" fill="#0c0d14"/></g>')
    out += f'<g transform="translate(-24,-250)">{leg(-4 - tuck * .3, tuck * 1.2)}</g><g transform="translate(24,-250)">{leg(6 + tuck * .2, tuck * 1.5)}</g>'
    out += f'<g transform="translate(0,-250) rotate({sn(t * 1.1) * 2 + (-6 if mode == "claw" else 0):.1f})">'
    out += f'<g transform="translate(-44,-190)">{arm(a2, e2)}</g>'
    out += (f'<path d="M-46,0 Q-60,-100 -44,-200 Q0,-226 44,-200 Q60,-100 46,0Z" fill="{cloak}"/>'
            f'<path d="M-30,-190 Q0,-150 30,-190" fill="#2b2f3d" stroke-width="4"/><circle cx="0" cy="-130" r="14" fill="#e0b24a" stroke-width="3"/>')
    out += f'<rect x="-10" y="-232" width="20" height="26" fill="{SK}"/><g transform="translate(0,{-276 + br:.1f})">{head()}</g>'
    out += f'<g transform="translate(44,-190)">{arm(a1, e1)}</g>'
    return out + '</g></g></g>'


# ---------------------------------------------------------------- the Bell Witch (hooded floating spirit rig)
def wraith(x, y, s=1.0, t=0.0, mode="float", flip=False, look=(0.0, 0.0), alpha=0.9, robe="#1d1a26", glowc="#d8f0ff"):
    """Rigged, animated hooded spirit, ~600 units tall, hem at (x, y). Floats; no legs.
    mode: float (drifting, arms swaying) | reach (both arms stretch toward you) | loom (leans in, arms spread) | face (hood only, centred at x,y)."""
    sn = _m.sin
    hov = -34 - sn(t * 1.5) * 18
    lean = sn(t * 1.0) * 4
    hr = sn(t * .6) * 5 + look[0] * 5
    blink = 0.2 if (t % 3.9) < .15 else 1.0
    if mode == "reach":
        a1, e1, a2, e2 = -100 + sn(t * 2.6) * 8, 8 + sn(t * 3) * 10, -96 - sn(t * 2.4) * 8, 6 + sn(t * 3.3) * 10
        lean = -8
    elif mode == "loom":
        a1, e1, a2, e2 = 70 + sn(t * 2) * 10, 12, -70 - sn(t * 2.2) * 10, 12
        lean = -4 + sn(t * 2.5) * 3
    else:
        a1, e1, a2, e2 = 16 + sn(t * 1.4) * 8, -18 + sn(t * 1.9) * 8, -16 - sn(t * 1.3 + 1) * 8, -18 - sn(t * 1.7) * 8

    def arm(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-18,-8 Q-34,70 -16,150 L16,150 Q30,70 18,-8Z" fill="{robe}"/>'
                f'<g transform="translate(0,146) rotate({e:.1f})"><path d="M-14,-4 Q-24,50 -10,110 L10,110 Q24,50 14,-4Z" fill="{robe}"/>'
                f'<path d="M-10,106 l-12,46 M-3,110 l-3,56 M5,110 l3,56 M12,106 l14,44" stroke="#cfd6e0" stroke-width="5" stroke-linecap="round" fill="none"/></g></g>')

    def head():
        eyes = "".join(f'<ellipse cx="{ex}" cy="-4" rx="11" ry="{15 * blink:.1f}" fill="{glowc}" stroke-width="3"/>'
                       f'<circle cx="{ex + look[0] * 3:.1f}" cy="{-4 + look[1] * 3:.1f}" r="3.5" fill="#06070b" stroke="none"/>' for ex in (-20, 20))
        return (f'<g transform="rotate({hr:.1f})"><path d="M-70,80 Q-84,-60 -30,-110 Q0,-130 30,-110 Q84,-60 70,80 Q0,40 -70,80Z" fill="{robe}"/>'
                f'<path d="M-46,56 Q-54,-50 0,-84 Q54,-50 46,56 Q0,28 -46,56Z" fill="#07080d"/>' + eyes +
                f'<path d="M-14,30 q14,8 28,0" fill="none" stroke="#cfd6e0" stroke-width="3" opacity=".6"/></g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + head() + '</g>'
    out += f'<g opacity="{alpha}" transform="translate(0,{hov:.1f})">'
    w1, w2, w3 = sn(t * 2.4) * 26, sn(t * 2.4 + 1.7) * 30, sn(t * 2.4 + 3.2) * 26
    out += (f'<path d="M-76,-300 Q-170,-120 {-200 + w1:.0f},10 L{-130 + w1:.0f},{-30 + w2 * .3:.0f} L{-70 + w2:.0f},30 L{-10 + w2:.0f},-24 L{50 + w3:.0f},34 L{110 + w3:.0f},-20 L{200 + w3:.0f},10 '
            f'Q170,-120 76,-300Z" fill="{robe}"/>'
            f'<path d="M-30,-250 Q-50,-120 {-60 + w1:.0f},-20 M30,-250 Q50,-120 {60 + w3:.0f},-20" fill="none" stroke="#0d0f15" stroke-width="4" opacity=".4"/>')
    out += f'<g transform="translate(0,-300) rotate({lean:.1f})">'
    out += f'<g transform="translate(-62,-190)">{arm(a1, e1)}</g>'
    out += f'<path d="M-64,0 Q-80,-100 -58,-206 Q0,-230 58,-206 Q80,-100 64,0Z" fill="{robe}"/>'
    out += f'<g transform="translate(0,-262)">{head()}</g>'
    out += f'<g transform="translate(62,-190)">{arm(a2, e2)}</g>'
    return out + '</g></g></g>'


# ---------------------------------------------------------------- rigs and props for the 2026-11-14 stories
def mothman(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(0.0, 0.0), body="#55535e", wingc="#3b3644"):
    """Rigged, animated Mothman, ~620 units tall, feet at (x, y). Faces LEFT (flip=True faces right).
    mode: stand (breathing, wings twitching, eyes glowing) | fly (hovering, big wing flaps, legs dangling) | face (eyes close-up, centred at x,y)."""
    sn = _m.sin
    fly = mode == "fly"
    fl = sn(t * (8.5 if fly else 1.7))
    wa = fl * (34 if fly else 5)
    hov = (-150 - sn(t * 2.9) * 36) if fly else sn(t * 1.6) * 2
    sway = sn(t * 1.3) * 3
    blink = 0.15 if (t % 3.4) < .13 else 1.0
    EYE = "#ff2a1a"

    def wing(side):
        a = (-14 + wa) if not fly else (26 + wa)
        return (f'<g transform="rotate({-side * a:.1f})"><g transform="scale({side},1)">'
                f'<path d="M0,0 L-70,-340 L-330,-310 L-400,-160 L-270,-30 L-310,100 L-110,50Z" fill="{wingc}"/>'
                f'<path d="M0,0 L-70,-340 L-20,-20Z" fill="{body}"/>'
                f'<path d="M-70,-340 L-250,-150 M-70,-340 L-180,-30 M-70,-340 L-300,-60" fill="none" stroke-width="4" opacity=".55"/>'
                f'<circle cx="-250" cy="-200" r="34" fill="#8a7f6e" stroke-width="4"/><circle cx="-250" cy="-200" r="14" fill="#1a1620" stroke="none"/>'
                f'<circle cx="-170" cy="-80" r="22" fill="#8a7f6e" stroke-width="4"/><circle cx="-170" cy="-80" r="9" fill="#1a1620" stroke="none"/></g></g>')

    def leg(ph, sd):
        a = (-22 + sn(t * 3.0 + ph) * 12) if fly else sd * 3
        k = (46 + sn(t * 3.0 + ph) * 12) if fly else 0
        return (f'<g transform="rotate({a:.1f})"><path d="M-34,-6 Q-52,60 -26,124 L26,124 Q38,60 34,-6Z" fill="{body}"/>'
                f'<g transform="translate(0,120) rotate({k:.1f})"><path d="M-22,-4 L-30,60 L-24,112 L24,112 L18,60 L26,-4Z" fill="{body}"/>'
                f'<path d="M-30,104 L-44,138 L38,138 L24,104Z" fill="#1a1620"/></g></g>')

    def arm(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-14,-6 Q-20,60 -10,120 L10,120 Q20,60 14,-6Z" fill="{body}"/>'
                f'<g transform="translate(0,116) rotate({e:.1f})"><path d="M-11,-4 Q-14,40 -8,92 L8,92 Q14,40 11,-4Z" fill="{body}"/>'
                f'<path d="M-8,88 l-8,34 M0,90 l0,40 M8,88 l10,32" stroke="#1a1620" stroke-width="6" stroke-linecap="round" fill="none"/></g></g>')

    def head(scale=1.0):
        eyes = ""
        for ex in (-36, 36):
            eyes += (f'<g stroke="none">{glow(ex, -34, 80, "#ff2a1a", .35)}</g><ellipse cx="{ex}" cy="-34" rx="30" ry="{38 * blink:.1f}" fill="{EYE}" stroke-width="4"/>'
                     f'<ellipse cx="{ex + look[0] * 5:.1f}" cy="{-34 + look[1] * 4:.1f}" rx="9" ry="{12 * blink:.1f}" fill="#ffd0a0" stroke="none"/>')
        return (f'<g transform="scale({scale})"><path d="M-84,10 Q-96,-70 -40,-100 Q0,-116 40,-100 Q96,-70 84,10 Q0,36 -84,10Z" fill="{body}"/>'
                f'<path d="M-60,-84 q-14,-30 -4,-56 M60,-84 q14,-30 4,-56" fill="none" stroke-width="6"/>' + eyes + '</g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + head(1.6) + '</g>'
    out += f'<g transform="translate(0,{hov:.1f})">'
    out += f'<g transform="translate(24,-440)">{wing(-1)}</g><g transform="translate(-24,-440)">{wing(1)}</g>'
    out += f'<g transform="translate(-36,-250)">{leg(0, -1)}</g><g transform="translate(36,-250)">{leg(2.2, 1)}</g>'
    aa = (-18 + sn(t * 3.0) * 10) if fly else 6 + sn(t * 1.4) * 3
    out += f'<g transform="translate(0,-250) rotate({sway:.1f})">'
    out += f'<g transform="translate(-72,-228)">{arm(aa, -14)}</g>'
    out += (f'<path d="M-70,0 Q-92,-120 -68,-232 Q0,-264 68,-232 Q92,-120 70,0Z" fill="{body}"/>'
            f'<path d="M-40,-200 q20,10 40,0 M-44,-150 q22,10 44,0 M-40,-100 q20,10 40,0" fill="none" stroke-width="4" opacity=".45"/>')
    out += f'<g transform="translate(0,-262)">{head()}</g>'
    out += f'<g transform="translate(72,-228)">{arm(-aa, 14)}</g>'
    return out + '</g></g></g>'


def yuki(x, y, s=1.0, t=0.0, mode="glide", flip=False, look=(0.0, 0.0), alpha=0.95, frost=True):
    """Rigged, animated snow woman (Yuki-onna): white kimono, long black hair, pale-blue skin, floats, ~640 units tall, hem at (x, y).
    mode: glide (drifting, hair and sleeves blowing) | reach (one long sleeve and hand stretch toward you) | stand (still, breathing) | face (head only, centred at x,y).
    frost: breath puffs from her mouth."""
    sn = _m.sin
    hov = -24 - sn(t * 1.5) * 14
    lean = sn(t * 1.0) * 3
    hr = sn(t * .7) * 4 + look[0] * 6
    blink = 0.12 if (t % 4.3) < .14 else 1.0
    if mode == "reach":
        a1, e1 = -100 + sn(t * 2.4) * 6, 10 + sn(t * 3) * 12
        a2, e2 = 12, -12
        lean = -6
    elif mode == "stand":
        a1, e1, a2, e2 = 8, -10, -8, -10
    else:
        a1, e1 = 14 + sn(t * 1.3) * 8, -14 + sn(t * 1.8) * 8
        a2, e2 = -14 - sn(t * 1.2 + 1) * 8, -14 - sn(t * 1.6) * 8
    KIM, SKIN, HAIR, OBI = "#e9eff6", "#d6e6f0", "#0c0d14", "#7f93bd"
    blow = sn(t * 2.2) * 16

    def sleeve(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-24,-10 Q-48,70 -30,150 L30,150 Q44,70 22,-10Z" fill="{KIM}"/>'
                f'<g transform="translate(0,146) rotate({e:.1f})"><path d="M-26,-4 Q-40,56 -24,128 L24,128 Q38,56 24,-4Z" fill="{KIM}"/>'
                f'<path d="M-24,120 L24,120" stroke="{OBI}" stroke-width="8"/>'
                f'<path d="M-10,126 l-6,34 M0,128 l0,42 M10,126 l8,34" stroke="{SKIN}" stroke-width="9" stroke-linecap="round" fill="none"/></g></g>')

    def head():
        eyes = "".join(f'<ellipse cx="{ex}" cy="-4" rx="11" ry="{12 * blink:.1f}" fill="#f4fbff" stroke-width="3"/>'
                       f'<circle cx="{ex + look[0] * 3:.1f}" cy="{-4 + look[1] * 3:.1f}" r="{6 * (1 if blink > .5 else .2):.1f}" fill="#4fa8e8" stroke="none"/>' for ex in (-18, 18))
        puffs = ""
        if frost:
            for i in range(5):
                p = ((t * .8) + i * .2) % 1.0
                puffs += f'<circle cx="{-4 - p * 160 * (1 if mode == "reach" else .5):.0f}" cy="{34 + p * 10 - p * 30:.0f}" r="{10 + p * 26:.0f}" fill="#eaf6ff" stroke="none" opacity="{(1 - p) * .55:.2f}"/>'
        hairflow = f'<path d="M-50,-30 Q-70,70 {-60 + blow:.0f},150 L{-10 + blow:.0f},120 Q-20,60 -34,20Z M50,-30 Q70,70 {60 + blow:.0f},150 L{10 + blow:.0f},120 Q20,60 34,20Z" fill="{HAIR}"/>'
        return (f'<g transform="rotate({hr:.1f})">{hairflow}'
                f'<ellipse cx="0" cy="-2" rx="44" ry="54" fill="{SKIN}"/>'
                f'<path d="M-48,-14 Q-44,-76 0,-74 Q44,-76 48,-14 Q24,-44 6,-34 Q-10,-48 -48,-14Z" fill="{HAIR}"/>'
                + eyes + f'<path d="M-9,30 q9,5 18,0" fill="none" stroke="#6a8fb8" stroke-width="4"/>'
                f'<path d="M-30,-24 l16,-2 M30,-24 l-16,-2" fill="none" stroke-width="3" opacity=".6"/>{puffs}</g>')

    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + head() + '</g>'
    out += f'<g opacity="{alpha}" transform="translate(0,{hov:.1f})">'
    w1, w2, w3 = sn(t * 2.2) * 24, sn(t * 2.2 + 1.6) * 28, sn(t * 2.2 + 3.1) * 24
    out += (f'<path d="M-66,-300 Q-130,-140 {-170 + w1:.1f},0 Q{-100 + w1:.1f},{22 + w2 * .3:.1f} {-50 + w2:.1f},8 Q0,{26 - w2 * .3:.1f} {50 + w3:.1f},8 '
            f'Q{100 + w3:.1f},{22 + w3 * .3:.1f} {170 + w3:.1f},0 Q130,-140 66,-300Z" fill="{KIM}"/>'
            f'<path d="M-30,-250 Q-44,-120 {-50 + w1:.1f},-20 M30,-250 Q44,-120 {50 + w3:.1f},-20" fill="none" stroke-width="4" opacity=".35"/>')
    out += f'<g transform="translate(0,-300) rotate({lean:.1f})">'
    out += f'<g transform="translate(-62,-196)">{sleeve(a1, e1)}</g>'
    out += (f'<path d="M-62,0 Q-76,-100 -56,-214 Q0,-236 56,-214 Q76,-100 62,0Z" fill="{KIM}"/>'
            f'<path d="M-56,-70 H56 V-10 H-56Z" fill="{OBI}" stroke-width="5"/><path d="M-40,-214 L0,-150 L40,-214" fill="none" stroke-width="5"/>')
    out += f'<rect x="-12" y="-244" width="24" height="34" fill="{SKIN}"/><g transform="translate(0,-292)">{head()}</g>'
    out += f'<g transform="translate(62,-196)">{sleeve(a2, e2)}</g>'
    return out + '</g></g></g>'


def car(x, y, s=1.0, t=0.0, flip=False, body="#6a2a2a", beams=True, speed=1.0):
    """Old-fashioned sedan, side view facing LEFT (flip=True faces right), wheels touching y. Wheels spin, body bounces, headlight beam."""
    sn = _m.sin
    f = -1 if flip else 1
    bounce = sn(t * 14 * speed) * 3 * speed
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if beams:
        o += '<path d="M-300,-110 L-1000,-250 L-1000,40 Z" fill="#fff1b0" opacity=".28" stroke="none"/>'
    o += f'<g transform="translate(0,{bounce:.1f})">'
    o += (f'<path d="M-290,-80 Q-300,-160 -230,-175 L240,-175 Q300,-170 300,-90 L300,-60 L-290,-60Z" fill="{body}"/>'
          f'<path d="M-150,-175 L-90,-290 L120,-290 L210,-175Z" fill="{body}"/>'
          f'<path d="M-130,-180 L-80,-272 L-10,-272 L-10,-180Z M10,-180 L10,-272 L112,-272 L180,-180Z" fill="#9fb4c8"/>'
          f'<circle cx="-50" cy="-228" r="22" fill="#e2c29a" stroke-width="4"/><circle cx="64" cy="-228" r="22" fill="#d6b48c" stroke-width="4"/>'
          f'<ellipse cx="-280" cy="-120" rx="20" ry="26" fill="#fff1b0"/><rect x="-300" y="-72" width="600" height="14" fill="#b8bcc8"/></g>')
    for wx in (-170, 170):
        a = (t * 400 * speed) % 360
        o += (f'<g transform="translate({wx},-52)"><circle r="56" fill="#14161b"/><circle r="30" fill="#aab0bc" stroke-width="4"/>'
              f'<g transform="rotate({a:.0f})"><path d="M-30,0 H30 M0,-30 V30" stroke-width="5" fill="none"/></g></g>')
    return o + '</g>'


def snow_particles(t, n=70, seed=3, speed=260, drift=-220, w=1350, h=2400, op=.85):
    """Falling, drifting snowflakes (call from an actor fn; time-driven)."""
    r = random.Random(seed); s = ''
    for i in range(n):
        x0, y0, sp, rad = r.uniform(0, w), r.uniform(0, h), r.uniform(.6, 1.4), r.choice([3, 4, 5, 7])
        x = (x0 + drift * sp * t) % w; y = (y0 + speed * sp * t) % h
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad}" fill="#f2f7ff" opacity="{op}"/>'
    return s


# ---------------------------------------------------------------- rigs for the 2026-11-15 stories: sailing ship + wolf-like beast
def galleon(x, y, s=1.0, t=0.0, ghost=False, flip=False, alpha=1.0, roll=1.0, tattered=None):
    """Animated old sailing ship, side view, bow to the RIGHT (flip=True: bow left), waterline at (x, y), ~900 units tall.
    Rocks on the waves, sails billow, pennant flutters. ghost=True: pale green hull, torn sails, glowing windows."""
    sn = _m.sin
    tat = ghost if tattered is None else tattered
    hull, dark = ("#2f463f", "#17261f") if ghost else ("#5a4331", "#2b2119")
    sail = "#b4cbc0" if ghost else "#d6cfb8"
    rock = sn(t * .9) * 3.2 * roll
    bob = sn(t * 1.3 + 1) * 10 * roll
    bil = sn(t * 1.1) * 16
    f = -1 if flip else 1
    g = f'<g opacity="{alpha:.2f}" transform="translate({x},{y}) scale({f * s},{s})">'
    if ghost:
        g += glow(0, -300, 620, "#7fffc8", .22)
    g += f'<g transform="translate(0,{bob:.1f}) rotate({rock:.2f})" {OUT}>'
    for mx, top, w in ((-250, -620, 120), (-10, -800, 160), (240, -690, 125)):
        g += f'<rect x="{mx - 11}" y="{top}" width="22" height="{-top - 100}" fill="#3a2b1f"/>'
    for mx, top, w, h in ((-250, -590, 105, 210), (-10, -760, 140, 250), (-10, -480, 170, 260), (240, -660, 108, 220), (240, -430, 130, 200)):
        b = bil * (.6 if mx != 240 else .9)
        bot = top + h
        d = f'M{mx - w},{top} Q{mx},{top - 12 + b * .3:.0f} {mx + w},{top} L{mx + w + b:.0f},{bot} '
        if tat:
            n = 6
            for k in range(n):
                xx = mx + w + b - (2 * w + 0) * (k + .5) / n
                yy = bot + (34 if k % 2 == 0 else -22) + sn(t * 2 + k) * 8
                d += f'L{xx:.0f},{yy:.0f} '
            d += f'L{mx - w + b:.0f},{bot}Z'
        else:
            d += f'Q{mx + b * .5:.0f},{bot + 20 + bil:.0f} {mx - w + b:.0f},{bot}Z'
        g += f'<path d="{d}" fill="{sail}"/>'
        g += f'<path d="M{mx},{top} Q{mx + b * .4:.0f},{(top + bot) / 2:.0f} {mx + b * .5:.0f},{bot}" fill="none" stroke="#0d0f15" stroke-width="3" opacity=".35"/>'
        if tat:
            g += f'<ellipse cx="{mx - w * .35:.0f}" cy="{top + h * .45:.0f}" rx="{w * .16:.0f}" ry="{h * .12:.0f}" fill="{dark}" opacity=".55" stroke="none"/>'
    pw = sn(t * 5) * 8
    g += f'<path d="M-10,-800 L-10,-850 q60,{-8 + pw:.0f} 100,{4 - pw:.0f} q-50,{14 + pw:.0f} -100,{12 - pw:.0f}" fill="{"#d8f4e8" if ghost else "#8c2a2a"}" stroke-width="4"/>'
    g += f'<path d="M-440,-150 L440,-160 Q480,-168 540,-215 L430,40 L-330,40 Q-430,0 -440,-150Z" fill="{hull}"/>'
    g += f'<path d="M-440,-150 L-440,-290 L-250,-290 L-250,-155Z" fill="{hull}"/><path d="M-440,-290 h190" stroke-width="10"/>'
    g += f'<path d="M-440,-150 L440,-160 L430,-132 L-440,-122Z" fill="{dark}"/>'
    g += '<path d="M520,-205 L680,-290" stroke-width="12" fill="none"/>'
    lit = "#b8ffe0" if ghost else "#f3c555"
    for wx in (-405, -350, -295):
        g += f'<rect x="{wx}" y="-262" width="38" height="46" fill="{lit}" stroke-width="4"/>'
    for px in range(-180, 420, 110):
        g += f'<circle cx="{px}" cy="-70" r="15" fill="{lit}" stroke-width="4"/>'
    g += f'<path d="M-330,40 Q-100,70 330,40" fill="none" stroke="{dark}" stroke-width="5" opacity=".5"/>'
    return g + '</g></g>'


def gevaudan(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(0.0, 0.0), fur="#7b4a2e", fur2="#93603d", jaw=None):
    """Rigged, animated wolf-like beast (reddish coat, dark stripe down the back), paws at (x, y), ~380 units tall, faces LEFT (flip=True: right).
    mode: stand (breathing, tail swaying, head sweeping) | prowl (walking) | leap (bounds through the air) | howl (head thrown back) | face (head only, centred at x,y).
    jaw: 0-1 mouth opening (None = automatic)."""
    sn = _m.sin
    blink = 0.15 if (t % 3.1) < .12 else 1.0
    ph = t * 5.0
    body_rot = 0.0; lift = 0.0; head_rot = sn(t * .7) * 6 + look[0] * 6
    fa = [0, 0]; ba = [0, 0]; fk = [0, 0]; bk = [0, 0]; tail = 16 + sn(t * 1.6) * 8
    jw = 0.1 if jaw is None else jaw
    bob = sn(t * 1.8) * 3
    if mode == "prowl":
        fa = [sn(ph) * 30, -sn(ph) * 30]; ba = [-sn(ph) * 28, sn(ph) * 28]
        fk = [max(0, sn(ph + 1.3)) * 40, max(0, sn(ph + 1.3 + _m.pi)) * 40]
        bk = [max(0, sn(ph + 1.3)) * 40, max(0, sn(ph + 1.3 + _m.pi)) * 40]
        bob = -abs(sn(ph)) * 9; head_rot = 10 + sn(ph) * 4 + look[0] * 4; tail = 8 + sn(ph) * 6
        if jaw is None: jw = 0.0
    elif mode == "leap":
        c = (t * 1.1) % 1.0
        air = max(0.0, sn(c * _m.pi))
        lift = -air * 300; body_rot = -air * 16 + 8
        fa = [75 * air, 62 * air]; ba = [-72 * air, -60 * air]; fk = [-10 * air] * 2; bk = [30 * air] * 2
        head_rot = -6; tail = -10; bob = 0
        if jaw is None: jw = 0.55 * air + .1
    elif mode == "howl":
        head_rot = 58 + sn(t * 1.2) * 4; bob = sn(t * 1.4) * 4; tail = 24
        if jaw is None: jw = 0.85 + sn(t * 2.2) * .08
    elif mode == "stand":
        head_rot += sn(t * 1.1) * 8 + 4
        if jaw is None: jw = 0.12 + .06 * sn(t * 2)
    f = -1 if flip else 1

    def head():
        eye = (f'<ellipse cx="-88" cy="-20" rx="15" ry="{12 * blink:.1f}" fill="#ffd34a" stroke-width="4"/>'
               f'<ellipse cx="{-88 + look[0] * 3:.1f}" cy="{-20 + look[1] * 3:.1f}" rx="4" ry="{10 * blink:.1f}" fill="#1a0c06" stroke="none"/>')
        op = jw * 34
        return (f'<path d="M-6,-48 L14,-132 L48,-40Z" fill="{fur}"/><path d="M-62,-54 L-54,-138 L-18,-56Z" fill="{fur}"/>'
                f'<ellipse cx="-34" cy="-4" rx="88" ry="64" fill="{fur}"/>'
                f'<path d="M-104,-22 Q-196,-18 -226,12 Q-210,38 -112,34Z" fill="{fur2}"/>'
                f'<g transform="translate(-112,30) rotate({-op:.1f})"><path d="M0,-4 Q-88,10 -118,-4 L-108,-30 L0,-30Z" fill="{fur2}"/>'
                f'<path d="M-96,-6 l8,-20 l10,20 l10,-20 l10,20" fill="#f1efe6" stroke-width="2"/></g>'
                f'<path d="M-120,32 Q-112,{32 - op * .6:.0f} -112,{32 - op:.0f}" fill="none"/>'
                f'<path d="M-204,22 l8,24 l10,-22 l10,24 l10,-22 l10,22 l10,-22" fill="#f1efe6" stroke-width="2"/>'
                f'<ellipse cx="-226" cy="10" rx="14" ry="11" fill="#0d0f15"/>{eye}'
                f'<path d="M-112,-40 l50,12" stroke-width="5" fill="none"/>')

    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    if mode == "face":
        return out + f'<g transform="rotate({head_rot * .3:.1f})">' + head() + '</g></g>'
    out += f'<g transform="translate(0,{lift + bob:.1f}) rotate({body_rot:.1f},0,-200)">'

    def leg(hx, a, k, shade):
        c = "#5e3920" if shade else fur
        return (f'<g transform="translate({hx},-190) rotate({a:.1f})"><path d="M-30,-10 L30,-10 L22,120 L-22,120Z" fill="{c}"/>'
                f'<g transform="translate(0,116) rotate({k:.1f})"><path d="M-20,0 L20,0 L16,84 L-16,84Z" fill="{c}"/>'
                f'<ellipse cx="-12" cy="88" rx="34" ry="15" fill="{c}"/></g></g>')

    out += leg(-130, fa[1], fk[1], True) + leg(170, ba[1], bk[1], True)
    out += f'<g transform="translate(250,-260) rotate({tail:.1f})"><path d="M0,0 Q70,10 70,110 Q40,70 -10,40Z" fill="{fur}"/><path d="M50,60 q16,40 20,50 q-24,-10 -30,-30" fill="#5e3920" stroke="none"/></g>'
    out += f'<ellipse cx="40" cy="-235" rx="215" ry="108" fill="{fur}"/><ellipse cx="-160" cy="-262" rx="100" ry="105" fill="{fur}"/>'
    out += '<path d="M-90,-335 Q60,-352 250,-300 Q60,-322 -90,-312Z" fill="#35200f" stroke="none"/>'
    out += f'<path d="M-40,-150 q70,40 160,10" fill="none" stroke="#0d0f15" stroke-width="4" opacity=".35"/>'
    out += leg(-130, fa[0], fk[0], False) + leg(170, ba[0], bk[0], False)
    out += f'<g transform="translate(-232,-300) rotate({head_rot:.1f})">' + head() + '</g>'
    return out + '</g></g>'


# ---------------------------------------------------------------- Headless horseman rig (galloping horse + rider without a head, glowing pumpkin)
def horseman(x, y, s=1.0, t=0.0, mode="gallop", flip=False, pumpkin=True, horse="#2a2f42", cloak="#1c2030", ember="#ff9a2e"):
    """Rigged, animated headless rider on a black horse, hooves at (x, y), ~760 units tall, ~600 wide, faces LEFT (flip=True: right).
    mode: gallop | trot | rear (horse rears up) | stand (breathing, tail swishing, horse stamping) | throw (rider hurls the pumpkin arm forward).
    pumpkin: glowing jack-o'-lantern held in the raised hand."""
    sn = _m.sin
    ph = t * (9.0 if mode == "gallop" else 5.5 if mode == "trot" else 0)
    bob = rot = 0.0
    fa = [0, 0]; ba = [0, 0]; fk = [0, 0]; bk = [0, 0]
    arm = -60 + sn(t * 1.5) * 4; head = sn(t * 1.3) * 3
    tail = 14 + sn(t * 1.7) * 6; wave = 1.0
    if mode in ("gallop", "trot"):
        a = 38 if mode == "gallop" else 24
        fa = [sn(ph) * a, sn(ph + 1.0) * a]; ba = [-sn(ph + 2.4) * a, -sn(ph + 3.4) * a]
        fk = [max(0, sn(ph + 1.5)) * 62, max(0, sn(ph + 2.5)) * 62]; bk = [max(0, sn(ph + 3.9)) * 62, max(0, sn(ph + 4.9)) * 62]
        bob = -abs(sn(ph)) * (22 if mode == "gallop" else 9); rot = sn(ph * 1.0 + .4) * (3 if mode == "gallop" else 1.5)
        head = sn(ph) * 5 + 6; tail = 38 + sn(ph) * 10; wave = 2.2 if mode == "gallop" else 1.4
        arm = -100 + sn(ph) * 5
    elif mode == "rear":
        c = .5 + .5 * sn(t * 1.6)
        rot = 22 * c; fa = [-70 * c, -50 * c]; fk = [-60 * c, -40 * c]; head = -12 * c; tail = 30; wave = 1.6
        arm = -150 + sn(t * 3) * 6; bob = -4 * c
    elif mode == "throw":
        c = (t * .9) % 1.0
        arm = -40 - 140 * (sn(c * _m.pi) ** .6) if c < .6 else -50
        ph = t * 8.0; a = 30
        fa = [sn(ph) * a, sn(ph + 1.0) * a]; ba = [-sn(ph + 2.4) * a, -sn(ph + 3.4) * a]
        fk = [max(0, sn(ph + 1.5)) * 55, max(0, sn(ph + 2.5)) * 55]; bk = [max(0, sn(ph + 3.9)) * 55, max(0, sn(ph + 4.9)) * 55]
        bob = -abs(sn(ph)) * 18; tail = 36; wave = 2.0
    else:
        bob = sn(t * 1.8) * 3; fa[1] = max(0, sn(t * 2.4)) * -22; fk[1] = max(0, sn(t * 2.4)) * 40
        head = -6 + sn(t * 1.1) * 6; tail = 18 + sn(t * 2.0) * 14
    f = -1 if flip else 1
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    out += f'<g transform="translate(0,{bob:.1f}) rotate({rot:.1f},150,-60)">'

    def leg(hx, a, k, shade):
        c = "#10121a" if shade else horse
        return (f'<g transform="translate({hx},-250) rotate({a:.1f})"><path d="M-32,-14 L32,-14 L20,130 L-20,130Z" fill="{c}"/>'
                f'<g transform="translate(0,126) rotate({k:.1f})"><path d="M-19,0 L19,0 L14,100 L-14,100Z" fill="{c}"/>'
                f'<path d="M-24,92 L24,92 L22,128 L-26,128Z" fill="#2a2d3a" stroke-width="4"/></g></g>')

    out += leg(-110, fa[1], fk[1], True) + leg(150, ba[1], bk[1], True)
    out += f'<g transform="translate(205,-330) rotate({tail:.1f})"><path d="M0,0 Q90,20 80,160 Q50,90 -10,60Z" fill="#0b0c12"/></g>'
    # rider (behind the horse's body, saddle at (40,-400))
    r = f'<g transform="translate(40,-400)">'
    wv = sn(t * (9 if mode in ("gallop", "throw") else 3)) * 10 * wave
    ck = ''
    ck += f'<path d="M20,-60 Q150,-30 {210 + wv * 2:.0f},{60 + wv:.0f} Q150,60 {120 + wv:.0f},{150 + wv:.0f} Q60,120 10,40Z" fill="{cloak}"/>'
    ck += f'<path d="M40,-30 Q150,10 {190 + wv * 2:.0f},{70 + wv:.0f}" fill="none" stroke="#2c3040" stroke-width="4"/>'
    r += f'<g transform="rotate({-14 + head * .5:.1f})"><path d="M-48,0 Q-64,-110 -34,-210 Q10,-236 56,-206 Q80,-110 52,0Z" fill="#242838"/>'
    r += '<path d="M-34,-208 Q10,-190 56,-206 L52,-232 Q4,-250 -36,-232Z" fill="#161824" stroke-width="5"/>'      # collar, neck stump
    r += '<path d="M-26,-232 Q10,-216 48,-232" fill="#050609" stroke="none"/>'
    # raised arm with pumpkin
    r += f'<g transform="translate(-40,-190) rotate({arm:.1f})"><path d="M-22,-8 Q-30,50 -20,104 L20,104 Q30,50 22,-8Z" fill="#242838"/>'
    r += f'<g transform="translate(0,100) rotate({-30 + arm * -.1:.1f})"><path d="M-19,-4 Q-22,40 -15,84 L15,84 Q22,40 19,-4Z" fill="#242838"/><circle cx="0" cy="92" r="16" fill="#8a8f9c"/>'
    if pumpkin:
        fl = 1 + .08 * sn(t * 23) + .05 * sn(t * 37)
        r += (f'<g transform="translate(0,112)"><circle cx="0" cy="0" r="{110 * fl:.0f}" fill="{ember}" opacity=".28" stroke="none"/>'
              f'<ellipse cx="0" cy="0" rx="62" ry="54" fill="#e0701c"/><path d="M-24,-50 Q-30,0 -24,50 M24,-50 Q30,0 24,50" fill="none" stroke="#a84c10" stroke-width="4"/>'
              f'<path d="M-6,-54 q4,-24 22,-26" fill="none" stroke="#2a4a22" stroke-width="8"/>'
              f'<path d="M-38,-14 L-18,-14 L-28,-34Z M18,-14 L38,-14 L28,-34Z" fill="#ffd25a" stroke-width="3"/>'
              f'<path d="M-30,12 L-18,26 L-8,14 L4,28 L14,14 L24,26 L32,12 Q0,44 -30,12Z" fill="#ffd25a" stroke-width="3"/></g>')
    r += '</g></g></g>'
    # other arm holding the reins
    r += '<path d="M10,-150 Q-40,-120 -90,-100" fill="none" stroke="#242838" stroke-width="36" stroke-linecap="round"/>'
    r += '</g>'
    # horse body, neck, head
    out += f'<g transform="translate(0,0)">'
    out += r
    out += f'<ellipse cx="20" cy="-330" rx="215" ry="105" fill="{horse}"/>'
    out += f'<path d="M-130,-300 Q-200,-480 -250,-560 L-170,-600 Q-100,-480 -40,-400Z" fill="{horse}"/>'
    out += '<path d="M-200,-560 Q-120,-500 -60,-380 Q-110,-500 -170,-590Z" fill="#0b0c12" stroke="none"/>'
    out += (f'<g transform="translate(-220,-580) rotate({head:.1f})"><path d="M-10,-30 L20,-100 L48,-30Z" fill="{horse}"/>'
            f'<path d="M-28,-40 Q60,-70 76,-10 Q20,40 -150,110 Q-190,100 -176,70 Q-60,10 -28,-40Z" fill="{horse}"/>'
            f'<ellipse cx="-168" cy="90" rx="22" ry="16" fill="#0b0c12" stroke="none"/>'
            f'<ellipse cx="-4" cy="-8" rx="13" ry="11" fill="#ff7a2a" stroke-width="4"/><circle cx="-4" cy="-8" r="5" fill="#ffd25a" stroke="none"/></g>')
    out += leg(-110, fa[0], fk[0], False) + leg(150, ba[0], bk[0], False)
    out += f'<g transform="translate(40,-400)">{ck}</g>'
    out += '<path d="M-120,-270 Q20,-230 160,-270" fill="none" stroke="#0d0f15" stroke-width="4" opacity=".4"/>'
    out += '<path d="M10,-420 Q60,-450 110,-420 L100,-380 Q55,-395 10,-380Z" fill="#3a2a22" stroke-width="5"/>'   # saddle
    return out + '</g></g></g>'


# ---------------------------------------------------------------- Ghost light (orb) rig
def orb(x, y, s=1.0, t=0.0, mode="float", col="#ffe9a8", seed=0, split=None):
    """Animated glowing ghost light centred at (x, y), radius ~60*s. mode: float (drifting, pulsing) | flicker (fast flicker) | dance (circles around).
    split: 0-1 shows a smaller twin orb splitting off to the right."""
    sn = _m.sin
    if mode == "dance":
        dx, dy = sn(t * 1.7 + seed) * 120, sn(t * 2.3 + seed * 2) * 60
    elif mode == "flicker":
        dx, dy = sn(t * 3 + seed) * 20, sn(t * 4 + seed) * 12
    else:
        dx, dy = sn(t * .8 + seed) * 50, sn(t * 1.1 + seed * 1.7) * 30
    pul = 1 + .12 * sn(t * (14 if mode == "flicker" else 3) + seed)
    if mode == "flicker" and sn(t * 17 + seed) > .9:
        pul *= .55

    def one(ox, oy, k):
        r = 60 * s * k * pul
        return (f'<circle cx="{ox:.0f}" cy="{oy:.0f}" r="{r * 4.2:.0f}" fill="{col}" opacity=".10"/>'
                f'<circle cx="{ox:.0f}" cy="{oy:.0f}" r="{r * 2.4:.0f}" fill="{col}" opacity=".22"/>'
                f'<circle cx="{ox:.0f}" cy="{oy:.0f}" r="{r * 1.3:.0f}" fill="{col}" opacity=".55"/>'
                f'<circle cx="{ox:.0f}" cy="{oy:.0f}" r="{r * .7:.0f}" fill="#fffdf0"/>')
    o = '<g>' + one(x + dx, y + dy, 1.0)
    if split:
        o += one(x + dx + split * 260 * s, y + dy - split * 40 + sn(t * 2.1) * 20, .7)
    return o + '</g>'


# ---------------------------------------------------------------- Hairy Hand rig (Dartmoor)
def hairyhand(x, y, s=1.0, t=0.0, mode="reach", rot=0.0, flip=False, skin="#8c7562", hair="#241a14", alpha=1.0, seed=1):
    """Rigged, animated shaggy hand. (x, y) = wrist; the hand points UP (rot rotates it clockwise around the wrist), the forearm
    trails 300 units downward. mode: reach (fingers wiggle, sways) | grip (clenched, trembling) | crawl (fingers walking) | wave."""
    sn = _m.sin
    f = -1 if flip else 1
    sway = sn(t * 1.7 + seed) * 5
    if mode == "grip":
        c1 = [68 + sn(t * 31 + i) * 3 for i in range(4)]; c2 = [78 + sn(t * 29 + i) * 3 for i in range(4)]
        th = 50; sway = sn(t * 33) * 2.5
    elif mode == "crawl":
        c1 = [max(0, sn(t * 6 + i * 1.2)) * 36 - 8 for i in range(4)]; c2 = [max(0, sn(t * 6 + i * 1.2 + .8)) * 44 for i in range(4)]
        th = 10 + sn(t * 6) * 8; sway = sn(t * 3) * 3
    elif mode == "wave":
        c1 = [6 + sn(t * 4 + i) * 6 for i in range(4)]; c2 = [6 + sn(t * 4 + i + .5) * 8 for i in range(4)]
        th = 0; sway = sn(t * 4) * 16
    else:
        c1 = [14 + sn(t * 3 + i * .9) * 12 for i in range(4)]; c2 = [20 + sn(t * 3.4 + i * .9) * 14 for i in range(4)]
        th = -10 + sn(t * 2.4) * 6
    o = (f'<g transform="translate({x},{y}) rotate({rot + sway:.1f}) scale({f * s},{s})" {OUT} opacity="{alpha}">'
         f'<path d="M-44,0 L-54,330 L54,330 L44,0Z" fill="{skin}"/>')
    rr = random.Random(seed * 7 + 3); hs = f'<g stroke="{hair}" stroke-width="4" fill="none" stroke-linecap="round">'
    for _ in range(46):
        px, py = rr.randint(-38, 38), rr.randint(-100, 300); a = rr.choice([-1, 1]) * rr.randint(10, 24)
        hs += f'<path d="M{px},{py} l{a * .5:.0f},-{rr.randint(14, 28)}"/>'
    hs += '</g>'
    L1, L2, W = (78, 60, 24)
    for i, (px, k) in enumerate(zip((-36, -12, 12, 36), (.9, 1.1, 1.0, .8))):
        l1, l2 = L1 * k, L2 * k
        o += (f'<g transform="translate({px},-96) rotate({(c1[i] * (1 if i > 1 else .8)) * (-1 if px < 0 else 1) * .6 + c1[i] * .4:.1f})">'
              f'<rect x="{-W / 2}" y="{-l1}" width="{W}" height="{l1 + 8}" rx="12" fill="{skin}"/>'
              f'<g transform="translate(0,{-l1}) rotate({c2[i]:.1f})"><rect x="{-W * .45}" y="{-l2}" width="{W * .9}" height="{l2 + 6}" rx="12" fill="{skin}"/>'
              f'<path d="M{-W * .3},{-l2 + 6} l{W * .3},10 l{W * .3},-10" fill="none" stroke-width="3"/></g></g>')
    o += (f'<g transform="translate(-44,-34) rotate({-48 + th:.1f})"><rect x="-14" y="-74" width="28" height="84" rx="14" fill="{skin}"/></g>'
          f'<path d="M-50,10 Q-56,-60 -44,-104 L44,-104 Q56,-60 50,10Z" fill="{skin}"/>')
    return o + hs + '</g>'


# ---------------------------------------------------------------- Baba Yaga rig (hunched witch; walks, points, cackles, flies in a mortar)
def babayaga(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(0.0, 0.0), dress="#4b2f52", scarf="#8a2f2f", skin="#b4c098", cackle=False):
    """Rigged, animated Baba Yaga, feet at (x, y), ~430 units tall, faces RIGHT (flip=True faces left).
    mode: stand (leaning on a broom, breathing) | walk (hobbling) | point (arm out, leaning forward) | fly (sitting in a flying mortar, broom trailing; (x, y) = mortar centre)."""
    sn = _m.sin
    f = -1 if flip else 1
    ph = t * 4.2
    bob = la = ra = lk = rk = 0.0; lean = 14.0
    al, el, ar, er = 8, 20, -20, -30
    if mode == "walk":
        la, ra = sn(ph) * 20, -sn(ph) * 20; lk, rk = max(0, sn(ph + 1.3)) * 26, max(0, sn(ph + 1.3 + _m.pi)) * 26
        bob = -abs(sn(ph)) * 8; ar, er = -sn(ph) * 14 - 25, -35
    elif mode == "point":
        ar, er = -95 + sn(t * 3) * 3, -4; lean = 22; bob = sn(t * 1.6) * 3
    else:
        bob = sn(t * 1.7) * 3; ar = -22 + sn(t * 1.3) * 4
    if cackle:
        bob += sn(t * 17) * 4; lean += sn(t * 17) * 3
    blink = 0.15 if (t % 4.1) < .12 else 1.0
    hr = sn(t * .9) * 4 + look[0] * 8
    wild = sn(t * 2.4)

    def arm(a, e, item):
        g = (f'<g transform="rotate({a:.1f})"><path d="M-16,-6 Q-22,40 -12,88 L12,88 Q20,40 16,-6Z" fill="{dress}"/>'
             f'<g transform="translate(0,84) rotate({e:.1f})"><path d="M-13,-4 Q-16,36 -9,76 L9,76 Q16,36 13,-4Z" fill="{dress}"/>'
             f'<path d="M-8,70 q-6,26 -2,38 M0,72 q0,28 2,40 M8,70 q6,26 2,36" fill="none" stroke-width="7" stroke="#0d0f15"/>'
             f'<circle cx="0" cy="84" r="14" fill="{skin}"/>')
        if item == "broom":
            g += ('<g transform="translate(0,84)"><rect x="-6" y="-170" width="12" height="400" fill="#6a4a2c"/>'
                  '<path d="M-26,150 L26,150 L52,260 L-52,260Z" fill="#b89a4a"/><path d="M-26,176 H26 M-14,150 V260 M14,150 V260" fill="none" stroke-width="3"/></g>')
        return g + '</g></g>'

    def leg(a, k):
        return (f'<g transform="rotate({a:.1f})"><path d="M-22,-4 L22,-4 L18,76 L-18,76Z" fill="{dress}"/>'
                f'<g transform="translate(0,74) rotate({k:.1f})"><path d="M-17,0 L17,0 L15,58 L-15,58Z" fill="{skin}"/>'
                f'<path d="M-16,54 Q-18,76 2,76 Q34,76 38,66 Q34,56 16,54Z" fill="#14161b"/></g></g>')

    if mode == "fly":
        fb = sn(t * 2.2) * 14
        o = f'<g transform="translate({x},{y + fb:.1f}) rotate({sn(t * 1.6) * 4:.1f}) scale({f * s},{s})" {OUT}>'
        # broom trailing behind (left), swept by her
        o += (f'<g transform="translate(-30,60) rotate({-62 + sn(t * 3) * 6:.1f})"><rect x="-6" y="0" width="12" height="260" fill="#6a4a2c"/>'
              f'<g transform="translate(0,255) rotate({sn(t * 5) * 8:.1f})"><path d="M-30,0 L30,0 L56,120 L-56,120Z" fill="#b89a4a"/><path d="M-14,0 V120 M14,0 V120" fill="none" stroke-width="3"/></g></g>')
        o += f'<g transform="translate(10,-60) rotate({lean * .6:.1f})"><path d="M-60,0 Q-70,-100 -30,-150 L40,-150 Q74,-90 60,0Z" fill="{dress}"/>'
        o += f'<g transform="translate(34,-132)">{arm(-50 + sn(t * 2) * 6, -40, None)}</g>'
        o += _baba_head(t, skin, scarf, blink, hr, look, cackle, wild, -178)
        o += '</g>'
        o += (f'<path d="M-130,-70 Q-140,60 -90,110 L90,110 Q140,60 130,-70Z" fill="#7a7a86"/><ellipse cx="0" cy="-70" rx="130" ry="26" fill="#4a4a56"/>'
              f'<path d="M-100,10 H100 M-110,-30 H110" fill="none" stroke-width="4" opacity=".6"/>'
              f'<g transform="translate(70,-30) rotate({-22 + sn(t * 2.4) * 6:.1f})"><rect x="-9" y="-190" width="18" height="260" rx="8" fill="#9a9aa6"/></g></g>')
        return o
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(0,{bob:.1f})">'
    o += f'<g transform="translate(-16,-150)">{leg(la, lk)}</g><g transform="translate(18,-150)">{leg(ra, rk)}</g>'
    o += f'<g transform="translate(0,-150) rotate({lean:.1f})">'
    o += f'<g transform="translate(-34,-140)">{arm(al, el, "broom" if mode == "stand" else None)}</g>'
    o += (f'<path d="M-62,10 Q-74,-80 -46,-150 Q0,-176 52,-148 Q74,-70 64,10Z" fill="{dress}"/>'
          f'<path d="M-40,-30 H50 M-30,-70 H44" fill="none" stroke-width="4" opacity=".35"/>')
    o += _baba_head(t, skin, scarf, blink, hr, look, cackle, wild, -182)
    o += f'<g transform="translate(40,-140)">{arm(ar, er, None)}</g>'
    return o + '</g></g></g>'


def _baba_head(t, skin, scarf, blink, hr, look, cackle, wild, hy):
    lx, ly = look
    o = f'<g transform="translate(14,{hy}) rotate({hr:.1f})">'
    o += f'<path d="M-44,-20 Q-70,30 -52,70 Q-40,40 -34,10Z M-30,10 Q-56,60 -30,92 Q-26,50 -18,16Z" fill="#d9dbe0" stroke-width="4"/>'
    o += f'<circle cx="0" cy="-30" r="44" fill="{skin}"/>'
    o += f'<path d="M-48,-30 A48,48 0 0 1 48,-30 Q24,-60 0,-56 Q-26,-62 -48,-30Z" fill="{scarf}"/><path d="M-46,-26 q-18,20 -8,48 q10,-20 14,-30Z" fill="{scarf}"/>'
    o += f'<path d="M28,-30 Q80,-18 70,6 Q56,-6 36,-8Z" fill="{skin}"/>'
    o += f'<path d="M-6,-12 Q4,-6 18,-14" fill="none" stroke-width="4"/>'
    for ex in (-10, 16):
        o += (f'<ellipse cx="{ex}" cy="-34" rx="8" ry="{8 * blink:.1f}" fill="#fff" stroke-width="3"/>'
              f'<circle cx="{ex + lx * 3:.1f}" cy="{-34 + ly * 2:.1f}" r="{3.4 if blink > .5 else .1}" fill="#0d0f15" stroke="none"/>')
    o += '<path d="M-20,-50 l16,-6 M10,-52 l18,4" fill="none" stroke-width="4"/>'
    if cackle:
        o += f'<path d="M-6,0 Q14,{20 + abs(wild) * 8:.0f} 36,-2 Q14,-8 -6,0Z" fill="#2a1014" stroke-width="4"/><path d="M8,-4 l4,10 l4,-10Z" fill="#c8ccd4" stroke-width="2"/>'
    else:
        o += '<path d="M-4,4 Q16,12 38,-4" fill="none" stroke-width="4"/><path d="M14,6 l4,10 l4,-10Z" fill="#c8ccd4" stroke-width="2"/>'
    o += '<circle cx="-14" cy="-6" r="5" fill="#7a5a4a" stroke-width="2"/>'
    return o + '</g>'


# ---------------------------------------------------------------- Baba Yaga's hut on chicken legs
def hutlegs(x, y, s=1.0, t=0.0, mode="stand", flip=False, door=0.0, spin=False):
    """Rigged hut standing on two huge chicken legs, feet at (x, y), ~700 units tall, front faces RIGHT (flip=True faces left).
    mode: stand (shifting weight, creaking) | walk (stomping along) .  door: 0-1 how far the door is open (light spills out). spin=True turns the hut like a lazy top."""
    sn = _m.sin
    f = -1 if flip else 1
    ph = t * 3.0
    if mode == "walk":
        a1, a2 = sn(ph) * 30, -sn(ph) * 30; k1, k2 = max(0, sn(ph + 1.2)) * 50, max(0, sn(ph + 1.2 + _m.pi)) * 50
        bob = -abs(sn(ph)) * 16; tilt = sn(ph) * 2
    else:
        a1, a2 = sn(t * 1.1) * 5, -sn(t * 1.1) * 5 - 4; k1 = k2 = 6 + sn(t * 1.1) * 4
        bob = sn(t * 1.1) * 6; tilt = sn(t * .7) * 1.5

    def leg(a, k):
        return (f'<g transform="rotate({a:.1f})"><path d="M-22,0 L22,0 L16,160 L-16,160Z" fill="#d9a83e"/><path d="M-18,50 h36 M-16,100 h32" fill="none" stroke-width="4"/>'
                f'<g transform="translate(0,160) rotate({-k:.1f})"><path d="M-16,0 L16,0 L12,150 L-12,150Z" fill="#c9962e"/><path d="M-12,60 h24 M-12,100 h24" fill="none" stroke-width="4"/>'
                f'<g transform="translate(0,150) rotate({k * .6 - a * .5:.1f})"><path d="M-14,0 L14,0 L10,14 L-10,14Z" fill="#c9962e"/>'
                f'<path d="M-6,8 Q60,10 84,34 Q40,40 -6,30Z M-6,8 Q-50,10 -74,34 Q-30,40 6,30Z M0,8 Q80,-8 120,10 Q70,30 6,26Z" fill="#d9a83e"/></g></g></g>')
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    o += f'<g transform="translate(-70,{-310 + bob:.1f})">{leg(a1, k1)}</g><g transform="translate(60,{-300 + bob:.1f})">{leg(a2, k2)}</g>'
    sx = abs(_m.cos(t * 1.1)) * .75 + .25 if spin else 1.0
    o += f'<g transform="translate(0,{-310 + bob:.1f}) rotate({tilt:.1f}) scale({sx:.2f},1)">'
    o += ('<rect x="-200" y="-300" width="400" height="300" fill="#6a4a2c"/>'
          '<path d="M-200,-100 H200 M-200,-200 H200" fill="none" stroke-width="5"/><path d="M-224,-300 L0,-470 L224,-300Z" fill="#a8935a"/>'
          '<path d="M-150,-320 l-10,24 M-90,-340 l-6,40 M-30,-356 l0,56 M40,-350 l6,50 M110,-334 l10,34" fill="none" stroke-width="4"/>'
          '<rect x="-150" y="-230" width="90" height="90" fill="#f3c555"/><path d="M-105,-230 V-140 M-150,-185 H-60" fill="none" stroke-width="5"/>'
          '<rect x="40" y="-250" width="110" height="250" fill="#2a1a10"/>')
    if door > 0:
        o += (f'<rect x="40" y="-250" width="110" height="250" fill="#ffcf6a"/>'
              f'<path d="M40,-250 L{40 + 90 * (1 - door * .7):.0f},{-250 + 14 * door:.0f} L{40 + 90 * (1 - door * .7):.0f},{-14 * door:.0f} L40,0Z" fill="#4a2f1a"/>')
    else:
        o += '<circle cx="62" cy="-120" r="8" fill="#d9b44a"/>'
    o += '</g></g>'
    return o


# ---------------------------------------------------------------- Dutchman helpers (Arizona desert)
def saguaro(x, y, s=1.0, col="#2c4a34"):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT} fill="{col}"><rect x="-34" y="-420" width="68" height="420" rx="34"/>'
            '<path d="M-34,-250 Q-110,-250 -110,-330 L-110,-380 Q-110,-410 -84,-410 Q-60,-410 -60,-380 L-60,-330 Q-60,-300 -34,-300Z"/>'
            '<path d="M34,-200 Q106,-200 106,-270 L106,-320 Q106,-350 82,-350 Q58,-350 58,-320 L58,-270 Q58,-250 34,-250Z"/></g>')


def needle(x, y, s=1.0, col="#6a4a3a", hi="#9a6a4a"):
    """Weaver's Needle-style rock spire, base centred at (x, y)."""
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-260,0 L-200,-260 L-120,-420 L-80,-900 L-30,-1000 L20,-960 L60,-560 L110,-420 L230,-200 L300,0Z" fill="{col}"/>'
            f'<path d="M-30,-1000 L20,-960 L60,-560 L110,-420 L40,-420 L-10,-700Z" fill="{hi}" stroke="none"/>'
            '<path d="M-120,-420 L-60,-300 L-90,-100 M110,-420 L70,-300 L100,-90" fill="none" stroke-width="4" opacity=".6"/></g>')


def mesa(x, y, w, h, col="#5a3a34", hi="#7a4a3c"):
    return (f'<g {OUT}><path d="M{x - w / 2:.0f},{y} L{x - w * .4:.0f},{y - h} L{x + w * .4:.0f},{y - h} L{x + w / 2:.0f},{y}Z" fill="{col}"/>'
            f'<path d="M{x - w * .4:.0f},{y - h} L{x + w * .4:.0f},{y - h} L{x + w * .38:.0f},{y - h * .85:.0f} L{x - w * .38:.0f},{y - h * .85:.0f}Z" fill="{hi}" stroke="none"/></g>')


def nuggets(x, y, s=1.0, n=14, seed=2):
    r = random.Random(seed); o = f'<g transform="translate({x},{y}) scale({s})" {OUT} stroke-width="4">'
    for i in range(n):
        px, py, w = r.randint(-120, 120), r.randint(-60, 10) + abs(r.randint(-120, 120)) * -.2, r.randint(18, 34)
        o += f'<path d="M{px - w},{py} l{w * .4:.0f},-{w * .8:.0f} l{w * 1.2:.0f},-{w * .2:.0f} l{w * .7:.0f},{w:.0f}Z" fill="{r.choice(["#e8b830", "#f3cc48", "#d9a820"])}"/>'
    return o + '</g>'


def mine_door(x, y, s=1.0, lit=True):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-220,0 L-190,-380 Q0,-470 190,-380 L220,0Z" fill="#4a3a34"/>'
            f'<path d="M-140,0 L-130,-300 Q0,-360 130,-300 L140,0Z" fill="{"#e8b830" if lit else "#07060a"}"/>'
            '<path d="M-150,0 V-320 M150,0 V-320 M-170,-330 H170" fill="none" stroke="#6a4a2c" stroke-width="22"/></g>')


# ---------------------------------------------------------------- misc helpers for Baba Yaga
def skullpost(x, y, s=1.0, t=0.0, col="#ffd060"):
    fl = 1 + .08 * _m.sin(t * 9 + x)
    return (glow(x, y - 150 * s, 160 * s * fl, col, .45) +
            f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-12" y="-230" width="24" height="230" fill="#8a7a5a"/>'
            f'<path d="M-52,-230 Q-60,-330 0,-336 Q60,-330 52,-230 L30,-196 H-30Z" fill="#e8e2c8"/>'
            f'<ellipse cx="-20" cy="-270" rx="14" ry="18" fill="{col}"/><ellipse cx="20" cy="-270" rx="14" ry="18" fill="{col}"/>'
            f'<path d="M-6,-242 l6,-12 l6,12Z M-24,-212 V-198 M0,-212 V-198 M24,-212 V-198" fill="#0d0f15" stroke-width="4"/></g>')


def bonefence(y, step=130, col="#d9d2b4", x0=-40, x1=1400):
    o = f'<g {OUT} fill="{col}"><path d="M{x0},{y - 120} H{x1} M{x0},{y - 40} H{x1}" fill="none" stroke="#6a5a42" stroke-width="14"/>'
    for i, x in enumerate(range(x0, x1, step)):
        h = 220 + (i * 37) % 70
        o += f'<rect x="{x - 12}" y="{y - h}" width="24" height="{h}" rx="10"/><circle cx="{x}" cy="{y - h - 4}" r="20"/>'
    return o + '</g>'


# ---------------------------------------------------------------- rigs for the 2026-11-18 stories
def kappa(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(0.0, 0.0), skin="#4f8a5a", shell="#6a5a2e", water=1.0, fangs=False):
    """Rigged, animated kappa (Japanese river imp), feet at (x, y), ~380 units tall, faces RIGHT (flip=True faces left).
    mode: stand (breathing, looking around) | walk | bow (bows deeply, head dish spills water) | reach (arm out, grabbing) | face (head only at x,y).
    water: 0..1 amount of water in the head dish."""
    sn = _m.sin
    ph = t * 5.0 if mode == "walk" else 0
    bob = sn(t * 1.8) * 3; lean = 0.0; hr = sn(t * .9) * 3 + look[0] * 4
    la = ra = lk = rk = 0.0
    al, el, ar, er = 10 + sn(t * 1.4) * 4, 12, -10 - sn(t * 1.4) * 4, 12
    bend = 0.0
    if mode == "walk":
        la, ra = sn(ph) * 26, -sn(ph) * 26
        lk, rk = max(0, sn(ph + 1.3)) * 30, max(0, sn(ph + 1.3 + _m.pi)) * 30
        bob = -abs(sn(ph)) * 9; lean = 6; al, ar = -sn(ph) * 22, sn(ph) * 22
    elif mode == "bow":
        bend = 40 + sn(t * 1.2) * 4; hr = 25 + sn(t * 1.0) * 3; al, el = 25, 10; ar, er = -25, 10
    elif mode == "reach":
        ar, er = -88 + sn(t * 3) * 5, -10 + sn(t * 4) * 8; lean = 8; fangs = True
    blink = 0.15 if (t % 3.4) < .13 else 1.0
    f = -1 if flip else 1
    wl = max(0.0, min(1.0, water))

    def arm(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-14,-6 Q-20,40 -12,80 L12,80 Q20,40 14,-6Z" fill="{skin}"/>'
                f'<g transform="translate(0,76) rotate({e:.1f})"><path d="M-12,-2 Q-16,34 -9,66 L9,66 Q16,34 12,-2Z" fill="{skin}"/>'
                f'<path d="M-14,62 l-8,26 l14,-10 l6,12 l6,-12 l14,10 l-8,-26Z" fill="#8ab070" stroke-width="4"/></g></g>')

    def leg(a, k):
        return (f'<g transform="rotate({a:.1f})"><path d="M-20,-4 L20,-4 L16,70 L-16,70Z" fill="{skin}"/>'
                f'<g transform="translate(0,66) rotate({k:.1f})"><path d="M-16,0 L16,0 L13,60 L-13,60Z" fill="{skin}"/>'
                f'<path d="M-18,56 Q-20,74 0,74 Q34,74 40,66 Q36,58 16,56Z" fill="#8ab070" stroke-width="4"/></g></g>')

    def head():
        dish = (f'<ellipse cx="0" cy="-58" rx="30" ry="9" fill="#3a2a1a" stroke-width="4"/>'
                f'<ellipse cx="0" cy="-59" rx="{24 * wl + 2:.0f}" ry="{6 * wl + 1:.0f}" fill="#7fd0f0" stroke="none"/>')
        eyes = "".join(f'<ellipse cx="{ex}" cy="-22" rx="11" ry="{12 * blink:.1f}" fill="#f6f0c0" stroke-width="3"/>'
                       f'<circle cx="{ex + 3 + look[0] * 3:.1f}" cy="{-22 + look[1] * 3:.1f}" r="3.6" fill="#0d0f15" stroke="none"/>' for ex in (-8, 26))
        fg = '<path d="M10,6 l4,12 l5,-12 M24,6 l4,12 l5,-12" fill="#fff" stroke-width="3"/>' if fangs else ''
        return (f'<g transform="rotate({hr:.1f})"><path d="M-40,-30 Q-44,-60 -24,-66 L-16,-52 L-6,-68 L6,-52 L16,-68 L24,-52 L30,-60 Q44,-50 40,-30Z" fill="#2a3a20" stroke-width="4"/>'
                f'<circle cx="0" cy="-20" r="44" fill="{skin}"/>' + dish + eyes +
                f'<path d="M26,-8 Q64,-12 62,4 Q60,16 26,12Z" fill="#e2b84a" stroke-width="4"/><path d="M28,2 H58" stroke-width="3"/>' + fg + '</g>')

    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(0,{bob:.1f})">'
    o += f'<g transform="translate(0,-170)">{leg(la, lk)}</g>'
    if mode == "face":
        return f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>' + head() + '</g>'
    o += f'<g transform="translate(-14,-170)">{leg(ra, rk)}</g>' if False else f'<g transform="translate(26,-170)">{leg(ra, rk)}</g>'
    o += f'<g transform="translate(0,-170) rotate({lean + bend:.1f})">'
    o += f'<g transform="translate(-18,-130)">{arm(al, el)}</g>'
    o += (f'<path d="M-52,-6 Q-74,-80 -40,-150 Q0,-170 40,-150 Q70,-80 50,-6Z" fill="{shell}"/>'
          f'<path d="M-60,-130 Q-100,-90 -60,-20 Q-30,-60 -30,-130Z" fill="{shell}"/>'
          f'<path d="M-48,-110 l22,16 M-52,-70 l24,10 M-40,-40 l22,6" stroke-width="4" fill="none"/>'
          f'<path d="M-30,-8 Q-34,-80 -14,-150 Q18,-162 34,-130 Q40,-70 30,-8Z" fill="#a8c080" stroke-width="4"/>')
    o += f'<g transform="translate(6,-168)">{head()}</g>'
    o += f'<g transform="translate(24,-130)">{arm(ar, er)}</g>'
    if bend:
        o += f'<path d="M20,-190 q{10 + sn(t * 9) * 3:.0f},{40 + 120 * wl:.0f} {6 + sn(t * 7) * 4:.0f},{150 + sn(t * 6) * 8:.0f}" fill="none" stroke="#7fd0f0" stroke-width="10" stroke-linecap="round" opacity=".8"/>' if wl > 0 else ''
    return o + '</g></g></g>'


def ghostman(x, y, s=1.0, t=0.0, mode="stand", flip=False, expr="calm", look=(1, 0), alpha=0.62):
    """The Grey Man: a pale grey, see-through gentleman in a hat and long coat (rigged via human()). mode as in human(); wisps of mist at the feet."""
    body = human(0, 0, 1.0, t, mode, coat="#8f9aa8", pants="#7a8594", skin="#cdd5dd", hair="#6a7380", hat=True, expr=expr, look=look)
    mist = "".join(f'<ellipse cx="{mx + sn_(t * 1.2 + mx) * 16:.0f}" cy="{8 + k * 4}" rx="{120 - k * 20}" ry="{18}" fill="#c8d4e0" opacity=".35" stroke="none"/>' for k, mx in enumerate((-30, 20, 0)))
    f = -1 if flip else 1
    return f'<g transform="translate({x},{y}) scale({f * s},{s})">{mist}<g opacity="{alpha}">{body}</g></g>'


def sn_(v):
    return _m.sin(v)


def torchlit_hall_floor(y=2050):
    return f'<rect x="-20" y="{y}" width="1400" height="500" fill="#4a3a30" {OUT}/><path d="M-20,{y + 120} H1370 M-20,{y + 260} H1370" stroke="#2a1e18" stroke-width="6"/>'


def devilman(x, y, s=1.0, t=0.0, mode="stand", flip=False, expr="grin", look=(1, 0)):
    """Red horned Devil with a swishing tail (rigged via human(); modes as in human())."""
    f = -1 if flip else 1
    sw = _m.sin(t * 3) * 14
    tail = (f'<g transform="translate(-40,-200)" {OUT}><path d="M0,0 Q-70,{20 + sw:.0f} -90,{-50 + sw:.0f} Q-100,{-90 + sw:.0f} -130,{-80 + sw:.0f}" fill="none" stroke-width="14"/>'
            f'<path d="M-130,{-80 + sw:.0f} l-22,-8 l10,24Z" fill="#7a1f1f"/></g>')
    body = human(0, 0, 1.0, t, mode, coat="#7a1f1f", pants="#4a1418", skin="#b83a2a", hair="#2a1014", expr=expr, look=look, horns=True)
    return f'<g transform="translate({x},{y}) scale({f * s},{s})">{tail}{body}</g>'


def bunyip(x, y, s=1.0, t=0.0, mode="swim", flip=False, look=(1, 0), rise=1.0, fur="#3a4638", fur2="#566a4e"):
    """Bunyip: a shaggy swamp beast with a long swaying neck and a dog-like head, faces RIGHT (flip=True: left).
    (x, y) = water line under the body. mode: swim (neck low, swaying) | rise (neck up) | roar (neck up, mouth open, shaking) | peek (only the head above water).
    rise 0..1 scales how far the neck stretches."""
    sn = _m.sin
    f = -1 if flip else 1
    jaw = 0.0
    if mode == "roar":
        jaw = 26 + sn(t * 9) * 8; rise = max(rise, .9)
    elif mode == "swim":
        rise = min(rise, .45)
    elif mode == "peek":
        rise = 0.0
    L = 60 + 90 * rise
    a1 = -6 + sn(t * 1.1) * 7 + (sn(t * 14) * 2 if mode == "roar" else 0)
    a2 = 22 + sn(t * 1.3 + 1) * 9
    a3 = 30 + sn(t * 1.5 + 2) * 8 - (14 if mode == "roar" else 0)
    blink = 0.12 if (t % 3.2) < .12 else 1.0
    lx, ly = look
    head = (f'<g transform="rotate({-a3 + 20:.1f})">'
            f'<path d="M-30,-38 L-52,-84 L-8,-52Z M10,-44 L14,-92 L40,-48Z" fill="{fur}" stroke-width="5"/>'
            f'<path d="M-6,34 Q-52,64 -40,10 Q-70,-20 -30,-44 Q10,-62 52,-34 Q120,-30 128,-2 Q124,14 60,22 Q30,46 -6,34Z" fill="{fur2}" stroke-width="6"/>'
            f'<path d="M-30,-40 q-10,22 -4,40 M-6,-52 q-6,22 0,40 M-48,-4 q-12,16 -8,32" fill="none" stroke="#0d0f15" stroke-width="4"/>'
            f'<g transform="translate(46,16) rotate({jaw:.1f})"><path d="M0,0 Q70,4 84,-6 Q80,18 40,24 Q10,26 0,18Z" fill="{fur}" stroke-width="5"/>'
            + ('<path d="M20,0 l6,-14 l8,14 M50,0 l5,-12 l7,12" fill="#fff" stroke-width="3"/>' if jaw > 4 else '') + '</g>'
            f'<ellipse cx="62" cy="-14" rx="13" ry="{13 * blink:.1f}" fill="#ffe28a" stroke-width="4"/>'
            f'<circle cx="{66 + lx * 3:.1f}" cy="{-14 + ly * 3:.1f}" r="{4 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/>'
            f'<ellipse cx="118" cy="-8" rx="9" ry="6" fill="#0d0f15" stroke="none"/></g>')
    neck = (f'<g transform="rotate({a1:.1f})"><path d="M-38,0 L-26,{-L} L26,{-L} L40,0Z" fill="{fur}" stroke-width="6"/>'
            f'<g transform="translate(0,{-L}) rotate({a2:.1f})"><circle cx="0" cy="0" r="30" fill="{fur}" stroke-width="6"/><path d="M-26,0 L-18,{-L * .8:.0f} L18,{-L * .8:.0f} L26,0Z" fill="{fur}" stroke-width="6"/>'
            f'<g transform="translate(0,{-L * .8:.0f}) rotate({a3 * .4:.1f})">{head}</g></g></g>')
    body = (f'<path d="M-190,10 Q-170,-120 -40,-130 Q80,-140 190,10Z" fill="{fur}" stroke-width="6"/>'
            f'<path d="M-130,-30 q10,-40 30,-60 M-60,-40 q10,-40 30,-70 M20,-40 q10,-40 30,-70 M90,-30 q10,-30 28,-50" fill="none" stroke="{fur2}" stroke-width="10" stroke-linecap="round"/>')
    inner = (neck if mode == "peek" else body + f'<g transform="translate(70,-110)">{neck}</g>')
    rip = "".join(f'<ellipse cx="{k * 90 + sn(t * 1.5 + k) * 12:.0f}" cy="{14 + abs(k) * 2}" rx="{150 - abs(k) * 20}" ry="14" fill="none" stroke="#9ec0d8" stroke-width="5" opacity=".55"/>' for k in (-1, 0, 1))
    return f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(0,{sn(t * 1.2) * 4:.1f})">{inner}</g>{rip}</g>'


# ---------------------------------------------------------------- rigs for the 2026-11-20 stories (kelpie, ghost train, lightning bird)
def kelpie(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(1, 0), coat="#2c3446", mane="#1f7a72", eyec="#8ff0ff", water=None):
    """Kelpie: a wet black water-horse with a weed mane, faces RIGHT (flip=True: left), hooves at (x, y).
    mode: stand (breathing, ear flicks, tail swish) | walk | gallop | rear (up on hind legs, pawing) | peek (only head and neck above the water line at y).
    water: if given (e.g. 1.0) draws ripples around the water line."""
    sn = _m.sin
    f = -1 if flip else 1
    blink = 0.15 if (t % 4.1) < .12 else 1.0
    ph = t * (4.2 if mode == "walk" else 10.5 if mode == "gallop" else 0)
    bob = 0.0; rot = 0.0; amp = 0.0; kn = 0.0; hr = sn(t * 1.1) * 4; open_ = 0.0
    fa = [0.0, 0.0]; fk = [0.0, 0.0]; ha = [0.0, 0.0]; hk = [0.0, 0.0]
    if mode in ("walk", "gallop"):
        amp = 24 if mode == "walk" else 48
        kn = 38 if mode == "walk" else 70
        fa = [sn(ph) * amp, -sn(ph) * amp]; ha = [-sn(ph + .5) * amp, sn(ph + .5) * amp]
        fk = [max(0, sn(ph + 1.4)) * kn, max(0, -sn(ph + 1.4)) * kn]; hk = [max(0, sn(ph + 1.9)) * kn, max(0, -sn(ph + 1.9)) * kn]
        bob = -abs(sn(ph)) * (8 if mode == "walk" else 22); rot = sn(ph) * (1 if mode == "walk" else 3); hr += 6 + sn(ph * 2) * (2 if mode == "walk" else 5)
    elif mode == "rear":
        rot = 38 + sn(t * 3) * 3; fa = [-50 + sn(t * 6) * 18, -70 + sn(t * 6 + 1) * 18]; fk = [90, 70]; hr = -6 + sn(t * 4) * 4; open_ = 14 + sn(t * 8) * 6
    else:
        bob = sn(t * 1.7) * 3
    sw = sn(t * (3 if mode in ("stand", "peek") else 7))
    ear = sn(t * 0.8) * 8 + (sn(t * 17) * 10 if (t % 5) < .4 else 0)

    def leg(hx, hy, a, k, near):
        c = coat if near else "#1c2230"
        return (f'<g transform="translate({hx},{hy}) rotate({a:.1f})"><path d="M-26,-6 L26,-6 L18,124 L-18,124Z" fill="{c}"/>'
                f'<g transform="translate(0,120) rotate({-k:.1f})"><path d="M-18,0 L18,0 L13,112 L-13,112Z" fill="{c}"/>'
                f'<path d="M-17,106 h34 l5,18 h-44Z" fill="#0f1218"/></g></g>')

    seaweed = "".join(
        f'<path d="M{128 + k * 17},{-396 - k * 20} q{20 + sn(t * 2.2 + k) * 14:.0f},{-8 + k} {34 + sn(t * 2.6 + k * 1.3) * 12:.0f},{16 + k * 4} q{-12 + sn(t * 2 + k) * 8:.0f},{14} {-6},{44 + k * 3}" '
        f'fill="none" stroke="{mane}" stroke-width="{12 - k}" stroke-linecap="round"/>' for k in range(6))
    tail = (f'<path d="M-170,-350 Q{-250 + sw * 22:.0f},-330 {-262 + sw * 30:.0f},-190 Q{-250 + sw * 30:.0f},-90 {-214 + sw * 36:.0f},-40 Q{-216 + sw * 20:.0f},-170 -150,-290Z" fill="{mane}"/>'
            f'<path d="M{-240 + sw * 28:.0f},-120 q-6,24 4,46" fill="none" stroke="#9ee6f0" stroke-width="5" opacity=".7"/>')
    eye = (f'<ellipse cx="62" cy="-12" rx="12" ry="{12 * blink:.1f}" fill="{eyec}" stroke-width="4"/>'
           f'<circle cx="{64 + look[0] * 3:.1f}" cy="{-12 + look[1] * 3:.1f}" r="{4.5 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/>')
    head = (f'<g transform="rotate({hr:.1f})"><path d="M-14,-30 L-24,-86 L14,-42Z" fill="{coat}" transform="rotate({ear:.1f} -10 -34)" stroke-width="5"/>'
            f'<path d="M-30,-14 Q-30,-52 14,-56 Q70,-52 120,-4 Q150,20 138,44 Q124,62 96,58 Q40,60 -4,38 Q-30,26 -30,-14Z" fill="{coat}"/>'
            f'<path d="M64,36 L132,40 Q140,50 126,60 Q96,66 62,52Z" fill="#161b27" transform="rotate({open_ * .8:.1f} 60 40)" stroke-width="5"/>'
            f'<path d="M-30,-14 Q-52,6 -44,40 Q-14,30 -4,0Z" fill="{mane}" stroke-width="4"/>' + eye +
            f'<ellipse cx="128" cy="20" rx="7" ry="9" fill="#0d0f15" stroke="none"/>'
            + ('<path d="M92,50 l4,12 l5,-12 M112,50 l4,10 l4,-10" fill="#f4f4ea" stroke-width="3"/>' if open_ > 8 else '') + '</g>')
    neck = (f'<path d="M96,-386 Q150,-470 176,-566 L252,-540 Q238,-440 214,-352Z" fill="{coat}"/>' + seaweed
            + f'<g transform="translate(232,-552)">{head}</g>')
    body = (f'<path d="M-180,-300 Q-196,-396 -70,-392 Q60,-384 160,-402 Q226,-392 214,-300 Q204,-214 110,-204 Q0,-192 -110,-204 Q-190,-214 -180,-300Z" fill="{coat}"/>'
            f'<path d="M-150,-300 q60,-60 120,-10 M60,-330 q40,-20 90,0" fill="none" stroke="#4a5570" stroke-width="6" opacity=".7"/>')
    if mode == "peek":
        out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(-170,330) scale(1)">{neck}</g></g>'
        return out + (_ripples(x, y, s, t) if water else "")
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(0,{bob:.1f}) rotate({-rot:.1f} -120 0)">'
    out += leg(-120, -232, ha[1], hk[1], False) + leg(130, -228, fa[1], fk[1], False) + tail + body + neck
    out += leg(-90, -236, ha[0], hk[0], True) + leg(160, -226, fa[0], fk[0], True)
    return out + '</g></g>' + (_ripples(x, y, s, t) if water else "")


def _ripples(x, y, s, t):
    return "".join(f'<ellipse cx="{x + k * 150 * s + _m.sin(t * 1.5 + k) * 10:.0f}" cy="{y + 8 + abs(k) * 6}" rx="{(240 - abs(k) * 50) * s:.0f}" ry="{20 * s:.0f}" fill="none" stroke="#a8d4e4" stroke-width="5" opacity=".6"/>' for k in (-1, 0, 1))


def steam_engine(x, y, s=1.0, t=0.0, speed=1.0, flip=False, ghost=0.0, flag=True):
    """Old steam locomotive (side view, faces RIGHT, flip=True: left), wheels on the rails at (x, y). Rolling wheels, working rods, smoke puffs.
    ghost 0..1 makes it pale and see-through with a cold glow. flag draws black funeral drapes."""
    sn = _m.sin
    f = -1 if flip else 1
    ph = t * 6.0 * speed
    body_c = "#2a2c38" if not ghost else "#6f7f95"
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT} opacity="{1 - ghost * .35:.2f}">'
    for k in range(7):
        age = (t * .9 + k * .5) % 3.5
        o += f'<circle cx="{190 + age * 110:.0f}" cy="{-470 - age * 120:.0f}" r="{34 + age * 22:.0f}" fill="#c9d2de" opacity="{max(0, .6 - age * .17):.2f}" stroke="none"/>'
    o += (f'<rect x="-330" y="-110" width="640" height="26" fill="#14161c"/>'
          f'<path d="M-330,-96 L-410,-60 L-410,-20 L-330,-40Z" fill="#14161c"/>'
          f'<rect x="-310" y="-380" width="260" height="280" fill="{body_c}"/><path d="M-330,-380 h300 v-30 h-300Z" fill="#14161c"/>'
          f'<rect x="-270" y="-340" width="90" height="100" fill="{"#d8f0ff" if ghost else "#f3c555"}"/>'
          f'<rect x="-50" y="-330" width="360" height="230" rx="30" fill="{body_c}"/><path d="M-50,-330 q180,-40 360,0" fill="none"/>'
          f'<rect x="250" y="-460" width="64" height="150" fill="#14161c"/><path d="M230,-470 h104 l-20,-34 h-64Z" fill="#14161c"/>'
          f'<rect x="60" y="-400" width="80" height="80" rx="40" fill="#8a8f9a"/><path d="M310,-250 L400,-120 L310,-110Z" fill="#14161c"/>'
          f'<circle cx="326" cy="-286" r="26" fill="{"#e8f6ff" if ghost else "#f3e08a"}"/>')
    if ghost:
        o += f'<circle cx="326" cy="-286" r="{90 + sn(t * 3) * 8:.0f}" fill="#bfe8ff" opacity=".25" stroke="none"/>'
    for wx, wr in ((-210, 78), (-60, 78), (90, 78), (240, 78)):
        a = ph * 57.3
        o += (f'<g transform="translate({wx},{-wr + 4})"><circle r="{wr}" fill="#1b1d26"/><circle r="{wr - 16}" fill="#3a3d4a" stroke-width="4"/>'
              f'<g transform="rotate({a:.0f})">' + "".join(f'<path d="M0,0 L{(wr - 12) * _m.cos(i * 1.047):.0f},{(wr - 12) * sn(i * 1.047):.0f}" stroke-width="6"/>' for i in range(6)) + '</g></g>')
    rod = sn(ph) * 34
    o += f'<rect x="{-215 + rod:.0f}" y="-98" width="300" height="18" fill="#8a8f9a"/><circle cx="{-210 + 34 * _m.cos(ph) * 0:.0f}" cy="-74" r="10" fill="#8a8f9a"/>'
    if flag:
        o += ('<path d="M-300,-300 q40,60 90,10 q40,60 90,10" fill="none" stroke="#08090d" stroke-width="22"/>'
              f'<path d="M300,-330 q{10 + sn(t * 3) * 6:.0f},50 40,60 l-20,60Z" fill="#08090d"/>')
    return o + '</g>'


def impundulu(x, y, s=1.0, t=0.0, mode="perch", flip=False, look=(1, 0), spark=0.0, body_c="#1d2230", belly="#e8e8f0"):
    """Impundulu, the lightning bird: a huge black-and-white bird with a crest, faces RIGHT (flip=True: left). (x, y) = feet (perch) or body centre (fly/glide).
    mode: perch (wings folded, head turning, preening) | fly (strong wing beats) | glide (wings spread) | screech (perched, beak wide open, wings half spread).
    spark 0..1 adds crackling lightning around the claws and wing tips."""
    sn = _m.sin
    f = -1 if flip else 1
    blink = 0.15 if (t % 3.3) < .12 else 1.0
    lx, ly = look
    flying = mode in ("fly", "glide")
    if mode == "fly":
        wa = sn(t * 5.5) * 55 - 5; wb = sn(t * 5.5 - 1.0) * 40 + 10; bob = sn(t * 5.5 + 1.2) * 18; tilt = sn(t * 5.5) * 3
    elif mode == "glide":
        wa = -8 + sn(t * 1.3) * 5; wb = 6 + sn(t * 1.6) * 5; bob = sn(t * 1.2) * 8; tilt = -3
    elif mode == "screech":
        wa = 62 + sn(t * 9) * 5; wb = 20; bob = sn(t * 8) * 3; tilt = 0
    else:
        wa = wb = 0; bob = sn(t * 1.5) * 2; tilt = 0
    beak_open = 18 + sn(t * 10) * 6 if mode == "screech" else (4 if mode == "perch" and (t % 6) < .5 else 0)
    hr = sn(t * 0.9) * 6 + (14 if (mode == "perch" and 3 < (t % 8) < 5) else 0)

    def wing(near):
        c = body_c if near else "#141824"
        ang = -wa if near else -wa * .92
        return (f'<g transform="translate({-10 if near else 0},-215) rotate({ang:.1f})"><g transform="scale(-1,-1)">'
                f'<path d="M-40,0 Q-70,150 -30,250 L40,300 L60,230 L100,310 L120,230 L160,290 L150,150 Q130,50 60,0Z" fill="{c}"/>'
                f'<g transform="translate(20,240) rotate({-wb:.1f})"><path d="M-50,0 Q-60,120 -20,200 L30,250 L46,190 L80,260 L96,180 L132,230 L120,90 Q100,20 50,0Z" fill="{"#f1f1f6" if near else "#c9c9d6"}"/></g></g></g>')

    def tailf():
        return (f'<g transform="translate(-170,-170) rotate({18 + sn(t * 1.6) * 4 - (tilt * 2):.1f})"><path d="M0,-20 L-190,-30 L-170,-6 L-200,12 L-168,26 L-186,50 L0,34Z" fill="#141824"/>'
                f'<path d="M-90,-26 L-120,-26 M-90,10 L-130,12" stroke="#f1f1f6" stroke-width="10"/></g>')

    head = (f'<g transform="translate(150,-290) rotate({hr:.1f})"><path d="M-30,-40 Q-44,-96 -80,-124 Q-30,-112 0,-64 Q20,-118 4,-150 Q40,-120 38,-56Z" fill="#a8222a" stroke-width="5"/>'
            f'<path d="M-40,40 Q-52,-20 -10,-50 Q40,-64 70,-30 L92,0 L50,12 Q30,50 -10,52Z" fill="{body_c}"/><path d="M-6,44 Q20,56 46,18 L56,6 Q30,40 -6,44Z" fill="{belly}" stroke-width="4"/>'
            f'<g transform="rotate({-beak_open * .5:.1f} 60 0)"><path d="M54,-20 Q120,-36 156,12 Q116,6 56,4Z" fill="#e8c46a" stroke-width="5"/></g>'
            f'<g transform="rotate({beak_open:.1f} 60 4)"><path d="M54,4 Q110,10 140,34 Q96,36 52,24Z" fill="#d2a850" stroke-width="5"/></g>'
            f'<ellipse cx="32" cy="-12" rx="12" ry="{12 * blink:.1f}" fill="#ffe36a" stroke-width="4"/><circle cx="{34 + lx * 3:.1f}" cy="{-12 + ly * 3:.1f}" r="{4.5 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/></g>')
    neck = f'<path d="M80,-210 Q150,-250 170,-330 L214,-320 Q210,-230 130,-150Z" fill="{body_c}"/>' + head
    body = (f'<path d="M-190,-170 Q-190,-290 -40,-300 Q110,-300 170,-230 Q190,-150 100,-100 Q-20,-70 -140,-110 Q-190,-130 -190,-170Z" fill="{body_c}"/>'
            f'<path d="M20,-150 Q110,-170 150,-210 Q180,-150 100,-104 Q50,-90 10,-110Z" fill="{belly}" stroke-width="4"/>')
    legs = ""
    if not flying:
        legs = (f'<path d="M10,-110 L-8,-24 M-8,-24 l-34,22 M-8,-24 l4,32 M-8,-24 l34,20" fill="none" stroke="#0d0f15" stroke-width="22"/>'
                f'<path d="M10,-110 L-8,-24 M-8,-24 l-34,22 M-8,-24 l4,32 M-8,-24 l34,20" fill="none" stroke="#7a6a5a" stroke-width="10" stroke-linecap="round"/>')
    else:
        legs = '<path d="M20,-104 L50,-30 l-30,20 M50,-30 l26,18" fill="none" stroke="#7a6a5a" stroke-width="12" stroke-linecap="round"/>'
    folded = ('' if (flying or mode == "screech") else
              f'<path d="M-170,-230 Q-40,-300 120,-210 Q40,-130 -120,-150Z" fill="#141824"/><path d="M-100,-210 Q10,-240 80,-196" fill="none" stroke="#f1f1f6" stroke-width="8"/>')
    sp = ""
    if spark > 0:
        r = random.Random(int(t * 12) % 50)
        for k in range(5):
            bx, by = r.choice((-20, 40, 70)) if not flying else r.randint(-200, 200), (-24 if not flying else r.randint(-420, -100))
            pts = f'M{bx},{by} ' + " ".join(f'l{r.randint(-40, 40)},{r.randint(-50, -10)}' for _ in range(4))
            sp += f'<path d="{pts}" fill="none" stroke="#f4fbff" stroke-width="6" stroke-linecap="round"/><path d="{pts}" fill="none" stroke="#8fd0ff" stroke-width="14" opacity=".4"/>'
        sp = f'<g opacity="{spark:.2f}">{sp}</g>'
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(0,{bob:.1f}) rotate({tilt:.1f})">'
    if flying:
        o += wing(False) + legs + tailf() + body + neck + wing(True)
    else:
        o += tailf() + (wing(False) if mode == "screech" else "") + legs + body + folded + (wing(True) if mode == "screech" else "") + neck
    return o + sp + '</g></g>'


# ---------------------------------------------------------------- Krampus rig (horned goat-legged beast, chains, birch switches)
def krampus(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(1, 0), fur="#2b211e", fur2="#4a382f", roar=None):
    """Rigged, animated Krampus (Alpine winter beast), faces RIGHT (flip=True: left), feet at (x, y), ~600 units tall.
    mode: stand (breathing, head turning, swinging chains) | walk (heavy stomping) | roar (arms up, mouth wide) | reach (arm stretched forward).
    roar: mouth opening 0-1 (None = automatic)."""
    sn = _m.sin
    f = -1 if flip else 1
    ph = t * 4.2 if mode == "walk" else 0
    bob = sn(t * 1.6) * 3; lean = 6; la = ra = 0.0; lk = rk = 0.0
    a1, e1, a2, e2 = 10 + sn(t * 1.5) * 4, -20, -8 - sn(t * 1.5) * 4, -26   # near arm (chains), far arm (switches)
    hr = sn(t * .8) * 5 + look[0] * 4
    mo = 0.12 + 0.08 * sn(t * 2.1)
    if mode == "walk":
        la, ra = sn(ph) * 22, -sn(ph) * 22
        lk, rk = max(0, sn(ph + 1.2)) * 26, max(0, sn(ph + 1.2 + _m.pi)) * 26
        bob = -abs(sn(ph)) * 14; lean = 12
        a1, a2 = -sn(ph) * 24 + 10, sn(ph) * 24 - 8
    elif mode == "roar":
        bob = sn(t * 9) * 3; lean = -8; a1, e1, a2, e2 = -140 + sn(t * 8) * 6, -20, 140 - sn(t * 8) * 6, 20; hr = -8 + sn(t * 9) * 3; mo = 0.9
    elif mode == "reach":
        a1, e1 = -85 + sn(t * 3) * 4, -10; lean = 14; hr = 6
    if roar is not None:
        mo = roar
    blink = 0.15 if (t % 3.4) < .12 else 1.0
    chain_sw = sn(t * 2.3) * 8

    def leg(a, k):
        return (f'<g transform="rotate({-20 + a:.1f})"><path d="M-30,-8 Q-48,70 -26,136 L28,136 Q46,60 30,-8Z" fill="{fur}"/>'
                f'<path d="M-34,40 l10,10 l-8,10 M30,40 l-10,10 l8,10" fill="none" stroke="{fur2}" stroke-width="5"/>'
                f'<g transform="translate(0,132) rotate({58 + k:.1f})"><path d="M-20,-6 L-26,112 L20,112 L24,-6Z" fill="{fur}"/>'
                f'<g transform="translate(0,108) rotate({-38 - a * .5:.1f})"><path d="M-22,0 L-28,38 L-34,70 L26,70 L22,0Z" fill="#17110f"/></g></g></g>')

    def arm(a, e, kind):
        g = (f'<g transform="rotate({a:.1f})"><path d="M-26,-12 Q-40,60 -24,130 L24,130 Q40,60 26,-12Z" fill="{fur}"/>'
             f'<path d="M-28,30 l12,10 l-12,10 M-26,80 l12,10 l-12,10" fill="none" stroke="{fur2}" stroke-width="5"/>'
             f'<g transform="translate(0,126) rotate({e:.1f})"><path d="M-22,-6 Q-30,60 -16,128 L20,128 Q32,60 22,-6Z" fill="{fur}"/>'
             f'<circle cx="0" cy="132" r="22" fill="{fur}"/><path d="M-18,146 l-6,26 M0,152 l0,28 M18,146 l6,26" stroke="#e8dcc4" stroke-width="7" stroke-linecap="round" fill="none"/>'
             f'<rect x="-27" y="96" width="54" height="14" rx="5" fill="#6a6a74"/>')
        if kind == "chain":
            g += (f'<g transform="translate(0,136) rotate({chain_sw - a * .4:.1f})"><path d="M0,0 q-6,40 4,80 q10,40 -6,90 q-10,30 4,60" fill="none" stroke="#0d0f15" stroke-width="16"/>'
                  f'<path d="M0,0 q-6,40 4,80 q10,40 -6,90 q-10,30 4,60" fill="none" stroke="#9aa0ae" stroke-width="7" stroke-dasharray="14 7"/>'
                  f'<circle cx="4" cy="230" r="16" fill="#d9b24a"/></g>')
        elif kind == "switch":
            g += ('<g transform="translate(0,140) rotate(-18)">' + "".join(
                f'<path d="M0,0 L{-24 + i * 12},-190 " stroke="#7a5a34" stroke-width="5" fill="none"/>' for i in range(5))
                + '<rect x="-16" y="-14" width="32" height="26" rx="6" fill="#b89a5a"/></g>')
        return g + '</g></g>'

    eyec = "#ffcf3a"
    head = (f'<g transform="rotate({hr:.1f})">'
            f'<path d="M-30,-70 Q-60,-150 -20,-200 Q-26,-130 0,-96Z M16,-80 Q10,-190 70,-226 Q40,-150 56,-96Z" fill="#d8cdb0" stroke-width="5"/>'   # horns
            f'<path d="M-40,-30 q-40,-10 -62,-44 q40,-2 70,24Z" fill="{fur}"/>'                                                              # ear
            f'<circle cx="0" cy="-30" r="60" fill="{fur}"/>'
            f'<path d="M20,-60 Q96,-70 120,-20 Q130,30 112,{40 + 36 * mo:.0f} L20,{40 + 36 * mo:.0f}Z" fill="{fur}"/>'
            f'<path d="M20,{22 + 6 * mo:.0f} L116,{20 + 6 * mo:.0f} L108,{34 + 56 * mo:.0f} Q60,{52 + 56 * mo:.0f} 18,{46 + 56 * mo:.0f}Z" fill="#2a0f12" stroke-width="4"/>'
            f'<path d="M70,{36 + 20 * mo:.0f} q16,{50 + 40 * mo:.0f} -6,{80 + 40 * mo:.0f} q-22,-14 -30,-{60 - 30 * mo:.0f}Z" fill="#c4323c" stroke-width="4"/>'
            + "".join(f'<path d="M{34 + i * 17},{20 + 6 * mo:.0f} l7,16 l7,-16Z" fill="#f4efe2" stroke-width="2"/>' for i in range(5))
            + f'<ellipse cx="38" cy="-44" rx="13" ry="{11 * blink:.1f}" fill="{eyec}" stroke-width="4"/>'
              f'<circle cx="{40 + look[0] * 3:.1f}" cy="{-44 + look[1] * 3:.1f}" r="{4.5 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/>'
              f'<path d="M20,-62 l36,12" stroke-width="6" fill="none"/>'
              f'<circle cx="112" cy="-12" r="5" fill="#0d0f15" stroke="none"/></g>')
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(0,{bob:.1f})">'
    o += f'<g transform="translate(-10,-262)">{leg(ra, rk)}</g>'
    o += f'<g transform="translate(-40,-290) rotate({-10 + sn(t * 2.4) * 8:.1f})"><path d="M0,0 Q-70,10 -110,-50 Q-80,-4 0,-26Z" fill="{fur}"/></g>'   # tail
    o += f'<g transform="translate(-6,-280) rotate({lean:.1f})">'
    o += f'<g transform="translate(40,-210)">{arm(a2, e2, "switch")}</g>'
    o += (f'<path d="M-62,0 Q-100,-120 -40,-232 Q40,-290 116,-200 Q132,-100 66,0Z" fill="{fur}"/>'
          f'<path d="M-20,-30 Q30,-60 80,-30 Q96,-130 40,-200 Q-30,-160 -20,-30Z" fill="{fur2}" stroke="none"/>'
          f'<path d="M-94,-90 l-26,-12 l22,-14 l-20,-18 l28,-6 M-70,-180 l-22,-16 l28,-4" fill="none" stroke="{fur2}" stroke-width="6"/>'
          f'<rect x="-52" y="-24" width="116" height="16" rx="6" fill="#6a5438"/>')
    o += f'<g transform="translate(96,-236)">{head}</g>'
    o += f'<g transform="translate(60,-216)">{arm(a1, e1, "chain")}</g></g>'
    o += f'<g transform="translate(26,-262)">{leg(la, lk)}</g>'
    return o + '</g></g>'


# ---------------------------------------------------------------- knocker rig (small mine goblin with candle hat and pick)
def knocker(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(1, 0), skin="#7e9a6a", coat="#5a4630", hat="#3a2c22", glowc="#ffd36a"):
    """Rigged, animated Tommyknocker (mine spirit), ~250 units tall, faces RIGHT (flip=True: left), feet at (x, y).
    mode: stand (breathing, looking about) | knock (swings the pick at the wall in front of it) | walk | wave | peek (hides behind its own feet line: only head and hat, sinks and rises)."""
    sn = _m.sin
    f = -1 if flip else 1
    ph = t * 6 if mode == "walk" else 0
    bob = sn(t * 2.0) * 2; la = ra = 0.0; lk = rk = 0.0
    a1, e1, a2, e2 = 8, -12, -8, -12; hr = sn(t * 1.1) * 4 + look[0] * 5
    if mode == "walk":
        la, ra = sn(ph) * 28, -sn(ph) * 28; lk, rk = max(0, sn(ph + 1.3)) * 30, max(0, sn(ph + 4.4)) * 30
        bob = -abs(sn(ph)) * 7; a1, a2 = -sn(ph) * 26, sn(ph) * 26
    elif mode == "knock":
        sw = sn(t * 7.0)
        a1, e1 = -110 + sw * 38, -20 + sw * 40; bob = -abs(sw) * 3; hr = 6
    elif mode == "wave":
        a1, e1 = -150 + sn(t * 7) * 14, 18 + sn(t * 7) * 20
    blink = 0.15 if (t % 3.1) < .12 else 1.0
    dy = 0.0
    if mode == "peek":
        dy = 70 + sn(t * 1.3) * 22 - 40

    def leg(a, k):
        return (f'<g transform="rotate({a:.1f})"><path d="M-12,0 L-14,40 L12,40 L12,0Z" fill="{coat}"/><g transform="translate(0,38) rotate({k:.1f})">'
                f'<path d="M-12,0 L-13,34 L11,34 L12,0Z" fill="{coat}"/><path d="M-14,30 Q-14,48 0,48 Q26,48 28,38 Q22,30 12,30Z" fill="#241a14"/></g></g>')

    def arm(a, e, pick):
        g = (f'<g transform="rotate({a:.1f})"><path d="M-10,0 L-12,46 L12,46 L10,0Z" fill="{coat}"/><g transform="translate(0,44) rotate({e:.1f})">'
             f'<path d="M-9,0 L-11,40 L11,40 L9,0Z" fill="{skin}"/><circle cx="0" cy="44" r="12" fill="{skin}"/>')
        if pick:
            g += ('<g transform="translate(0,44) rotate(-12)"><rect x="-5" y="-20" width="10" height="120" rx="4" fill="#6a4a2a"/>'
                  '<path d="M-60,-24 Q0,-52 62,-24 L56,-12 Q0,-36 -54,-12Z" fill="#8a909c"/></g>')
        return g + '</g></g>'

    head = (f'<g transform="rotate({hr:.1f})"><path d="M-30,-14 l-28,-14 l8,22 l24,6Z M30,-14 l28,-14 l-8,22 l-24,6Z" fill="{skin}"/>'
            f'<ellipse cx="0" cy="-20" rx="36" ry="34" fill="{skin}"/>'
            f'<path d="M-30,0 Q-26,52 0,58 Q26,52 30,0 Q0,22 -30,0Z" fill="#cfc8b4"/>'
            f'<path d="M4,-18 Q34,-12 36,12 Q20,18 8,6Z" fill="{skin}"/>'
            f'<ellipse cx="-12" cy="-28" rx="8" ry="{8 * blink:.1f}" fill="#fff" stroke-width="3"/><ellipse cx="14" cy="-28" rx="8" ry="{8 * blink:.1f}" fill="#fff" stroke-width="3"/>'
            f'<circle cx="{-12 + look[0] * 3:.1f}" cy="{-28 + look[1] * 2:.1f}" r="{3 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/>'
            f'<circle cx="{14 + look[0] * 3:.1f}" cy="{-28 + look[1] * 2:.1f}" r="{3 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/>'
            f'<path d="M-6,22 q8,8 16,0" fill="none" stroke-width="3.5"/>'
            f'<path d="M-40,-44 Q0,-92 40,-44Z" fill="{hat}"/><rect x="-46" y="-50" width="92" height="12" rx="5" fill="{hat}"/>'
            f'<rect x="-8" y="-80" width="16" height="22" fill="#e8dcc4" stroke-width="3"/>'
            f'<path d="M0,-84 q-9,-12 0,-26 q9,14 0,26Z" fill="{glowc}" stroke-width="3"/></g>')
    gl = glow(0, -110, 140, glowc, 0.35)
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(0,{bob + dy:.1f})">'
    o += f'<g transform="translate(-12,-88)">{leg(ra, rk)}</g><g transform="translate(-30,-130)">{arm(a2, e2, False)}</g>'
    o += f'<path d="M-32,-84 Q-36,-150 -22,-178 Q0,-190 24,-176 Q40,-150 34,-84Z" fill="{coat}"/><path d="M-30,-110 H32" stroke="#241a14" stroke-width="8"/>'
    o += f'<g transform="translate(8,-88)">{leg(la, lk)}</g><g transform="translate(0,-186)">{head}</g><g transform="translate(24,-136)">{arm(a1, e1, mode == "knock")}</g>'
    return o + '</g></g>' + f'<g transform="translate({x},{y - 190 * s + dy * s}) scale({s})">{gl}</g>'


# ---------------------------------------------------------------- heavy coffin (prop that can rattle, tilt and slide)
def coffin(x, y, s=1.0, t=0.0, mode="still", angle=0.0, flip=False, lead="#59606e", trim="#c9a24a"):
    """Old lead-lined coffin, ~150 wide x 480 long when upright-lying; base-centre at (x, y), drawn lying along the x axis (length ~520, height ~150).
    mode: still | shake (rattling) | rock (slow heavy rocking) ; angle = extra tilt in degrees."""
    sn = _m.sin
    f = -1 if flip else 1
    sh = sn(t * 31) * 2.5 if mode == "shake" else 0
    rk = sn(t * 1.7) * 6 if mode == "rock" else 0
    jx = sn(t * 47) * 5 if mode == "shake" else 0
    o = f'<g transform="translate({x + jx:.1f},{y}) scale({f * s},{s}) rotate({angle + sh + rk:.1f})" {OUT}>'
    o += (f'<path d="M-260,-120 L-200,-150 L200,-150 L260,-120 L230,0 L-230,0Z" fill="{lead}"/>'
          f'<path d="M-200,-150 L-170,-110 L170,-110 L200,-150" fill="#6e7684" stroke-width="4"/>'
          f'<path d="M-230,0 L-250,-90 M230,0 L250,-90" stroke-width="3" fill="none" opacity=".5"/>'
          f'<path d="M-30,-60 h60 M0,-90 v60" stroke="{trim}" stroke-width="12" stroke-linecap="round"/>'
          + "".join(f'<circle cx="{cx}" cy="-70" r="10" fill="{trim}" stroke-width="3"/>' for cx in (-170, -100, 100, 170)))
    return o + '</g>'


# ---------------------------------------------------------------- rigs for the 2026-11-22 stories (ghost bride, tikbalang, death worm)
def bride(x, y, s=1.0, t=0.0, mode="stand", flip=False, expr="calm", look=(1, 0), alpha=0.8, headturn=0.0):
    """Pale ghost bride in a long white gown (rigged via human(); modes as in human()), floats and trails mist.
    headturn 0..1 twists the head sideways (uncanny)."""
    sn = _m.sin
    fl = sn(t * 1.3) * 10
    body = human(0, 0, 1.0, t, "stand" if mode == "glide" else mode, coat="#e6ecf4", pants="#e6ecf4", skin="#d6dee8", hair="#1c1a24", expr=expr, look=look, longhair=True)
    sway = sn(t * 1.6) * 8
    skirt = (f'<path d="M-62,-190 Q-120,-60 {-150 + sway:.0f},0 Q{-60 + sway:.0f},26 0,10 Q{60 + sway:.0f},26 {150 + sway:.0f},0 Q120,-60 62,-190Z" fill="#e6ecf4" {OUT}/>'
             f'<path d="M-40,-150 Q{-50 + sway:.0f},-60 {-70 + sway:.0f},0 M40,-150 Q{50 + sway:.0f},-60 {70 + sway:.0f},0 M0,-160 V10" fill="none" stroke="#9aa6b8" stroke-width="4"/>')
    veil = f'<path d="M-46,-430 Q{-110 - sway:.0f},-330 {-120 - sway * 2:.0f},-190 Q-60,-260 -30,-330Z" fill="#cfd8e6" opacity=".6" stroke-width="3" {OUT}/>'
    mist = "".join(f'<ellipse cx="{mx + sn(t * 1.2 + mx) * 16:.0f}" cy="{12 + k * 6}" rx="{150 - k * 25}" ry="20" fill="#c8d4e0" opacity=".4" stroke="none"/>' for k, mx in enumerate((-30, 20, 0)))
    f = -1 if flip else 1
    tw = f'<g transform="translate(0,-402) rotate({headturn * 70:.0f}) translate(0,402)">' if headturn else '<g>'
    return (f'<g transform="translate({x},{y - 30 - fl:.1f}) scale({f * s},{s})"><g transform="translate(0,{fl + 30:.1f})">{mist}</g><g opacity="{alpha}">'
            f'{body}{skirt}{veil}</g></g>')


def tikbalang(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(1, 0), fur="#5a4634", mane="#1c1410", eyec="#ffcf5a", neigh=0.0):
    """Tikbalang: very tall, thin dark creature with a horse head and long limbs (rigged via human(), stretched).
    mode as in human() (stand / walk / scared / point / reach). neigh 0..1 opens the mouth and tosses the head."""
    sn = _m.sin
    f = -1 if flip else 1
    ST = 1.3
    body = human(0, 0, 1.0, t, mode, coat=fur, pants="#241c15", skin=fur, hair=mane, look=look)
    bob = -abs(sn(t * 5)) * 10 if mode == "walk" else -abs(sn(t * 9)) * 18 if mode == "run" else sn(t * 1.8) * 3
    lean = 4 if mode == "walk" else 12 if mode == "run" else 0
    hy = -402 * ST + bob * ST
    sway = sn(t * 1.1) * 6 + neigh * (sn(t * 9) * 8 - 10)
    blink = 0.12 if (t % 3.5) < .12 else 1.0
    lx, ly = look
    jaw = neigh * 22 + (3 if mode == "stand" else 0) * (sn(t * 2) + 1)
    head = (f'<g transform="translate({lean * 3:.0f},{hy:.1f}) rotate({sway:.1f})">'
            f'<path d="M-60,-50 Q-96,-70 -88,-150 Q-60,-110 -40,-92Z M60,-50 Q96,-70 88,-150 Q60,-110 40,-92Z" fill="{fur}"/>'
            f'<path d="M-30,-150 Q-70,-100 -62,-20 Q-40,40 -20,52 Q-10,100 0,106 Q10,100 20,52 Q40,40 62,-20 Q70,-100 30,-150 Q0,-170 -30,-150Z" fill="{fur}"/>'
            f'<path d="M-20,-152 Q-70,-190 -30,-230 Q-20,-190 0,-176 Q20,-190 30,-230 Q70,-190 20,-152Z M0,-176 Q-6,-100 -4,-20" fill="{mane}"/>'
            f'<path d="M-30,52 Q-24,90 -14,96 Q0,106 14,96 Q24,90 30,52Z" fill="#4a3a2c" stroke-width="5"/>'
            f'<ellipse cx="-9" cy="76" rx="5" ry="8" fill="#0d0f15" stroke="none"/><ellipse cx="9" cy="76" rx="5" ry="8" fill="#0d0f15" stroke="none"/>'
            f'<g transform="translate(0,{jaw:.1f})"><path d="M-22,96 Q0,{120 + jaw:.0f} 22,96 Q0,100 -22,96Z" fill="#2a1014" stroke-width="4"/></g>'
            + "".join(f'<ellipse cx="{ex}" cy="-34" rx="17" ry="{17 * blink:.1f}" fill="{eyec}" stroke-width="4"/><circle cx="{ex + lx * 5:.1f}" cy="{-34 + ly * 3:.1f}" r="{6 * (1 if blink > .5 else .1):.1f}" fill="#0d0f15" stroke="none"/>' for ex in (-30, 30))
            + '</g>')
    # human head is hidden by painting over it with a neck + the horse head
    neck = f'<path d="M-30,{-340 * ST:.0f} L-26,{hy:.0f} L26,{hy:.0f} L30,{-340 * ST:.0f}Z" fill="{fur}"/>'
    return (f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="scale(1,{ST})">{body}</g>{neck}{head}</g>')


def deathworm(x, y, s=1.0, t=0.0, mode="rise", flip=False, look=(1, 0), rise=1.0, col="#b23a22", col2="#d8663a", spit=0.0, zap=0.0, n=15):
    """Mongolian death worm: a blood-red segmented worm without eyes, coming out of a sand mound at (x, y).
    mode: lurk (only a small hump with ripples) | rise (swaying upright, mouth gaping) | lunge (head bent forward, mouth wide) | spit (head back, spraying yellow venom).
    rise 0..1 = how much of the body is out. spit/zap 0..1 draw yellow venom droplets / a blue-white shock bolt towards the facing side."""
    sn = _m.sin
    f = -1 if flip else 1
    if mode == "lurk":
        rise = min(rise, .22)
    seg = 36
    segs = []
    px, py = 0.0, 0.0
    N = max(2, int(n * rise + 1))
    bend = {"rise": 0.0, "lunge": 1.0, "spit": -.6, "lurk": 0.0}[mode]
    ang = -90.0
    for i in range(N):
        k = i / max(1, N - 1)
        ang += sn(t * 2.2 + i * .55) * (7 + 10 * k) + bend * (10 * k if k > .45 else 0)
        px += _m.cos(_m.radians(ang)) * seg
        py += _m.sin(_m.radians(ang)) * seg
        segs.append((px, py, ang))
    o = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>'
    o += '<ellipse cx="0" cy="6" rx="210" ry="38" fill="#c4a15e"/><ellipse cx="0" cy="-4" rx="150" ry="26" fill="#d8b872" stroke-width="5"/>'
    for i in range(N - 1, -1, -1):
        sx, sy, a = segs[i]
        r = 54 - 20 * (i / max(1, N)) + (4 if i == N - 1 else 0)
        o += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" fill="{col if i % 2 == 0 else col2}"/>'
    if mode != "lurk":
        hx, hy, ha = segs[-1]
        gape = 26 + sn(t * 8) * 6 + (18 if mode in ("lunge", "spit") else 0)
        o += (f'<g transform="translate({hx:.1f},{hy:.1f}) rotate({ha + 90:.1f})"><path d="M-62,6 Q-66,-66 0,-72 Q66,-66 62,6Z" fill="{col}"/>'
              f'<ellipse cx="0" cy="-14" rx="{40 + gape * .25:.0f}" ry="{gape + 10:.0f}" fill="#2a0a10" stroke-width="5"/>'
              + "".join(f'<path d="M{-34 + j * 17},{-14 - (gape + 6)} l7,16 l7,-16Z" fill="#f4eed8" stroke-width="3"/>' for j in range(5))
              + "".join(f'<path d="M{-34 + j * 17},{-14 + (gape + 6)} l7,-16 l7,16Z" fill="#f4eed8" stroke-width="3"/>' for j in range(5))
              + '<ellipse cx="0" cy="-14" rx="18" ry="12" fill="#6a1a22" stroke="none"/></g>')
        if spit > 0:
            for j in range(10):
                u = ((t * 1.7 + j * .13) % 1.0)
                dx = hx + 80 + u * 520 * spit
                dy = hy - 40 + (-1 + 2 * u) * 120 * u + u * u * 260 + (j % 3) * 14
                o += f'<circle cx="{dx:.0f}" cy="{dy:.0f}" r="{16 - 10 * u:.0f}" fill="#e8d84a" stroke-width="3"/>'
        if zap > 0:
            pts = " ".join(f"{hx + 60 + k * 70:.0f},{hy - 20 + (28 if k % 2 else -28) * sn(t * 30 + k):.0f}" for k in range(8))
            o += f'<polyline points="{pts}" fill="none" stroke="#bfe8ff" stroke-width="10"/><polyline points="{pts}" fill="none" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>'
    grains = "".join(f'<circle cx="{(j - 3) * 55 + sn(t * 3 + j) * 10:.0f}" cy="{-10 - ((t * 60 + j * 20) % 70):.0f}" r="5" fill="#d8b872" stroke="none" opacity=".8"/>' for j in range(7))
    return o + grains + '</g>'


def dunes(y=1700, col="#6a5238", seed=3, hi=170, step=420, x0=-60, x1=1420):
    r = random.Random(seed)
    pts = f"M{x0},2400 L{x0},{y} "
    x = x0
    while x < x1:
        pts += f"Q{x + step / 2:.0f},{y - r.randint(hi // 2, hi):.0f} {x + step:.0f},{y + r.randint(-30, 30)} "
        x += step
    return f'<path d="{pts}L{x1 + step},2400Z" fill="{col}" {OUT}/>'


def tent(x, y, s=1.0, col="#7a6a50", lit=True):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-260,0 L0,-300 L260,0Z" fill="{col}"/>'
            f'<path d="M-70,0 L0,-170 L70,0Z" fill="{"#f3c555" if lit else "#17141a"}"/><path d="M0,-300 V-340" stroke-width="8"/></g>')


def campfire(x, y, s=1.0, t=0.0):
    fl = "".join(f'<path d="M{dx},0 Q{dx - 26},{-60 - h + _m.sin(t * 9 + dx) * 12:.0f} {dx},{-120 - h + _m.sin(t * 11 + dx) * 14:.0f} Q{dx + 26},{-60 - h} {dx},0Z" fill="{c}" stroke-width="4"/>' for dx, h, c in ((-24, 0, "#d8561f"), (22, 20, "#e88a2a"), (0, 40, "#f3c555")))
    return f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-70,10 L70,-10 M-70,-10 L70,10" stroke="#4a3322" stroke-width="22" stroke-linecap="round"/>{fl}</g>'


def bed(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-300" y="-140" width="600" height="110" rx="16" fill="#8a3a3a"/>'
            f'<rect x="-300" y="-30" width="600" height="30" fill="#3a2a22"/><rect x="-300" y="-260" width="70" height="260" fill="#3a2a22"/><rect x="-250" y="-200" width="130" height="60" rx="22" fill="#d8d2c0"/></g>')


def farmhouse(x, y, s=1.0, lit="#f3c555", wall="#8a7a66", roof="#3a2c28", snow_=True):
    d = (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-260" y="-300" width="520" height="300" fill="{wall}"/>'
         f'<path d="M-300,-290 L0,-470 L300,-290Z" fill="{roof}"/>'
         f'<rect x="-190" y="-220" width="90" height="100" fill="{lit}"/><rect x="100" y="-220" width="90" height="100" fill="{lit}"/>'
         f'<rect x="-40" y="-170" width="80" height="170" fill="#3a2a22"/><rect x="150" y="-460" width="50" height="110" fill="#5a4a46"/>')
    if snow_:
        d += '<path d="M-300,-290 L0,-470 L300,-290 L260,-286 L0,-436 L-260,-286Z" fill="#e8eef6" stroke-width="4"/>'
    return d + '</g>'


def bench_court(y=1500):
    return (f'<rect x="-20" y="{y}" width="1400" height="900" fill="#5a3f2c" {OUT}/><rect x="300" y="{y - 300}" width="750" height="320" fill="#6b4a32" {OUT}/>'
            f'<rect x="270" y="{y - 330}" width="810" height="50" fill="#4a3322" {OUT}/><rect x="-20" y="{y - 700}" width="1400" height="700" fill="#2a2430"/>'
            f'<path d="M0,{y} H1350" stroke="#0d0f15" stroke-width="8"/>')


# ---------------------------------------------------------------- 2026-11-23 rigs: Wampus Cat, steamer (Baychimo), banshee
def _cathead(t, fur, fur2, eyec, look, scream, blink, rot=0.0):
    """Front-view cat face centred at (0,0), ~120 wide. scream 0..1 opens the mouth."""
    lx, ly = look
    eyes = "".join(
        f'<path d="M{ex - 17},-6 Q{ex},{-24 * blink - 4:.1f} {ex + 17},-6 Q{ex},{12 * blink - 2:.1f} {ex - 17},-6Z" fill="{eyec}" stroke-width="4"/>'
        f'<rect x="{ex + lx * 4 - 2.5:.1f}" y="{-6 - 11 * blink + ly * 2:.1f}" width="5" height="{22 * blink:.1f}" rx="2" fill="#0d0f15" stroke="none"/>' for ex in (-26, 26))
    mouth = (f'<path d="M-22,28 Q0,{34 + scream * 40:.0f} 22,28 Q0,{26 + scream * 14:.0f} -22,28Z" fill="#2a1014" stroke-width="4"/>'
             + (f'<path d="M-14,30 l4,{10 + scream * 8:.0f} l5,-9 M14,30 l-4,{10 + scream * 8:.0f} l-5,-9" fill="#f4f4ea" stroke-width="3"/>' if scream > .2 else ''))
    return (f'<g transform="rotate({rot:.1f})"><path d="M-54,-30 L-72,-104 L-16,-58Z M54,-30 L72,-104 L16,-58Z" fill="{fur}"/>'
            f'<path d="M-48,-40 L-60,-86 L-28,-58Z M48,-40 L60,-86 L28,-58Z" fill="#c07a74" stroke="none"/>'
            f'<path d="M-64,0 Q-70,40 -40,56 Q0,70 40,56 Q70,40 64,0 Q60,-54 0,-58 Q-60,-54 -64,0Z" fill="{fur}"/>'
            f'<path d="M-14,-56 v22 M0,-58 v26 M14,-56 v22 M-60,-6 l22,6 M60,-6 l-22,6" stroke="{fur2}" stroke-width="7" fill="none"/>'
            + eyes + '<path d="M-8,14 L8,14 L0,24Z" fill="#c07a74" stroke-width="3"/>' + mouth +
            '<path d="M-34,24 l-58,-8 M-34,30 l-58,6 M34,24 l58,-8 M34,30 l58,6" stroke="#e6e0d0" stroke-width="3" fill="none"/></g>')


def wampus(x, y, s=1.0, t=0.0, mode="prowl", flip=False, look=(1, 0), fur="#8a6a3a", fur2="#5a4226", eyec="#ffe04a", scream=0.0):
    """Wampus Cat: half woman, half cougar with glowing yellow eyes. Feet at (x, y).
    mode: prowl (four-legged walk, faces RIGHT) | crouch (low, tail twitching) | run |
          upright (stands on hind legs like a woman, tall; claws out, sways) | upwalk (walks upright) | rear (upright, arms spread, screaming)
    scream 0..1 opens the mouth."""
    sn = _m.sin
    f = -1 if flip else 1
    blink = 0.15 if (t % 4.3) < .12 else 1.0
    if mode in ("upright", "upwalk", "rear"):
        hm = {"upright": "stand", "upwalk": "walk", "rear": "scared"}[mode]
        body = human(0, 0, 1.0, t, hm, coat=fur, pants=fur2, skin=fur, hair=fur2, look=look)
        sw = sn(t * 2.2) * 26
        tail = (f'<path d="M-10,-180 Q-140,-170 {-190 + sw:.0f},-250 Q{-230 + sw:.0f},-330 {-190 + sw * 1.4:.0f},-380 Q{-160 + sw:.0f},-310 {-120 + sw * .6:.0f},-250 Q-70,-200 10,-150Z" fill="{fur}" {OUT}/>'
                f'<path d="M{-196 + sw:.0f},-290 q22,-8 30,6 M{-200 + sw:.0f},-340 q20,-8 28,6" stroke="{fur2}" stroke-width="9" fill="none"/>')
        bob = (-abs(sn(t * 5)) * 10 if hm == "walk" else sn(t * 1.8) * 3)
        claws = "".join(f'<path d="M{cx},{cy} l{dx},30" stroke="#f4f4ea" stroke-width="5" stroke-linecap="round" fill="none"/>' for cx, cy, dx in ((0, 0, 0),))
        head = f'<g transform="translate(0,{-410 + bob:.1f}) scale(1.05)">{_cathead(t, fur, fur2, eyec, look, scream, blink, sn(t * 1.1) * 4)}</g>'
        dress = (f'<path d="M-60,-186 Q-96,-80 -112,-8 L112,-8 Q96,-80 60,-186Z" fill="#6a5a46" {OUT}/>'
                 f'<path d="M-90,-40 q10,10 20,0 M-30,-20 q10,10 20,0 M40,-30 q10,10 20,0" stroke="#0d0f15" stroke-width="4" fill="none"/>')
        neck = f'<rect x="-22" y="-430" width="44" height="60" fill="{fur}" stroke="none"/>'
        return (f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>{tail}{body}{dress}{neck}{head}</g>')
    # quadruped, faces right
    ph = t * (5.0 if mode == "prowl" else 11.0 if mode == "run" else 0)
    low = 70 if mode == "crouch" else 0
    amp = 26 if mode == "prowl" else 52 if mode == "run" else 0
    kn = 30 if mode == "prowl" else 60 if mode == "run" else 0
    bob = -abs(sn(ph)) * (6 if mode == "prowl" else 22) if amp else sn(t * 1.6) * 3
    wig = sn(t * 3.4) * 20 if mode == "crouch" else sn(t * 2.1) * 14
    def leg(hx, hy, a, k, near):
        c = fur if near else fur2
        return (f'<g transform="translate({hx},{hy}) rotate({a:.1f})"><path d="M-26,-6 L26,-6 L16,92 L-14,92Z" fill="{c}"/>'
                f'<g transform="translate(0,88) rotate({-k:.1f})"><path d="M-14,0 L16,0 L11,{86 - low * .5:.0f} L-11,{86 - low * .5:.0f}Z" fill="{c}"/>'
                f'<ellipse cx="6" cy="{88 - low * .5:.0f}" rx="26" ry="12" fill="{c}"/><path d="M20,{90 - low * .5:.0f} l8,6 M14,{94 - low * .5:.0f} l7,6" stroke="#f4f4ea" stroke-width="3" fill="none"/></g></g>')
    hy = -214 + low
    legs_far = leg(-120, hy, sn(ph + .6) * amp, max(0, sn(ph + 2)) * kn, False) + leg(120, hy, -sn(ph + .6) * amp, max(0, sn(ph + 3.5)) * kn, False)
    legs_near = leg(-100, hy, -sn(ph) * amp, max(0, sn(ph + 1.4)) * kn, True) + leg(140, hy, sn(ph) * amp, max(0, sn(ph + 2.8)) * kn, True)
    tail = (f'<path d="M-170,{hy - 30} Q{-290 + wig:.0f},{hy - 20} {-300 + wig:.0f},{hy - 150} Q{-300 + wig:.0f},{hy - 220} {-250 + wig:.0f},{hy - 240} Q{-260 + wig:.0f},{hy - 170} {-230 + wig:.0f},{hy - 110} Q{-210 + wig:.0f},{hy - 40} -150,{hy + 14}Z" fill="{fur}"/>')
    body = (f'<path d="M-200,{hy - 10} Q-210,{hy - 100} -80,{hy - 106} Q40,{hy - 116} 150,{hy - 100} Q222,{hy - 80} 214,{hy - 10} Q190,{hy + 50} 60,{hy + 46} Q-100,{hy + 54} -200,{hy - 10}Z" fill="{fur}"/>'
            f'<path d="M-130,{hy - 100} l16,50 M-60,{hy - 106} l12,60 M20,{hy - 110} l10,60 M100,{hy - 104} l8,56" stroke="{fur2}" stroke-width="12" fill="none"/>')
    neck = f'<path d="M120,{hy - 90} Q200,{hy - 130} 240,{hy - 110} L250,{hy - 10} Q190,{hy + 10} 140,{hy + 30}Z" fill="{fur}"/>'
    head = f'<g transform="translate(262,{hy - 70 + sn(t * 1.3) * 3:.1f})">{_cathead(t, fur, fur2, eyec, look, scream, blink, 8 + sn(t * 1.2) * 3)}</g>'
    ans = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g transform="translate(0,{bob:.1f})">{tail}{legs_far}{body}{neck}{legs_near}{head}</g></g>'
    return ans


def icefield(y=1700, seed=5, col="#d8e4f0", shade="#9fb4cc", n=7):
    """Jagged Arctic pack ice from y down to the bottom."""
    r = random.Random(seed)
    d = f"M-20,2420 L-20,{y} "
    xx = -20
    while xx < 1400:
        d += f"L{xx + r.randint(40, 90)},{y - r.randint(20, 70)} L{xx + r.randint(110, 170)},{y + r.randint(-10, 20)} "
        xx += 170
    out = f'<path d="{d}L1400,2420Z" fill="{col}" {OUT}/>'
    for _ in range(n):
        px, py = r.randint(0, 1250), r.randint(y + 60, 2360)
        out += f'<path d="M{px},{py} l{r.randint(50, 110)},{r.randint(-20, 10)} l{r.randint(30, 80)},{r.randint(10, 40)}" fill="none" stroke="{shade}" stroke-width="6"/>'
    return out


def steamer(x, y, s=1.0, t=0.0, flip=False, roll=1.0, smoke=0.0, lights=False, tilt=0.0, alpha=1.0):
    """Old cargo steamer (the Baychimo), side view, ~760 wide, ~520 tall, waterline/ice at (x, y). Rolls gently; flag flutters;
    smoke 0..1 draws a funnel plume; lights=True lights the windows (ghostly)."""
    sn = _m.sin
    f = -1 if flip else 1
    rl = sn(t * .8) * 2.2 * roll + tilt
    fl = sn(t * 4) * 10
    win = "#f3c555" if lights else "#1a2030"
    sm = ""
    for k in range(5 if smoke else 0):
        u = (t * .35 + k * .2) % 1.0
        sm += f'<circle cx="{-60 + u * 160 + sn(t + k) * 12:.0f}" cy="{-470 - u * 260:.0f}" r="{34 + u * 70:.0f}" fill="#6f7a8c" opacity="{(1 - u) * .55 * smoke:.2f}" stroke="none"/>'
    g = f'<g opacity="{alpha}" transform="translate({x},{y}) scale({f * s},{s}) rotate({rl:.2f} 0 0)" {OUT}>'
    g += sm
    g += '<rect x="170" y="-440" width="14" height="260" fill="#3a2b1f"/><rect x="-250" y="-420" width="14" height="240" fill="#3a2b1f"/>'
    g += f'<path d="M184,-436 q{50 + fl * .5:.0f},{-12 + fl * .3:.0f} {100 + fl:.0f},0 l-20,12 l12,14 l-92,2Z" fill="#8c2a2a" stroke-width="4"/>'
    g += '<path d="M-236,-420 L-390,-170 M-236,-420 L-60,-200 M184,-436 L330,-190 M184,-436 L40,-200" stroke="#0d0f15" stroke-width="3" fill="none"/>'
    g += '<path d="M-380,-190 L400,-190 L330,10 L-330,10 Q-400,-60 -380,-190Z" fill="#1c2230"/><path d="M-372,-130 H388 L378,-100 H-366Z" fill="#8c2a2a" stroke-width="4"/>'
    g += '<rect x="-210" y="-300" width="300" height="112" fill="#d8d4c4"/><rect x="-170" y="-380" width="190" height="82" fill="#d8d4c4"/>'
    g += f'<rect x="-150" y="-360" width="46" height="40" fill="{win}" stroke-width="4"/><rect x="-92" y="-360" width="46" height="40" fill="{win}" stroke-width="4"/><rect x="-34" y="-360" width="46" height="40" fill="{win}" stroke-width="4"/>'
    g += "".join(f'<circle cx="{wx}" cy="-244" r="20" fill="{win}" stroke-width="4"/>' for wx in (-160, -90, -20, 50))
    g += '<rect x="90" y="-420" width="86" height="240" fill="#14161b"/><rect x="90" y="-360" width="86" height="34" fill="#d8863a" stroke-width="4"/>'
    g += '<path d="M-212,-300 H92 M-172,-380 H22" stroke="#0d0f15" stroke-width="4"/><path d="M-380,-190 L400,-190" stroke="#0d0f15" stroke-width="8"/>'
    g += '<path d="M-368,-190 v-50 M-300,-190 v-50 M300,-190 v-50 M360,-190 v-50 M-370,-240 H-210 M270,-240 H394" stroke="#0d0f15" stroke-width="5" fill="none"/>'
    return g + '</g>'


def shipwheel(x, y, s=1.0, t=0.0, spin=1.0, col="#6a4a2c"):
    """Wooden ship's wheel that turns by itself; centre at (x, y)."""
    a = t * 40 * spin
    sp = "".join(f'<g transform="rotate({k * 45})"><rect x="-9" y="-190" width="18" height="380" rx="8" fill="{col}"/><rect x="-16" y="-214" width="32" height="46" rx="10" fill="{col}"/>'
                 f'<rect x="-16" y="168" width="32" height="46" rx="10" fill="{col}"/></g>' for k in range(4))
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><g transform="rotate({a:.1f})"><circle r="150" fill="none" stroke="{col}" stroke-width="30"/>'
            f'<circle r="150" fill="none" stroke="#0d0f15" stroke-width="3"/>{sp}<circle r="40" fill="#8a6a3c"/></g></g>')


def banshee(x, y, s=1.0, t=0.0, mode="float", flip=False, look=(1, 0), alpha=0.92, gown="#c4ced8", hair="#aeb4c0", wail=0.0, face_only=False):
    """Banshee: pale woman in a long gown, wild long grey hair, red-rimmed eyes. Hem at (x, y), ~480 tall, no legs.
    mode: float (drifts, arms hang, hair streams) | wail (head thrown back, arms spread, mouth open) | comb (sits/hovers, one arm combing her hair) | reach.
    wail 0..1 opens the mouth. face_only draws just the head centred at (x, y)."""
    sn = _m.sin
    f = -1 if flip else 1
    hov = -26 - sn(t * 1.4) * 14
    blink = 0.15 if (t % 4.0) < .13 else 1.0
    if mode == "wail":
        wail = max(wail, .6 + .4 * sn(t * 6)); la, lb, ra, rb = 140 + sn(t * 3) * 8, 10, -140 - sn(t * 3.3) * 8, -10; hr = -10 + sn(t * 5) * 3
    elif mode == "comb":
        la, lb, ra, rb = 150 + sn(t * 5) * 10, -70 + sn(t * 5) * 14, -8, -6; hr = 6 + sn(t * 1.2) * 3
    elif mode == "reach":
        la, lb, ra, rb = 8, -6, -98 + sn(t * 2.5) * 6, 4; hr = 4
    else:
        la, lb, ra, rb = 14 + sn(t * 1.5) * 6, -10, -14 - sn(t * 1.4) * 6, -10; hr = sn(t * .9) * 5 + look[0] * 4
    # hair: long wavy strands behind the head
    strands = ""
    for k in range(7):
        ox = (k - 3) * 15; L = 330 + (k % 3) * 40
        w = sn(t * 1.8 + k * .9) * 24
        strands += (f'<path d="M{ox},-30 Q{ox * 2.4 + w:.0f},{L * .35:.0f} {ox * 2 + w * 1.5:.0f},{L:.0f} Q{ox * 1.2 + w * .5:.0f},{L * .5:.0f} {ox * .5 + 10},-20Z" fill="{hair}" stroke-width="4"/>')
    def head():
        ey = "".join(f'<ellipse cx="{ex}" cy="-6" rx="12" ry="{11 * blink:.1f}" fill="#fff" stroke="#b02a2a" stroke-width="5"/>'
                     f'<circle cx="{ex + look[0] * 3:.1f}" cy="{-6 + look[1] * 2:.1f}" r="3.5" fill="#0d0f15" stroke="none"/>' for ex in (-19, 19))
        mo = (f'<ellipse cx="0" cy="{24 + wail * 6:.0f}" rx="{10 + wail * 12:.0f}" ry="{4 + wail * 24:.0f}" fill="#2a1014" stroke-width="4"/>')
        return (f'<g transform="rotate({hr:.1f})"><g transform="translate(0,-30)">{strands}</g>'
                f'<ellipse cx="0" cy="0" rx="48" ry="58" fill="#dfe6ee"/>'
                f'<path d="M-50,-10 Q-56,-70 0,-72 Q56,-70 50,-10 Q40,-46 0,-44 Q-40,-46 -50,-10Z" fill="{hair}" stroke-width="4"/>'
                + ey + '<path d="M-30,-24 l16,6 M30,-24 l-16,6" stroke-width="4" fill="none"/>' + mo + '</g>')
    if face_only:
        return f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}>{head()}</g>'

    def arm(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-16,-6 Q-34,60 -22,120 L22,120 Q36,60 16,-6Z" fill="{gown}"/>'
                f'<g transform="translate(0,116) rotate({e:.1f})"><path d="M-20,0 Q-34,50 -26,100 L26,100 Q34,50 20,0Z" fill="{gown}"/>'
                f'<circle cx="0" cy="104" r="14" fill="#dfe6ee"/><path d="M-8,112 l-4,26 M0,114 l0,30 M8,112 l5,26" stroke="#dfe6ee" stroke-width="6" stroke-linecap="round" fill="none"/>'
                + ('<g transform="translate(0,120)"><rect x="-26" y="0" width="52" height="16" rx="4" fill="#e8dcc0"/>' + ''.join(f'<path d="M{-22 + i * 9},16 v18" stroke="#e8dcc0" stroke-width="4"/>' for i in range(6)) + '</g>' if mode == "comb" and a > 100 else '')
                + '</g></g>')
    w1, w2, w3 = sn(t * 2.2) * 22, sn(t * 2.2 + 1.8) * 26, sn(t * 2.2 + 3.4) * 22
    out = f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT}><g opacity="{alpha}" transform="translate(0,{hov:.1f})">'
    out += (f'<path d="M-62,-330 Q-150,-130 {-176 + w1:.0f},6 L{-110 + w1:.0f},-26 L{-56 + w2:.0f},30 L{-4 + w2:.0f},-20 L{54 + w3:.0f},34 L{108 + w3:.0f},-22 L{180 + w3:.0f},6 Q150,-130 62,-330Z" fill="{gown}"/>'
            f'<path d="M-24,-280 Q-40,-140 {-48 + w1:.0f},-20 M26,-280 Q42,-140 {50 + w3:.0f},-20" fill="none" stroke="#8d98a8" stroke-width="4" opacity=".7"/>')
    out += f'<g transform="translate(-52,-306)">{arm(la, lb)}</g>'
    out += f'<path d="M-58,-250 Q-66,-320 -40,-346 Q0,-360 40,-346 Q66,-320 58,-250Z" fill="{gown}"/>'
    out += f'<g transform="translate(0,-396)">{head()}</g>'
    out += f'<g transform="translate(52,-306)">{arm(ra, rb)}</g>'
    return out + '</g></g>'


def nainrouge(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(1, 0), skin="#b03a2e", skin2="#7a221e", grin=0.0):
    """Nain Rouge: little red dwarf with pointed ears, glowing eyes, wolfish fur and hooves. Feet at (x, y), ~300 tall.
    mode: stand (sways, rubs hands) | walk (waddle) | dance (hops, arms up) | point (right arm points, laughs). grin 0..1 opens the mouth."""
    sn = _m.sin
    f = -1 if flip else 1
    ph = t * 6
    bob = 0.0; la = ra = 0.0
    al, el, ar, er = -40 + sn(t * 6) * 12, 80, 40 - sn(t * 6.3) * 12, -80
    sway = sn(t * 2) * 3
    if mode == "walk":
        la, ra = sn(ph) * 30, -sn(ph) * 30; bob = -abs(sn(ph)) * 10; sway = sn(ph) * 5
        al, el, ar, er = -sn(ph) * 35, -20, sn(ph) * 35, 20
    elif mode == "dance":
        ph = t * 8
        la, ra = sn(ph) * 35, -sn(ph) * 35; bob = -abs(sn(ph)) * 32; sway = sn(ph) * 8
        al, el, ar, er = 140 + sn(ph) * 25, 30, -140 - sn(ph + 1) * 25, -30; grin = max(grin, .8)
    elif mode == "point":
        al, el, ar, er = 20, 20, -88 + sn(t * 3) * 4, 0; grin = max(grin, .5 + .4 * sn(t * 7)); sway = sn(t * 6) * 3
    blink = 0.2 if (t % 3.3) < .12 else 1.0
    hr = sn(t * 1.1) * 4 + look[0] * 5

    def leg(a):
        return (f'<g transform="translate(0,-100) rotate({a:.1f})"><path d="M-20,0 Q-26,50 -16,92 L18,92 Q26,50 20,0Z" fill="{skin2}"/>'
                f'<path d="M-22,88 L24,88 L28,108 L-24,108Z" fill="#1d1416"/></g>')

    def arm(a, e):
        return (f'<g transform="rotate({a:.1f})"><path d="M-12,0 Q-18,36 -10,66 L12,66 Q18,36 12,0Z" fill="{skin}"/>'
                f'<g transform="translate(0,62) rotate({e:.1f})"><path d="M-11,0 Q-16,30 -9,58 L11,58 Q16,30 11,0Z" fill="{skin}"/>'
                f'<circle cx="0" cy="62" r="13" fill="{skin2}"/><path d="M-8,70 l-4,16 M0,72 l0,18 M8,70 l4,16" stroke="#1d1416" stroke-width="5" stroke-linecap="round" fill="none"/></g></g>')
    ey = "".join(f'<ellipse cx="{ex}" cy="-4" rx="12" ry="{9 * blink:.1f}" fill="#ffe04a"/><circle cx="{ex + look[0] * 3:.1f}" cy="{-4 + look[1] * 2:.1f}" r="3.5" fill="#0d0f15" stroke="none"/>' for ex in (-22, 22))
    mo = (f'<path d="M-30,24 Q0,{40 + grin * 26:.0f} 30,24 Q0,{30 + grin * 10:.0f} -30,24Z" fill="#2a0e10" stroke-width="4"/>'
          '<path d="M-22,26 l5,12 l5,-10 M4,28 l5,10 l5,-12 M16,26 l3,8" fill="#f4f0dc" stroke="none"/>')
    head = (f'<g transform="rotate({hr:.1f})"><path d="M-48,-30 L-98,-80 L-60,-4Z M48,-30 L98,-80 L60,-4Z" fill="{skin}"/>'
            f'<path d="M-54,-18 Q-60,-86 0,-92 Q60,-86 54,-18 Q56,44 0,56 Q-56,44 -54,-18Z" fill="{skin}"/>'
            f'<path d="M-44,-62 L-30,-96 L-14,-66 L0,-100 L14,-66 L30,-96 L44,-62Z" fill="{skin2}"/>'
            + ey + '<path d="M-36,-24 l22,10 M36,-24 l-22,10" stroke-width="5" fill="none"/>' + mo + '</g>')
    return (f'<g transform="translate({x},{y + bob:.1f}) scale({f * s},{s})" {OUT}><g transform="rotate({sway:.1f})">'
            f'{leg(la)}{leg(ra)}'
            f'<path d="M-46,-90 Q-62,-150 -42,-196 Q0,-216 42,-196 Q62,-150 46,-90Z" fill="{skin}"/>'
            f'<path d="M-30,-160 q10,10 0,22 M10,-170 q10,10 0,24 M26,-140 q8,8 0,18" stroke="{skin2}" stroke-width="4" fill="none"/>'
            f'<g transform="translate(-44,-186)">{arm(al, el)}</g>'
            f'<g transform="translate(0,-252)">{head}</g>'
            f'<g transform="translate(44,-186)">{arm(ar, er)}</g></g></g>')


def watcher(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(1, 0), alpha=1.0, cloak="#0c0f1a", edge="#3a4668", eyes=0.0):
    """Dark Watcher: very tall silhouette in a long cloak and wide-brimmed hat. Feet at (x, y), ~620 tall.
    mode: stand (cloak sways, head turns slowly) | walk (strides) | turn (head turns to face you) | wave (one arm raised). eyes 0..1 = glowing eyes."""
    sn = _m.sin
    f = -1 if flip else 1
    sw = sn(t * 1.1) * 6
    hr = sn(t * .6) * 8 + look[0] * 6
    la = ra = 0.0; bob = 0.0
    al, ar = 6 + sn(t * 1.2) * 3, -6 - sn(t * 1.2) * 3
    if mode == "walk":
        ph = t * 3.2; la, ra = sn(ph) * 24, -sn(ph) * 24; bob = -abs(sn(ph)) * 8; al, ar = -sn(ph) * 14, sn(ph) * 14; sw = sn(ph) * 8
    elif mode == "turn":
        hr = 0; eyes = max(eyes, .8)
    elif mode == "wave":
        ar = -150 + sn(t * 5) * 14
    leg = lambda a: f'<g transform="translate(0,-200) rotate({a:.1f})"><path d="M-20,0 L-16,196 L24,196 L20,0Z" fill="{cloak}"/></g>'
    face = ""
    if eyes > 0:
        face = f'<ellipse cx="-16" cy="-6" rx="9" ry="6" fill="#fff6c0"/><ellipse cx="16" cy="-6" rx="9" ry="6" fill="#fff6c0"/>' + glow(0, -6, 60, "#fff6c0", .3 * eyes)
    head = (f'<g transform="rotate({hr:.1f})"><ellipse cx="0" cy="0" rx="42" ry="50" fill="{cloak}"/>{face}'
            f'<ellipse cx="0" cy="-40" rx="110" ry="20" fill="{cloak}"/><path d="M-52,-42 Q-48,-120 0,-124 Q48,-120 52,-42Z" fill="{cloak}"/></g>')
    arm = lambda a: f'<g transform="rotate({a:.1f})"><path d="M-14,0 Q-26,120 -16,250 L16,250 Q26,120 14,0Z" fill="{cloak}"/></g>'
    return (f'<g opacity="{alpha:.2f}" transform="translate({x},{y + bob:.1f}) scale({f * s},{s})" stroke="{edge}" stroke-width="5">'
            f'{leg(la)}{leg(ra)}'
            f'<path d="M-62,-520 Q-92,-250 {-118 + sw:.0f},-30 L{118 + sw:.0f},-30 Q92,-250 62,-520Z" fill="{cloak}"/>'
            f'<g transform="translate(-58,-500)">{arm(al)}</g><g transform="translate(58,-500)">{arm(ar)}</g>'
            f'<g transform="translate(0,-560)">{head}</g></g>')


# ---------------------------------------------------------------- 2026-11-25 rigs: Bigfoot, cobra, jiangshi + scenery
def bigfoot(x, y, s=1.0, t=0.0, mode="stand", flip=False, look=(1, 0), fur="#3b2a22", fur2="#5a4034", roar=0.0):
    """Bigfoot: tall hunched ape-man, long arms. Feet at (x, y), ~560 tall.
    mode: stand (breathes, arms sway, looks around) | walk | run | throw (winds up and hurls rocks) | roar (arms up, beats chest). roar 0..1 opens the mouth."""
    sn = _m.sin
    f = -1 if flip else 1
    ph = t * (4.0 if mode == "walk" else 8.5)
    bob = lean = 0.0; la = ra = 0.0
    al, el, ar, er = 6 + sn(t * 1.3) * 3, 6, -6 - sn(t * 1.3) * 3, -6
    hr = sn(t * .8) * 4 + look[0] * 5
    rock = False
    if mode in ("walk", "run"):
        amp = 22 if mode == "walk" else 36
        la, ra = sn(ph) * amp, -sn(ph) * amp
        bob = -abs(sn(ph)) * (10 if mode == "walk" else 22); lean = 3 if mode == "walk" else 13
        al, ar = -sn(ph) * amp * 1.2, sn(ph) * amp * 1.2
        er, el = (-8, 8) if mode == "walk" else (-60, 60)
    elif mode == "throw":
        p = (t * 1.1) % 1.0
        rock = p < .62
        if p < .62:
            k = p / .62; ar = -60 - 110 * k; er = -20 - 40 * k; lean = -6 * k
        else:
            k = (p - .62) / .38; ar = -170 + 150 * k; er = -60 + 55 * k; lean = -6 + 18 * k
        al, el = 25 + sn(t * 3) * 4, 10
    elif mode == "roar":
        roar = max(roar, .7 + .3 * sn(t * 9)); beat = sn(t * 11) * 14
        al, el, ar, er = 120 + beat, 70, -120 - beat, -70; bob = -abs(sn(t * 5.5)) * 8
    blink = 0.15 if (t % 4.1) < .12 else 1.0
    fx, fy = look

    def leg(a):
        return (f'<g transform="translate(0,-232) rotate({a:.1f})"><path d="M-36,0 Q-46,110 -34,226 L34,226 Q48,110 36,0Z" fill="{fur}"/>'
                f'<path d="M-34,216 Q-44,248 -10,248 Q50,248 58,234 Q52,214 34,214Z" fill="{fur2}"/></g>')

    def arm(a, e, item=False):
        g = (f'<g transform="rotate({a:.1f})"><path d="M-27,-6 Q-36,90 -25,172 L25,172 Q36,90 27,-6Z" fill="{fur}"/>'
             f'<path d="M-30,60 l-12,18 l16,-4 M28,90 l12,18 l-16,-4" fill="none" stroke="{fur2}" stroke-width="5"/>'
             f'<g transform="translate(0,166) rotate({e:.1f})"><path d="M-23,-4 Q-30,84 -19,158 L19,158 Q30,84 23,-4Z" fill="{fur}"/>'
             f'<circle cx="0" cy="166" r="27" fill="{fur2}"/>')
        if item:
            g += '<g transform="translate(0,176)"><path d="M-30,-6 L-10,-30 L24,-24 L34,6 L10,26 L-22,20Z" fill="#8a8d94" stroke-width="5"/></g>'
        return g + '</g></g>'
    mo = (f'<path d="M-22,34 Q0,{40 + roar * 26:.0f} 22,34 Q0,{34 + roar * 4:.0f} -22,34Z" fill="#240e10" stroke-width="4"/>'
          + ('<path d="M-14,36 l4,10 l5,-9 M6,36 l5,9 l4,-10" fill="#f4f0dc" stroke="none"/>' if roar > .3 else ''))
    ey = "".join(f'<ellipse cx="{ex}" cy="-10" rx="10" ry="{9 * blink:.1f}" fill="#fff" stroke-width="3"/>'
                 f'<circle cx="{ex + fx * 3:.1f}" cy="{-10 + fy * 2:.1f}" r="4" fill="#0d0f15" stroke="none"/>' for ex in (-21, 21))
    head = (f'<g transform="rotate({hr:.1f})"><path d="M-50,-10 Q-58,-84 0,-96 Q58,-84 50,-10 Q54,52 0,58 Q-54,52 -50,-10Z" fill="{fur}"/>'
            f'<path d="M-16,-96 L0,-124 L16,-96Z" fill="{fur}"/>'
            f'<ellipse cx="0" cy="14" rx="36" ry="38" fill="#7a6254" stroke-width="4"/>' + ey +
            '<path d="M-40,-26 Q0,-10 40,-26 L36,-18 Q0,-2 -36,-18Z" fill="#1d1412" stroke-width="3"/>'
            '<path d="M-8,10 l-4,8 M8,10 l4,8" stroke-width="4" fill="none"/>' + mo + '</g>')
    torso = (f'<path d="M-76,0 Q-128,-110 -104,-250 Q-60,-304 0,-304 Q60,-304 104,-250 Q128,-110 76,0Z" fill="{fur}"/>'
             f'<ellipse cx="0" cy="-130" rx="52" ry="96" fill="{fur2}" opacity=".7" stroke="none"/>'
             f'<path d="M-100,-200 l-18,18 l24,-2 M96,-150 l20,16 l-26,0 M-80,-60 l-16,20 l22,-4 M70,-40 l14,22 l-20,-6" fill="none" stroke="{fur2}" stroke-width="5"/>')
    return (f'<g transform="translate({x},{y + bob:.1f}) scale({f * s},{s})" {OUT}>'
            f'{leg(la)}{leg(ra)}'
            f'<g transform="translate(0,-222) rotate({lean:.1f})"><g transform="translate(-106,-250)">{arm(al, el)}</g>'
            f'{torso}<g transform="translate(0,-292)">{head}</g><g transform="translate(106,-250)">{arm(ar, er, rock)}</g></g></g>')


def cobra(x, y, s=1.0, t=0.0, mode="sway", flip=False, look=(1, 0), col="#6a7a3a", col2="#c8b868", strike=0.0):
    """Cobra: coiled tail, rearing neck with a flared hood. Base at (x, y), ~380 tall.
    mode: sway (rears and sways, tongue flicks) | strike (lunges forward and back, hood wide) | low (near the ground)."""
    sn = _m.sin
    f = -1 if flip else 1
    if mode == "strike":
        strike = max(strike, max(0.0, sn(t * 2.4)) ** 2)
    rear = .45 if mode == "low" else 1.0
    pts = []
    for k in range(11):
        pts.append((-340 + k * 34, -sn(k * .95 + t * 1.4) * 16 - 14))
    neck = []
    N = 13
    for k in range(N + 1):
        v = k / N
        px = 12 * sn(t * 1.7 + v * 2.6) * v + strike * 300 * v * v + 8
        py = -v * 330 * rear
        neck.append((px, py))
    body = pts + neck
    d = "M" + " L".join(f"{a:.0f},{b:.0f}" for a, b in body)
    nd = "M" + " L".join(f"{a:.0f},{b:.0f}" for a, b in neck)
    hx, hy = neck[-1]
    flick = max(0.0, sn(t * 7)) * 30
    hood = 76 * (1.0 + .18 * strike)
    tongue = (f'<path d="M0,38 l0,{14 + flick:.0f} l-8,10 M0,{52 + flick:.0f} l8,10" stroke="#c43a4a" stroke-width="4" fill="none"/>' if flick > 8 else '')
    face = (f'<ellipse cx="0" cy="0" rx="40" ry="32" fill="{col}"/>'
            + "".join(f'<ellipse cx="{ex}" cy="-6" rx="9" ry="9" fill="#ffe04a" stroke-width="3"/><ellipse cx="{ex + look[0] * 2:.1f}" cy="-6" rx="2.6" ry="8" fill="#0d0f15" stroke="none"/>' for ex in (-18, 18))
            + tongue)
    return (f'<g transform="translate({x},{y}) scale({f * s},{s})" {OUT} fill="none">'
            f'<path d="{d}" stroke="#0d0f15" stroke-width="50" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="38" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{nd}" stroke="{col2}" stroke-width="12" stroke-linecap="round" opacity=".7"/>'
            f'<g transform="translate({hx:.0f},{hy + 20:.0f})"><ellipse cx="0" cy="40" rx="{hood:.0f}" ry="{hood * 1.05:.0f}" fill="{col}"/>'
            f'<path d="M-30,10 Q0,70 30,10" stroke="{col2}" stroke-width="10" fill="none"/><ellipse cx="0" cy="62" rx="{hood * .36:.0f}" ry="{hood * .5:.0f}" fill="{col2}" stroke="none" opacity=".6"/>'
            f'<g transform="translate(0,-26)">{face}</g></g></g>')


def jiangshi(x, y, s=1.0, t=0.0, mode="hop", flip=False, look=(1, 0), robe="#2c4a5a", trim="#b8963a", skin="#8fa58f", paper="#f0d060", speed=1.0, tilt=0.0):
    """Jiangshi (Chinese hopping corpse): stiff, pale, in an old official robe and cap, yellow paper charm on the forehead, arms straight out. Feet at (x, y), ~480 tall.
    mode: hop (hops with feet together) | stand (stiff, swaying) | sniff (hops slowly, head swings side to side, sniffing) | lean (leans forward, arms out)."""
    sn = _m.sin
    f = -1 if flip else 1
    ph = t * 5.2 * speed
    lift = 0.0; lean = 4.0; hr = 0.0; arms = -88 + sn(t * 1.5) * 2; sway = 0.0
    if mode == "hop":
        lift = abs(sn(ph)) * 74; lean = 6 + lift / 74 * 7; arms = -88 + sn(ph * 2) * 4
    elif mode == "sniff":
        ph = t * 2.2; lift = abs(sn(ph)) * 34; hr = sn(t * 2.4) * 16 + tilt; lean = 8
    elif mode == "lean":
        lean = 16 + sn(t * 1.3) * 2; hr = sn(t * 1.9) * 6
    else:
        sway = sn(t * 1.2) * 3
    paper_sw = sn(t * 4.3 + lift * .03) * 5
    blink = 0.0
    legs = ''.join(f'<path d="M{dx - 20},-110 L{dx - 18},-26 L{dx + 22},-26 L{dx + 20},-110Z" fill="#1c1a22"/><path d="M{dx - 24},-30 Q{dx - 26},-2 {dx},-2 Q{dx + 44},-2 {dx + 46},-14 Q{dx + 40},-30 {dx + 22},-30Z" fill="#0f1016"/>' for dx in (-24, 24))
    sleeve = lambda dy, c: (f'<g transform="translate(0,{dy}) rotate({arms:.1f})"><path d="M-26,-4 Q-34,100 -22,200 L22,200 Q34,100 26,-4Z" fill="{c}"/>'
                            f'<path d="M-24,170 h48" stroke="{trim}" stroke-width="7"/><path d="M-12,196 L-14,246 L14,246 L12,196Z" fill="{skin}"/>'
                            f'<path d="M-14,240 l-3,22 M-4,246 l-1,26 M6,246 l1,26 M14,240 l4,22" stroke="#0d0f15" stroke-width="5" fill="none"/></g>')
    # head
    eyes = (f'<path d="M-30,-4 q9,7 18,0 M12,-4 q9,7 18,0" fill="none" stroke-width="5"/>'
            f'<path d="M-30,6 q10,8 20,0 M10,6 q10,8 20,0" fill="none" stroke="#5a6a5a" stroke-width="4"/>')
    head = (f'<g transform="rotate({hr:.1f})"><circle cx="0" cy="-44" r="50" fill="{skin}"/>'
            f'<g transform="translate(0,-44)">{eyes}<path d="M-14,34 q14,10 28,0" fill="#2a1a1a" stroke-width="4"/><path d="M-7,34 l2,9 l3,-8 M3,35 l3,8 l2,-7" fill="#f4f0dc" stroke="none"/></g>'
            f'<path d="M-62,-62 Q0,-94 62,-62 L56,-92 Q0,-132 -56,-92Z" fill="#14151c"/><path d="M-66,-60 Q0,-80 66,-60 L66,-50 Q0,-68 -66,-50Z" fill="{trim}"/>'
            f'<g transform="translate(0,-64) skewX({paper_sw:.1f})"><path d="M-20,0 L20,0 L18,58 L0,68 L-18,58Z" fill="{paper}" stroke-width="4"/>'
            f'<path d="M-9,12 h18 M-10,26 h20 M-7,40 h14 M0,8 v46" stroke="#b02a22" stroke-width="4" fill="none"/></g></g>')
    body = (f'<g transform="translate(0,-110) rotate({lean + sway:.1f})">'
            f'<g transform="translate(0,-170)">{sleeve(0, "#223a48")}</g>'
            f'<path d="M-66,44 L-76,-170 Q-40,-205 0,-205 Q40,-205 76,-170 L66,44Z" fill="{robe}"/>'
            f'<path d="M0,-200 V44" stroke="{trim}" stroke-width="7" fill="none"/><path d="M-66,34 H66" stroke="{trim}" stroke-width="8"/>'
            f'<rect x="-34" y="-136" width="68" height="56" fill="none" stroke="{trim}" stroke-width="6"/><path d="M-22,-124 h44 M-22,-108 h44 M-22,-92 h44" stroke="{trim}" stroke-width="3"/>'
            f'<g transform="translate(0,-190)">{sleeve(0, robe)}</g>'
            f'<rect x="-14" y="-224" width="28" height="30" fill="{skin}"/><g transform="translate(0,-196)">{head}</g></g>')
    return (f'<g transform="translate({x},{y - lift:.1f}) scale({f * s},{s})" {OUT}>{legs}{body}</g>')


def volcano(x, y, w=1100, h=900, col="#4a5470", snow_="#dce4ee"):
    return (f'<path d="M{x - w / 2},{y} L{x - w * .12},{y - h} L{x - w * .04},{y - h * .93} L{x + w * .06},{y - h * 1.0} L{x + w * .14},{y - h * .96} L{x + w / 2},{y}Z" fill="{col}" {OUT}/>'
            f'<path d="M{x - w * .12},{y - h} L{x - w * .04},{y - h * .93} L{x + w * .06},{y - h} L{x + w * .14},{y - h * .96} L{x + w * .2},{y - h * .72} L{x + w * .08},{y - h * .78} L{x - w * .02},{y - h * .7} L{x - w * .1},{y - h * .78} L{x - w * .18},{y - h * .7}Z" fill="{snow_}" {OUT}/>')


def cabin(x, y, s=1.0, lit="#f3c555", logs="#6a4a30", roof="#3a2a22", shake=0.0, t=0.0):
    sh = _m.sin(t * 40) * shake
    g = f'<g transform="translate({x + sh:.1f},{y}) scale({s})" {OUT}><rect x="-230" y="-250" width="460" height="250" fill="{logs}"/>'
    for yy in range(-210, 0, 42):
        g += f'<path d="M-230,{yy} H230" stroke="#2a1c12" stroke-width="5"/>'
    g += (f'<path d="M-270,-240 L0,-400 L270,-240Z" fill="{roof}"/><rect x="-170" y="-190" width="90" height="90" fill="{lit}"/>'
          f'<path d="M-125,-190 V-100 M-170,-145 H-80" stroke="#2a1c12" stroke-width="5"/><rect x="60" y="-180" width="90" height="180" fill="#2a1c12"/>'
          f'<rect x="130" y="-420" width="46" height="100" fill="#4a3a36"/></g>')
    return g


def pyramid(x, y, s=1.0, col="#a8946a", shade="#7a6a4a"):
    return (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-420,0 L0,-420 L420,0Z" fill="{col}"/><path d="M0,-420 L420,0 L120,0Z" fill="{shade}"/></g>')


def torch(x, y, s=1.0, t=0.0):
    fl = f'<path d="M0,-6 Q-30,{-50 - _m.sin(t * 9) * 10:.0f} 0,{-110 - _m.sin(t * 11) * 12:.0f} Q30,-50 0,-6Z" fill="#e8892a" stroke-width="4"/><path d="M0,-6 Q-14,-34 0,{-66 - _m.sin(t * 13) * 8:.0f} Q14,-34 0,-6Z" fill="#f6d36a" stroke="none"/>'
    return f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-10,0 L-16,230 L16,230 L10,0Z" fill="#4a3322"/><path d="M-26,0 L26,0 L18,-18 L-18,-18Z" fill="#2a2a30"/>{fl}</g>'


def tomb_wall(y=1500, stone="#6a5a44", seed=12):
    r = random.Random(seed)
    g = f'<rect width="1350" height="2400" fill="#1c1812"/><rect x="-20" y="-20" width="1390" height="{y + 20}" fill="{stone}" {OUT}/>'
    for row in range(0, y, 130):
        off = 0 if (row // 130) % 2 == 0 else 100
        for cx in range(-100 + off, 1400, 200):
            g += f'<rect x="{cx}" y="{row}" width="200" height="130" fill="none" stroke="#2a2218" stroke-width="4" opacity=".6"/>'
    # abstract wall paintings: eyes, waves, little birds, figures (original, not real glyphs)
    for gx in range(80, 1300, 210):
        for gy in range(150, y - 150, 260):
            k = r.randint(0, 3)
            c = r.choice(["#b8452e", "#2f7a8a", "#d8b44a"])
            if k == 0:
                g += f'<path d="M{gx},{gy} q40,-34 80,0 q-40,34 -80,0Z" fill="none" stroke="{c}" stroke-width="6"/><circle cx="{gx + 40}" cy="{gy}" r="9" fill="{c}" stroke="none"/>'
            elif k == 1:
                g += f'<path d="M{gx},{gy} q20,-26 40,0 t40,0 t40,0" fill="none" stroke="{c}" stroke-width="6"/>'
            elif k == 2:
                g += f'<path d="M{gx + 20},{gy + 40} L{gx + 40},{gy - 20} L{gx + 60},{gy + 40}M{gx + 40},{gy - 20} v-26" fill="none" stroke="{c}" stroke-width="6"/><circle cx="{gx + 40}" cy="{gy - 56}" r="12" fill="{c}" stroke="none"/>'
            else:
                g += f'<rect x="{gx + 10}" y="{gy - 30}" width="60" height="60" fill="none" stroke="{c}" stroke-width="6"/><path d="M{gx + 10},{gy} h60" stroke="{c}" stroke-width="5"/>'
    return g + f'<rect x="-20" y="{y}" width="1390" height="{2420 - y}" fill="#3a3024" {OUT}/>'


def goldshrine(x, y, s=1.0, gold="#d8b43a", dark="#8a6a1e"):
    g = f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-300" y="-420" width="600" height="420" fill="{gold}"/><rect x="-300" y="-470" width="600" height="60" fill="{dark}"/>'
    for px in (-250, -90, 90, 250):
        g += f'<rect x="{px - 14}" y="-410" width="28" height="400" fill="{dark}"/>'
    g += f'<path d="M-200,-300 q50,-40 100,0 q-50,40 -100,0Z M100,-300 q50,-40 100,0 q-50,40 -100,0Z" fill="#2f7a8a"/><path d="M-60,-200 h120 v60 h-120Z" fill="#b8452e"/>'
    return g + '</g>'


def sealed_door(x, y, s=1.0, glow_=0.0):
    g = (f'<g transform="translate({x},{y}) scale({s})" {OUT}><path d="M-260,0 L-260,-520 Q0,-640 260,-520 L260,0Z" fill="#7a6a50"/>'
         f'<path d="M-190,0 L-190,-480 Q0,-570 190,-480 L190,0Z" fill="#4a3e2e"/><path d="M-190,-250 H190" stroke="#2a2218" stroke-width="8"/>'
         f'<path d="M-60,-330 q60,-40 120,0 q-60,40 -120,0Z" fill="#d8b43a"/><circle cx="0" cy="-330" r="12" fill="#0d0f15"/><path d="M0,-400 v-40" stroke="#d8b43a" stroke-width="10"/></g>')
    if glow_ > 0:
        g += glow(x, y - 330 * s, 260 * s, "#ffd860", .5 * glow_)
    return g


def cairo_city(y=1700, lit=1.0, seed=7, col="#1f2a40", shapes=True, windows=True):
    """Night skyline with domes and minarets; `lit` 0..1 = share of windows still lit (decreasing in a story animation).
    Use shapes=True/windows=False for the static buildings and shapes=False/windows=True in an actor for animated windows."""
    r = random.Random(seed); g = ''
    for bx in range(-40, 1400, 190):
        h = r.randint(260, 520); w = 170
        if shapes:
            g += f'<rect x="{bx}" y="{y - h}" width="{w}" height="{h + 700}" fill="{col}" {OUT}/>'
        dome = r.random() < .5
        if shapes:
            if dome:
                g += f'<path d="M{bx + 10},{y - h} Q{bx + w / 2},{y - h - 150} {bx + w - 10},{y - h}Z" fill="{col}" {OUT}/><path d="M{bx + w / 2},{y - h - 148} v-50" stroke="#0d0f15" stroke-width="6"/>'
            else:
                g += f'<rect x="{bx + w / 2 - 14}" y="{y - h - 160}" width="28" height="160" fill="{col}" {OUT}/><path d="M{bx + w / 2 - 22},{y - h - 160} L{bx + w / 2},{y - h - 220} L{bx + w / 2 + 22},{y - h - 160}Z" fill="{col}" {OUT}/>'
        for wy in range(y - h + 40, y + 500, 90):
            for wx in (bx + 30, bx + 100):
                v = r.random()
                if windows and v < lit * 0.85:
                    g += f'<rect x="{wx}" y="{wy}" width="36" height="46" fill="#f3c555" stroke="#0d0f15" stroke-width="3"/>'
    return g


def bamboo(x, y, h=1200, col="#4a7a52", seed=1):
    r = random.Random(seed); g = f'<g {OUT}>'
    for i, dx in enumerate((-50, 0, 46)):
        hh = h * r.uniform(.8, 1.0)
        g += f'<rect x="{x + dx - 16}" y="{y - hh}" width="32" height="{hh}" fill="{col}"/>'
        for k in range(1, int(hh // 150)):
            g += f'<path d="M{x + dx - 16},{y - k * 150} h32" stroke="#0d0f15" stroke-width="5"/><path d="M{x + dx + 16},{y - k * 150} q50,-20 80,-50 q-50,8 -80,20Z" fill="{col}" stroke-width="4"/>'
    return g + '</g>'


def inn(x, y, s=1.0, lit="#f3c555", wall="#7a5a44", roof="#2c2430"):
    g = (f'<g transform="translate({x},{y}) scale({s})" {OUT}><rect x="-300" y="-300" width="600" height="300" fill="{wall}"/>'
         f'<path d="M-380,-290 Q-260,-300 -200,-380 L200,-380 Q260,-300 380,-290 L330,-250 L-330,-250Z" fill="{roof}"/>'
         f'<path d="M-330,-250 Q-200,-260 -150,-330 L-150,-380 M330,-250 Q200,-260 150,-330" fill="none"/>'
         f'<rect x="-230" y="-230" width="110" height="110" fill="{lit}"/><path d="M-175,-230 V-120 M-230,-175 H-120" stroke="#2a1c12" stroke-width="6"/>'
         f'<rect x="-50" y="-200" width="100" height="200" fill="#3a1e18"/><path d="M0,-200 V0" stroke="#0d0f15" stroke-width="5"/>'
         f'<rect x="120" y="-230" width="110" height="110" fill="{lit}"/><path d="M175,-230 V-120 M120,-175 H230" stroke="#2a1c12" stroke-width="6"/>'
         f'<ellipse cx="-300" cy="-190" rx="26" ry="36" fill="#c8382e" stroke-width="5"/><ellipse cx="300" cy="-190" rx="26" ry="36" fill="#c8382e" stroke-width="5"/></g>')
    return g + glow(x - 300 * s, y - 190 * s, 140 * s, "#ff8a60", .35) + glow(x + 300 * s, y - 190 * s, 140 * s, "#ff8a60", .35)
