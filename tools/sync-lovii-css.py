#!/usr/bin/env python3
# ============================================================
# Разнос lovii.css по сайтам LOVII (снапшоты с провенансом).
#
# Схема «одно место правки — везде одинаково»:
#   1. правишь исходники в lovii-design (tokens/tokens.css,
#      css/lovii-components.css);
#   2. python3 tools/build-lovii-css.py      — сборка lovii.css;
#   3. python3 tools/sync-lovii-css.py       — этот скрипт кладёт
#      снапшот в каждый репо-потребитель (без commit/push —
#      обновление прода всегда осознанный шаг);
#   4. git diff в каждом репо → коммит → пуш.
#
# Снапшот = lovii.css + инъекция шапки-провенанса
# («СНАПШОТ из lovii-design@<hash>; не редактировать»).
# Направление строго одно: lovii-design → сайты. Правки
# снапшота на месте запрещены и будут перезатёрты.
#
# Запуск из корня репо lovii-design:
#   python3 tools/sync-lovii-css.py [--check]
#   --check — только сверка (код 1 = есть расхождение).
# ============================================================
import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "lovii.css"

# Потребители: (путь к репо от /home/z/my-project, файл назначения)
# lovii-demo — ПОСЛЕ миграции витрины на LOVII UI (сейчас там
# поколение --pink); lovii-legacy — архив, не размножаем.
TARGETS = [
    ("lovii", "assets/lovii.css"),
    ("lovii-site", "assets/lovii.css"),
]


def git_short() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def provenance(repo: str) -> str:
    return (
        f"/* СНАПШОТ LOVII UI из репо bestdeejay-design/lovii-design@{git_short()}\n"
        f"   Потребитель: {repo}. НЕ РЕДАКТИРОВАТЬ ЗДЕСЬ.\n"
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
    body = SRC.read_text(encoding="utf-8")

    drift = []
    for repo, dest_rel in TARGETS:
        dest = ROOT.parent / repo / dest_rel
        name = f"{repo}/{dest_rel}"
        if not dest.parent.exists():
            print(f"{name}: НЕТ КАТАЛОГА {dest.parent} — пропущен")
            drift.append(name)
            continue
        expected = provenance(repo) + body
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
