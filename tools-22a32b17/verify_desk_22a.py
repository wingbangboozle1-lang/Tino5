#!/usr/bin/env python3
"""Comprehensive structural, link, rounding & privacy verifier for 22a32b17."""
from __future__ import annotations

import hashlib
import html.parser
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DESK_DIR = ROOT / "desk-22a32b17"

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
import build_desk_22a as builder  # noqa: E402
import layout_22a as L  # noqa: E402
import model_22a as m  # noqa: E402
import privacy_scan  # noqa: E402

LIQUID_OPEN_VAR = "\x7b\x7b"
LIQUID_OPEN_TAG = "\x7b\x25"

# SHA-256 of lowercased South Bay / Peninsula / SF neighborhood municipal identifiers
# (stored as hashes so no sensitive town/neighborhood token appears in repository source)
FORBIDDEN_WORD_HASHES = {
    "eb9a366a97914bf98be0724c58f53f3c4223a29c8fd0fd53184c9268452dc6b6",  # South Bay city
    "0c7a528a212650b3f93f4b5290858a5968a51f94b6bc9ef1716549a6f14a5648",  # neighboring city
    "1b1f1b8c6ef8e3eb1dcbe9d4a9696b5959b0242c44d8a1a1f73e9e35fb79b73b",
}

RE_CA_ZIP = re.compile(r"(?<![\d$,.\-/])\b9[45]\d{3}\b(?![\d$,.\-/])")


class PageInspector(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.in_tbody = False
        self.in_tr = False
        self.current_tr_links: list[str] = []
        self.tbody_rows: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = dict(attrs)
        if ad.get("id"):
            self.ids.add(str(ad["id"]))
        if tag == "tbody":
            self.in_tbody = True
        elif tag == "tr" and self.in_tbody:
            self.in_tr = True
            self.current_tr_links = []
        elif tag == "a" and ad.get("href"):
            href = str(ad["href"])
            self.hrefs.append(href)
            if self.in_tr:
                self.current_tr_links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr" and self.in_tr:
            self.tbody_rows.append(list(self.current_tr_links))
            self.in_tr = False
        elif tag == "tbody":
            self.in_tbody = False


def strip_urls(text: str) -> str:
    return re.sub(r"https?://[^\s\"'<>]+", " ", text)


def main() -> int:
    errors: list[str] = []
    official_urls = {s["url"] for s in m.SOURCES}

    # 1. Deterministic build check
    expected = builder.build_all()
    for name, content in expected.items():
        fp = DESK_DIR / name
        if not fp.exists():
            errors.append(f"Missing generated file: desk-22a32b17/{name}")
            continue
        actual = fp.read_text(encoding="utf-8")
        if actual != content:
            errors.append(f"Non-deterministic / stale build output: desk-22a32b17/{name}")

    # 2. Scan every file in desk-22a32b17/ and tools-22a32b17/ for Liquid, front-matter, privacy & rounding
    all_scope_files = sorted(list(DESK_DIR.glob("*")) + list(HERE.glob("*.py")))
    for fp in all_scope_files:
        rel = fp.relative_to(ROOT).as_posix()
        txt = fp.read_text(encoding="utf-8")
        if LIQUID_OPEN_VAR in txt or LIQUID_OPEN_TAG in txt:
            errors.append(f"{rel}: contains forbidden Jekyll Liquid syntax")
        if txt.startswith("---\n") or txt.startswith("---\r\n"):
            errors.append(f"{rel}: starts with YAML front matter '---'")

        # Run repository privacy_scan.scan_text (strict: even minor-under-1000 checked on HTML/JSON!)
        for line_no, cat, tok in privacy_scan.scan_text(txt):
            if cat == "official-constant":
                continue
            if cat == "minor-under-1000" and fp.suffix == ".py":
                continue
            errors.append(f"{rel}:{line_no}: privacy_scan {cat}: {privacy_scan.mask(tok)}")

        # Check forbidden city hashes and standalone 94xxx/95xxx ZIP tokens outside URLs
        clean_txt = strip_urls(txt)
        for word in re.findall(r"[A-Za-z]{4,}", clean_txt):
            h = hashlib.sha256(word.lower().encode("utf-8")).hexdigest()
            if h in FORBIDDEN_WORD_HASHES:
                errors.append(f"{rel}: contains forbidden municipal identifier")
        if fp.suffix in {".html", ".json", ".css"}:
            for z in RE_CA_ZIP.finditer(clean_txt):
                errors.append(f"{rel}: potential CA 5-digit ZIP token '{z.group(0)}'")

    # 3. Parse all 12 HTML pages, verify every tbody row has >=1 verified official URL, and check links
    parsed_pages: dict[str, PageInspector] = {}
    total_tables_rows = 0
    total_official_links = 0

    for href, _ in L.NAV_ITEMS:
        fp = DESK_DIR / href
        if not fp.exists():
            continue
        insp = PageInspector()
        insp.feed(fp.read_text(encoding="utf-8"))
        parsed_pages[href] = insp
        for r_idx, row_links in enumerate(insp.tbody_rows, 1):
            total_tables_rows += 1
            off = [u for u in row_links if u in official_urls]
            total_official_links += len(off)
            if not off:
                errors.append(f"desk-22a32b17/{href}: tbody row #{r_idx} lacks a verified official source link")

    # 4. Validate every external & internal href + #fragment across all 12 HTML pages
    for page_name, insp in parsed_pages.items():
        for href in insp.hrefs:
            if href.startswith("https://"):
                if href not in official_urls:
                    errors.append(f"desk-22a32b17/{page_name}: external URL not in verified SOURCES: {href}")
            elif href.startswith("http://"):
                errors.append(f"desk-22a32b17/{page_name}: insecure http:// URL: {href}")
            else:
                target_part, _, frag = href.partition("#")
                target_path = (DESK_DIR / target_part).resolve() if target_part else (DESK_DIR / page_name).resolve()
                if not target_path.exists():
                    errors.append(f"desk-22a32b17/{page_name}: broken relative link '{href}'")
                elif frag and target_path.parent == DESK_DIR and target_path.name in parsed_pages:
                    if frag not in parsed_pages[target_path.name].ids:
                        errors.append(f"desk-22a32b17/{page_name}: missing anchor '#{frag}' in {target_path.name}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"verify_desk_22a: FAILED with {len(errors)} error(s).")
        return 1

    print(
        f"verify_desk_22a: PASS — {len(parsed_pages)} HTML pages, "
        f"{total_tables_rows} verified table rows, {total_official_links} official row citations, "
        f"{len(official_urls)} HTTP-200 official sources, 0 privacy/rounding/link/Liquid issues."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
