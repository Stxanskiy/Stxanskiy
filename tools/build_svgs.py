#!/usr/bin/env python3
"""Generate the animated SVGs for the profile README (light + dark variants).

    python3 tools/build_svgs.py        # writes assets/{header,tot-lab}-{light,dark}.svg

Everything is plain SVG with CSS/SMIL animation, so GitHub renders it as an image
with no external services. Edit the text constants / PALETTES below and rerun.
"""
from pathlib import Path

NAME = "Timur"
TAGLINE = "DevOps engineer · Kubernetes · GitOps"
SUBLINE = "Clusters, pipelines, alerts — and the Go services that run on them."
PROMPT_PATH = "~/stxanskiy"
HUB = "k8s"
SATELLITES = [((598, 62), "argocd"), ((812, 52), "vault"), ((860, 140), "linux"),
              ((806, 206), "prometheus"), ((620, 200), "docker"), ((556, 128), "ci")]

PALETTES = {
    "dark": dict(bg="#0F1623", border="#223047", ink="#E6EDF3", muted="#8B98A9", faint="#2A3A52",
                 accent="#00ADD8", amber="#F2A541", green="#3FB950", box="#142033", box_stroke="#2A3B55",
                 chip="#17243A", term="#0A0F18"),
    "light": dict(bg="#F6F8FA", border="#D0D7DE", ink="#1F2328", muted="#59636E", faint="#D5DDE6",
                  accent="#0086A8", amber="#B86E00", green="#1A7F37", box="#FFFFFF", box_stroke="#C9D3DE",
                  chip="#EEF2F6", term="#FFFFFF"),
}
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def typing(x, y, text, size, color, delay=0.5, per_char=0.05):
    """Text revealed letter by letter via a discrete clip animation, plus a blinking cursor.
    Without SMIL support the base attributes show the full text."""
    cw = size * 0.6
    n = len(text)
    full = n * cw + 2
    dur = delay + n * per_char + 0.05
    times = [0.0] + [delay + i * per_char for i in range(n + 1)] + [dur]
    widths = [0.0] + [i * cw for i in range(n + 1)] + [full]
    kt = ";".join(f"{t / dur:.4f}" for t in times)
    vw = ";".join(f"{w:.1f}" for w in widths)
    vx = ";".join(f"{x + w + 2:.1f}" for w in widths)
    return f"""
  <clipPath id="typeclip"><rect x="{x}" y="{y - size}" width="{full:.1f}" height="{size * 1.5:.0f}">
    <animate attributeName="width" values="{vw}" keyTimes="{kt}" dur="{dur:.2f}s" calcMode="discrete" fill="freeze"/>
  </rect></clipPath>
  <text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{color}" clip-path="url(#typeclip)">{esc(text)}</text>
  <rect x="{x + full + 2:.1f}" y="{y - size + 3}" width="{size * 0.55:.1f}" height="{size + 1}" fill="{color}" opacity=".85">
    <animate attributeName="x" values="{vx}" keyTimes="{kt}" dur="{dur:.2f}s" calcMode="discrete" fill="freeze"/>
    <animate attributeName="opacity" values=".85;0" dur="1.05s" calcMode="discrete" repeatCount="indefinite"/>
  </rect>""", dur


def header(p):
    W, H = 900, 250
    hub = (712, 128)
    net = []
    for i, ((x, y), _) in enumerate(SATELLITES):
        d = f"M{hub[0]},{hub[1]} L{x},{y}" if i % 2 == 0 else f"M{x},{y} L{hub[0]},{hub[1]}"
        net.append(f'<path d="{d}" stroke="{p["faint"]}" stroke-width="1.5" fill="none"/>')
        net.append(f'<path d="{d}" class="pkt" style="animation-delay:-{i * 0.37:.2f}s" stroke="{p["accent"]}" stroke-width="2" fill="none"/>')
    for (x, y), label in SATELLITES:
        net.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{p["bg"]}" stroke="{p["accent"]}" stroke-width="2"/>')
        dy = -12 if y <= hub[1] else 22
        anchor = "end" if x + len(label) * 3.2 > W - 8 else "middle"
        lx = x + 8 if anchor == "end" else x
        net.append(f'<text x="{lx}" y="{y + dy}" text-anchor="{anchor}" font-family="{MONO}" font-size="10.5" fill="{p["muted"]}">{label}</text>')
    net.append(f'<circle cx="{hub[0]}" cy="{hub[1]}" r="12" fill="{p["accent"]}" class="ring"/>')
    net.append(f'<circle cx="{hub[0]}" cy="{hub[1]}" r="12" fill="{p["accent"]}"/>')
    net.append(f'<text x="{hub[0]}" y="{hub[1] + 4}" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="{p["bg"]}">{HUB}</text>')
    typed, tdur = typing(40, 164, TAGLINE, 19, p["accent"])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME}, {esc(TAGLINE)}. {esc(SUBLINE)}">
  <style>
    .pkt {{ stroke-dasharray: 8 140; animation: run 2.2s linear infinite; }}
    @keyframes run {{ from {{ stroke-dashoffset: 148; }} to {{ stroke-dashoffset: 0; }} }}
    .ring {{ transform-origin: {hub[0]}px {hub[1]}px; animation: ring 2.4s ease-out infinite; }}
    @keyframes ring {{ from {{ transform: scale(1); opacity: .5; }} to {{ transform: scale(2.6); opacity: 0; }} }}
    {REDUCED}
  </style>
  <defs>
    <pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="{p["faint"]}"/></pattern>
    <linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{p["bg"]}" stop-opacity="1"/><stop offset=".55" stop-color="{p["bg"]}" stop-opacity="0"/></linearGradient>
  </defs>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{p["bg"]}" stroke="{p["border"]}"/>
  <rect x="480" y="1" width="{W - 481}" height="{H - 2}" fill="url(#dots)"/>
  <rect x="480" y="1" width="{W - 481}" height="{H - 2}" fill="url(#fade)"/>
  {''.join(net)}
  <text x="40" y="62" font-family="{MONO}" font-size="15" fill="{p["muted"]}"><tspan fill="{p["accent"]}">{PROMPT_PATH}</tspan> $ whoami</text>
  <text x="38" y="124" font-family="{SANS}" font-size="58" font-weight="700" fill="{p["ink"]}" letter-spacing="-1">{NAME}</text>
  {typed}
  <text x="40" y="208" font-family="{SANS}" font-size="16" fill="{p["muted"]}">{esc(SUBLINE)}
    <animate attributeName="opacity" values="0;0;1" keyTimes="0;.8;1" dur="{tdur + 0.6:.2f}s" fill="freeze"/>
  </text>
