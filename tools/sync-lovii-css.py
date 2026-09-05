#!/usr/bin/env python3
# ============================================================
# Разнос lovii.css по сайтам LOVII (снапшоты с провенансом).
#
# Схема «одно место правки — везде одинаково» (фреймворк-цикл):
#   1. правишь исходники в lovii-design (tokens/tokens.css,
#      css/lovii-components.css);
#   2. python3 tools/build-lovii-css.py      — сборка lovii.css;
#   3. git commit + push в lovii-design (провенанс снапшотов
#      должен указывать на запушенный коммит);
#   4. python3 tools/propagate.py --push     — снапшоты во ВСЕ
#      потребителей + стражи + коммиты + пуши одной командой.
#
# Этот скрипт — низкоуровневый шаг №4 без commit/push (его же
# использует propagate.py). Список потребителей — реестр
# tools/targets.json (добавил сайт — добавь запись в реестр).
#
# Снапшот = выбранный артефакт (по умолчанию lovii.css; поле "src"
# в реестре — lovii-tokens.css для потребителей со своим
# компонентным слоем) + инъекция шапки-провенанса
# («СНАПШОТ из lovii-design@<hash>; не редактировать»).
# Направление строго одно: lovii-design → сайты. Правки
# снапшота на месте запрещены и будут перезатёрты.
#
# Запуск из корня репо lovii-design:
#   python3 tools/sync-lovii-css.py [--check]
#   --check — только сверка (код 1 = есть расхождение).
# ============================================================
import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "lovii.css"
REGISTRY = ROOT / "tools" / "targets.json"

# Резервный список, если реестра нет (реестр — источник истины).
FALLBACK = [("lovii", "assets/lovii.css", "lovii.css"),
            ("lovii-site", "assets/lovii.css", "lovii.css")]


def load_targets():
    """Реестр потребителей tools/targets.json → [(repo, dest, src), …].
    src — имя артефакта lovii-design (по умолчанию lovii.css)."""
    if not REGISTRY.exists():
        print(f"ВНИМАНИЕ: нет {REGISTRY.name} — используется резервный список")
        return list(FALLBACK)
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return [(c["repo"], c["dest"], c.get("src", "lovii.css"))
            for c in data.get("consumers", [])]


def git_short() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def provenance(repo: str, src: str = "lovii.css") -> str:
    artifact = ("lovii.css (полный файл ДС)" if src == "lovii.css"
                else f"{src} (слой токенов без компонентов)")
    return (
        f"/* СНАПШОТ LOVII UI из репо bestdeejay-design/lovii-design@{git_short()}\n"
        f"   Потребитель: {repo}. НЕ РЕДАКТИРОВАТЬ ЗДЕСЬ.\n"
        f"   Артефакт: {artifact}.\n"
        f"   Правки только в lovii-design: css/lovii-components.css или\n"
        f"   tokens/tokens.css → build-lovii-css.py → sync-lovii-css.py. */\n\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="только сверка, без записи")
    args = ap.parse_args()

    if not SRC.exists():
        print(f"Нет {SRC} — сначала python3 tools/build-lovii-css.py")
        return 1

    drift = []
    for repo, dest_rel, src_rel in load_targets():
        src = ROOT / src_rel
        if not src.exists():
            print(f"lovii-design/{src_rel}: НЕТ АРТЕФАКТА — сначала сборка")
            drift.append(f"{repo}/{dest_rel}")
            continue
        body = src.read_text(encoding="utf-8")
        dest = ROOT.parent / repo / dest_rel
        name = f"{repo}/{dest_rel}"
        if not dest.parent.exists():
            print(f"{name}: НЕТ КАТАЛОГА {dest.parent} — пропущен")
            drift.append(name)
            continue
        expected = provenance(repo, src_rel) + body
        if dest.exists() and dest.read_text(encoding="utf-8") == expected:
            print(f"{name}: синхронен ✓")
        elif args.check:
            print(f"{name}: РАСХОЖДЕНИЕ (нужна разноска)")
            drift.append(name)
        else:
            dest.write_text(expected, encoding="utf-8")
            print(f"{name}: обновлён ← lovii-design@{git_short()}")

    if args.check and drift:
        print("\nЕсть расхождения — запусти разноску без --check, затем коммиты в репо-потребителях.")
        return 1
    print("\nГотово. Дальше: git diff в каждом репо-потребителе → коммит → пуш (прод обновится осознанно).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
