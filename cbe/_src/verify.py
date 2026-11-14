# -*- coding: utf-8 -*-
"""Structural, privacy and sourcing verification for the owner-brief desk.

Run:   python3 cbe/_src/verify.py            (prints a report, non-zero exit on failure)
       python3 cbe/_src/build.py             (builds, then runs this)

The published artifact is static HTML and CSS only. These checks are what make that a
guarantee rather than an intention, and they are the strictest checks applied anywhere
in this repository: an earlier desk let an identifying city and county pairing reach the
live hub because its verifier did not look for it.

  V1  every table body row links an official source or carries a "no official source" marker
  V2  every external link points at a host on the official allowlist
  V3  every internal link resolves to a page that exists
  V4  every money figure is a multiple of $10, except statutory literals quoted verbatim
  V5  no personal or geographic identifier
  V6  no NaN, Infinity, None or undefined leaked into the output
  V7  no script, iframe, form, embedded object, external asset or inline event handler
  V8  the source register is internally consistent
  V9  every page carries the privacy banner, the full navigation and the robots directives
"""

import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import shell as sh             # noqa: E402
import sources as src          # noqa: E402

# --------------------------------------------------------------------------- config

STATUTORY_LITERALS = src.STATUTORY_LITERALS | {v.replace(",", "") for v in src.STATUTORY_LITERALS}

# Money followed by a scale word is a quotation from an official document about a public
# aggregate ("$89 billion for local government"), not a household figure.
SCALE = re.compile(r"^\$\s?[\d,]+(?:\.\d+)?\s*(?:million|billion|trillion|thousand)\b", re.I)

MONEY = re.compile(r"\$\s?([\d,]+)(?:\.(\d+))?")

