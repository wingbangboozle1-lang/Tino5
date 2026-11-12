#!/usr/bin/env python3
"""Deterministic builder for desk-22a32b17/ static dashboard site & JSON summary."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT_DIR = ROOT / "desk-22a32b17"

sys.path.insert(0, str(HERE))
import layout_22a as L  # noqa: E402
import model_22a as m  # noqa: E402
import pages_core_22a as PC  # noqa: E402
import pages_gov_22a as PG  # noqa: E402


def build_all() -> dict[str, str]:
    files: dict[str, str] = {
        "style.css": L.CSS_CONTENT,
        "index.html": PC.build_index_page(),
        "properties-and-tax.html": PC.build_properties_page(),
        "operating-costs.html": PC.build_operating_costs_page(),
        "inheritance-and-estate-tax.html": PC.build_estate_tax_page(),
        "decision-scenarios.html": PC.build_decision_page(),
        "projections-50yr.html": PC.build_projections_page(),
        "black-swan-economics.html": PG.build_black_swan_page(),
        "inheritance-process.html": PG.build_process_page(),
        "law-watch.html": PG.build_law_watch_page(),
        "repo-audit.html": PG.build_repo_audit_page(),
        "flagged.html": PG.build_flagged_page(),
        "sources.html": PG.build_sources_page(),
    }

    summary_payload = {
        "desk": "desk-22a32b17",
        "verified_date": "2026-11-12",
        "rounding_increment_usd": 10,
        "official_sources_count": len(m.SOURCES),
        "flagged_items_count": 18,
        "scenarios": {},
        "black_swan_regimes_2045_to_2070": [],
    }
    for ty in (2040, 2045, 2050):
        ev = m.evaluate_strategies(ty, 25)
        summary_payload["scenarios"][str(ty)] = {
            "end_year": int(ev["meta"]["end_year"]),
            "fmv_transfer": m.r10(ev["meta"]["fmv_transfer"]),
            "net_proceeds_transfer": m.r10(ev["meta"]["proceeds_transfer"]),
            "liquidated_wealth": {
                k: m.r10(ev[k]["liquidated_wealth"]) for k in ("S1a", "S1b", "S2", "S3a", "S3b")
            },
            "hold_net_worth": {
                k: m.r10(ev[k]["hold_net_worth"]) for k in ("S1a", "S1b", "S2", "S3a", "S3b")
            },
        }
    for reg in m.build_black_swan_regimes():
        summary_payload["black_swan_regimes_2045_to_2070"].append({
            "code": reg["code"],
            "name": reg["name"],
            "fmv_2045": m.r10(float(reg["fmv_2045"])),
            "occupy_2070": m.r10(float(reg["w_occ"])),
            "rent_2070": m.r10(float(reg["w_rent"])),
            "sell_equities_2070": m.r10(float(reg["w_eq"])),
            "sell_treasuries_2070": m.r10(float(reg["w_tr"])),
            "winner": reg["winner"],
        })

    files["summary_22a.json"] = json.dumps(summary_payload, indent=2) + "\n"
    return files


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rendered = build_all()
    for name, content in rendered.items():
        (OUT_DIR / name).write_text(content, encoding="utf-8")
    print(f"build_desk_22a: wrote {len(rendered)} files to {OUT_DIR.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
