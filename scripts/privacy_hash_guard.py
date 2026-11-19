#!/usr/bin/env python3
"""Hash-based guard against owner-location identifiers (session arena-c9f0d60a, task c9f/G).

The guard stores only SHA-256 digests of the forbidden words and word pairs, so the repository does
not repeat the identifiers it is meant to keep out. Each tracked text file is scanned line by line
after external http(s) URLs are removed (official source links to public city pages are allowed).
Words and adjacent word pairs are lower-cased and compared with the digests. Exit 1 on any hit.

Covered: two ZIP codes, the owner's city name, and the owner's neighbourhood name (the last as the
word pairs of its three spellings). County-level geography, agency names and regulatory uses of the
word for a legal or tariff expiry are not covered.

Guard code: a few verifier and test files (GUARD_CODE_ALLOWLIST) must name the forbidden words in
their own detection patterns. They are the only exemption, they must be Python source, and none of
them is a published page or data file.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN = {
    # home-region words (digest only; session arena-c9f0d60a)
    "ae16e3e7a45d4a88b998b2ee95a8b6f3fe1fc68b493dfaf2fab88f9a5f150f30",
    "fc15d22c9db9957ba867cd618f5ef0cba3c58097295fe48ed2858e922586ac40",
    "13ec7cc438685651ee4e808146d43f73ce84994ae3f8c5fe6786c38f2a9d9a3a",
    "2478d903d7c875f05299efe5a271b802046c65fdbb33ab2d0a0085f5b73748ed",
    "43086d953bcc428c4a8bf097446b87d9f577a80d4bd010a4313d575484cc9f21",
    "64c28ebb31e5b4a0cd743f1b02dc1afad7cd129495a8854b2fbc9ddbb03d75a4",
    "e5d7a1bef408b5503a842040e287d88c16911a3b7857f15d144e3aa7065cdcf6",
    "f6f9c5f004b4e5b525d9712aaafefcf17a8e93130541a137e5d7d9cf495a50f9",
}

# Python detector files whose own patterns name the forbidden words. Their generated output does not
# contain the words (the desk checks confirm this). Reviewed in session arena-c9f0d60a; keep it short.
GUARD_CODE_ALLOWLIST = {
    "cbd/_src/verify.py", "cbe/_src/verify.py",
    "desk-03242c78/_src/verify.py", "desk-85a01c5c/_src/verify.py", "desk-8be2/_src/verify.py",
    "desk-d75/_src/build.py", "desk-d75/_src/test_desk_d75.py", "desk-d75/_src/verify.py",
    "desk-e86/verify.py", "inheritance-desk/_src/verify.py", "phase-99220/_src/verify.py",
    "referee-abae/_src/test_build.py", "review-092b/_src/test_review_092b.py",
    "review-092b/_src/verify.py", "scripts/test_model_v5.py", "scripts/verify_safe.py",
    "scripts/verify_desk_v5.py", "scripts/check_published_surface.py",
    "swan-3a49/build.py", "tino5-3f269806/_src/verify.py", "verify-552/verify.py",
    # recheck-2026-11-17 (arena-1e93b0b8): same detection-only purpose (verifier word list).
    "recheck-2026-11-17/_src/verify.py",
    # recheck-2026-11-19 (arena-c267f0b0): same detection-only purpose (verifier word list).
    "recheck-2026-11-19/_src/verify.py",
}

URL = re.compile(r'https?://[^\s"\'<>)\]\\]*')
WORD = re.compile(r"[A-Za-z0-9]+")


def _digest(text: str) -> str:
    return hashlib.sha256(text.lower().encode("utf-8")).hexdigest()


def scan_text(text: str):
    """Yield the line number of each forbidden word or pair found outside URLs."""
    for lineno, line in enumerate(text.split("\n"), 1):
        words = [w.lower() for w in WORD.findall(URL.sub(" ", line))]
        candidates = words + [f"{a} {b}" for a, b in zip(words, words[1:])]
        for c in candidates:
            if _digest(c) in FORBIDDEN:
                yield lineno


def tracked_files() -> list[str]:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    return out.stdout.splitlines()


def main() -> int:
    for rel in GUARD_CODE_ALLOWLIST:
        if not rel.endswith(".py"):
            print(f"privacy_hash_guard: allowlist entry is not Python source: {rel}")
            return 1
    hits = []
    scanned = 0
    for rel in tracked_files():
        if rel in GUARD_CODE_ALLOWLIST:
            continue
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            continue
        raw = open(path, "rb").read()
        if b"\0" in raw:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for lineno in scan_text(text):
            hits.append((rel, lineno))
    for rel, lineno in hits:
        print(f"privacy_hash_guard: {rel}:{lineno} contains a forbidden owner-location token")
    print(f"privacy_hash_guard: {len(hits)} hit(s) in {scanned} tracked text file(s) "
          f"({len(GUARD_CODE_ALLOWLIST)} reviewed guard-code file(s) excluded)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
