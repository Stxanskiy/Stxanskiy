#!/usr/bin/env python3
"""Generate the animated SVGs for the profile README (light + dark variants).

    python3 tools/build_svgs.py     # writes assets/{hero,card-tot,card-vibibay}-{light,dark}.svg

Plain SVG with CSS/SMIL animation: GitHub shows it as an image, no external services.
Without animation support every image falls back to its finished frame.
"""
import random
from pathlib import Path

NAME = "TIMUR"
ROLE = "DevOps engineer"
WORDS = ["kubernetes", "gitops", "automation", "observability"]

PALETTES = {
    "dark": dict(bg="#0F1623", border="#223047", ink="#E6EDF3", muted="#8B98A9", faint="#26364D",
                 accent="#00ADD8", amber="#F2A541", green="#3FB950", panel="#121C2B", stroke="#2A3B55", term="#0A0F18"),
    "light": dict(bg="#F6F8FA", border="#D0D7DE", ink="#1F2328", muted="#59636E", faint="#D5DDE6",
                  accent="#0086A8", amber="#B86E00", green="#1A7F37", panel="#FFFFFF", stroke="#C9D3DE", term="#FFFFFF"),
}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pct(t, period):
    return f"{t / period * 100:.2f}%"


# ───────────────────────── hero ─────────────────────────

