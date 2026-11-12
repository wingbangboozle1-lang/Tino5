"""Checks on the generated pages. Run:  python3 -m unittest discover -s referee-abae/_src -p 'test_*.py' -v

These tests enforce the project's privacy and verification rules on this folder's own output:
  - every data row of every table carries a link to an official host;
  - no dollar figure that comes from household inputs appears (the desk anchors are read at run time, in memory);
  - no place names, ZIP-like codes, e-mail addresses or parcel-number shapes in visible text;
  - repository privacy scan finds nothing; relative links resolve; the build is deterministic.
"""
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(HERE))
import crosscheck as C  # noqa: E402
import engine as E  # noqa: E402
import reproduce as RP  # noqa: E402

PAGES = ["index", "constants", "traceability", "robustness", "baselines", "discrepancies", "flagged"]
PLACES = ["cupertino", "san jose", "santa clara", "san francisco", "sunnyvale", "los altos", "saratoga"]


class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.t, self.skip = [], 0
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self.skip += 1
        for k, v in attrs:
            if k == "href":
                self.hrefs.append(v)

    def handle_endtag(self, tag):
        if tag in ("style", "script") and self.skip:
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip:
            self.t.append(d)


def visible(slug):
    p = Visible()
    p.feed((OUT / f"{slug}.html").read_text(encoding="utf-8"))
    return re.sub(r"\s+", " ", " ".join(p.t)), p.hrefs


class Pages(unittest.TestCase):
    def test_pages_exist(self):
        for s in PAGES:
            self.assertTrue((OUT / f"{s}.html").exists(), s)
        self.assertTrue((OUT / "style.css").exists())

    def test_every_row_has_an_official_link(self):
        for s in PAGES:
            a = C.analyse((OUT / f"{s}.html").read_text(encoding="utf-8"))
            self.assertGreater(a["rows"], 0, s)
            self.assertEqual(a["official"], a["rows"], f"{s}: rows without an official link")
            self.assertEqual(a["non_official_hosts"], [], s)

    def test_no_places_or_identifiers(self):
        for s in PAGES:
            txt, _ = visible(s)
            low = txt.lower()
            for w in PLACES:
                self.assertNotIn(w, low, f"{s}: {w}")
            self.assertFalse(re.search(r"(?<![\d.,$])9[0-9]{4}(?![\d.,])", txt), f"{s}: ZIP-like token")
            self.assertFalse(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", txt), f"{s}: e-mail")
            self.assertFalse(re.search(r"\b\d{3}-\d{2}-\d{3,4}\b", txt), f"{s}: parcel/SSN shape")

    def test_repository_privacy_scan_is_clean(self):
        ps = C._privacy_scan()
        for s in PAGES:
            raw = (OUT / f"{s}.html").read_text(encoding="utf-8")
            bad = [(c, t) for _, c, t in ps.scan_text(raw) if c not in ("official-constant", "minor-under-1000")]
            self.assertEqual(bad, [], s)
        for f in HERE.glob("*.py"):
            raw = f.read_text(encoding="utf-8")
            bad = [(c, t) for _, c, t in ps.scan_text(raw) if c not in ("official-constant", "minor-under-1000")]
            self.assertEqual(bad, [], f.name)

    def test_no_household_dollar_levels(self):
        desk = RP.load_desk_module()
        if desk is None:
            self.skipTest("desk module not present")
        p = RP.params_from_desk(desk)
        official = {p.hox, p.allowance0}
        anchors = {p.v0, p.taxable0, p.fixed, p.insurance, p.water, p.maint, p.reserve, p.rent0, abs(p.elec_pre), p.elec_post} - official
        found = set()
        for T in (2040, 2045, 2050):
            x = E.run(p, T)
            for k in ("fmv_T", "S1", "S2", "S3", "assess_occ", "taxable_pre", "allowance", "proceeds", "rent_y1", "tax_occ_y1", "tax_rent_y1"):
                found.add(x[k])
            found.add(x["S3"] - x["S2"])
        needles = set()
        for v in anchors | found:
            v = abs(v)
            if v < 1000:
                continue
            for r in (int(round(v)), int(round(v / 10.0) * 10), int(v)):
                needles.add(f"{r:,}")
                needles.add(str(r))
        blob = " ".join(visible(s)[0] for s in PAGES) + " ".join((OUT / f"{s}.html").read_text(encoding="utf-8") for s in PAGES)
        hits = [n for n in needles if re.search(r"(?<![\d,.])" + re.escape(n) + r"(?![\d,])", blob)]
        self.assertEqual(hits, [], "household-derived level appears in a page (values withheld)")

    def test_relative_links_resolve(self):
        for s in PAGES:
            _, hrefs = visible(s)
            for h in hrefs:
                if h.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                target = (OUT / h).resolve()
                if h in ("../", ".."):
                    self.assertTrue(OUT.parent.exists())
                    continue
                self.assertTrue(target.exists(), f"{s}: broken link {h}")

    def test_only_https_links(self):
        for s in PAGES:
            for h in visible(s)[1]:
                self.assertFalse(h.startswith("http://"), f"{s}: {h}")

    def test_build_is_deterministic(self):
        import build
        before = {s: (OUT / f"{s}.html").read_bytes() for s in PAGES}
        build.main()
        after = {s: (OUT / f"{s}.html").read_bytes() for s in PAGES}
        self.assertEqual(before, after)


class Register(unittest.TestCase):
    def test_every_constant_has_a_source_and_status(self):
        import registry as R
        ids = [c[0] for c in R.CONSTANTS]
        self.assertEqual(len(ids), len(set(ids)))
        for cid, topic, val, keys, status, used, note in R.CONSTANTS:
            self.assertTrue(keys, cid)
            self.assertIn(status, ("opened", "secondary", "transcribed"), cid)
            for k in keys:
                self.assertIn(k, R.L, f"{cid}: unknown link {k}")
                self.assertTrue(R.is_official(__import__("urllib.parse").parse.urlparse(R.L[k][1]).hostname), f"{cid}: {k} not official")

    def test_links_are_https_and_unique_labels(self):
        import registry as R
        labels = [v[0] for v in R.L.values()]
        self.assertEqual(len(labels), len(set(labels)))
        for k, (label, url) in R.L.items():
            self.assertTrue(url.startswith("https://"), k)


if __name__ == "__main__":
    unittest.main()
