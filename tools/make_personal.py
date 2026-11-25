#!/usr/bin/env python3
"""Plantilla editorial de la cuenta PERSONAL (Miguel Fruto): Lora + DM Sans, fondo crema, barra lateral verde.
Uso: python3 -I make_personal.py piezas.json salida_dir"""
import json, subprocess, sys, tempfile
from html import escape
from pathlib import Path

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#F5F1E8;color:#1F2933;font-family:'DM Sans',sans-serif;
position:relative;overflow:hidden;padding:110px 110px 100px 140px;display:flex;flex-direction:column;justify-content:space-between}
body:before{content:'';position:absolute;left:0;top:0;bottom:0;width:36px;background:#0F766E}
.kick{font-family:'Lora',serif;font-style:italic;font-size:34px;color:#0F766E;border-bottom:3px solid #1F2933;padding-bottom:22px}
h1{font-family:'Lora',serif;font-weight:700;font-size:80px;line-height:1.14;letter-spacing:-1px;margin-top:70px}
h1 em{color:#0F766E;font-style:italic;font-weight:600}
h2{font-family:'Lora',serif;font-weight:700;font-size:72px;line-height:1.15;margin-top:30px}
p.body{font-size:44px;line-height:1.45;color:#3E4C59;margin-top:34px}
ol{list-style:none}
ol li{display:flex;gap:34px;align-items:baseline;font-size:41px;line-height:1.3;padding:22px 0;border-top:1px solid rgba(31,41,51,.25)}
ol li b{font-family:'Lora',serif;font-size:46px;color:#0F766E;font-weight:600;min-width:70px}
.num{font-family:'Lora',serif;font-size:260px;font-weight:700;color:#0F766E;line-height:.9;opacity:.9}
.foot{font-family:'Lora',serif;font-style:italic;font-size:34px;color:#52606D;display:flex;justify-content:space-between}
"""

def shell(inner): return f"<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{inner}</body></html>"

def card(p):
    acc = f"<br><em>{escape(p['accent'])}</em>" if p.get("accent") else ""
    items = "".join(f"<li><b>{i+1:02d}</b><span>{escape(t)}</span></li>" for i, t in enumerate(p.get("items", [])))
    return shell(f"<div><div class='kick'>{escape(p.get('kicker',''))}</div><h1>{escape(p['title'])}{acc}</h1></div><ol>{items}</ol><div class='foot'><span>— Miguel Fruto · migfru</span></div>")

def slide(p, i, n, s):
    if i == 0:
        mid = f"<h1 style='font-size:92px'>{escape(s['title'])}</h1>"
    else:
        body = f"<p class='body'>{escape(s['body'])}</p>" if s.get("body") else ""
        mid = f"<div class='num'>{i}</div><h2>{escape(s['title'])}</h2>{body}"
    return shell(f"<div class='kick'>{escape(p.get('kicker',''))}</div><div>{mid}</div><div class='foot'><span>— Miguel Fruto · migfru</span><span>{i+1} / {n}</span></div>")

def shot(html, out):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html); path = f.name
    subprocess.run(["google-chrome","--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--window-size=1080,1350",f"--screenshot={out}",f"file://{path}"],check=True,capture_output=True)
    Path(path).unlink()

def main():
    ps = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    for p in ps:
        if p["kind"] == "card":
            shot(card(p), str(out / f"{p['id']}_imagen.png"))
        else:
            pages = []
            for i, s in enumerate(p["slides"]):
                png = out / f"_{p['id']}_{i}.png"; shot(slide(p, i, len(p["slides"]), s), str(png)); pages.append(Image.open(png).convert("RGB"))
            pages[0].save(out / f"{p['id']}_carrusel.pdf", save_all=True, append_images=pages[1:])
            for i in range(len(p["slides"])): (out / f"_{p['id']}_{i}.png").unlink()
        print("ok", p["id"], flush=True)

if __name__ == "__main__": main()
