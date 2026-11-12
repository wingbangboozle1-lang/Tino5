#!/usr/bin/env python3
"""Unit tests for tools-22a32b17/model_22a.py."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model_22a as m  # noqa: E402


class TestModel22a(unittest.TestCase):
    def test_r10_and_fmt_money_invariants(self) -> None:
        self.assertEqual(m.r10(7214.4), 7210)
        self.assertEqual(m.r10(7215.1), 7220)
        self.assertEqual(m.fmt_money(6531234.0), "$6,531,230")
        self.assertEqual(m.fmt_money(-182.0), "-$180")
        self.assertEqual(m.fmt_money(0.0, dash_zero=True), "—")

    def test_boe_and_scc_prop19_worked_examples(self) -> None:
        # BOE Pub 801 worked example: $300k FBYV + $1M allowance vs $1.5M FMV -> $500k
        self.assertEqual(m.prop19_new_taxable(1_500_000, 300_000, 1_000_000), 500_000)
        # Below cap -> keeps FBYV unchanged
        self.assertEqual(m.prop19_new_taxable(1_200_000, 300_000, 1_044_586), 300_000)
        # Santa Clara County Assessor parent-to-child-2 page worked example ($10-rounded display):
        # FBYV $500,000 + $1,044,586 allowance vs FMV $2,000,000 -> $955,410 ($10-rounded)
        self.assertEqual(m.r10(m.prop19_new_taxable(2_000_000, 500_000, 1_044_586)), 955_410)

    def test_federal_estate_exclusions_2026_2027(self) -> None:
        self.assertEqual(m.federal_estate_exclusion_at(2026), 15_000_000.0)
        self.assertEqual(m.federal_estate_exclusion_at(2027), 15_480_000.0)
        self.assertGreater(m.federal_estate_exclusion_at(2045), 24_000_000.0)

    def test_sf_transfer_tax_tiers(self) -> None:
        self.assertAlmostEqual(m.sf_transfer_tax_rate(200_000), 0.0050)
        self.assertAlmostEqual(m.sf_transfer_tax_rate(800_000), 0.0068)
        self.assertAlmostEqual(m.sf_transfer_tax_rate(1_800_000), 0.0075)
        self.assertAlmostEqual(m.sf_transfer_tax_rate(6_000_000), 0.0225)
        self.assertAlmostEqual(m.sf_transfer_tax_rate(12_000_000), 0.0550)
        self.assertAlmostEqual(m.sf_transfer_tax_rate(30_000_000), 0.0600)

    def test_rev_rul_2023_2_step_up_vs_carryover_penalty(self) -> None:
        step = m.evaluate_strategies(transfer_year=2045, step_up_applies=True)
        no_step = m.evaluate_strategies(
            transfer_year=2045, step_up_applies=False, carryover_basis_a=250_000.0
        )
        self.assertEqual(step["S3a"]["terminal_tax"], 0.0)
        # Losing IRC §1014 step-up on ~$6.40M net sale triggers >$2.2M immediate tax
        self.assertGreater(no_step["S3a"]["terminal_tax"], 2_200_000.0)
        self.assertGreater(
            step["S3a"]["liquidated_wealth"] - no_step["S3a"]["liquidated_wealth"],
            8_000_000.0,
        )

    def test_baseline_and_black_swan_r0_exact_match(self) -> None:
        base = m.evaluate_strategies(transfer_year=2045, horizon_years=25)
        r0 = m.build_black_swan_regimes()[0]
        self.assertEqual(r0["code"], "R0")
        self.assertAlmostEqual(base["S1a"]["liquidated_wealth"], float(r0["w_occ"]), places=2)
        self.assertAlmostEqual(base["S2"]["liquidated_wealth"], float(r0["w_rent"]), places=2)
        self.assertAlmostEqual(base["S3a"]["liquidated_wealth"], float(r0["w_eq"]), places=2)
        self.assertAlmostEqual(base["S3b"]["liquidated_wealth"], float(r0["w_tr"]), places=2)

    def test_sources_all_https_and_unique(self) -> None:
        ids = [s["id"] for s in m.SOURCES]
        urls = [s["url"] for s in m.SOURCES]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(urls), len(set(urls)))
        for u in urls:
            self.assertTrue(u.startswith("https://"), msg=u)


if __name__ == "__main__":
    unittest.main()
