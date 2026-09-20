#!/usr/bin/env python3
# ============================================================
# Сборка lovii.css — единого файла дизайн-системы LOVII UI.
#
# lovii.css        = шапка + СЛОЙ A (tokens/tokens.css: токены,
#                    база, движение) + COMPAT (tokens/
#                    compat-legacy.css: легаси-алиасы) + СЛОЙ B
#                    (css/lovii-components.css: компоненты).
# lovii-tokens.css = шапка + СЛОЙ A + COMPAT — для потребителей
#                    со СВОИМ компонентным слоем (витрина демо);
#                    полный lovii.css им нельзя — конфликт словаря
#                    классов.
#
# Правишь исходники слоёв, потом запускаешь эту сборку —
# оба файла обновляются целиком. Напрямую их не править.
#
# Разноска на сайты: python3 tools/propagate.py --push
# (низкоуровнево: tools/sync-lovii-css.py)
# Страж канона:      python3 tools/check-sync.py
# ============================================================
import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAYER_A = ROOT / "tokens" / "tokens.css"
LAYER_B = ROOT / "css" / "lovii-components.css"
LAYER_COMPAT = ROOT / "tokens" / "compat-legacy.css"
OUT = ROOT / "lovii.css"
OUT_TOKENS = ROOT / "lovii-tokens.css"
UI_VERSION = "1.0.0"


LAYER_ORDER = "@layer tokens, base, primitives, components, utilities, screens;"
LAYER_MARKER = "/* == @layer:base =="


def split_layers(a: str):
    """Делит слой A на «до маркера» (tokens) и «от маркера» (base).
    Маркер живёт в tokens/tokens.css — см. его пояснение."""
    i = a.find(LAYER_MARKER)
    if i < 0:
        print("ВНИМАНИЕ: маркер слоя base не найден — весь слой A уйдёт в @layer tokens")
        return a, ""
    return a[:i], a[i:]


def layer_banner(title: str) -> str:
    return f"/* ══════════════════ {title} ══════════════════ */\n\n"


def token_version() -> str:
    m = re.search(r"дизайн-токены\s+(v[\d.]+)", LAYER_A.read_text(encoding="utf-8"))
    return m.group(1) if m else "unknown"


def build_date() -> str:
    return datetime.date.today().isoformat()


def main() -> int:
    a = LAYER_A.read_text(encoding="utf-8").rstrip() + "\n"
    b = LAYER_B.read_text(encoding="utf-8").rstrip() + "\n"

    header = f"""/* ============================================================
   LOVII UI v{UI_VERSION} — ЕДИНЫЙ ФАЙЛ дизайн-системы «Лови»
   Канон токенов: {token_version()} · собрано {build_date()}
   Провенанс снапшота (из какого коммита lovii-design взят файл)
   добавляется разносчиком — см. шапку файла на сайте-потребителе.
   ------------------------------------------------------------
   ОДИН файл на любой сайт LOVII. Меняется в одном месте
   (репо lovii-design) и разносится во все сайты одной командой:
     python3 tools/propagate.py --push
   Править здесь нельзя — правятся исходники слоёв:
     tokens/tokens.css            — токены, база, движение
     tokens/compat-legacy.css     — легаси-алиасы (мост миграции)
     css/lovii-components.css     — компоненты
   Живой каталог компонентов: style-guide.html, examples/08.
   Правила: только var(--lv-*), классы только канонические.
   ============================================================ */

/* ══════════════════ СЛОЙ A: ТОКЕНЫ И БАЗА ══════════════════ */

"""
    footer = "\n/* ══════════════════ СЛОЙ B: КОМПОНЕНТЫ ══════════════════ */\n\n"

    compat = ("\n/* ══════════════ СЛОЙ A-COMPAT: ЛЕГАСИ-АЛИАСЫ ══════════════ */\n\n"
              + LAYER_COMPAT.read_text(encoding="utf-8").rstrip() + "\n")

    a_tokens, a_base = split_layers(a)
    layer_frame = ("\n" + layer_banner("КАРКАС СЛОЁВ") + LAYER_ORDER + "\n\n")
    full = (header + layer_frame
            + layer_banner("СЛОЙ A · ТОКЕНЫ") + "@layer tokens {\n" + a_tokens + compat + "}\n\n"
            + layer_banner("СЛОЙ A · БАЗА") + "@layer base {\n" + a_base + "}\n"
            + footer
            + "@layer components {\n" + b + "}\n")
    OUT.write_text(full, encoding="utf-8")
    print(f"OK: {OUT} ({len(full.splitlines())} строк) — LOVII UI v{UI_VERSION}, токены {token_version()}")

    tok_header = f"""/* ============================================================
   LOVII UI v{UI_VERSION} — СЛОЙ ТОКЕНОВ (lovii-tokens.css)
   Канон токенов: {token_version()} · собрано {build_date()}
   Провенанс снапшота добавляется разносчиком — см. шапку файла
   на сайте-потребителе.
   ------------------------------------------------------------
   Токены + база + движение + легаси-алиасы — БЕЗ компонентов.
   Раскладка по слоям каскада: @layer tokens → @layer base (порядок объявлен в шапке).
   Для потребителей, ведущих свой компонентный слой (сейчас:
   витрина lovii.mobiap.com). Полный lovii.css им подключать
   НЕЛЬЗЯ — канонические классы конфликтуют с их локальными.
   Править здесь нельзя — правятся исходники:
     tokens/tokens.css, tokens/compat-legacy.css → сборка.
   ============================================================ */

"""
    a_tokens, a_base = split_layers(a)
    layer_frame = ("\n" + layer_banner("КАРКАС СЛОЁВ") + LAYER_ORDER + "\n\n")
    tokens_file = (tok_header + layer_frame
                   + layer_banner("СЛОЙ A · ТОКЕНЫ") + "@layer tokens {\n" + a_tokens + compat + "}\n\n"
                   + layer_banner("СЛОЙ A · БАЗА") + "@layer base {\n" + a_base + "}\n")
    OUT_TOKENS.write_text(tokens_file, encoding="utf-8")
    print(f"OK: {OUT_TOKENS} ({len(tokens_file.splitlines())} строк) — слой токенов для своих компонентных слоёв")
    return 0


if __name__ == "__main__":
    sys.exit(main())
