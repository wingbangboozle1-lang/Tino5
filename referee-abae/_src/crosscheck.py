"""Cross-check every HTML tree in the repository, and the HTML on the live session branches.

Reports COUNTS and PATHS only. No scanned value is ever printed or written, so a finding cannot leak the thing
it found. Rounding and identifier detection reuse scripts/privacy_scan.py (one definition of "private-looking"
for the whole repository); this module adds what that scan does not look at:

  * is each tree published by GitHub Pages or excluded (read from _config.yml)?
  * does every data row of every table carry a link to an official host?
  * does a page present a superseded official figure?
  * which official constants appear in which tree (cross-desk reconciliation)?
"""
import importlib.util
import re
import subprocess
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import registry as R  # noqa: E402

LIVE_BRANCHES = ["c098bf16", "22a32b17", "3a49d618", "966cc934", "7864052a"]


def _git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def _privacy_scan():
    spec = importlib.util.spec_from_file_location("privacy_scan", ROOT / "scripts" / "privacy_scan.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["privacy_scan"] = mod
    spec.loader.exec_module(mod)
    return mod


def excluded_names(config_text):
    return {m.group(1) for m in re.finditer(r"^\s*-\s*[\"']?([^\"'\s#]+)[\"']?\s*$", config_text, re.M)}


def is_published(path, excludes):
    """Jekyll skips excluded names, and any file or directory whose name starts with '_' or '.'."""
    parts = path.split("/")
    if any(p.startswith(("_", ".")) for p in parts):
        return False
    return not any("/".join(parts[:i + 1]) in excludes or parts[i] in excludes for i in range(len(parts)))


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = 0
        self.rows = []              # (exempt, [hrefs], has_td)
        self._row = None
        self._exempt = False
        self.links = []
        self.text = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("style", "script"):
            self._skip += 1
        if tag == "table":
            self.tables += 1
            self._exempt = bool(re.search(r"nav|meta", a.get("class", "")))
        if tag == "tr":
            self._row = [self._exempt, [], False]
        if tag == "td" and self._row is not None:
            self._row[2] = True
        if tag == "a" and a.get("href", "").startswith("http"):
            self.links.append(a["href"])
            if self._row is not None:
                self._row[1].append(a["href"])

    def handle_endtag(self, tag):
        if tag in ("style", "script") and self._skip:
            self._skip -= 1
        if tag == "tr" and self._row is not None:
            self.rows.append(tuple(self._row))
            self._row = None

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def analyse(html_text):
    p = Page()
    p.feed(html_text)
    data_rows = [r for r in p.rows if r[2] and not r[0]]
    with_official = sum(1 for _, hrefs, _ in data_rows if any(R.is_official(urlparse(h).hostname) for h in hrefs))
    with_other_only = sum(1 for _, hrefs, _ in data_rows if hrefs and not any(R.is_official(urlparse(h).hostname) for h in hrefs))
    none = sum(1 for _, hrefs, _ in data_rows if not hrefs)
    hosts = Counter((urlparse(h).hostname or "") for h in p.links)
    non_official = sorted({h for h in hosts if not R.is_official(h)})
    text = re.sub(r"\s+", " ", " ".join(p.text))
    markers = ("superseded", "earlier", "stale", "previous", "print", "not current", "1 apr 2022", "2023-25", "2021-23", "only for", "was $", "from $")
    stale = []
    for k in R.SUPERSEDED:
        for m in re.finditer(re.escape(k), text):
            ctx = text[max(0, m.start() - 200): m.end() + 200].lower()
            if not any(w in ctx for w in markers):
                stale.append(k)
                break
    stale = sorted(set(stale))
    return {"tables": p.tables, "rows": len(data_rows), "official": with_official, "other_only": with_other_only,
            "no_link": none, "links": len(p.links), "non_official_hosts": non_official, "stale": stale, "text": text}


def scan_tree(files, reader, excludes, label_of):
    """files: list of repo paths. reader(path) -> text. label_of(path) -> tree label."""
    ps = _privacy_scan()
    trees = {}
    for f in files:
        t = trees.setdefault(label_of(f), {"published": is_published(f, excludes), "pages": 0, "tables": 0, "rows": 0,
                                           "official": 0, "other_only": 0, "no_link": 0, "stale": 0,
                                           "non_official_hosts": set(), "scan": Counter(), "files": []})
        txt = reader(f)
        a = analyse(txt)
        t["pages"] += 1
        for k in ("tables", "rows", "official", "other_only", "no_link"):
            t[k] += a[k]
        t["stale"] += len(a["stale"])
        t["non_official_hosts"] |= set(a["non_official_hosts"])
        for _, cat, _tok in ps.scan_text(txt):
            t["scan"][cat] += 1
        t["files"].append((f, a))
    return trees


PROBES = [  # (constant id, label, substring that the page must contain to "show" it)
    ("K01", "Federal exclusion 2026 (15,000,000)", "15,000,000"),
    ("K02", "Federal exclusion 2027 (15,480,000)", "15,480,000"),
    ("K13", "Prop 19 allowance (1,044,586)", "1,044,586"),
    ("K15", "Prop 13 factor basis (CCPI 3.307%)", "3.307"),
    ("K20", "SF FY2026-27 rate (1.18162182%)", "1.18162182"),
    ("K21", "CDI average premium (1,571)", "1,571"),
    ("K22", "CDI 2025 homeowners average (2,339.99)", "2,339.99"),
    ("K19", "Small-estate limit, current (208,850)", "208,850"),
]


def constants_matrix(trees):
    out = []
    for cid, label, needle in PROBES:
        row = {"id": cid, "label": label, "cells": {}}
        for name, t in trees.items():
            if not t["published"] and name not in ("desk-b4f",):
                continue
            row["cells"][name] = any(needle in a["text"] for _f, a in t["files"])
        out.append(row)
    return out


def working_tree():
    files = [f for f in _git("ls-files", "*.html").splitlines() if f]
    excludes = excluded_names((ROOT / "_config.yml").read_text(encoding="utf-8"))

    def label(f):
        parts = f.split("/")
        return parts[0] if len(parts) > 1 else "(root)"

    trees = scan_tree(files, lambda f: (ROOT / f).read_text(encoding="utf-8", errors="replace"), excludes, label)
    return trees, excludes


def branches():
    out = {}
    for b in LIVE_BRANCHES:
        ref = f"origin/arena/{b}-tino5"
        if not _git("rev-parse", "--verify", "-q", ref).strip():
            continue
        changed = [f for f in _git("diff", "--name-only", f"origin/main...{ref}").splitlines() if f]
        html = [f for f in changed if f.endswith(".html")]
        last = _git("log", "-1", "--format=%cI", ref).strip()
        out[b] = {"files": len(changed), "html": len(html), "last_commit": last, "changed": changed}
    return out


def run_all():
    trees, excludes = working_tree()
    return {"trees": trees, "excludes": sorted(excludes), "matrix": constants_matrix(trees), "branches": branches()}


if __name__ == "__main__":
    res = run_all()
    for name, t in sorted(res["trees"].items()):
        print(f"{name:22} published={str(t['published']):5} pages={t['pages']:3} rows={t['rows']:4} official={t['official']:4} "
              f"other_only={t['other_only']:3} no_link={t['no_link']:3} stale={t['stale']} scan={dict(t['scan'])}")
    print()
    for r in res["matrix"]:
        print(r["id"], r["label"], r["cells"])
    print()
    for b, v in res["branches"].items():
        print(b, v["files"], "files,", v["html"], "html, last", v["last_commit"])
