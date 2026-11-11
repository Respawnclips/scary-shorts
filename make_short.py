#!/usr/bin/env python3
"""Build an animated cartoon scary-story Short.

Usage: python3 make_short.py stories/<id>.json [--preview]
Needs next to the JSON: stories/<id>.py exporting SCENES (see toon.py for the drawing helpers).
Output: videos/<id>.mp4 (1080x1920, 30fps, H.264 + AAC). --preview writes work/<id>/sheet.jpg only.

Story JSON: id, lang ("en" or "nl", default "en"), lines[],
scenes[{name, from (first line index), move [dx, dy, zoom0, zoom1], rain}],
flash_lines[] (lines that get lightning + thunder).
"""
import importlib.util, json, os, subprocess, sys, zlib, random
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
W, H, FPS = 1080, 1920, 30
CW, CH = 1350, 2400                # scene canvas (bigger than the frame: room to pan and zoom)
SR = 24000
VOICE, SPEED, GAP = "bm_fable", 0.95, 0.28
NL_MODEL = "voices/nl2/vits-piper-nl_NL-miro-high/nl_NL-miro-high.onnx"      # Dutch narrator (piper)
VOICE_FX = ("highpass=f=70,equalizer=f=180:t=q:w=1:g=2.5,equalizer=f=3500:t=q:w=1.5:g=-1.5,"
            "acompressor=threshold=-20dB:ratio=3:attack=8:release=120,aecho=0.8:0.55:70|140:0.16|0.08")
FONTS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
FONT = next(f for f in FONTS if os.path.exists(f))
DEPTH = {"bg": 0.25, "mid": 0.6, "glow": 0.6, "fg": 1.0}


# ---------------- audio ----------------
def _say_en(lines):
    from kokoro_onnx import Kokoro
    k = Kokoro(f"{HERE}/voices/kokoro-v1.0.int8.onnx", f"{HERE}/voices/voices-v1.0.bin")
    for line in lines:
        s, _ = k.create(line, voice=VOICE, speed=SPEED, lang="en-gb")
        yield s.astype(np.float32)


def _say_nl(lines):
    """Dutch narrator (piper, 22050 Hz) resampled to SR."""
    from piper import PiperVoice
    from piper.config import SynthesisConfig
    v = PiperVoice.load(f"{HERE}/{NL_MODEL}")
    cfg = SynthesisConfig(length_scale=1.03)
    sr0 = v.config.sample_rate
    for line in lines:
        a = np.concatenate([c.audio_float_array for c in v.synthesize(line, cfg)]).astype(np.float32)
        n = int(round(len(a) * SR / sr0))
        yield np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)


