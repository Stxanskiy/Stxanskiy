#!/usr/bin/env python3
"""Render README.md the way GitHub does (via its public Markdown API) into preview.html.

    python3 tools/preview.py && open preview.html

The page follows the browser's light/dark setting, like github.com does. preview.html is gitignored.
"""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIO = "DevOps engineer."


def main():
    md = (ROOT / "README.md").read_text(encoding="utf-8")
    req = urllib.request.Request(
        "https://api.github.com/markdown",
        data=json.dumps({"text": md, "mode": "gfm"}).encode(),
        headers={"Accept": "application/vnd.github+json", "Content-Type": "application/json"},
    )
    body = urllib.request.urlopen(req, timeout=30).read().decode()
    user = json.load(urllib.request.urlopen("https://api.github.com/users/Stxanskiy", timeout=30))
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Preview · Stxanskiy profile</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown.min.css">
<style>
 :root {{ --bg:#fff; --fg:#1f2328; --muted:#59636e; --line:#d1d9e0; }}
 @media (prefers-color-scheme: dark) {{ :root {{ --bg:#0d1117; --fg:#f0f6fc; --muted:#9198a1; --line:#3d444d; }} }}
 body {{ margin:0; background:var(--bg); color:var(--fg); font:14px -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif; }}
 .wrap {{ max-width:1280px; margin:0 auto; padding:32px 24px; display:grid; grid-template-columns:296px minmax(0,1fr); gap:24px; }}
 @media (max-width:860px) {{ .wrap {{ grid-template-columns:minmax(0,1fr); }} }}
 .side img {{ width:100%; max-width:296px; border-radius:50%; border:1px solid var(--line); }}
 .side h1 {{ margin:16px 0 0; font-size:24px; line-height:1.25; }} .side .login {{ color:var(--muted); font-size:20px; font-weight:300; }}
 .side .bio {{ margin-top:16px; font-size:16px; }}
 .box {{ border:1px solid var(--line); border-radius:6px; padding:24px; }}
 .box .t {{ font:12px ui-monospace,Menlo,monospace; color:var(--muted); margin-bottom:16px; }}
 .markdown-body {{ background:transparent; }}
</style></head><body><div class="wrap">
<aside class="side"><img src="{user['avatar_url']}" alt=""><h1>Timur</h1><div class="login">Stxanskiy</div><div class="bio">{BIO}</div></aside>
<main><div class="box"><div class="t">Stxanskiy / README.md</div><article class="markdown-body">{body}</article></div></main>
</div></body></html>"""
    (ROOT / "preview.html").write_text(page, encoding="utf-8")
    print("wrote", ROOT / "preview.html")


if __name__ == "__main__":
    main()
