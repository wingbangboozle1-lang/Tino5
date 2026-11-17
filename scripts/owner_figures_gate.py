#!/usr/bin/env python3
"""Owner-figure gate (session arena-c4161fb6).

Fails if any comma-formatted money figure on a PUBLISHED surface equals one of the owner's
raw (unrounded) bill / roll figures for annual property tax and assessed value.

Policy this enforces: the owner asked for every money figure to be rounded to the nearest $10.
A value that is already a multiple of $10 is identical to its rounded form and is permitted, so
only RAW figures (not multiples of $10) are denylisted. Rounded history tables are a separate
owner decision and are logged on the Flagged for Review page.

Why this exists: scripts/verify_safe.py and scripts/privacy_scan.py both passed while
review-092b/questions.html printed an exact 2025 bill and roll value. Those checks only test
rounding and identifier shapes, not the specific owner values.

Design: the denylist is stored as salted SHA-256 digests only, so no plaintext owner figure is
added to the tree by this file. The salt is public; the digests protect against accidental
publication (they are not a secrecy mechanism — the figures already exist in the git history).

Scope: root index.html plus every directory in PUBLISHED_DESKS (scripts/verify_safe.py) and
public-safe/. Only comma-formatted numbers are checked (for example a comma-formatted amount whose last digits are not zeros), so bare 4-digit
numbers such as years are not matched.

Run: python3 scripts/owner_figures_gate.py
"""
import hashlib
import re
import sys
from pathlib import Path