def _fx(a, echo=True):
    """Warm up one spoken line: EQ, light compression, small room echo (the raw TTS sounds flat)."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        sf.write(f"{td}/i.wav", a, SR)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{td}/i.wav", "-af", (VOICE_FX if echo else VOICE_FX.rsplit(",aecho", 1)[0]) + ",loudnorm=I=-16",
                        "-ar", str(SR), f"{td}/o.wav"], check=True)
        out, _ = sf.read(f"{td}/o.wav", dtype="float32")
    return out


def _load_pre(tts_dir, n):
    """Pre-synthesized lines (tts/<id>/00.wav, 01.wav, ...) e.g. from a cloud voice; resampled to SR."""
    for i in range(n):
        a, sr0 = sf.read(f"{tts_dir}/{i:02d}.wav", dtype="float32")
        if a.ndim > 1: a = a.mean(1)
        m = int(round(len(a) * SR / sr0))
        yield np.interp(np.linspace(0, len(a) - 1, m), np.arange(len(a)), a).astype(np.float32)


def narrate(lines, lang="en", tts_dir=None):
    chunks, times, t = [np.zeros(int(0.4 * SR), np.float32)], [], 0.4
    pre = tts_dir and all(os.path.exists(f"{tts_dir}/{i:02d}.wav") for i in range(len(lines)))
    for s in (_load_pre(tts_dir, len(lines)) if pre else _say_nl(lines) if lang == "nl" else _say_en(lines)):
        s = _fx(s, echo=not pre)
        d = len(s) / SR
        times.append((t, t + d))
        chunks += [s, np.zeros(int(GAP * SR), np.float32)]
        t += d + GAP
    return np.concatenate(chunks + [np.zeros(int(0.9 * SR), np.float32)]), times


def music(voice, seed):
    """Original spooky music: music-box melody in minor, dark string pad, bell hits, big reverb; ducks under the voice."""
    n = len(voice); t = np.arange(n) / SR; T = t[-1]; rng = np.random.default_rng(seed + 11)
    root = (440.0, 392.0, 466.16, 349.23)[seed % 4] / 2          # A, G, Bb or F (per story)
    hz = lambda semi: root * 2 ** (semi / 12)
    bpm = 66 + seed % 3 * 4; beat = 60 / bpm
    # natural minor with raised 7th; phrase of 12 eighth-notes per bar-pair, chords: i, bVI, V, i
    chords = [(0, 3, 7), (-4, 0, 3), (-5, -1, 2), (0, 3, 7)]
    phrases = [[12, 15, 19, 15, 12, 14, 11, 14, 17, 14, 11, None],
               [15, 19, 22, 19, 15, 17, 14, 17, 20, 17, 14, None],
               [14, 17, 20, 17, 14, 16, 11, 14, 18, 14, 11, None],
               [12, 15, 19, 24, 22, 19, 15, 19, 12, None, None, None]]
    mb = np.zeros(n); pad = np.zeros(n)
    bar = 3 * beat; k = 0
    while k * bar < T:
        i0 = k * bar; ch = chords[k % 4]; ph = phrases[k % 4]
        step = bar / 12
        for j, sm in enumerate(ph):
            if sm is None or rng.random() < 0.12: continue
            f = hz(sm); i = int((i0 + j * step) * SR); L = int(1.6 * SR); xx = np.arange(L) / SR
            tone = (np.sin(2 * np.pi * f * xx) + 0.45 * np.sin(2 * np.pi * f * 2.76 * xx) * np.exp(-xx / 0.12)
                    + 0.2 * np.sin(2 * np.pi * f * 5.4 * xx) * np.exp(-xx / 0.05)) * np.exp(-xx / 0.45) * (1 - np.exp(-xx / 0.004))
            seg = mb[i:i + L]; seg += tone[:len(seg)] * 0.5
        for sm in ch:                                             # string pad, a bar long, overlapped
            for det in (-0.12, 0.12):
                f = hz(sm - 12) * 2 ** (det / 12)
                i = int(i0 * SR); L = int((bar + 1.2) * SR); xx = np.arange(L) / SR
                v = sum(np.sin(2 * np.pi * f * h * xx + h) / h ** 1.5 for h in range(1, 6)) * np.sin(np.pi * np.clip(xx / (bar + 1.2), 0, 1)) ** 1.5
                seg = pad[i:i + L]; seg += v[:len(seg)] * 0.18
        i = int(i0 * SR); L = int(bar * 1.3 * SR); xx = np.arange(L) / SR          # low bell on every bar
        bl = (np.sin(2 * np.pi * hz(chords[k % 4][0] - 24) * xx) + 0.5 * np.sin(2 * np.pi * hz(chords[k % 4][0] - 24) * 2.4 * xx)) * np.exp(-xx / 1.1) * 0.8
        seg = pad[i:i + L]; seg += bl[:len(seg)] * 0.5
        k += 1
    dry = mb * 0.8 + pad
    ir = rng.standard_normal(int(1.6 * SR)) * np.exp(-np.arange(int(1.6 * SR)) / SR / 0.5)
    m = len(dry) + len(ir); N = 1 << (m - 1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(dry, N) * np.fft.rfft(ir, N), N)[:n]
    out = dry + 0.22 * wet / (np.max(np.abs(wet)) + 1e-9) * np.max(np.abs(dry))
    out /= np.max(np.abs(out)) + 1e-9
    env = np.abs(voice); kk = int(0.3 * SR)
    env = np.convolve(env, np.ones(kk) / kk, "same"); env = np.clip(env / (np.percentile(env, 90) + 1e-9), 0, 1)
    fade = np.minimum(1, np.minimum(t / 2.0, (T - t) / 2.5))
    return (out * (1 - 0.5 * env) * fade * 0.40).astype(np.float32)


def dread(voice, cuts, seed):
    """Audible creepy bed (phones can't play the 49 Hz drone): dissonant drone, wind, heartbeat, end sting. Ducks under the voice."""
    n = len(voice); rng = np.random.default_rng(seed + 7)
    t = np.arange(n) / SR; T = t[-1]
    def saw(f, k=7):
        return sum(np.sin(2 * np.pi * f * h * t + h) / h ** 1.3 for h in range(1, k + 1))
    sw = lambda rate, ph: 0.55 + 0.45 * np.sin(2 * np.pi * rate * t + ph)
    d = (saw(110) * sw(.11, 0) + saw(116.5) * sw(.09, 2) + 0.7 * saw(155.6, 5) * sw(.13, 4) + 0.5 * saw(55, 4)) * 0.25
    nz = rng.standard_normal(n)
    wind = np.convolve(nz, np.ones(14) / 14, "same") * (0.5 + 0.5 * np.sin(2 * np.pi * 0.17 * t + 1)) ** 2 * 5
    wh = (nz - np.convolve(nz, np.ones(30) / 30, "same")) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * t + 3)) ** 3 * 0.8
    sh = np.sin(2 * np.pi * (1480 + 40 * np.sin(2 * np.pi * 0.3 * t)) * t) * np.clip(np.sin(2 * np.pi * 0.06 * t - 1), 0, 1) ** 2 * 0.1
    b = d + wind + wh + sh
    b /= np.max(np.abs(b)) + 1e-9
    hb = np.zeros(n)                                      # heartbeat, faster and louder toward the end
    x = 0.8
    while x < T - 1:
        prog = x / T; per = 1.1 - 0.45 * prog
        for off, lvl in ((0, 1.0), (0.22, 0.7)):
            i = int((x + off) * SR); L = int(0.25 * SR); xx = np.arange(L) / SR
            th = np.sin(2 * np.pi * 52 * xx) * np.exp(-xx / 0.07) * lvl * (0.25 + 0.75 * prog)
            seg = hb[i:i + L]; seg += th[:len(seg)]
        x += per
    out = b * 0.25 + hb * 0.45
    if cuts:                                              # scare sting when the last scene starts
        i = int(cuts[-1] * SR); L = int(2.2 * SR); xx = np.arange(L) / SR
        cl = sum(np.sin(2 * np.pi * f * xx) for f in (466, 493, 698, 740, 1244))
        st = (cl * 0.18 + rng.standard_normal(L) * 0.3) * np.exp(-xx / 0.6) * (1 - np.exp(-xx / 0.01))
        seg = out[i:i + L]; seg += st[:len(seg)]
    env = np.abs(voice); k = int(0.25 * SR)
    env = np.convolve(env, np.ones(k) / k, "same"); env = np.clip(env / (np.percentile(env, 90) + 1e-9), 0, 1)
    duck = 1 - 0.55 * env
    fade = np.minimum(1, np.minimum(t / 1.5, (T - t) / 1.5))
    return (out * duck * fade * 0.30).astype(np.float32)


