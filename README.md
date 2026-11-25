# linkedin-assets
Imágenes y PDFs de carrusel para publicaciones de LinkedIn (cuenta personal y página de empresa).
- `images/personal-v2/`: cuenta personal (estilo editorial crema/verde, Lora + DM Sans).
- `images/devup/`: página de empresa (azul marino, Inter).
- `images/` (raíz): piezas antiguas; no usar para piezas nuevas.
- `tools/make_personal.py` y `tools/make_devup.py`: generan PNG 1080x1350 y PDF de carrusel desde un JSON.
  Uso: `python3 -I tools/make_personal.py piezas.json salida/` y `python3 -I tools/make_devup.py piezas.json salida/ devup`.
  Pieza: {"id","kind":"card"|"carousel","kicker","title","accent","items":[...],"slides":[{"title","body"}]}.
  Requiere google-chrome headless, Pillow y las fuentes Lora, DM Sans e Inter.
