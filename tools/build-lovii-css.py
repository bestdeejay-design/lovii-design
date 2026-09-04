#!/usr/bin/env python3
# ============================================================
# Сборка lovii.css — единого файла дизайн-системы LOVII UI.
#
# lovii.css = шапка + СЛОЙ A (tokens/tokens.css: токены, база,
# движение) + СЛОЙ B (css/lovii-components.css: компоненты).
#
# Правишь исходники слоёв, потом запускаешь эту сборку —
# lovii.css обновляется целиком. Напрямую lovii.css не править.
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
OUT = ROOT / "lovii.css"
UI_VERSION = "1.0.0"


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
     css/lovii-components.css     — компоненты
   Живой каталог компонентов: style-guide.html, examples/08.
   Правила: только var(--lv-*), классы только канонические.
   ============================================================ */

/* ══════════════════ СЛОЙ A: ТОКЕНЫ И БАЗА ══════════════════ */

"""
    footer = "\n/* ══════════════════ СЛОЙ B: КОМПОНЕНТЫ ══════════════════ */\n\n"

    OUT.write_text(header + a + footer + b, encoding="utf-8")
    print(f"OK: {OUT} ({len((header + a + footer + b).splitlines())} строк) — LOVII UI v{UI_VERSION}, токены {token_version()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
