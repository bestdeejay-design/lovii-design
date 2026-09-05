#!/usr/bin/env python3
# ============================================================
# LOVII Framework — ОДНА КОМАНДА разноски стилей во все сайты.
#
# Фреймворк-цикл правки стиля (полный контракт — SKILL.md):
#   1. правишь исходники в lovii-design: tokens/tokens.css (слой A)
#      и/или css/lovii-components.css (слой B);
#   2. python3 tools/build-lovii-css.py   — сборка lovii.css;
#   3. python3 tools/check-sync.py        — страж канона;
#   4. git commit + push в lovii-design   (провенанс снапшотов =
#      коммит, чьё содержимое разъехалось по сайтам);
#   5. python3 tools/propagate.py --push  — ЭТА КОМАНДА: снапшоты
#      во всех потребителей из tools/targets.json + стражи
#      приёмки + точечные коммиты + пуши. Всё сразу.
#
# Режимы:
#   python3 tools/propagate.py             # снапшоты + стражи, БЕЗ коммитов (отчёт)
#   python3 tools/propagate.py --check     # только сверка (код 1 = есть расхождение)
#   python3 tools/propagate.py --push      # + коммит/пуш в каждом ИЗМЕНЁННОМ репо
#   python3 tools/propagate.py --smoke     # + медленная playwright-приёмка (--push рекомендуется)
#   python3 tools/propagate.py --only a,b  # подмножество репо-потребителей
#   python3 tools/propagate.py --no-build  # не пересобирать lovii.css (уже собран)
#
# Безопасность:
#   - коммитится ТОЛЬКО файл снапшота (git add <dest>), никогда -A;
#     несвязанные изменения репо-потребителя не трогаются и попадают
#     в отчёт;
#   - перед снапшотами lovii-design должен быть закоммичен и запушен
#     (иначе провенанс укажет на хеш, которого нет на GitHub — STOP);
#   - если в репо уже есть НЕЗАКОММИЧЕННОЕ содержимое в файле-приёмнике,
#     оно будет перезаписано снапшотом (снапшоты править запрещено —
#     AGENTS.md пр.14); изменения из lovii-design восстанавливаются
#     повторным циклом.
# ============================================================
import argparse
import importlib.util
import pathlib
import shlex
import subprocess
import sys

TOOLS = pathlib.Path(__file__).resolve().parent
ROOT = TOOLS.parent                 # корень репо lovii-design
WORLD = ROOT.parent                 # /home/z/my-project (каталог всех репо)