def ambience(n, seed, flashes, cuts, rain_spans):
    rng = np.random.default_rng(seed)
    t = np.arange(n) / SR
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)
    amb = (np.sin(2 * np.pi * 49 * t) + 0.5 * np.sin(2 * np.pi * 73.4 * t + 1)
           + 0.25 * np.sin(2 * np.pi * 98.2 * t)) * lfo * 0.5
    noise = rng.standard_normal(n)
    amb += np.convolve(noise, np.ones(400) / 400, "same") * 6 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t + 2))
    hiss = (noise - np.convolve(noise, np.ones(6) / 6, "same")) * 0.3
    for a, b in rain_spans:
        amb[int(a * SR):int(b * SR)] += hiss[int(a * SR):int(b * SR)]
    for ft in flashes:                                   # thunder
        i = int((ft + 0.12) * SR); L = int(3.0 * SR); x = np.arange(L) / SR
        env = np.exp(-x / 0.7) * (1 - np.exp(-x / 0.02))
        boom = (np.sin(2 * np.pi * 36 * x) * 1.5 + np.convolve(rng.standard_normal(L), np.ones(60) / 60, "same") * 9) * env * 2.2
        seg = amb[i:i + L]; seg += boom[:len(seg)]
    for ct in cuts:                                      # low hit on every scene change
        i = int(ct * SR); L = int(0.9 * SR); x = np.arange(L) / SR
        hit = np.sin(2 * np.pi * (70 - 30 * x) * x) * np.exp(-x / 0.18) * 1.6
        seg = amb[i:i + L]; seg += hit[:len(seg)]
    amb /= np.max(np.abs(amb)) + 1e-9
    fade = np.minimum(1, np.minimum(t / 1.0, (t[-1] - t) / 1.0))
    return (amb * fade * 0.17).astype(np.float32)


