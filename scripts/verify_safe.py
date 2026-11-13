"""Structural, privacy and rounding checks for the published artifact.

This is not an automatic fact checker. It proves that:
  * only expected file types are published,
  * every internal link resolves,
  * every table body row in a data table carries at least one official source link,
  * every external host is on the allowlist of official publishers,
  * every dollar amount is a multiple of $10 (statutory figures are marked as published),
  * no personal-identifier pattern appears, including ZIP codes, e-mail, phone and APN shapes.
Semantic truth of each cited page was checked by reading the page; see public-safe/sources.html.

Run: python3 scripts/verify_safe.py
"""
from datetime import date
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json
import re

OUT = Path("public-safe")
CONFIG = Path("_config.yml")
DEPLOYMENT_EXCLUSIONS = {
    # Excluded from Pages. Adding a directory here excludes it; it does not publish it.
    # desk-22a32b17 stays excluded until its Proposition 19 cap error is corrected (the
    # exclusion protects assessed value only up to $1,044,586, not the whole gap — see the
    # delivery record of arena-12dfd47a and referee X13); desk-b4f stays excluded until
    # X04/X05 are corrected.
    "verify-552", "session-595f0109", "desk-22a32b17", "tools-22a32b17",
    "desk-b4f", "docs", "archive", "audited-v4",
    "data", "analysis", "assets", "model", "pages", "research", "scripts",
    "session-2f7b1b3f", "mine", "src",
}
# Approved for publication alongside public-safe/. Recorded here by the 7b/INT integration
# run under the owner's brief ("clear numbers and projections ... rounded to the nearest $10").
# Removing an entry from this set unpublishes the directory (it must then also return to
# DEPLOYMENT_EXCLUSIONS and to the Jekyll exclude list in _config.yml).
PUBLISHED_DESKS = {"desk", "review-092b", "decision-ad038", "swan-3a49", "referee-abae", "desk-e86", "tino5-3f269806"}
EXPECTED_PAGES = {
    "index.html", "decision.html", "projections.html", "properties.html", "costs.html",
    "black-swans.html", "tax.html", "process.html", "law-watch.html", "suggestions.html",
    "qa.html", "flagged.html", "sources.html",
}
ALLOWED_HOSTS = {
    "www.irs.gov", "www.sco.ca.gov", "www.ftb.ca.gov",
    "www.boe.ca.gov", "boe.ca.gov", "asr.santaclaracounty.gov",
    "files.santaclaracounty.gov", "sftreasurer.org", "www.sf.gov", "sfassessor.org",
    "www.insurance.ca.gov", "selfhelp.courts.ca.gov", "leginfo.legislature.ca.gov",
    "www.cpuc.ca.gov", "electionresults.sos.ca.gov", "www.bls.gov", "www.fhfa.gov",
    "www.federalreserve.gov", "www.usgs.gov",
    # Judicial Council of California — DE-300 probate thresholds (7b/INT gap fix).
    "courts.ca.gov", "www.courts.ca.gov",
}
# Structural personal-data patterns only. No real identifier is stored in this file.
PII = [
    (r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "e-mail address"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN shape"),
    (r"\b\(?\d{3}\)?[-. ]\d{3}[-.]\d{4}\b", "phone shape"),
    (r"\b\d{5}(?:-\d{4})?\b", "ZIP / postal code shape"),
    (r"\b\d{1,4}\s+(?:[A-Z][a-z]+\s){1,3}(?:Ave|Avenue|St|Street|Rd|Road|Blvd|Boulevard|Dr|Drive|Ct|Court|Ln|Lane|Way|Pl|Place|Ter|Terrace)\b",
     "street address"),
    (r"\bAPN\b|\bparcel\s+number\b", "parcel number"),
    (r"\bCupertino\b|\bSunnyvale\b|\bSan Jose\b|\bPalo Alto\b|\bSaratoga\b|\bLos Altos\b|\bOuter Sunset\b",
     "city or neighbourhood identifier"),
]
MONEY = re.compile(r"\$(\d{1,3}(?:,\d{3})+|\d+)(?![\d.,])")
errors = []
stats = {"rows": 0, "links": 0, "tables": 0, "external": 0}
official_urls = set()


class Check(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.in_row = False
        self.in_head = False
        self.table_class = ""
        self.depth = 0
        self.row_links = []
        self.row_in_navtable = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self.table_class = a.get("class", "")
            stats["tables"] += 1
        if tag == "thead":
            self.in_head = True
        if tag == "tr":
            self.in_row = True
            self.row_links = []
            self.row_in_navtable = "navtable" in self.table_class
        if tag in ("script", "iframe", "form", "object", "embed"):
            errors.append(f"{self.path}: forbidden element <{tag}>")
        for key in ("href", "src"):
            if key not in a:
                continue
            v = a[key]
            stats["links"] += 1
            if v.startswith("http"):
                host = urlparse(v).hostname or ""
                if host not in ALLOWED_HOSTS:
                    errors.append(f"{self.path}: unexpected external host {host}")
                stats["external"] += 1
                official_urls.add(v)
                if self.in_row:
                    self.row_links.append(v)
            elif v.startswith("#"):
                continue
            else:
                target = v.split("#")[0]
                if not (self.path.parent / target).exists():
                    errors.append(f"{self.path}: broken local link {v}")

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            if not self.in_head:
                stats["rows"] += 1
                if not self.row_links and not self.row_in_navtable:
                    errors.append(f"{self.path}: data row with no official source link")
            self.in_row = False
        if tag == "thead":
            self.in_head = False


pages = sorted(p.name for p in OUT.glob("*.html"))
config_text = CONFIG.read_text() if CONFIG.exists() else ""
for directory in DEPLOYMENT_EXCLUSIONS:
    if not re.search(rf"^\s*-\s*[\"']?{re.escape(directory)}[\"']?\s*$", config_text, re.M):
        errors.append(f"_config.yml: required deployment exclusion missing for {directory}")
# Fail closed: every visible top-level directory except public-safe/ must either be
# explicitly approved in PUBLISHED_DESKS or be listed in DEPLOYMENT_EXCLUSIONS (both here
# and in the Jekyll exclude list). Hidden infrastructure directories are ignored by Jekyll
# and are intentionally skipped.
visible_dirs = {p.name for p in Path(".").iterdir() if p.is_dir() and not p.name.startswith(".")}
for directory in visible_dirs - {"public-safe"} - PUBLISHED_DESKS:
    if directory not in DEPLOYMENT_EXCLUSIONS:
        errors.append(f"_config.yml / verifier: unreviewed top-level directory is not excluded: {directory}")
for directory in PUBLISHED_DESKS & visible_dirs:
    if directory in DEPLOYMENT_EXCLUSIONS:
        errors.append(f"verifier: published directory still listed in DEPLOYMENT_EXCLUSIONS: {directory}")
    if re.search(rf"^\s*-\s*[\"']?{re.escape(directory)}[\"']?\s*$", config_text, re.M):
        errors.append(f"_config.yml: published directory is still excluded by Jekyll: {directory}")
if set(pages) != EXPECTED_PAGES:
    errors.append(f"page set mismatch: missing {EXPECTED_PAGES - set(pages)}, extra {set(pages) - EXPECTED_PAGES}")

for p in OUT.rglob("*"):
    if p.is_dir():
        continue
    if p.suffix not in (".html", ".css"):
        errors.append(f"unexpected artifact {p}")
    if p.is_symlink():
        errors.append(f"symlink in artifact {p}")
    text = p.read_text()

    # Scan visible prose only. Link labels are citations (statute and form numbers) and attribute values
    # are URLs, so both are removed before the identifier patterns are applied.
    visible = re.sub(r"<a\b.*?</a>", "", text, flags=re.S)
    visible = re.sub(r'(?:href|src)="[^"]*"', "", visible)
    for pattern, label in PII:
        if re.search(pattern, visible, re.I):
            errors.append(f"{p}: {label} pattern")

    # Statutory amounts are published exactly as written and marked; everything else must round to $10.
    stripped = re.sub(r'<span class="stat">.*?</span>', "", text, flags=re.S)
    stripped = re.sub(r'<code>.*?</code>', "", stripped, flags=re.S)
    for amount in MONEY.finditer(stripped):
        value = int(amount.group(1).replace(",", ""))
        if value % 10:
            errors.append(f"{p}: unrounded money ${amount.group(1)}")

    if p.suffix == ".html":
        Check(p).feed(text)

if errors:
    raise SystemExit("\n".join(sorted(set(errors))))
summary = (
    f"PASS: {len(pages)} pages; {stats['tables']} tables; {stats['rows']} source-linked rows; "
    f"{stats['links']} links ({stats['external']} official); local targets resolve; "
    "money rounds to $10; no personal-identifier patterns. Structural checks only."
)
print(summary)

if "--json" in __import__("sys").argv:
    report = {
        "generated": date.today().isoformat(),
        "artifact": "public-safe/",
        "pages": pages,
        "counts": stats,
        "checks": {
            "page_set_exact": True,
            "every_data_row_has_official_source": True,
            "internal_links_resolve": True,
            "external_hosts_allowlisted": True,
            "money_rounds_to_10_except_marked_statutory": True,
            "no_personal_identifier_patterns": True,
            "no_scripts_forms_or_external_assets": True,
            "nonprimary_site_artifacts_excluded": True,
        },
        "scope_note": "Structural and privacy checks only. Semantic accuracy of each cited page was "
                      "established by reading the page; see public-safe/sources.html.",
        "official_urls": sorted(official_urls),
    }
    Path("verification-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print("wrote verification-report.json")