</svg>
"""


# A real TOT lab (GoLearn backend): "Kubernetes › Lab 2: Deployment" (cmd/seed/labs_k8s_intro.go, ch-k8si-lab2).
LAB_TITLE = "Kubernetes › Lab 2: Deployment"
LAB_LINES = [  # (kind, text, start second, typing seconds)
    ("cmd", "kubectl create deployment nginx-deploy --image=nginx:alpine --replicas=2", 0.4, 1.8),
    ("out", "deployment.apps/nginx-deploy created", 2.5, 0),
    ("cmd", "kubectl rollout status deployment/nginx-deploy", 3.3, 1.3),
    ("dim", 'Waiting for deployment "nginx-deploy" rollout to finish: 1 of 2 updated replicas are available...', 4.9, 0),
    ("ok", 'deployment "nginx-deploy" successfully rolled out', 6.2, 0),
    ("cmd", "kubectl scale deployment nginx-deploy --replicas=1", 7.1, 1.3),
    ("out", "deployment.apps/nginx-deploy scaled", 8.7, 0),
]
LAB_CHECKS = [("Deployment created with 2 replicas", 2.8), ("both replicas are ready", 6.5), ("scaled down to 1 replica", 9.0)]
LAB_DONE = 9.6
LAB_HOW = ["Go API starts a sandbox per student", "Firecracker micro-VM, no network", "k3s, Docker, Linux baked into images", "each task: shell probe, exit 0 = solved"]
LOOP = 14.0
HIDE = 13.2


def lab(p):
    W, H = 900, 410
    fs, cw = 12.5, 12.5 * 0.6
    css, body = [], []

    def appear(name, t):
        a, b = t / LOOP * 100, HIDE / LOOP * 100
        css.append(f"@keyframes {name} {{ 0%, {a - 0.01:.2f}% {{ opacity: 0; }} {a:.2f}%, {b:.2f}% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}")
        css.append(f".{name} {{ animation: {name} {LOOP}s linear infinite; }}")

    def typed(name, t, dur, n, width):
        a, b = t / LOOP * 100, (t + dur) / LOOP * 100
        css.append(f"@keyframes {name} {{ 0%, {a:.2f}% {{ transform: translateX(0); }} {b:.2f}%, 100% {{ transform: translateX({width:.0f}px); }} }}")
        css.append(f".{name} {{ animation: {name} {LOOP}s steps({n}) infinite; }}")

    # terminal
    tx, ty, tw, th = 20, 20, 860, 226
    body.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{p["term"]}"/>')
    body.append(f'<path d="M{tx},{ty + 34} H{tx + tw}" stroke="{p["box_stroke"]}"/>')
    body.append(f'<text x="{tx + 16}" y="{ty + 22}" font-family="{MONO}" font-size="12" fill="{p["muted"]}"><tspan fill="{p["ink"]}" font-weight="700">tot</tspan>  ·  {esc(LAB_TITLE)}</text>')
    body.append(f'<circle cx="{tx + tw - 112}" cy="{ty + 18}" r="4" fill="{p["green"]}" class="live"/>')
    body.append(f'<text x="{tx + tw - 102}" y="{ty + 22}" font-family="{MONO}" font-size="12" fill="{p["muted"]}">sandbox up</text>')
    covers = []
    for i, (kind, text, t, dur) in enumerate(LAB_LINES):
        y = ty + 60 + i * 24
        name = f"l{i}"
        appear(name, t)
        color = {"cmd": p["ink"], "out": p["muted"], "dim": p["muted"], "ok": p["green"]}[kind]
        if kind == "cmd":
            body.append(f'<g class="{name}"><text x="{tx + 16}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{p["accent"]}">$</text>'
                        f'<text x="{tx + 32}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{color}">{esc(text)}</text></g>')
            width = len(text) * cw + 12
            typed(f"c{i}", t, dur, len(text), width)
            covers.append(f'<rect class="cover c{i}" x="{tx + 31}" y="{y - fs - 1}" width="{width:.0f}" height="{fs + 8}" fill="{p["term"]}"/>')
        else:
            opacity = ' opacity=".75"' if kind == "dim" else ""
            body.append(f'<text class="{name}" x="{tx + 16}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{color}"{opacity}>{esc(text)}</text>')
    body.append(f'<g clip-path="url(#termbody)">{"".join(covers)}</g>')
    body.append(f'<rect x="{tx + .5}" y="{ty + .5}" width="{tw - 1}" height="{th - 1}" rx="12" fill="none" stroke="{p["box_stroke"]}"/>')

    # checks panel
    cx, cy, cwid, ch = 20, 262, 520, 130
    body.append(f'<rect x="{cx}" y="{cy}" width="{cwid}" height="{ch}" rx="12" fill="{p["box"]}" stroke="{p["box_stroke"]}"/>')
    body.append(f'<text x="{cx + 16}" y="{cy + 26}" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{p["muted"]}">AUTO-CHECKS</text>')
    appear("done", LAB_DONE)
    body.append(f'<g class="done"><rect x="{cx + cwid - 150}" y="{cy + 12}" width="134" height="22" rx="11" fill="{p["green"]}" fill-opacity=".15" stroke="{p["green"]}"/>'
                f'<text x="{cx + cwid - 83}" y="{cy + 27}" text-anchor="middle" font-family="{MONO}" font-size="11.5" font-weight="700" fill="{p["green"]}">lab complete 3/3</text></g>')
    for i, (label, t) in enumerate(LAB_CHECKS):
        y = cy + 58 + i * 26
        appear(f"k{i}", t)
        body.append(f'<circle cx="{cx + 26}" cy="{y - 4}" r="7" fill="none" stroke="{p["faint"]}" stroke-width="1.5"/>')
        body.append(f'<g class="k{i}"><circle cx="{cx + 26}" cy="{y - 4}" r="8" fill="{p["green"]}"/>'
                    f'<path d="M{cx + 22},{y - 4} l3,3 l5,-6" fill="none" stroke="{p["box"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
        body.append(f'<text x="{cx + 44}" y="{y}" font-family="{SANS}" font-size="14" fill="{p["ink"]}">{esc(label)}</text>')

    # how it runs
    hx, hw = 556, 324
    body.append(f'<rect x="{hx}" y="{cy}" width="{hw}" height="{ch}" rx="12" fill="{p["box"]}" stroke="{p["box_stroke"]}"/>')
    body.append(f'<text x="{hx + 16}" y="{cy + 26}" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{p["muted"]}">HOW A LAB RUNS</text>')
    for i, line in enumerate(LAB_HOW):
        body.append(f'<text x="{hx + 16}" y="{cy + 54 + i * 22}" font-family="{MONO}" font-size="11.5" fill="{p["ink"]}"><tspan fill="{p["accent"]}">{i + 1} </tspan>{esc(line)}</text>')

    css.append(".live { animation: live 1.6s ease-in-out infinite; } @keyframes live { 50% { opacity: .25; } }")
    css.append("@media (prefers-reduced-motion: reduce) { .cover { display: none; } }")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="A TOT lab in action: a student creates a Kubernetes Deployment, waits for the rollout and scales it down; three automatic checks turn green and the lab is complete. Each student works in their own Firecracker micro-VM without network access.">
  <style>
    {chr(10).join('    ' + c for c in css).strip()}
    {REDUCED}
  </style>
  <defs><clipPath id="termbody"><rect x="21" y="55" width="858" height="190"/></clipPath></defs>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{p["bg"]}" stroke="{p["border"]}"/>
  {chr(10).join('  ' + b for b in body).strip()}
</svg>
"""


def main():
    root = Path(__file__).resolve().parent.parent / "assets"
    root.mkdir(exist_ok=True)
    for pattern in ("stack-map-*.svg", "golearn-lab-*.svg"):
        for old in root.glob(pattern):
            old.unlink()
    for theme, p in PALETTES.items():
        (root / f"header-{theme}.svg").write_text(header(p), encoding="utf-8")
        (root / f"tot-lab-{theme}.svg").write_text(lab(p), encoding="utf-8")
    print("wrote", ", ".join(sorted(f.name for f in root.glob("*.svg"))))


if __name__ == "__main__":
    main()