# Anything that could identify the owner, the properties or the area.
PII = [
    (r"(?i)\bcupertino\b", "city"),
    (r"(?i)\bsunnyvale\b", "city"),
    (r"(?i)\bsan jose\b", "city"),
    (r"(?i)\bpalo alto\b", "city"),
    (r"(?i)\bsaratoga\b", "city"),
    (r"(?i)\blos altos\b", "city"),
    (r"(?i)\bsanta clara\b", "county"),
    (r"(?i)\bouter sunset\b", "neighbourhood"),
    (r"(?i)\bsan francisco\b", "city"),
    (r"\b9[45]\d{3}(?:-\d{4})?\b", "postcode"),
    (r"(?i)\b(?:assessor(?:'s)?\s+parcel|parcel\s+(?:number|no\.?|id)|apn)\b\s*[:#]?\s*[\w-]+",
     "parcel identifier"),
    (r"(?i)\baccount\s*(?:number|no\.?|#)\b\s*[:#]?\s*[\w-]+", "account number"),
    (r"\b\d{1,6}\s+(?:[NSEW]\.?\s+)?[A-Z][a-z]+\s+(?:St|Ave|Street|Avenue|Road|Rd|Drive|Dr|Court|"
     r"Ct|Lane|Ln|Way|Boulevard|Blvd|Place|Pl)\b\.?", "street address"),
    (r"\b[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}\s+(?:Family|Revocable|Living)\s+Trust\b", "named trust"),
    (r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "email address"),
    (r"\b\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "telephone number"),
]

FORBIDDEN_MARKUP = [
    (re.compile(r"<\s*script\b", re.I), "script tag"),
    (re.compile(r"<\s*iframe\b", re.I), "iframe"),
    (re.compile(r"<\s*form\b", re.I), "form"),
    (re.compile(r"<\s*(?:img|object|embed|video|audio|source|track)\b", re.I), "embedded asset"),
    (re.compile(r"<\s*link\b[^>]*rel\s*=\s*['\"]?stylesheet", re.I), "external stylesheet"),
    (re.compile(r"<\s*link\b", re.I), "link tag (only external stylesheets are allowed)"),
    (re.compile(r"\son[a-z]+\s*=", re.I), "inline event handler"),
    (re.compile(r"\bjavascript\s*:", re.I), "javascript: URL"),
    (re.compile(r"<\s*input\b|<\s*textarea\b|<\s*select\b|<\s*button\b", re.I), "form control"),
]

BAD_VALUES = [
    (re.compile(r"\bnan\b", re.I), "nan"),
    (re.compile(r"\binf(?:inity)?\b", re.I), "infinity"),

    (re.compile(r"\bundefined\b"), "undefined"),
    (re.compile(r"\bTraceback\b"), "traceback"),
]


# ---------------------------------------------------------------------------- parse

class Doc(HTMLParser):
    """Collects rows, links, attributes and text from one page."""

    def __init__(self, name, raw):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.name = name
        self.raw = raw
        self.rows = []          # list of row dicts, only inside <tbody>
        self.links = []         # (href, text)
        self.attrs = []         # (tag, attr, value)
        self.text_parts = []
        self._in_tbody = 0
        self._row = None
        self._cell = None
        self._capture = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for k, v in attrs:
            self.attrs.append((tag, k, v or ""))
        if tag == "tbody":
            self._in_tbody += 1
        elif tag == "tr" and self._in_tbody:
            self._row = dict(cells=[], html=[], line=self.getpos()[0])
        elif tag == "td" and self._row is not None:
            self._cell = []
        if tag == "a" and d.get("href"):
            self._capture = [d["href"], []]
        # Markers so a row can be checked for what it LINKS, not just for what it says.
        if self._cell is not None:
            if tag == "a" and d.get("href"):
                self._cell.append(" href=%s " % d["href"])
            elif tag == "span" and "nosrc" in (d.get("class") or ""):
                self._cell.append(" NOSRC-MARKER ")

    def handle_endtag(self, tag):
        if tag == "tbody" and self._in_tbody:
            self._in_tbody = max(0, self._in_tbody - 1)
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None
        elif tag == "td" and self._cell is not None:
            self._row["cells"].append("".join(self._cell))
            self._cell = None
        elif tag == "a" and self._capture:
            self.links.append((self._capture[0], "".join(self._capture[1])))
            self._capture = None

    def handle_data(self, data):
        self.text_parts.append(data)
        if self._cell is not None:
            self._cell.append(data)
        if self._capture:
            self._capture[1].append(data)


# ---------------------------------------------------------------------------- checks

def load_pages():
    names = [fn for fn, _, _ in sh.PAGES]
    missing = [n for n in names if not os.path.isfile(os.path.join(OUT, n))]
    if missing:
        raise SystemExit("missing pages (run build.py first): %s" % ", ".join(missing))
    stray = sorted(f for f in os.listdir(OUT)
                   if f.endswith(".html") and f not in names)
    docs = {}
    for n in names:
        with open(os.path.join(OUT, n), encoding="utf-8") as fh:
            raw = fh.read()
        docs[n] = Doc(n, raw)
        docs[n].feed(raw)
    return docs, stray


def strip_attrs(raw):
    """Remove the contents of HTML attributes; they are not visible page text."""
    return re.sub(r'"[^"]*"', '" "', raw)


def check_rows(docs, errs):
    """V1: every tbody row carries an official link or an explicit no-source marker."""
    n = 0
    for name, doc in sorted(docs.items()):
        for row in doc.rows:
            n += 1
            joined = "".join(row["cells"])
            if "NOSRC-MARKER" in joined:
                continue
            if not re.search(r"href=https?://", joined):
                errs.append("V1 %s: row %d has no source link and no no-source marker: %s"
                            % (name, row["line"], joined[:110].replace("\n", " ")))
    return n


def check_hosts(docs, errs):
    """V2: external links only to official hosts."""
    n = 0
    for name, doc in sorted(docs.items()):
        for href, _ in doc.links:
            if href.startswith(("http://", "https://")):
                n += 1
                host = re.sub(r"^https?://", "", href).split("/")[0].split(":")[0]
                if host not in src.OFFICIAL_HOSTS:
                    errs.append("V2 %s: link host not on the official allowlist: %s" % (name, href))
                if not href.startswith("https://"):
                    errs.append("V2 %s: link is not https: %s" % (name, href))
    return n


def check_internal(docs, stray, errs):
    """V3: internal links resolve."""
    n = 0
    for name, doc in sorted(docs.items()):
        for href, _ in doc.links:
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            n += 1
            target = href.split("#")[0].split("?")[0]
            if not target:
                continue
            if not os.path.isfile(os.path.join(OUT, target)):
                errs.append("V3 %s: broken internal link to %s" % (name, href))
    return n


def check_money(docs, errs):
    """V4: money is a multiple of $10 unless it is a statutory literal or a scale word."""
    n = 0
    for name, doc in sorted(docs.items()):
        body = strip_attrs(doc.raw)
        for m in MONEY.finditer(body):
            digits, frac = m.group(1), m.group(2)
            token = m.group(0)
            tail = body[m.end():m.end() + 12]
            if re.match(r"^\s*(?:million|billion|trillion|thousand)\b", tail, re.I):
                continue
            if frac:
                errs.append("V4 %s: money figure has decimals: %s" % (name, token))
                continue
            value = digits.replace(",", "")
            if value in STATUTORY_LITERALS:
                continue
            if int(value) % 10 != 0:
                ctx = body[max(0, m.start() - 70):m.end() + 30].replace("\n", " ")
                errs.append("V4 %s: %s is not a multiple of $10 | ...%s..." % (name, token, ctx))
            else:
                n += 1
    return n


def check_pii(docs, errs):
    """V5: no personal or geographic identifier anywhere in the visible text."""
    for name, doc in sorted(docs.items()):
        body = strip_attrs(doc.raw)
        for pattern, label in PII:
            for m in re.finditer(pattern, body):
                ctx = body[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
                errs.append("V5 %s: possible %s: '%s' | ...%s..."
                            % (name, label, m.group(0), ctx))


# "None", "nan" and "inf" are ordinary English words, so they are only a leak inside a cell
# that was rendered as a number. Everything else is checked against the visible text.
NUM_CELL_BAD = re.compile(
    r'<td[^>]*class="[^"]*\bnum\b[^"]*"[^>]*>\s*(?:None|nan|inf|-inf|NaN|Infinity|undefined)\s*</td>',
    re.I)


def check_values(docs, errs):
    """V6: no NaN, infinity, None or similar leaked into the output."""
    for name, doc in sorted(docs.items()):
        body = strip_attrs(doc.raw)
        for pattern, label in BAD_VALUES:
            for m in re.finditer(pattern, body):
                ctx = body[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
                errs.append("V6 %s: %s leaked into the page | ...%s..." % (name, label, ctx))
        for m in NUM_CELL_BAD.finditer(doc.raw):
            ctx = doc.raw[max(0, m.start() - 60):m.end() + 30].replace("\n", " ")
            errs.append("V6 %s: %s leaked into a numeric cell | ...%s..." % (name, m.group(1), ctx))


def check_markup(docs, errs):
    """V7: no script, iframe, form, external asset or event handler."""
    for name, doc in sorted(docs.items()):
        for pattern, label in FORBIDDEN_MARKUP:
            for m in re.finditer(pattern, doc.raw):
                errs.append("V7 %s: %s found at offset %d" % (name, label, m.start()))
        if "target=\"_blank\"" in doc.raw and "rel=\"noopener noreferrer\"" not in doc.raw:
            errs.append("V7 %s: a link opens in a new tab without noopener noreferrer" % name)


def check_registry(errs):
    """V8: the source register is internally consistent."""
    ids = [s["id"] for s in src.SOURCES]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        errs.append("V8 duplicate source ids: %s" % ", ".join(dupes))
    for s in src.SOURCES:
        for field in ("id", "publisher", "title", "url", "evidences", "checked"):
            if not s.get(field):
                errs.append("V8 source %s has an empty %s field" % (s.get("id"), field))
        host = re.sub(r"^https?://", "", s["url"]).split("/")[0]
        if host not in src.OFFICIAL_HOSTS:
            errs.append("V8 source %s points at a host outside the allowlist: %s"
                        % (s["id"], host))
        if not s["url"].startswith("https://"):
            errs.append("V8 source %s is not https: %s" % (s["id"], s["url"]))
    known = set(ids)
    for sid in src.NOT_OPENED:
        if sid not in known:
            errs.append("V8 NOT_OPENED lists an unknown source id: %s" % sid)
    return len(ids)


def check_shell(docs, errs):
    """V9: every page carries the banner, the full navigation and the robots directives."""
    wanted = [fn for fn, _, _ in sh.PAGES]
    for name, doc in sorted(docs.items()):
        for needle, label in (('name="robots" content="noindex,nofollow"', "robots directive"),
                              ('name="referrer" content="no-referrer"', "referrer policy"),
                              ('class="banner"', "privacy banner"),
                              ("rounded to the nearest $10", "rounding statement")):
            if needle not in doc.raw:
                errs.append("V9 %s: missing %s" % (name, label))
        for fn in wanted:
            if 'href="%s"' % fn not in doc.raw:
                errs.append("V9 %s: navigation is missing a link to %s" % (name, fn))


def main(quiet=False):
    docs, stray = load_pages()
    errs = []
    if stray:
        errs.append("V0 stray HTML files that are not part of the desk: %s" % ", ".join(stray))

    n_rows = check_rows(docs, errs)
    n_ext = check_hosts(docs, errs)
    n_int = check_internal(docs, stray, errs)
    n_money = check_money(docs, errs)
    check_pii(docs, errs)
    check_values(docs, errs)
    check_markup(docs, errs)
    n_src = check_registry(errs)
    check_shell(docs, errs)

    if not quiet:
        print("owner-brief desk verification: %s" % OUT)
        print("  pages                 %d" % len(docs))
        print("  table rows checked    %d" % n_rows)
        print("  external source links %d" % n_ext)
        print("  internal links        %d" % n_int)
        print("  money figures         %d (all multiples of $10)" % n_money)
        print("  register sources      %d (%d linked but not opened)"
              % (n_src, len(src.NOT_OPENED)))
        print("")
    if errs:
        print("FAILED with %d problem(s):" % len(errs))
        for e in errs[:80]:
            print("  - %s" % e)
        if len(errs) > 80:
            print("  ... and %d more" % (len(errs) - 80))
        return False
    if not quiet:
        print("OK: all checks passed")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
