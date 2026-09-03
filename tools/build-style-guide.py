#!/usr/bin/env python3
# ============================================================
# Сборка style-guide.html дизайн-системы LOVII.
# Склеивает шаблон из трёх частей, инлайнит tokens/tokens.css
# (гайд никогда не расходится с токенами) и base64-логотипы
# (гайд самодостаточен — открывается одним файлом).
#
# Запуск из корня репо:  python3 tools/build-style-guide.py
# ============================================================
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = ROOT / "tools"

def read(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8")

def b64(p: pathlib.Path) -> str:
    return base64.b64encode(p.read_bytes()).decode("ascii")

tokens_css = read(ROOT / "tokens" / "tokens.css")
logo_light = b64(ROOT / "assets" / "lovii-logo-light.svg")
logo_dark = b64(ROOT / "assets" / "lovii-logo-dark.svg")

html = (
    read(TPL / "tpl-head.part.html")
    + read(TPL / "tpl-body.part.html")
    + read(TPL / "tpl-js.part.html")
)

html = html.replace("%%TOKENS_CSS%%", tokens_css)
html = html.replace("%%LOGO_LIGHT_B64%%", logo_light)
html = html.replace("%%LOGO_DARK_B64%%", logo_dark)

out = ROOT / "style-guide.html"
out.write_text(html, encoding="utf-8")
print(f"OK: {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
