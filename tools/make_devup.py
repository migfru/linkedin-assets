#!/usr/bin/env python3
"""Genera tarjetas PNG 1080x1350 y PDFs de carrusel a partir de un JSON de piezas.

Uso: python3 -I make_cards.py piezas.json salida_dir
Cada pieza: {"id": "L-002", "kind": "card"|"carousel", "kicker": str, "title": str,
             "accent": str (parte final del título en azul), "items": [str], "slides": [{"title":..,"body":..}]}
"""
import json
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

THEMES = {
 "devup": dict(bg="#0A1628", fg="#FFFFFF", top="#90CAF9", acc="#1E88E5", body="#E3F2FD", line="rgba(144,202,249,.25)", foot="#90CAF9", sign="DevUp Consulting"),
 "personal": dict(bg="#F5F1E8", fg="#1F2933", top="#0F766E", acc="#0F766E", body="#3E4C59", line="rgba(31,41,51,.18)", foot="#52606D", sign="Miguel Fruto · migfru"),
}
TH = THEMES["devup"]

BASE_CSS_T = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:__bg__;font-family:'Inter',sans-serif;color:__fg__;
padding:100px 90px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}
.top{font-size:30px;letter-spacing:4px;color:__top__;text-transform:uppercase;font-weight:600}
h1{font-size:88px;line-height:1.08;font-weight:800;letter-spacing:-2px}
h1 span{color:__acc__}
h2{font-size:78px;line-height:1.1;font-weight:800;letter-spacing:-1.5px}
p.body{font-size:46px;line-height:1.35;color:__body__;margin-top:30px}
ul{list-style:none}
li{font-size:42px;padding:24px 0;border-top:2px solid __line__}
.foot{font-size:32px;color:__foot__;font-weight:500;display:flex;justify-content:space-between}
.num{font-size:200px;font-weight:800;color:__acc__;line-height:1}
"""


def css():
    t = BASE_CSS_T
    for k in ("bg","fg","top","acc","body","line","foot"):
        t = t.replace(f"__{k}__", TH[k])
    return t


def card_html(p):
    items = "".join(f"<li>{escape(i)}</li>" for i in p.get("items", []))
    accent = f"<br><span>{escape(p['accent'])}</span>" if p.get("accent") else ""
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>{css()}</style></head><body>
<div class="top">{escape(p.get('kicker',''))}</div>
<div><h1>{escape(p['title'])}{accent}</h1></div>
<ul>{items}</ul>
<div class="foot"><span>{TH['sign']}</span></div></body></html>"""


def slide_html(p, idx, total, s):
    first = idx == 0
    head = f"<h1>{escape(s['title'])}</h1>" if first else f"<div class='num'>{idx}</div><h2>{escape(s['title'])}</h2>"
    body = f"<p class='body'>{escape(s['body'])}</p>" if s.get("body") else ""
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>{css()}</style></head><body>
<div class="top">{escape(p.get('kicker',''))}</div>
<div>{head}{body}</div>
<div class="foot"><span>{TH['sign']}</span><span>{idx + 1}/{total}</span></div></body></html>"""


def shot(html, out_png):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        path = f.name
    subprocess.run(["google-chrome", "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--window-size=1080,1350", f"--screenshot={out_png}", f"file://{path}"],
                   check=True, capture_output=True)
    Path(path).unlink()


def main():
    global TH
    TH = THEMES[sys.argv[3]]
    piezas = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    for p in piezas:
        if p["kind"] == "card":
            shot(card_html(p), str(out / f"{p['id']}_imagen.png"))
        elif p["kind"] == "carousel":
            pages = []
            slides = p["slides"]
            for i, s in enumerate(slides):
                png = out / f"_{p['id']}_{i}.png"
                shot(slide_html(p, i, len(slides), s), str(png))
                pages.append(Image.open(png).convert("RGB"))
            pages[0].save(out / f"{p['id']}_carrusel.pdf", save_all=True, append_images=pages[1:])
            for i in range(len(slides)):
                (out / f"_{p['id']}_{i}.png").unlink()
        print("ok", p["id"], flush=True)


if __name__ == "__main__":
    main()
