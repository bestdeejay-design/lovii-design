#!/usr/bin/env python3
# ============================================================
# Страж единого центра правды (v1.4.1).
#
# Гарантирует: цветовые значения живут только в tokens/tokens.css
# (+ design-tokens.json). В шаблонах гайда, хабе и примерах hex-
# литерал разрешён, только если он:
#   1) равен значению какого-то токена канона (контролируемый дубль);
#   2) входит в служебный белый список (#999, #bbb, #fff, #000);
#   3) строка помечена TOKEN-PIN (осознанный пин: meta, лого-подложки).
# Любой другой hex — ОШИБКА: дрейф от канона или цвет без токена.
# Именно эта проверка поймала бы баг v1.4.1: таблица свотчей гайда
# показывала старый #f7f2f4 при каноне #f8f5f0.
#
# Отдельный запрет: JS-массивы пар [имя токена, значение] в tpl-js —
# свотчи обязаны читать канон через parseTokenBuckets.
#
# Запуск из корня репо:  python3 tools/check-sync.py
# Код возврата: 0 — OK, 1 — есть нарушения.
# ============================================================
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

TARGETS = [
    "tools/tpl-head.part.html",
    "tools/tpl-body.part.html",
    "tools/tpl-js.part.html",
    "css/lovii-components.css",
    "index.html",
    *sorted(f"examples/{p.name}" for p in (ROOT / "examples").glob("*.html")),
]
# Примечание: lovii.css (сборка) в TARGETS не входит — он генерируется
# tools/build-lovii-css.py из tokens/tokens.css (источник канона) и
# css/lovii-components.css (под стражем выше). Hex-литералы определений
# токенов в сборке — ожидаемое содержимое слоя A.

# Служебные цвета демо-интерфейса, не токены (пары документированы в docs/02, AGENTS пр.6).
def norm(h: str) -> str:
    """#ABC -> #aabbcc, остальное — в нижний регистр."""
    h = h.lower()
    if len(h) == 4:
        h = "#" + "".join(c * 2 for c in h[1:])
    return h


UTILITY_RAW = {"#999", "#bbb", "#000", "#000000", "#fff", "#ffffff"}
UTILITY = {norm(u) for u in UTILITY_RAW}

HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
JS_VALUE_ARRAY_RE = re.compile(r"\[\s*['\"]--lv-[a-z0-9-]+['\"]\s*,\s*['\"](#|rgba)")


def canon_hexes() -> set:
    """Все hex-значения, входящие в значения токенов tokens.css."""
    css = (ROOT / "tokens" / "tokens.css").read_text(encoding="utf-8")
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)  # комментарии содержат исторические hex
    out = set()
    for m in re.finditer(r"--lv-[a-z0-9-]+\s*:\s*([^;]+);", css):
        for h in HEX_RE.findall(m.group(1)):
            out.add(norm(h))
    return out


def main() -> int:
    canon = canon_hexes()
    errors = []

    for rel in TARGETS:
        p = ROOT / rel
        if not p.exists():
            errors.append(f"{rel}: файл не найден")
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines, 1):
            if "TOKEN-PIN" in line:
                continue
            for h in HEX_RE.findall(line):
                n = norm(h)
                if n in UTILITY or n in canon:
                    continue
                errors.append(
                    f"{rel}:{i}: hex {h} не из канона tokens.css — "
                    f"заведи токен или используй var(--lv-*) (AGENTS пр.1/13)"
                )
        if rel.endswith("tpl-js.part.html"):
            for i, line in enumerate(lines, 1):
                if JS_VALUE_ARRAY_RE.search(line):
                    errors.append(
                        f"{rel}:{i}: JS-массив значений токена запрещён — "
                        f"читай канон через parseTokenBuckets (AGENTS пр.13)"
                    )
            if "parseTokenBuckets" not in p.read_text(encoding="utf-8"):
                errors.append(f"{rel}: нет parseTokenBuckets — свотчи оторваны от канона")

    if errors:
        print(f"check-sync: {len(errors)} нарушений центра правды")
        for e in errors:
            print("  ✗ " + e)
        return 1
    print(f"check-sync: OK — {len(TARGETS)} файлов, дрейфа цвета от канона нет ({len(canon)} канонных hex)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