SALT = "tino5-c4161fb6-owner-figures-v1"
DIGESTS = {
    "0697ddf3edd1fddd41a9e8bcc73b6fa3287da0cd4885f3fc219af0643365d907",
    "077957b1465de4b5c962c9496003c43f7d27f3ab87384ff3daff29291d4b5bb4",
    "0836ef7ce8382eb57f3fcbdf78e252ff00ab984e9cc087991995e59d72f2aca5",
    "15e8402082ec49ad353c13a815115233d35753eb2c00127842eddc2cf0cbee73",
    "1ce6bc013860f71c37b167da15a10f4621de18be65a07cf910fb96c56a42dd20",
    "1f84f55c8026b546184d258ba409793d4c67059b7d395b853e04a0e8e4991ad3",
    "223312d888878c2bafda52ae8ae1f887ddfb862366b341326fcfc6be690c95c9",
    "2f9f9f3ebe870ce4e91ad4fccba1542f500dde3bf2b6e7d2c4a498dd59c64f1d",
    "3068d09346d9d2cbbf1efe7ccbf473bb5c27e8ece5fdce7e853a9924203c373c",
    "307c78ac47749d5aba5cf2dc6e566e5181a31203f23aff6e0a35d970d6c53e27",
    "3122b129911f9ae9b255d2b113d9adb3b44d7c136c5d664e5214c945477de907",
    "42a39cbc17205761a28c385d9f6e93874a14fcc119ad633bfb0b1d858245449b",
    "45d0bb01de979f151d0a95fdcef6fe52120384d48e0b5aaf1be624a1f03144fa",
    "46f307a5481a36a21fc07664cd5af0424d2746622cfc2841fba58283f482fcd4",
    "4a9ab7a89bbd508e9aa99fc6222ea4854d42f7f5c214ec0812b57c5a7d4a6f66",
    "4e5a84c6afcee3b708d9f7fed0e3ae8b0009405ed65148d963bc56b15e00fba6",
    "5a3a5a83cb922c1978a12bbda93b88e6b608e3de9f9abd80c1feab5874322ba1",
    "6ef048ac98d17b619cc445ec77dee0c004580ea8172c389429551ad050d8a964",
    "7dd9be3d8b692a38c2564772afd24fd1259c81893380f8a0b38635a2dda14072",
    "89cc7cf22f896461a3ad52c68a48c05d0f5d755df76e84081dc9ec30133648cc",
    "8aa0f8dbb79a9e1da4f02b24c04a91892caefe5acb01456ed436f22f1bda2b64",
    "8afb182425fbc46755e50853e583b7a8bdab308896c02441bbae9181ea4d6fb4",
    "8e1be511d68e0a34ce42e45343bdc9f635c31635a2c050bb541d66ff1a4e07b0",
    "9018623bf981b0462ddcef70f9a1862224dd2c7457a17c9b6027aaf0e5c2f77c",
    "9111aae9da46e9513eeba338dc3d20cfa477891584605b31667d4c357a68431e",
    "b260f4b87691d1b6eaf0b730717d826f77288b8d09cfa5946efb8d7ef69b679a",
    "bb035bc40de3e472356485c3a3a23bb0dfeb2e78595e4962fa065e2462b61a8e",
    "bced4bf24b737eb9afbf196904f1764279b1ef79a290a1309b4880405ab1f02a",
    "bf0fbf743a7b853b0ea1d33856c53f969e4698f33cfec4f9a985b93ee473e6ea",
    "c74258ae36f841a42795a1d77e109e6446449102cc1767a93c5ba60772b110a9",
    "cc5e73f8d73e65eda59baeb16ad078b48c21e5dbe097c8810d9b9d63e1e3f85f",
    "d3148b22ad9f3cec7ff430fef8c268c021e9b12c1f1eb9ef6db09d13d28ee768",
    "e32679ecd69efc8d2b946b1e731b0486cc854dfe4b368ac613ba73d3727ef105",
    "e3b8589a1b5e85b6e4d8a95f05b4bb2c875735cdf69f719250ed029cbd20f4ed",
    "e3dd48d1cb6e6acb60b0761f938810ef89f9834b239bd462c817e5935bc4064f",
    "e65a9544bdfb4f83fa5e809eff64ab1e7b161edf4844bc75548c63f2cffd926f",
    "f12407f6f9cd0d897ac6687cb337b8365708149b1b4c868e3446fa74dc00ab88",
    "f2bd67d36bd36d4f280f62e2ca05b291e5314e2be7fd04dd0e1c0738a97ea5f8",
    "f7efc1974f6e7564e95e9e559366d85d88eef3bdf7021df8c4a86004a34bd325",
    "f9fad22ec2cc1c79916e8960d5af1222ec6374a578ffb4e178d9ad1ee8231823",
}
ROOT = Path(__file__).resolve().parent.parent
NUM = re.compile(r"(?<![\w.])\$?\s?(\d{1,3}(?:,\d{3})+)(?![\d,]*\d)")
TEXT_SUFFIXES = {".html", ".htm", ".json", ".md", ".txt", ".css", ".js", ".svg"}


def published_dirs():
    src = (ROOT / "scripts" / "verify_safe.py").read_text(encoding="utf-8")
    m = re.search(r"PUBLISHED_DESKS\s*=\s*\{(.*?)\}", src, re.S)
    names = set(re.findall(r"\"([^\"]+)\"", m.group(1))) if m else set()
    return sorted(names | {"public-safe"})


def surface_files():
    files = []
    if (ROOT / "index.html").exists():
        files.append(ROOT / "index.html")
    for d in published_dirs():
        base = ROOT / d
        if base.is_dir():
            files += [p for p in base.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES
                      and "_src" not in p.parts and "__pycache__" not in p.parts]
    return files


def digest(n):
    return hashlib.sha256(f"{SALT}:{n}".encode()).hexdigest()


def main():
    hits = []
    files = surface_files()
    for f in files:
        for lineno, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for m in NUM.finditer(line):
                value = int(m.group(1).replace(",", ""))
                if digest(value) in DIGESTS:
                    hits.append(f"{f.relative_to(ROOT)}:{lineno}")
    if hits:
        print(f"FAIL: {len(hits)} owner bill/roll figure(s) on the published surface:")
        for h in hits:
            print("  " + h)
        return 1
    print(f"PASS: owner-figure gate clean across {len(files)} published text files "
          f"({len(DIGESTS)} denylisted digests; comma-formatted figures only).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
