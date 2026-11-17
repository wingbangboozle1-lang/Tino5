#!/usr/bin/env python3
"""Privacy and link check on the surface GitHub Pages actually publishes.

Session arena-2bacf26a (2026-11-17). Run from the repository root:

    python3 scripts/check_published_surface.py          # exit 1 on any failure
    python3 scripts/check_published_surface.py --list   # print the published files

What it checks
  1. Published set: git-tracked files that _config.yml does not exclude and that
     Jekyll would skip (names starting with "_" or ".", node_modules, vendor).
  2. Owner figures. The owner's exact assessed values and tax bills are NOT stored in
     this repository. They are read from a private list outside the repo, by default
     ~/.estate-private/owner-figures.txt, one entry per line:
        "H <digits>"  owner history or bill figure. A figure that is not a multiple of
                      $10 FAILS the check (the brief's rounding rule is broken). A figure
                      that is a multiple of $10 is reported as an owner decision: the brief
                      asks for $10-rounded tables, but the README says histories are not
                      published at any precision.
        "A <digits>"  owner anchor (value, rent). Reported only; $10-rounded values are allowed.
     If the private list is absent the check is reported as SKIPPED, not passed.
  3. Place names (must be zero): city, neighbourhood and postcode names that the
     repository rules keep off the public site (county level only).
  4. Internal links in published HTML resolve to published files.
"""
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
PRIVATE_LIST = Path(os.environ.get("OWNER_FIGURES_FILE",
                                   str(Path.home() / ".estate-private" / "owner-figures.txt")))
PLACE_NAMES = ["Cupertino", "San Jose", "Sunnyvale", "Naaldwijk", "South Holland",
               "95014", "94122", "Monta Vista", "Richmond District", "Inner Sunset", "Outer Sunset"]  # bare "Sunset" is also a clause term (sunset date), so not checked
TEXT_EXT = (".html", ".htm", ".md", ".txt", ".json", ".csv", ".js", ".css", ".svg")


def load_config_excludes():
    import yaml
    cfg = yaml.safe_load((ROOT / "_config.yml").read_text()) or {}
    out = []
    for e in cfg.get("exclude", []) or []:
        e = str(e).rstrip("/")
        if e.endswith("/**"):
            e = e[:-3]
        out.append(e)
    return out


def published_files():
    excludes = load_config_excludes()
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                             text=True, check=True).stdout.splitlines()
    keep = []
    for f in tracked:
        if any(f == e or f.startswith(e + "/") for e in excludes):
            continue
        parts = f.split("/")
        if any(p.startswith(("_", ".")) for p in parts) or "node_modules" in parts or "vendor" in parts:
            continue
        if parts[-1] in ("Gemfile", "Gemfile.lock"):
            continue
        keep.append(f)
    return keep


def load_private_figures():
    if not PRIVATE_LIST.exists():
        return None
    hist, anchors = set(), set()
    for line in PRIVATE_LIST.read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1].isdigit():
            (hist if parts[0] == "H" else anchors).add(parts[1])
    return hist, anchors


# A figure counts only when it is written as money: comma-grouped (e.g. 1,234,567) or
# $-prefixed (e.g. $1230). Bare four-digit numbers are usually calendar years and are ignored.
NUM_RE = re.compile(r"(?<![0-9.])(\$?)(\d{1,3}(?:,\d{3})+|\d{4,})(?![0-9])")
HREF_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"'#?]+)""", re.I)


def number_hits(text, figures):
    found = set()
    for m in NUM_RE.finditer(text):
        dollar, raw = m.group(1), m.group(2)
        if not (dollar or "," in raw):
            continue
        digits = raw.replace(",", "")
        if digits in figures:
            found.add(digits)
    return found


def main():
    files = published_files()
    if "--list" in sys.argv:
        print("\n".join(files))
        return 0
    fileset = set(files)
    failures = []
    notes = []

    priv = load_private_figures()
    if priv is None:
        notes.append(f"parcel-history check SKIPPED: private list not found at {PRIVATE_LIST}")
    else:
        hist, _anchors = priv  # owner anchors ("A") are listed for reference; they are not failed
        for f in files:
            if not f.endswith(TEXT_EXT):
                continue
            text = (ROOT / f).read_text(errors="ignore")
            h = number_hits(text, hist)
            raw = {d for d in h if int(d) % 10}
            if raw:
                failures.append(f"raw (not $10-rounded) owner figure(s) in {f}: {len(raw)} distinct")
            rounded = h - raw
            if rounded:
                notes.append(f"owner history value(s), $10-rounded, in {f}: {len(rounded)} distinct (owner decision, see flagged-for-review)")

    for f in files:
        if not f.endswith(TEXT_EXT):
            continue
        text = (ROOT / f).read_text(errors="ignore")
        for name in PLACE_NAMES:
            if name in text:
                failures.append(f"place name '{name}' in {f}")
                break

    for f in files:
        if not f.endswith((".html", ".htm")):
            continue
        base = os.path.dirname(f)
        text = (ROOT / f).read_text(errors="ignore")
        for href in HREF_RE.findall(text):
            href = unquote(href.strip())
            if not href or re.match(r"^(https?:|mailto:|tel:|data:|javascript:)", href, re.I):
                continue
            if href.startswith("/"):
                failures.append(f"root-absolute link '{href}' in {f} (breaks under /Tino5/)")
                continue
            target = os.path.normpath(os.path.join(base, href)).lstrip("./") if base else os.path.normpath(href)
            candidates = [target]
            if target.endswith("/") or target == "" or target == ".":
                candidates = [os.path.join(target, "index.html")]
            else:
                candidates += [target + ".html", os.path.join(target, "index.html")]
            if not any(c in fileset for c in candidates):
                failures.append(f"broken link '{href}' in {f}")

    for n in notes:
        print("NOTE:", n)
    for x in failures:
        print("FAIL:", x)
    print(f"published files: {len(files)}; failures: {len(failures)}; notes: {len(notes)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