# ---------------- drawing ----------------
def render_layers(scenes, work):
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": CW, "height": CH})
        for name, layers in scenes.items():
            out[name] = {}
            for L in ("bg", "mid", "glow", "fg"):
                path = f"{work}/{name}_{L}.png"
                pg.set_content('<html><body style="margin:0;background:transparent">'
                               f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" '
                               'stroke-linejoin="round" stroke-linecap="round" font-family="DejaVu Sans">'
                               f'{layers.get(L, "")}</svg></body></html>')
                pg.screenshot(path=path, omit_background=True)
                out[name][L] = Image.open(path).convert("RGBA")
        b.close()
    return out


def make_rain(seed):
    rng = np.random.default_rng(seed)
    img = Image.new("RGBA", (W, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    for _ in range(1100):
        x, y, L = rng.uniform(0, W + 200), rng.uniform(0, H * 2), rng.uniform(40, 100)
        d.line((x, y, x - L * 0.2, y + L), fill=(205, 212, 228, int(rng.uniform(40, 110))), width=3)
    return img


def make_vignette():
    yy, xx = np.mgrid[0:H, 0:W]
    v = np.clip(((xx - W / 2) / (W * 0.74)) ** 2 + ((yy - H * 0.5) / (H * 0.7)) ** 2, 0, 1)
    arr = np.zeros((H, W, 4), np.uint8); arr[..., 2] = 12; arr[..., 3] = (v ** 1.6 * 215).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def make_fog(seed):
    """Seamless horizontal fog band (RGBA, 2W wide)."""
    rng = np.random.default_rng(seed + 3); P = W * 2
    small = np.tile(rng.random((9, 36)).astype(np.float32), (1, 3))
    im = Image.fromarray((small * 255).astype(np.uint8)).resize((P * 3, 520), Image.BICUBIC).filter(ImageFilter.GaussianBlur(46))
    a = np.array(im)[:, P:2 * P].astype(np.float32) / 255
    a = np.clip((a - 0.32) * 1.9, 0, 1) * (np.sin(np.linspace(0, np.pi, 520)) ** 1.6)[:, None]
    arr = np.zeros((520, P, 4), np.uint8); arr[..., 0], arr[..., 1], arr[..., 2] = 175, 188, 212; arr[..., 3] = (a * 78).astype(np.uint8)
    one = Image.fromarray(arr, "RGBA"); two = Image.new("RGBA", (P * 2, 520)); two.paste(one, (0, 0)); two.paste(one, (P, 0))
    return two, P


_wcache = {}
def word_img(word, accent=False):
    key = (word, accent)
    if key not in _wcache:
        f = ImageFont.truetype(FONT, 128)
        tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
        x0, y0, x1, y1 = tmp.textbbox((0, 0), word, font=f, stroke_width=12)
        if x1 - x0 > W - 110:                               # shrink very long words
            f = ImageFont.truetype(FONT, int(128 * (W - 110) / (x1 - x0)))
            x0, y0, x1, y1 = tmp.textbbox((0, 0), word, font=f, stroke_width=12)
        img = Image.new("RGBA", (x1 - x0 + 40, y1 - y0 + 48), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        d.text((20 - x0 + 6, 20 - y0 + 10), word, font=f, fill=(0, 0, 0, 170), stroke_width=12, stroke_fill=(0, 0, 0, 170))
        d.text((20 - x0, 20 - y0), word, font=f, fill=(255, 70, 50) if accent else (255, 255, 255),
               stroke_width=12, stroke_fill=(0, 0, 0))
        _wcache[key] = img
    return _wcache[key]


ACCENT = {"dead", "death", "blood", "never", "don't", "die", "died", "kill", "killed", "scream", "screamed",
          "burning", "red", "gone", "vanished", "run", "alone", "dark", "cursed", "ghost", "demon", "devil",
          # Dutch
          "dood", "doden", "bloed", "nooit", "niet", "sterft", "stierf", "schreeuw", "schreeuwde", "gil",
          "brandend", "rood", "weg", "verdwenen", "ren", "alleen", "donker", "vervloekt", "spook", "duivel",
          "geest", "lijk", "graf", "angst", "nacht", "zwart"}


def main():
    src = sys.argv[1]; preview = "--preview" in sys.argv
    story = json.load(open(src)); sid = story["id"]
    seed = zlib.crc32(sid.encode()) % 10_000; rnd = random.Random(seed)
    lines = story["lines"]; n = len(lines)
    work = f"{HERE}/work/{sid}"; os.makedirs(work, exist_ok=True); os.makedirs(f"{HERE}/videos", exist_ok=True)
    spec = importlib.util.spec_from_file_location("scenes", src[:-5] + ".py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    layers = render_layers(mod.SCENES, work)
    plan = story["scenes"]

    if preview:                                             # contact sheet of every scene
        tiles = []
        for sc in plan:
            L = layers[sc["name"]]; im = L["bg"].copy()
            for k in ("mid", "glow", "fg"): im.alpha_composite(L[k])
            im = im.crop((54, 96, CW - 54, CH - 96)).resize((W, H))
            w = word_img(lines[sc["from"]].split()[0].upper().strip(".,!?"))
            im.alpha_composite(w, ((W - w.width) // 2, int(H * 0.5) - w.height // 2))
            tiles.append(im.convert("RGB").resize((360, 640)))
        sheet = Image.new("RGB", (360 * 4, 640 * ((len(tiles) + 3) // 4)))
        for i, tl in enumerate(tiles): sheet.paste(tl, (360 * (i % 4), 640 * (i // 4)))
        sheet.save(f"{work}/sheet.jpg", quality=85); print("sheet:", f"{work}/sheet.jpg"); return

    voice, times = narrate(lines, story.get("lang", "en"), f"{HERE}/tts/{sid}"); D = len(voice) / SR
    if D > 59: sys.exit(f"Too long for a Short: {D:.1f}s - trim lines.")
    starts = [0.0 if i == 0 else times[sc["from"]][0] - 0.12 for i, sc in enumerate(plan)]
    ends = starts[1:] + [D]
    flashes = sorted(round(times[i][0] + 0.25, 2) for i in story.get("flash_lines", []) if i < n)
    rain_spans = [(a, b) for sc, a, b in zip(plan, starts, ends) if sc.get("rain")]
    mix = voice * 0.95 + ambience(len(voice), seed, flashes, starts[1:], rain_spans) + dread(voice, starts[1:], seed) + music(voice, seed)
    mix /= max(1.0, np.max(np.abs(mix)) / 0.97)
    sf.write(f"{work}/audio.wav", mix, SR)

    words = []                                              # (start, end, WORD, accent)
    for line, (a, b) in zip(lines, times):
        ws = line.split(); wt = np.array([len(w) + 2 for w in ws], float)
        cum = np.concatenate([[0], np.cumsum(wt)]) / wt.sum()
        for w, c0, c1 in zip(ws, cum[:-1], cum[1:]):
            clean = w.strip(".,!?…").upper()
            if clean:
                words.append((a + (b - a) * c0, a + (b - a) * c1 + 0.04, clean, clean.lower() in ACCENT))

    rain_l, vig = make_rain(seed), make_vignette()
    white = Image.new("RGBA", (W, H), (235, 232, 255, 255)); black = Image.new("RGBA", (W, H), (0, 0, 0, 255))

    def flash_a(t):
        a = 0.0
        for ft in flashes:
            dt = t - ft
            if 0 <= dt < 0.6: a = max(a, np.exp(-dt / 0.12) * (1 if dt < 0.07 or dt > 0.14 else 0.35))
        return a

    fog_img, fogP = make_fog(seed)
    prng = np.random.default_rng(seed + 5)
    motes = [(prng.random() * W, prng.random() * H, prng.uniform(-14, 14), prng.uniform(-30, -8), prng.uniform(2, 5.5), prng.random() * 6.28) for _ in range(34)]
    grain = [(prng.standard_normal((H, W)) * 2.6).astype(np.int16) for _ in range(6)]

    def shot_of(t, si):
        a, b = starts[si], ends[si]; dur = max(0.01, b - a)
        ns = max(1, int(round(dur / 2.6))); ln = dur / ns
        k = min(ns - 1, int((t - a) / ln))
        return k, a + k * ln, a + (k + 1) * ln

    def frame(t):
        si = max(i for i, s in enumerate(starts) if s <= t)
        sc = plan[si]; L = layers[sc["name"]]
        k, t0, t1 = shot_of(t, si)
        p = (t - t0) / max(0.01, t1 - t0); p = p * p * (3 - 2 * p)
        dx, dy, z0, z1 = sc.get("move", [0, 0, 1.08, 1.16])
        fx, fy = sc.get("focus", (0.5, 0.6))
        if k == 0:   zz0, zz1, cxn, cyn, ddx, ddy = z0, z1, CW / 2, CH / 2, dx, dy
        elif k % 2:  zz0, zz1, cxn, cyn, ddx, ddy = 1.42, 1.56, fx * CW, fy * CH, 38, 0          # close-up
        else:        zz0, zz1, cxn, cyn, ddx, ddy = 1.30, 1.14, (CW / 2 + fx * CW) / 2, (CH / 2 + fy * CH) / 2, -(dx or 30), 0  # pull back
        fa = flash_a(t)
        z = zz0 + (zz1 - zz0) * p                                                      # smooth zoom, no jolts
        cw, ch = CW / z, CH / z                                                        # float crop size: no pixel rounding = no jitter
        cx0 = min(max(cxn - cw / 2, 0), CW - cw); cy0 = min(max(cyn - ch / 2, 0), CH - ch)
        pan = (p - 0.5) * 2
        img = None
        for name in ("bg", "mid", "glow", "fg"):
            dp = DEPTH[name]
            ox = min(max(cx0 + ddx * pan * dp, 0), CW - cw)
            oy = min(max(cy0 + ddy * pan * dp, 0), CH - ch)
            c = L[name].resize((W, H), Image.BICUBIC, box=(ox, oy, ox + cw, oy + ch))
            if name == "glow":
                fl = 0.72 + 0.2 * np.sin(t * 9) + 0.08 * np.sin(t * 23 + 1)
                c.putalpha(c.getchannel("A").point(lambda v: int(v * fl)))
            img = c if img is None else (img.alpha_composite(c) or img)
        if sc.get("fog", True):                                                         # drifting fog bands
            for fy_, spd, fl_ in ((0.50, 34, 1), (0.70, -22, 0)):
                o = int(t * spd) % fogP
                band = fog_img.crop((o, 0, o + W, 520))
                img.alpha_composite(band, (0, int(H * fy_) - 260))
        dr = ImageDraw.Draw(img, "RGBA")                                                # floating dust / embers
        for mx, my, vx, vy, mr, ph in motes:
            x, y = (mx + vx * t) % W, (my + vy * t) % H
            al = int(70 + 70 * np.sin(t * 1.3 + ph))
            dr.ellipse((x - mr, y - mr, x + mr, y + mr), fill=(235, 238, 255, al))
        if sc.get("rain"):
            ry = H - int(t * 1700) % H
            img.alpha_composite(rain_l.crop((0, ry, W, ry + H)))
        img.alpha_composite(vig)
        if fa > 0.02: img = Image.blend(img, white, min(0.55, fa))
        for a, b, wd, acc in words:
            if a <= t < b:
                wi = word_img(wd, acc); age = t - a
                if age < 0.09:
                    k = 1.22 - 0.22 * age / 0.09
                    wi = wi.resize((int(wi.width * k), int(wi.height * k)), Image.BILINEAR)
                img.alpha_composite(wi, (max(0, (W - wi.width) // 2), int(H * 0.5) - wi.height // 2))
                break
        f = min(1, t / 0.5, (D - t) / 0.6)
        if f < 1: img = Image.blend(black, img, max(0, f))
        arr = np.asarray(img.convert("RGB"), dtype=np.int16) + grain[int(t * FPS) % 6][..., None]   # film grain
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    tmp = f"{HERE}/videos/{sid}.tmp.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", f"{work}/audio.wav",
                           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-maxrate", "6M", "-bufsize", "12M",
                           "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp],
                          stdin=subprocess.PIPE)
    for k in range(int(D * FPS)):
        ff.stdin.write(frame(k / FPS).tobytes())
    ff.stdin.close()
    if ff.wait() != 0: sys.exit("ffmpeg failed")
    os.replace(tmp, f"{HERE}/videos/{sid}.mp4")
    print(f"done: videos/{sid}.mp4  ({D:.1f}s)")


if __name__ == "__main__":
    main()