def load_sync_module():
    spec = importlib.util.spec_from_file_location("sync_lovii_css", TOOLS / "sync-lovii-css.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SYNC = load_sync_module()


def run(cmd, cwd, capture=True):
    r = subprocess.run(shlex.split(cmd) if isinstance(cmd, str) else cmd,
                       cwd=str(cwd), capture_output=capture, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def git(repo_path, args):
    return run(["git"] + args, repo_path)


def branch_of(repo: pathlib.Path) -> str:
    code, out = git(repo, ["rev-parse", "--abbrev-ref", "HEAD"])
    return out.strip() if code == 0 else "main"


def head_short(repo: pathlib.Path) -> str:
    code, out = git(repo, ["rev-parse", "--short", "HEAD"])
    return out.strip() if code == 0 else "unknown"


def unpushed_count(repo: pathlib.Path) -> int:
    br = branch_of(repo)
    code, out = git(repo, ["rev-list", "--count", f"origin/{br}..{br}"])
    return int(out.strip()) if code == 0 and out.strip().isdigit() else 0


def dirty_files(repo: pathlib.Path):
    code, out = git(repo, ["status", "--porcelain"])
    return [l[3:].strip() for l in out.splitlines() if l.strip()]


def guard_cmd(consumer):
    return list(consumer.get("guards") or [])


def main() -> int:
    ap = argparse.ArgumentParser(description="LOVII Framework: разнос lovii.css по всем сайтам")
    ap.add_argument("--check", action="store_true", help="только сверка, без записи и стражей")
    ap.add_argument("--push", action="store_true", help="коммит+пуш изменённых репо-потребителей (только файл снапшота)")
    ap.add_argument("--smoke", action="store_true", help="прогнать smoke-приёмку потребителей перед пушем")
    ap.add_argument("--no-build", action="store_true", help="не пересобирать lovii.css")
    ap.add_argument("--only", default="", help="подмножество репо: lovii,lovii-site")
    args = ap.parse_args()

    registry = ROOT / "tools" / "targets.json"
    if not registry.exists():
        print(f"Нет {registry} — фреймворк не настроен")
        return 1
    data = __import__("json").loads(registry.read_text(encoding="utf-8"))
    consumers = data.get("consumers", [])
    only = [s.strip() for s in args.only.split(",") if s.strip()]
    if only:
        consumers = [c for c in consumers if c["repo"] in only]
        if not consumers:
            print(f"--only {args.only}: в реестре таких нет")
            return 1

    print(f"LOVII Framework · lovii-design@{head_short(ROOT)} · потребителей: "
          f"{', '.join(c['repo'] for c in consumers)}\n")

    # ── Шаг 0: lovii-design должен быть чист и запушен ────────
    if not args.check and not args.no_build:
        code, out = run("python3 tools/build-lovii-css.py", ROOT)
        print(out.strip() or f"build exit={code}")
        if code != 0:
            return 1
    dirty = dirty_files(ROOT)
    if dirty:
        print(f"STOP: lovii-design не закоммичен ({len(dirty)} файл.) — "
              f"сначала commit+push, иначе провенанс снапшотов укажет в пустоту.")
        for f in dirty:
            print("  -", f)
        return 1
    if unpushed_count(ROOT):
        print("STOP: в lovii-design есть незапушенные коммиты — сначала git push.")
        return 1

    # ── Шаг 1: снапшоты ───────────────────────────────────────
    changed, in_sync, failed = [], [], []
    for c in consumers:
        repo = WORLD / c["repo"]
        dest = repo / c["dest"]
        src_name = c.get("src", "lovii.css")
        src = ROOT / src_name
        name = f"{c['repo']}/{c['dest']}"
        if not repo.exists():
            print(f"{name}: НЕТ РЕПО {repo} — пропущен")
            failed.append(name)
            continue
        if not src.exists():
            print(f"{name}: НЕТ АРТЕФАКТА lovii-design/{src_name} — сначала сборка")
            failed.append(name)
            continue
        body = src.read_text(encoding="utf-8")
        expected = SYNC.provenance(c["repo"], src_name) + body
        current = dest.read_text(encoding="utf-8") if dest.exists() else None
        if current == expected:
            # содержимое верное; но снапшот мог быть записан ранее и не закоммичен
            if c["dest"] in dirty_files(repo):
                print(f"{name}: содержимое верное, снапшот НЕ закоммичен — включён в разноску")
                changed.append((c, src_name))
            else:
                print(f"{name}: синхронен ✓")
                in_sync.append(name)
            continue
        if args.check:
            print(f"{name}: РАСХОЖДЕНИЕ (нужна разноска)")
            failed.append(name)
            continue
        dest.write_text(expected, encoding="utf-8")
        print(f"{name}: обновлён ← lovii-design/{src_name}@{head_short(ROOT)}")
        changed.append((c, src_name))

    if args.check:
        print("\nСВЕРКА: " + ("всё синхронно ✓" if not failed else f"расхождения: {len(failed)}"))
        return 0 if not failed else 1

    if not changed:
        print("\nОбновлять нечего — все потребители синхронны.")
        return 0

    # ── Шаг 2: стражи приёмки ─────────────────────────────────
    print("\n— Стражи приёмки —")
    blocked = []
    for c, _src_name in changed:
        for g in guard_cmd(c):
            code, out = run(g, WORLD)
            tail = (out.strip().splitlines() or [""])[-1]
            print(f"[{c['repo']}] {g} → {'OK' if code == 0 else f'FAIL ({code})'}{(' · ' + tail) if code == 0 else ''}")
            if code != 0:
                print(out[-1500:])
                blocked.append(c["repo"])
        if args.smoke and c.get("smoke") and c["repo"] not in blocked:
            code, out = run(c["smoke"], WORLD)
            tail = (out.strip().splitlines() or [""])[-1]
            print(f"[{c['repo']}] SMOKE → {'OK' if code == 0 else f'FAIL ({code})'}{(' · ' + tail) if code == 0 else ''}")
            if code != 0:
                print(out[-1500:])
                blocked.append(c["repo"])
    if blocked:
        print(f"\nSTOP: стражи заблокировали {', '.join(sorted(set(blocked)))} — коммитов нет, разберись и перезапусти.")
        return 1

    # ── Шаг 3: коммиты и пуши (только --push) ─────────────────
    if not args.push:
        print("\nБез --push: коммитов нет. Дальше вручную либо: python3 tools/propagate.py --push")
        return 0

    print("\n— Коммиты и пуши (только файлы снапшотов) —")
    pushed, skipped = [], []
    for c, src_name in changed:
        repo = WORLD / c["repo"]
        br = branch_of(repo)
        _code, staged_before = git(repo, ["diff", "--cached", "--name-only"])
        if staged_before.strip():
            print(f"[{c['repo']}] SKIP: в индексе уже есть чужие файлы — вручную: {staged_before.strip()}")
            skipped.append(c["repo"])
            continue
        git(repo, ["add", c["dest"]])
        code, out = git(repo, ["diff", "--cached", "--quiet"])
        if code == 0:
            print(f"[{c['repo']}] SKIP: после стражей снапшот не изменился")
            skipped.append(c["repo"])
            continue
        msg = f"chore(ds): снапшот {src_name} → lovii-design@{head_short(ROOT)}"
        code, out = git(repo, ["commit", "-m", msg])
        if code != 0:
            print(f"[{c['repo']}] COMMIT FAIL:\n{out[-800:]}")
            failed.append(c["repo"])
            continue
        code, out = git(repo, ["push", "origin", br])
        if code != 0:
            print(f"[{c['repo']}] PUSH FAIL:\n{out[-800:]}")
            failed.append(c["repo"])
            continue
        others = [f for f in dirty_files(repo) if f != c["dest"]]
        note = f" · несвязанных изменений в репо: {len(others)} (не тронуты)" if others else ""
        print(f"[{c['repo']}] {msg} → pushed origin/{br}{note}")
        pushed.append(c["repo"])

    # ── Отчёт ─────────────────────────────────────────────────
    print("\nИТОГ:")
    print(f"  обновлено и запушено : {', '.join(pushed) if pushed else '—'}")
    if skipped:
        print(f"  пропущены            : {', '.join(skipped)}")
    if failed:
        print(f"  ОШИБКИ               : {', '.join(failed)}")
        return 1
    for c, _src_name in changed:
        if c.get("live"):
            print(f"  live {c['repo']:<10}: {c['live']} (CDN Pages до 10 мин — приёмка с cache-buster)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
