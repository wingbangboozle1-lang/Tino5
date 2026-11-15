"""Structural, privacy and rounding checks for the live Pages surfaces.

This is not an automatic fact checker. It proves that:
  * only the curated desks are configured for publication,
  * every internal link resolves,
  * every public-safe table row carries an official source link,
  * external hosts in the public-safe reference are on the official allowlist,
  * money in the public-safe reference rounds to $10 unless marked as published, and
  * the root hub and every selected live desk contain no known personal-identifier pattern.
The cbe/ and phase-99220/ semantic, sourcing, rounding and link checks run in their own
verifiers; this gate additionally scans their entire published trees for privacy patterns.
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
    # Excluded from Pages. Exclusion is not deletion and does not scrub Git history.
    # Older independent desks are retained for audit but are not served: the live site uses
    # one reconciled model (cbe/) plus its historical phased-entry supplement (phase-99220/).
    "verify-552", "session-595f0109", "desk-22a32b17", "tools-22a32b17",
    "desk-b4f", "docs", "archive", "audited-v4",
    "data", "analysis", "assets", "model", "pages", "research", "scripts",
    "session-2f7b1b3f", "mine", "src",
    "desk", "review-092b", "decision-ad038", "swan-3a49", "referee-abae",
    "desk-e86", "tino5-3f269806", "verify-476", "decision", "desk-d75",
    "cbd", "inheritance-desk", "desk-8be2", "desk-31cb5781",
}
# The curated live set alongside public-safe/. To unpublish a directory, move it into
# DEPLOYMENT_EXCLUSIONS and _config.yml's exclude list in the same integration change.
# cbe/ is the primary decision model; phase-99220/ provides the historical 1929/2008
# crash-entry replay; desk-9af5443d/ adds the official tax, local-measure and evidence gaps
# specifically requested in the owner brief. The other completed desks remain in Git for
# audit but are not served as competing versions.
PUBLISHED_DESKS = {"cbe", "phase-99220", "desk-9af5443d"}
PUBLISHED_SITE_DIRS = {"public-safe"} | PUBLISHED_DESKS
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
    # phase-99220 (arena-99220bc7): Treasury yields, FRED, Federal Reserve History, SFPUC link (flagged, not opened).
    "home.treasury.gov", "fred.stlouisfed.org", "www.federalreservehistory.org", "www.sfpuc.org",
    # Judicial Council of California — DE-300 probate thresholds (7b/INT gap fix).
    "courts.ca.gov", "www.courts.ca.gov",
    # desk-9af5443d (arena-9af5443d): Census ACS QuickFacts, SF Department of Elections,
    # SFMTA, NBER, San Jose Water, SFPUC, California FAIR Plan.
    "census.gov", "sfelections.org", "sfmta.com", "nber.org", "sjwater.com", "sfpuc.gov", "cfpnet.com",
}
# Structural personal-data patterns only. No real identifier is stored in this file.
PII = [
    (r"[\w.+-]+@[\w-]+\.[a-z]{2,}", "e-mail address"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN shape"),
    (r"\b\(?\d{3}\)?[-. ]\d{3}[-.]\d{4}\b", "phone shape"),
    (r"\b\d{5}(?:-\d{4})?(?!\d)(?!\.\d)", "ZIP / postal code shape"),
    (r"\b\d{1,4}\s+(?:[A-Z][a-z]+\s){1,3}(?:Ave|Avenue|St|Street|Rd|Road|Blvd|Boulevard|Dr|Drive|Ct|Court|Ln|Lane|Way|Pl|Place|Ter|Terrace)\b",
     "street address"),
    (r"\b(?:APN|parcel\s+number)\s*[:#]?\s*(?:\d[\w-]{4,}|[A-Z0-9][A-Z0-9-]{5,})\b", "parcel identifier"),
    # Broad county references and official source titles are general jurisdiction context;
    # a city/neighbourhood name used to locate either property is still rejected.
    (r"\bCupertino\b|\bSunnyvale\b|\bSan Jose\b|\bPalo Alto\b|\bSaratoga\b|\bLos Altos\b|\bOuter Sunset\b|\bSan Francisco\b(?!\s+(?:County|Treasurer|secured))",
     "city or neighbourhood identifier"),
]


def has_identifier_pattern(text, pattern, label):
    """Avoid treating visible statutory section citations as postal codes."""
    for match in re.finditer(pattern, text, re.I):
        if label == "ZIP / postal code shape":
            prefix = text[max(0, match.start() - 72):match.start()]
            if re.search(r"(?:§\s*|(?:section|code|R&TC)\s*)$", prefix, re.I):
                continue
        return True
    return False


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

    # Statutory amounts are published exactly as written and marked; everything else must round to $10.
    stripped = re.sub(r'<span class="stat">.*?</span>', "", text, flags=re.S)
    stripped = re.sub(r'<code>.*?</code>', "", stripped, flags=re.S)
    for amount in MONEY.finditer(stripped):
        value = int(amount.group(1).replace(",", ""))
        if value % 10:
            errors.append(f"{p}: unrounded money ${amount.group(1)}")

    if p.suffix == ".html":
        Check(p).feed(text)

# Scan the complete Pages surface, including visible link labels and the root landing page.
# Jekyll does not publish underscore-prefixed working directories (including _src/).
robots_path = Path("robots.txt")
if not robots_path.is_file():
    errors.append("robots.txt: missing crawler restriction")
else:
    robots_text = robots_path.read_text(encoding="utf-8")
    if not re.search(r"(?m)^User-agent:\s*\*\s*$", robots_text):
        errors.append("robots.txt: missing wildcard User-agent")
    if not re.search(r"(?m)^Disallow:\s*/\s*$", robots_text):
        errors.append("robots.txt: missing site-wide Disallow")
privacy_scanned_files = 0
privacy_roots = [Path("index.html")] + [Path(d) for d in sorted(PUBLISHED_SITE_DIRS)]
for root in privacy_roots:
    if not root.exists():
        errors.append(f"missing published surface: {root}")
        continue
    files = [root] if root.is_file() else sorted(root.rglob("*"))
    for p in files:
        if p.is_dir():
            continue
        if p.is_symlink():
            errors.append(f"symlink in published surface: {p}")
            continue
        if root.is_dir() and any(part.startswith("_") for part in p.relative_to(root).parts):
            continue
        if p.suffix.lower() not in {".html", ".css", ".js"}:
            errors.append(f"unexpected published artifact: {p}")
            continue
        text = p.read_text(encoding="utf-8")
        # Scan rendered prose, including anchor labels; skip non-visible inline CSS/JS and
        # color literals so a six-digit stylesheet color cannot look like a postal code.
        if p.suffix.lower() == ".html":
            prose = re.sub(r"<(style|script)\b[^>]*>.*?</\1>", " ", text, flags=re.I | re.S)
            visible = re.sub(r"<[^>]*>", " ", prose)
        else:
            visible = text
        visible = re.sub(r"#[0-9a-fA-F]{3,8}\b", " ", visible)
        for pattern, label in PII:
            if has_identifier_pattern(visible, pattern, label):
                errors.append(f"{p}: {label} pattern")
        privacy_scanned_files += 1

if errors:
    raise SystemExit("\n".join(sorted(set(errors))))
summary = (
    f"PASS: {len(pages)} public-safe pages; {stats['tables']} public-safe tables; "
    f"{stats['rows']} source-linked rows; {stats['links']} links ({stats['external']} official); "
    f"{privacy_scanned_files} live files privacy-scanned; local targets resolve; "
    "robots.txt requests no crawling (not access control); public-safe money rounds to $10; "
    "no known personal-identifier patterns. Structural checks only."
)
print(summary)

if "--json" in __import__("sys").argv:
    report = {
        "generated": date.today().isoformat(),
        "artifact": "GitHub Pages root + public-safe/, cbe/, phase-99220/",
        "pages": pages,
        "privacy_scanned_files": privacy_scanned_files,
        "counts": stats,
        "checks": {
            "page_set_exact": True,
            "every_data_row_has_official_source": True,
            "internal_links_resolve": True,
            "external_hosts_allowlisted": True,
            "money_rounds_to_10_except_marked_statutory": True,
            "no_personal_identifier_patterns": True,
            "robots_disallows_crawling": True,
            "no_scripts_forms_or_external_assets": True,
            "nonprimary_site_artifacts_excluded": True,
        },
        "scope_note": "Structural/privacy checks plus the cbe/ and phase-99220/ page-specific verifiers. "
                      "Official sources and what each supports are linked from cbe/sources.html and "
                      "phase-99220/sources.html; no automatic verifier proves legal interpretation.",
        "official_urls": sorted(official_urls),
    }
    Path("verification-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print("wrote verification-report.json")