def hero(p):
    W, H, CYCLE = 900, 340, 10.0
    rnd = random.Random(7)  # fixed seed: the same scramble every build
    glyphs = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#$%&@*+=<>/"
    out = []
    a = out.append

    # master clock: everything in the name block restarts every CYCLE seconds
    a(f'<rect width="0" height="0"><animate id="clk" attributeName="x" values="0;0" dur="{CYCLE}s" begin="0s;clk.end"/></rect>')

    a(f'<text x="46" y="82" font-family="{MONO}" font-size="15" fill="{p["muted"]}"><tspan fill="{p["accent"]}">~</tspan> $ whoami</text>')
    size, step, x0, y0 = 96, 62, 44, 186
    for i, ch in enumerate(NAME):
        x = x0 + i * step
        lock = 0.9 + i * 0.22
        t = 0.1
        while t < lock:
            g = rnd.choice(glyphs)
            a(f'<text x="{x}" y="{y0}" font-family="{MONO}" font-size="{size}" font-weight="700" fill="{p["accent"]}" opacity="0">{esc(g)}'
              f'<set attributeName="opacity" to=".9" begin="clk.begin+{t:.2f}s" dur="0.07s"/></text>')
            t += 0.07
        a(f'<text x="{x}" y="{y0}" font-family="{MONO}" font-size="{size}" font-weight="700" fill="{p["ink"]}">{ch}'
          f'<set attributeName="opacity" to="0" begin="clk.begin" dur="{lock:.2f}s"/></text>')
    name_w = len(NAME) * step - 6
    last = 0.9 + (len(NAME) - 1) * 0.22
    a(f'<rect x="{x0 + 2}" y="{y0 + 18}" width="{name_w}" height="4" rx="2" fill="{p["accent"]}">'
      f'<animate attributeName="width" values="0;0;{name_w};{name_w}" keyTimes="0;{last / CYCLE:.3f};{(last + .45) / CYCLE:.3f};1" dur="{CYCLE}s" begin="clk.begin"/></rect>')

    ty = 254
    a(f'<text x="46" y="{ty}" font-family="{MONO}" font-size="20" font-weight="700" fill="{p["ink"]}">{ROLE}<tspan fill="{p["muted"]}" font-weight="400"> /</tspan></text>')
    wx = 46 + (len(ROLE) + 2) * 12 + 12
    slot = CYCLE / len(WORDS)
    for k, word in enumerate(WORDS):
        if k == 0:
            a(f'<text x="{wx}" y="{ty}" font-family="{MONO}" font-size="20" fill="{p["accent"]}">{word}'
              f'<set attributeName="opacity" to="0" begin="clk.begin+{slot:.2f}s" dur="{CYCLE - slot:.2f}s"/></text>')
        else:
            a(f'<text x="{wx}" y="{ty}" font-family="{MONO}" font-size="20" fill="{p["accent"]}" opacity="0">{word}'
              f'<set attributeName="opacity" to="1" begin="clk.begin+{k * slot:.2f}s" dur="{slot:.2f}s"/></text>')

    # cluster panel with a looping rolling update (CSS)
    P = 12.0
    css = []
    px, py, pw, ph = 500, 34, 366, 272
    a(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{p["panel"]}" stroke="{p["stroke"]}"/>')
    a(f'<text x="{px + 16}" y="{py + 28}" font-family="{MONO}" font-size="12.5" fill="{p["ink"]}">deployment/<tspan font-weight="700">timur</tspan></text>')
    css.append(f"@keyframes st-roll {{ 0% {{ opacity: 0; }} {pct(.8, P)} {{ opacity: 0; }} {pct(.81, P)} {{ opacity: 1; }} {pct(5.6, P)} {{ opacity: 1; }} {pct(5.61, P)} {{ opacity: 0; }} "
               f"{pct(6.8, P)} {{ opacity: 0; }} {pct(6.81, P)} {{ opacity: 1; }} {pct(11.6, P)} {{ opacity: 1; }} {pct(11.61, P)} {{ opacity: 0; }} 100% {{ opacity: 0; }} }}")
    css.append(f"@keyframes st-ready {{ 0% {{ opacity: 1; }} {pct(.8, P)} {{ opacity: 1; }} {pct(.81, P)} {{ opacity: 0; }} {pct(5.6, P)} {{ opacity: 0; }} {pct(5.61, P)} {{ opacity: 1; }} "
               f"{pct(6.8, P)} {{ opacity: 1; }} {pct(6.81, P)} {{ opacity: 0; }} {pct(11.6, P)} {{ opacity: 0; }} {pct(11.61, P)} {{ opacity: 1; }} 100% {{ opacity: 1; }} }}")
    css.append(f".st-roll {{ animation: st-roll {P}s linear infinite; opacity: 0; }} .st-ready {{ animation: st-ready {P}s linear infinite; }}")
    a(f'<text class="st-roll" x="{px + pw - 16}" y="{py + 28}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{p["amber"]}">● rolling update</text>')
    a(f'<text class="st-ready" x="{px + pw - 16}" y="{py + 28}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{p["green"]}">● 9/9 ready</text>')
    a(f'<rect x="{px + 16}" y="{py + 40}" width="{pw - 32}" height="3" rx="1.5" fill="{p["faint"]}"/>')
    css.append(f"@keyframes prog {{ 0% {{ transform: scaleX(1); }} {pct(.8, P)} {{ transform: scaleX(0); }} {pct(5.3, P)} {{ transform: scaleX(1); }} "
               f"{pct(6.8, P)} {{ transform: scaleX(1); }} {pct(6.81, P)} {{ transform: scaleX(0); }} {pct(11.3, P)} {{ transform: scaleX(1); }} 100% {{ transform: scaleX(1); }} }}")
    css.append(f".prog {{ transform-box: fill-box; transform-origin: left center; animation: prog {P}s steps(9, end) infinite; }}")
    a(f'<rect class="prog" x="{px + 16}" y="{py + 40}" width="{pw - 32}" height="3" rx="1.5" fill="{p["accent"]}"/>')

    nodes_x = [px + 16 + n * 118 for n in range(3)]
    pods, order = {}, 0
    for row in range(3):
        for n in range(3):
            pods[(n, row)] = order
            order += 1
    for n, nx in enumerate(nodes_x):
        a(f'<rect x="{nx}" y="{py + 58}" width="102" height="196" rx="10" fill="none" stroke="{p["stroke"]}" stroke-dasharray="3 4"/>')
        a(f'<text x="{nx + 51}" y="{py + 244}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{p["muted"]}">node-{n + 1}</text>')
        for row in range(3):
            k = pods[(n, row)]
            cx, cy = nx + 51, py + 96 + row * 50
            pts = " ".join(f"{cx + 20 * c:.1f},{cy + 20 * s:.1f}" for c, s in [(0.866, 0.5), (0, 1), (-0.866, 0.5), (-0.866, -0.5), (0, -1), (0.866, -0.5)])
            t1, t2 = 0.8 + k * 0.5, 6.8 + k * 0.5
            frames = [f"0% {{ fill: {p['accent']}; transform: scale(1); opacity: 1; }}"]
            for t, to in [(t1, p["green"]), (t2, p["accent"])]:
                frm = p["accent"] if to == p["green"] else p["green"]
                frames += [f"{pct(t, P)} {{ fill: {frm}; transform: scale(1); opacity: 1; }}",
                           f"{pct(t + .12, P)} {{ fill: {frm}; transform: scale(.35); opacity: .25; }}",
                           f"{pct(t + .26, P)} {{ fill: {to}; transform: scale(1.15); opacity: 1; }}",
                           f"{pct(t + .38, P)} {{ fill: {to}; transform: scale(1); opacity: 1; }}"]
            frames.append(f"100% {{ fill: {p['accent']}; transform: scale(1); opacity: 1; }}")
            css.append(f"@keyframes pod{k} {{ {' '.join(frames)} }}")
            css.append(f".pod{k} {{ transform-box: fill-box; transform-origin: center; animation: pod{k} {P}s ease-in-out infinite; }}")
            a(f'<polygon class="pod{k}" points="{pts}" fill="{p["accent"]}"/>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME}, {ROLE}. A Kubernetes deployment rolls out pod by pod next to the name.">
  <style>
    {(chr(10) + '    ').join(css)}
    {REDUCED}
  </style>
  <defs>
    <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="{p["faint"]}"/></pattern>
    <radialGradient id="glow" cx="25%" cy="45%" r="60%"><stop offset="0" stop-color="{p["accent"]}" stop-opacity=".16"/><stop offset="1" stop-color="{p["accent"]}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="{p["bg"]}" stroke="{p["border"]}"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#grid)"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#glow)"/>
  {(chr(10) + '  ').join(out)}
</svg>
"""


# ───────────────────────── cards ─────────────────────────

def card_frame(p, title, url, subtitle, W=440, H=250):
    return [
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{p["bg"]}" stroke="{p["border"]}"/>',
        f'<text x="26" y="58" font-family="{SANS}" font-size="38" font-weight="800" letter-spacing="-.5" fill="{p["ink"]}">{esc(title)}</text>',
        f'<text x="{W - 24}" y="44" text-anchor="end" font-family="{MONO}" font-size="12.5" fill="{p["accent"]}">{esc(url)} ↗</text>',
        f'<text x="27" y="86" font-family="{SANS}" font-size="15" fill="{p["muted"]}">{esc(subtitle)}</text>',
    ]


def card_tot(p):
    W, H, P = 440, 250, 9.0
    out = card_frame(p, "TOT", "learn.prod-factory.ru", "learn DevOps in a real terminal")
    css = []
    tx, ty, tw, th = 22, 106, 396, 124
    out.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="10" fill="{p["term"]}" stroke="{p["stroke"]}"/>')
    out.append(f'<path d="M{tx},{ty + 26} H{tx + tw}" stroke="{p["stroke"]}"/>')
    out.append(f'<text x="{tx + 14}" y="{ty + 17}" font-family="{MONO}" font-size="11" fill="{p["muted"]}">student@tot: ~</text>')
    lines = [("cmd", "tot --version", .4, .9), ("out", "tot 1.0.0", 1.6, 0), ("cmd", "ls ~/directions", 2.6, 1.0), ("hi", "frontend   backend   infra", 3.9, 0)]
    fs, cw = 13, 13 * .6
    covers = []
    for i, (kind, text, t, dur) in enumerate(lines):
        y = ty + 50 + i * 21
        css.append(f"@keyframes tl{i} {{ 0%, {pct(t - .01, P)} {{ opacity: 0; }} {pct(t, P)}, {pct(8.3, P)} {{ opacity: 1; }} 100% {{ opacity: 0; }} }} .tl{i} {{ animation: tl{i} {P}s linear infinite; }}")
        if kind == "cmd":
            out.append(f'<g class="tl{i}"><text x="{tx + 14}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{p["accent"]}">$</text>'
                       f'<text x="{tx + 30}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{p["ink"]}">{esc(text)}</text></g>')
            w = len(text) * cw + 10
            css.append(f"@keyframes tc{i} {{ 0%, {pct(t, P)} {{ transform: translateX(0); }} {pct(t + dur, P)}, 100% {{ transform: translateX({w:.0f}px); }} }} .tc{i} {{ animation: tc{i} {P}s steps({len(text)}) infinite; }}")
            covers.append(f'<rect class="cover tc{i}" x="{tx + 29}" y="{y - fs}" width="{w:.0f}" height="{fs + 6}" fill="{p["term"]}"/>')
        else:
            col = p["green"] if kind == "hi" else p["muted"]
            out.append(f'<text class="tl{i}" x="{tx + 14}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{col}" xml:space="preserve">{esc(text)}</text>')
    out.append(f'<g clip-path="url(#tclip)">{"".join(covers)}</g>')
    css.append("@keyframes blink { 50% { opacity: 0; } } .cur { animation: blink 1s steps(1) infinite; }")
    css.append("@media (prefers-reduced-motion: reduce) { .cover { display: none; } }")
    last_text, last_y = lines[-1][1], ty + 50 + 3 * 21
    out.append(f'<rect class="cur" x="{tx + 14 + len(last_text) * cw + 6:.0f}" y="{last_y - fs + 2}" width="8" height="{fs + 1}" fill="{p["accent"]}"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="TOT, learn DevOps in a real terminal. learn.prod-factory.ru">
  <style>
    {(chr(10) + '    ').join(css)}
    {REDUCED}
  </style>
  <defs><clipPath id="tclip"><rect x="{tx + 1}" y="{ty + 27}" width="{tw - 2}" height="{th - 28}"/></clipPath></defs>
  {(chr(10) + '  ').join(out)}
</svg>
"""


def card_vibibay(p):
    W, H = 440, 250
    out = card_frame(p, "ViBiBAY", "vibibay.com", "built and run end to end")
    css = []
    cx, cy, r = 318, 160, 74
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 16}" fill="{p["accent"]}" opacity=".06"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{p["panel"]}" stroke="{p["stroke"]}" stroke-width="1.5"/>')
    g = []
    for dy in (-48, -24, 0, 24, 48):
        rx = (r * r - dy * dy) ** .5
        g.append(f'<ellipse cx="{cx}" cy="{cy + dy}" rx="{rx:.1f}" ry="{max(3, 9 - abs(dy) / 8):.1f}" fill="none" stroke="{p["faint"]}"/>')
    css.append("@keyframes spin { 0% { transform: scaleX(1); } 50% { transform: scaleX(-1); } 100% { transform: scaleX(1); } }")
    for i in range(5):
        css.append(f".m{i} {{ transform-box: view-box; transform-origin: {cx}px {cy}px; animation: spin 7s linear infinite; animation-delay: -{i * 1.4:.1f}s; }}")
        g.append(f'<ellipse class="m{i}" cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="none" stroke="{p["accent"]}" stroke-opacity=".45"/>')
    out.append(f'<g clip-path="url(#globe)">{"".join(g)}</g>')
    dots = [(-38, -30), (24, -44), (46, 6), (-12, 22), (-44, 26), (20, 44)]
    links = [(0, 1), (1, 2), (2, 5), (3, 4), (0, 3), (3, 2)]
    css.append("@keyframes pkt { to { stroke-dashoffset: -28; } } .lnk { stroke-dasharray: 6 8; animation: pkt 1.1s linear infinite; }")
    for a_, b_ in links:
        (x1, y1), (x2, y2) = dots[a_], dots[b_]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        out.append(f'<path class="lnk" d="M{cx + x1},{cy + y1} Q{cx + mx * 1.25:.0f},{cy + my * 1.25 - 18:.0f} {cx + x2},{cy + y2}" fill="none" stroke="{p["accent"]}" stroke-width="1.6"/>')
    css.append("@keyframes led { 0%, 100% { opacity: .35; } 50% { opacity: 1; } }")
    for i, (dx, dy) in enumerate(dots):
        css.append(f".d{i} {{ animation: led 2s ease-in-out infinite; animation-delay: {i * .33:.2f}s; }}")
        out.append(f'<circle class="d{i}" cx="{cx + dx}" cy="{cy + dy}" r="4.5" fill="{p["amber"]}"/>')
    # a calm heartbeat line on the left, purely decorative
    css.append("@keyframes beat { to { stroke-dashoffset: -260; } } .beat { stroke-dasharray: 130 130; animation: beat 2.6s linear infinite; }")
    pulse = "M26,190 H70 l8,-22 l10,40 l8,-30 l6,12 H190"
    out.append(f'<path d="{pulse}" fill="none" stroke="{p["faint"]}" stroke-width="2"/>')
    out.append(f'<path class="beat" d="{pulse}" fill="none" stroke="{p["green"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="ViBiBAY, built and run end to end. vibibay.com">
  <style>
    {(chr(10) + '    ').join(css)}
    {REDUCED}
  </style>
  <defs><clipPath id="globe"><circle cx="{cx}" cy="{cy}" r="{r - 1}"/></clipPath></defs>
  {(chr(10) + '  ').join(out)}
</svg>
"""


def main():
    root = Path(__file__).resolve().parent.parent / "assets"
    root.mkdir(exist_ok=True)
    for old in root.glob("*.svg"):
        old.unlink()
    for theme, p in PALETTES.items():
        (root / f"hero-{theme}.svg").write_text(hero(p), encoding="utf-8")
        (root / f"card-tot-{theme}.svg").write_text(card_tot(p), encoding="utf-8")
        (root / f"card-vibibay-{theme}.svg").write_text(card_vibibay(p), encoding="utf-8")
    print("wrote", ", ".join(sorted(f.name for f in root.glob("*.svg"))))


if __name__ == "__main__":
    main()
