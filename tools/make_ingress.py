#!/usr/bin/env python3
"""Carrusel L-046: guia de decision para reemplazar ingress-nginx. Tema editorial personal (Lora + DM Sans, crema/verde).
Uso: python3 -I make_ingress.py salida_dir"""
import subprocess, sys, tempfile
from html import escape as E
from pathlib import Path
from PIL import Image

AV = "/home/claude/li/src/avatar/avatar_caja_crop.png"
N = 9
KICK = "ingress-nginx · guía de decisión"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#F5F1E8;color:#1F2933;font-family:'DM Sans',sans-serif;position:relative;overflow:hidden;
padding:100px 100px 90px 140px;display:flex;flex-direction:column;justify-content:space-between}
body:before{content:'';position:absolute;left:0;top:0;bottom:0;width:36px;background:#0F766E}
.kick{font-family:'Lora',serif;font-style:italic;font-size:32px;color:#0F766E;border-bottom:3px solid #1F2933;padding-bottom:20px}
h1{font-family:'Lora',serif;font-weight:700;font-size:90px;line-height:1.12;letter-spacing:-1px}
h1 em{color:#0F766E;font-style:italic;font-weight:600}
h2{font-family:'Lora',serif;font-weight:700;font-size:64px;line-height:1.14;margin:34px 0 26px}
.sub{font-size:38px;line-height:1.4;color:#3E4C59}
.foot{font-family:'Lora',serif;font-style:italic;font-size:30px;color:#52606D;display:flex;justify-content:space-between}
.src{font-size:27px;line-height:1.35;color:#52606D;margin-top:22px}
ul.l{list-style:none}
ul.l li{font-size:36px;line-height:1.32;padding:20px 0 20px 40px;border-top:1px solid rgba(31,41,51,.25);position:relative;color:#1F2933}
ul.l li:before{content:'';position:absolute;left:0;top:34px;width:16px;height:16px;background:#0F766E}
ul.l li b{font-weight:700}
.row{display:flex;gap:28px;align-items:baseline;border-top:1px solid rgba(31,41,51,.25);padding:20px 0}
.row .n{font-family:'Lora',serif;font-size:46px;color:#0F766E;font-weight:600;min-width:64px}
.row .t{font-size:35px;line-height:1.32}
.row .t b{display:block;font-family:'Lora',serif;font-size:40px;margin-bottom:4px}
table{width:100%;border-collapse:collapse}
td{vertical-align:top;padding:11px 0;border-top:1px solid rgba(31,41,51,.25);font-size:31px;line-height:1.26}
td.a{width:44%;color:#3E4C59;padding-right:24px}
td.b{font-weight:700;color:#0F766E}
td.b span{display:block;font-weight:400;font-size:27px;color:#52606D;margin-top:4px}
.bar{height:62px;display:flex;align-items:center;padding-left:22px;color:#fff;font-weight:700;font-size:34px}
.lab{font-size:30px;color:#3E4C59;margin:22px 0 8px}
.av{position:absolute;right:50px;bottom:140px}
"""

def shell(inner):
    return f"<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><style>{CSS}</style></head><body>{inner}</body></html>"

def foot(i):
    return f"<div class='foot'><span>— Miguel Fruto · migfru</span><span>{i} / {N}</span></div>"

def kick(): return f"<div class='kick'>{E(KICK)}</div>"

def s1():
    return shell(f"{kick()}<div><h1>¿Qué reemplaza a ingress-nginx?<br><em>Depende de lo que ya tengas.</em></h1>"
        f"<p class='sub' style='margin-top:44px;max-width:640px'>Documentación oficial y casos reales de CERN, Boeing, Zapier y Qovery.</p></div>"
        f"<img class='av' src='file://{AV}' width='330'>{foot(1)}")

def s2():
    return shell(f"{kick()}<div><h2>Qué se retiró, y qué no</h2><ul class='l'>"
        "<li>Se retiró el <b>controlador</b> ingress-nginx del proyecto Kubernetes, en marzo de 2026: sin versiones ni parches de seguridad.</li>"
        "<li>El <b>proxy NGINX</b> no se retiró. Hay otras implementaciones basadas en NGINX, como NGINX Gateway Fabric.</li>"
        "<li>Kubernetes lo describió como pieza crítica de cerca de la mitad de los entornos cloud native.</li>"
        "<li>En AKS, Microsoft indica que el add-on NGINX administrado deja de tener soporte de Azure después de noviembre de 2026.</li></ul>"
        "<p class='src'>Fuentes: Kubernetes (29 ene 2026) y Microsoft Learn.</p></div>" + foot(2))

def s3():
    return shell(f"{kick()}<div><h2>Tres criterios oficiales para elegir</h2>"
        "<div class='row'><span class='n'>01</span><span class='t'><b>Conformidad</b>Revisa los reportes de conformidad para las funciones que usas.</span></div>"
        "<div class='row'><span class='n'>02</span><span class='t'><b>Tecnología</b>El proxy que tu equipo ya sabe operar: Envoy, NGINX u otros.</span></div>"
        "<div class='row'><span class='n'>03</span><span class='t'><b>Integración</b>Tu nube o tu CNI puede traer una implementación propia.</span></div>"
        "<p class='src'>Fuente: guía de Gateway API para usuarios de ingress-nginx. En su lista de implementaciones (consultada el 28 nov 2026) figuran como conformes Envoy Gateway, NGINX Gateway Fabric, Istio, GKE, Cilium y Traefik.</p></div>" + foot(3))

def s4():
    rows = [
        ("Ya operas Istio", "Gateway API de Istio", ""),
        ("Tu CNI es Cilium", "Gateway API de Cilium", ""),
        ("Prefieres operar menos, en la nube", "GKE Gateway, AWS Load Balancer Controller o Application Gateway for Containers", ""),
        ("Quieres un gateway sobre Envoy", "Envoy Gateway", ""),
        ("Tu equipo domina NGINX", "NGINX Gateway Fabric", "Revisa su tabla de compatibilidad"),
        ("Una dependencia aún no soporta Gateway API", "Un puente temporal, como Traefik", "Es lo que hace CERN"),
    ]
    t = "".join(f"<tr><td class='a'>{E(a)}</td><td class='b'>{E(b)}" + (f"<span>{E(c)}</span>" if c else "") + "</td></tr>" for a, b, c in rows)
    return shell(f"{kick()}<div><h2>Si tu caso es… mira primero…</h2><table>{t}</table>"
        "<p class='src' style='font-size:25px;margin-top:14px'>Orientación a partir de casos documentados, no un ranking: no hallé una comparativa oficial de rendimiento.</p></div>" + foot(4))

def s5():
    return shell(f"{kick()}<div><h2>Qué eligieron otros</h2><ul class='l' style='font-size:33px'>"
        "<li style='font-size:33px'><b>CERN:</b> Gateway API. Cilium, su CNI desde 2025, la incluye. Traefik como puente donde una dependencia no la soporta.</li>"
        "<li style='font-size:33px'><b>Boeing:</b> Istio, en los clústeres que ya lo integraban.</li>"
        "<li style='font-size:33px'><b>Zapier:</b> Envoy Gateway. Descartó Istio por convertir la migración en una de malla, y Gloo por funciones clave en licencia enterprise. En dic 2025 vio inmaduros a HAProxy, NGINX Gateway y Traefik.</li>"
        "<li style='font-size:33px'><b>Qovery:</b> Envoy Gateway, con más de 300 clústeres previstos.</li></ul>"
        "<p class='src'>Fuentes: CNCF (16 abr 2026), Zapier (12 dic 2025), Qovery (feb y oct 2026). Son decisiones de cada equipo, no recomendaciones generales.</p></div>" + foot(5))

def s6():
    return shell(f"{kick()}<div><h2>Lo que cambia al pasar a Envoy</h2>"
        "<div class='lab'>Timeout de petición por defecto, según Qovery</div>"
        "<div class='bar' style='width:100%;background:#52606D'>NGINX · 60 s</div>"
        "<div class='bar' style='width:25%;background:#0F766E;margin-top:12px;min-width:240px'>Envoy · 15 s</div>"
        "<ul class='l' style='margin-top:34px'>"
        "<li style='font-size:32px;padding:16px 0 16px 40px'>NGINX reintentaba por defecto; Envoy necesitó reintentos configurados.</li>"
        "<li style='font-size:32px;padding:16px 0 16px 40px'>Las políticas de Gateway API se reemplazan entre sí, no se combinan.</li>"
        "<li style='font-size:32px;padding:16px 0 16px 40px'>Un buffer de conexión pequeño causó errores 503 con cargas grandes (Zapier).</li></ul>"
        "<p class='src'>Fuentes: Qovery (10 oct 2026) y Zapier. Verifica estos valores en tu versión.</p></div>" + foot(6))

def s7():
    months = ["Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov"]
    W = 820; start = 0.77  # 23 feb
    def x(m): return int((m / len(months)) * W)
    start = 0.82  # 23 feb
    plan_l, plan_w = x(start), x(1.97) - x(start)   # 31 mar
    real_l, real_w = x(start), x(8.32) - x(start)   # 10 oct
    ticks = "".join(f"<div style='position:absolute;left:{x(i)}px;top:0;font-size:25px;color:#52606D;width:{W//len(months)}px'>{m}</div>" for i, m in enumerate(months))
    return shell(f"{kick()}<div><h2>El plan vs la realidad</h2>"
        "<p class='sub' style='font-size:32px;margin-bottom:26px'>Migrar los clústeres gestionados de Qovery a Envoy Gateway</p>"
        f"<div style='position:relative;width:{W}px;height:40px'>{ticks}</div>"
        f"<div class='lab'>Plan: terminar a fines de marzo</div>"
        f"<div style='position:relative;width:{W}px;height:58px;background:rgba(31,41,51,.08)'><div style='position:absolute;left:{plan_l}px;width:{plan_w}px;height:58px;background:#52606D'></div></div>"
        f"<div class='lab'>Real: 94 % migrado al 10 de octubre</div>"
        f"<div style='position:relative;width:{W}px;height:58px;background:rgba(31,41,51,.08)'><div style='position:absolute;left:{real_l}px;width:{real_w}px;height:58px;background:#0F766E'></div></div>"
        "<ul class='l' style='margin-top:38px'>"
        "<li style='font-size:32px;padding:16px 0 16px 40px'>Cada versión menor de Envoy Gateway, de la 1.6.1 a la 1.9.1, cambió comportamientos de los que dependían.</li>"
        "<li style='font-size:32px;padding:16px 0 16px 40px'>Lección: presupuesta las actualizaciones del stack nuevo, no solo la migración.</li></ul>"
        "<p class='src'>Fuente: Qovery (17 feb y 10 oct 2026). Barras aproximadas a partir de su cronograma.</p></div>" + foot(7))

def s8():
    items = [
        ("Inventario", "Corre ingress2gateway 1.0 (más de 30 anotaciones). configuration-snippet no se traduce."),
        ("Regex", "ingress-nginx coincide por prefijo y sin distinguir mayúsculas. En Envoy, la coincidencia es completa."),
        ("En paralelo", "El controlador nuevo con su propia IP, junto al ingress-nginx."),
        ("DNS ponderado", "No borres el Ingress hasta que expire el TTL: en un caso de la CNCF, el primer corte perdió peticiones."),
        ("Explícito", "Fija timeouts, reintentos y buffers; no heredes valores por defecto."),
        ("Mide", "Compara tasa de error y latencia en ambos durante el cambio."),
    ]
    rows = "".join(f"<div class='row' style='padding:9px 0'><span class='n' style='font-size:38px;min-width:56px'>{i+1:02d}</span><span class='t' style='font-size:29px;line-height:1.25'><b style='font-size:33px;margin-bottom:0'>{E(a)}</b>{E(b)}</span></div>" for i, (a, b) in enumerate(items))
    return shell(f"{kick()}<div><h2 style='margin-bottom:12px'>Cómo migrar sin caídas</h2>{rows}"
        "<p class='src' style='font-size:24px;margin-top:10px'>Fuentes: Gateway API, Kubernetes, CNCF, Qovery, Zapier y Datadog.</p></div>" + foot(8))

def s9():
    return shell(f"{kick()}<div><h2>Fuentes</h2><ul class='l' style='font-size:29px'>"
        "<li style='font-size:29px;padding:13px 0 13px 40px'><b>Kubernetes:</b> declaración del 29 ene 2026; «Antes de migrar» (27 feb); ingress2gateway 1.0 (20 mar)</li>"
        "<li style='font-size:29px;padding:13px 0 13px 40px'><b>Gateway API:</b> guía para usuarios de ingress-nginx y lista de implementaciones</li>"
        "<li style='font-size:29px;padding:13px 0 13px 40px'><b>Documentación:</b> Istio, NGINX Gateway Fabric, Cilium, GKE, AWS Load Balancer Controller, Microsoft Learn (AKS)</li>"
        "<li style='font-size:29px;padding:13px 0 13px 40px'><b>Casos:</b> CNCF (16 abr y 25 may 2026), Zapier (12 dic 2025), Qovery (feb y oct 2026)</li></ul>"
        "<p class='src' style='font-size:27px'>Los enlaces completos están en el texto del post.</p>"
        "<p style='font-family:Lora,serif;font-weight:700;font-size:62px;line-height:1.15;margin-top:36px;max-width:560px'>¿Qué elegiste <em style='color:#0F766E'>y por qué?</em></p></div>"
        f"<img class='av' src='file://{AV}' width='250' style='bottom:165px;right:60px'>{foot(9)}")

SLIDES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]

def shot(html, out):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html); path = f.name
    subprocess.run(["google-chrome", "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--window-size=1080,1350",
                    f"--screenshot={out}", f"file://{path}"], check=True, capture_output=True)
    Path(path).unlink()

def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    pages = []
    for i, fn in enumerate(SLIDES, 1):
        png = out / f"_s{i}.png"; shot(fn(), str(png)); pages.append(Image.open(png).convert("RGB"))
    pages[0].save(out / "L-046_carrusel.pdf", save_all=True, append_images=pages[1:])
    print("ok", len(pages))

if __name__ == "__main__": main()
