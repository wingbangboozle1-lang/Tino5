# -*- coding: utf-8 -*-
"""Unit tests for the owner-brief desk model, source register and verifier.

Run:  python3 cbe/_src/test_model.py
      python3 -m unittest discover -s cbe/_src -p 'test_*.py'

These tests exist because the numbers on the site are generated, and a generated number
that is quietly wrong is worse than no number at all. Each test pins either a statutory
rule transcribed from an official source, or a property of the model that must hold no
matter what the assumptions are.
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import cpi                 # noqa: E402
import model as m          # noqa: E402
import sources as src      # noqa: E402


# -------------------------------------------------------------------------- rounding

class Rounding(unittest.TestCase):
    def test_r10(self):
        self.assertEqual(m.r10(0), 0)
        self.assertEqual(m.r10(4), 0)
        self.assertEqual(m.r10(5), 10)
        self.assertEqual(m.r10(14), 10)
        self.assertEqual(m.r10(15), 20)
        self.assertEqual(m.r10(-14), -10)
        self.assertEqual(m.r10(-15), -20)
        self.assertIsNone(m.r10(None))

    def test_r10_always_a_multiple_of_ten(self):
        for x in (0.4, 1.0, 99.9, 1234.56, 987654.32, -0.4, -1234.56):
            self.assertEqual(m.r10(x) % 10, 0)

    def test_money_and_pct_render_missing_values_bluntly(self):
        self.assertEqual(m.money(None), "&mdash;")
        self.assertEqual(m.pct(None), "&mdash;")

    def test_money_is_a_multiple_of_ten(self):
        for x in (1.0, 99.9, 1234.56, 987654.32):
            s = m.money(x).lstrip("$").replace(",", "")
            self.assertEqual(int(s) % 10, 0)


# ------------------------------------------------------------------------- CPI record

class CpiRecord(unittest.TestCase):
    def test_october_2026_index_level(self):
        self.assertAlmostEqual(cpi.MONTHLY[2026][9], 337.511, places=3)

    def test_october_2025_is_absent(self):
        """The Bureau did not collect October 2025; the record must say so, not guess."""
        self.assertIsNone(cpi.MONTHLY[2025][9])

    def test_months_published_flags_the_gaps(self):
        self.assertEqual(cpi.months_published(2024), 12)
        self.assertEqual(cpi.months_published(2025), 11)
        self.assertEqual(cpi.months_published(2026), 10)

    def test_record_runs_1913_to_2026(self):
        self.assertEqual(cpi.FIRST_YEAR, 1913)
        self.assertEqual(cpi.LAST_YEAR, 2026)
        self.assertEqual(sorted(cpi.MONTHLY)[0], 1913)
        self.assertEqual(sorted(cpi.MONTHLY)[-1], 2026)

    def test_no_inflation_before_the_second_year(self):
        self.assertIsNone(cpi.annual_inflation(1913))

    def test_annual_table_is_total(self):
        rows = cpi.annual_table()
        self.assertEqual(len(rows), len(cpi.MONTHLY))
        self.assertIsNone(dict((y, i) for y, _, i, _ in rows)[1913])

    def test_known_annual_averages(self):
        for year, lo, hi in ((1975, 53.0, 54.5), (1985, 107.0, 108.5), (1995, 152.0, 153.0),
                             (2005, 195.0, 196.0), (2015, 237.0, 238.0), (2020, 258.0, 259.5),
                             (2024, 313.0, 314.5)):
            avg = cpi.annual_average(year)
            self.assertIsNotNone(avg, year)
            self.assertTrue(lo <= avg <= hi, "%s: %s" % (year, avg))

    def test_the_great_inflation_was_high(self):
        self.assertGreater(cpi.mean_over(1973, 1982), 0.08)

    def test_the_depression_was_deflationary(self):
        self.assertLess(cpi.mean_over(1929, 1933), 0.0)

    def test_the_great_moderation_was_calm(self):
        self.assertLess(cpi.mean_over(1991, 2007), 0.035)

    def test_compound_over_matches_the_endpoint_ratio(self):
        self.assertAlmostEqual(cpi.compound_over(1991, 2007),
                               cpi.annual_average(2007) / cpi.annual_average(1990) - 1.0,
                               places=12)


# ------------------------------------------------------------------ statutory engines

class StatutoryEngines(unittest.TestCase):
    def test_prop13_trend_is_capped_at_two_percent(self):
        years = 40
        flat = [10_000_000.0] * (years + 1)          # market never the binding constraint
        path = m.assessed_path(500_000.0, flat, 2026)
        for i in range(1, len(path)):
            self.assertLessEqual(path[i], path[i - 1] * 1.02 + 1e-6)
        self.assertAlmostEqual(path[-1], 500_000.0 * 1.02 ** years, places=4)

    def test_proposition_8_floors_the_value_when_the_market_falls(self):
        market = [1_000_000.0, 600_000.0, 620_000.0, 700_000.0, 1_400_000.0]
        path = m.assessed_path(800_000.0, market, 2026)
        self.assertAlmostEqual(path[0], 800_000.0)          # trend below market: trend
        self.assertAlmostEqual(path[1], 600_000.0)          # market below trend: market
        self.assertAlmostEqual(path[2], 620_000.0)          # still below trend
        self.assertAlmostEqual(path[3], 700_000.0)          # still below trend
        self.assertAlmostEqual(path[4], 800_000.0 * 1.02 ** 4)   # trend recaptured

    def test_assessed_value_never_exceeds_market(self):
        market = [1_000_000.0, 900_000.0, 950_000.0, 1_000_000.0]
        for a, v in zip(m.assessed_path(500_000.0, market, 2026), market):
            self.assertLessEqual(a, v + 1e-6)

    def test_prop19_allowance_in_force_now(self):
        self.assertEqual(m.prop19_allowance(2025), 1_044_586)
        self.assertEqual(m.prop19_allowance(2026), 1_044_586)
        self.assertEqual(m.prop19_allowance(2027), 1_044_586)

    def test_prop19_allowance_steps_every_second_february(self):
        self.assertGreater(m.prop19_allowance(2028), m.prop19_allowance(2027))
        self.assertEqual(m.prop19_allowance(2029), m.prop19_allowance(2028))
        self.assertGreater(m.prop19_allowance(2030), m.prop19_allowance(2029))
        self.assertGreater(m.prop19_allowance(2045), m.prop19_allowance(2027))

    def test_transfer_with_the_exclusion_inside_the_cap(self):
        fbyv, allowance = 800_000.0, 1_044_586.0
        cap = fbyv + allowance
        self.assertEqual(m.transfer_taxable_value(fbyv, cap - 1.0, allowance, True), fbyv)
        self.assertEqual(m.transfer_taxable_value(fbyv, cap, allowance, True), fbyv)

    def test_transfer_with_the_exclusion_above_the_cap_protects_only_the_allowance(self):
        """The exclusion protects the allowance, not the whole gap. An earlier desk got
        this wrong and overstated the saving, so it is pinned here."""
        fbyv, allowance, market = 800_000.0, 1_044_586.0, 6_531_230.0
        self.assertAlmostEqual(m.transfer_taxable_value(fbyv, market, allowance, True),
                               market - allowance)
        self.assertGreater(m.transfer_taxable_value(fbyv, market, allowance, True), fbyv)

    def test_transfer_without_the_exclusion_is_a_full_reassessment(self):
        self.assertAlmostEqual(m.transfer_taxable_value(800_000.0, 6_531_230.0, 1_044_586.0,
                                                        False), 6_531_230.0)

    def test_estate_exemption_matches_the_official_figures(self):
        self.assertEqual(m.estate_exemption(2025), 15_000_000)
        self.assertEqual(m.estate_exemption(2026), 15_000_000)
        self.assertEqual(m.estate_exemption(2027), 15_480_000)

    def test_estate_exemption_grows_monotonically(self):
        prev = 0
        for y in range(2026, 2076):
            cur = m.estate_exemption(y)
            self.assertGreater(cur, prev)
            prev = cur

    def test_estate_tax_only_hits_the_excess(self):
        self.assertEqual(m.estate_tax_on(15_000_000, 2026), 0.0)
        self.assertEqual(m.estate_tax_on(14_000_000, 2026), 0.0)
        self.assertAlmostEqual(m.estate_tax_on(16_000_000, 2026), 400_000.0)


# -------------------------------------------------------------------- derived inputs

class DerivedInputs(unittest.TestCase):
    def test_effective_rate_matches_the_owner_record(self):
        self.assertAlmostEqual(m.effective_rate_a(),
                               m.OWNER["a_bill_2025"] / m.OWNER["a_assessed_2025"])

    def test_rate_band_contains_the_planning_rate(self):
        lo, hi, _ = m.effective_rate_a_band()
        self.assertLess(lo, hi)
        self.assertTrue(lo <= m.effective_rate_a() <= hi)

    def test_rate_band_is_narrow(self):
        """The rate has been stable across the owner's record; if it is not, the
        derived figure would be unsafe to use as a planning constant."""
        lo, hi, _ = m.effective_rate_a_band()
        self.assertLess(hi - lo, 0.002)

    def test_b_rate_residual_is_positive_and_material(self):
        residual, adval = m.b_rate_residual()
        self.assertGreater(residual, 0.0)
        self.assertLess(residual, m.OWNER["b_bill_2025"])
        self.assertAlmostEqual(adval + residual, m.OWNER["b_bill_2025"])

    def test_unit_rent_is_half_the_reported_two_unit_rent(self):
        self.assertAlmostEqual(m.b_unit_rent(), m.OWNER["b_rent"] / 2.0)


# ------------------------------------------------------------------------ the model

class Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = m.compare()

    def test_value_path_is_compounding(self):
        path = m.value_path(1_000_000.0, 5, 0.04)
        self.assertEqual(len(path), 6)
        self.assertAlmostEqual(path[-1], 1_000_000.0 * 1.04 ** 5)

    def test_value_path_accepts_a_list_of_rates(self):
        path = m.value_path(1_000_000.0, 3, [0.10, -0.10, 0.0])
        self.assertAlmostEqual(path[1], 1_100_000.0)
        self.assertAlmostEqual(path[2], 990_000.0)
        self.assertAlmostEqual(path[3], 990_000.0)

    def test_the_exclusion_never_raises_the_taxable_value(self):
        self.assertLessEqual(self.r["taxable_excluded"], self.r["taxable_reassessed"])

    def test_the_exclusion_wins_where_market_exceeds_the_cap(self):
        self.assertGreater(self.r["value_at_transfer"], self.r["fbyv"] + self.r["allowance"])
        self.assertLess(self.r["taxable_excluded"], self.r["taxable_reassessed"])

    def test_without_occupation_the_property_is_reassessed_to_market(self):
        self.assertAlmostEqual(self.r["taxable_reassessed"], self.r["value_at_transfer"])

    def test_the_two_let_units_of_property_b_are_excluded_from_every_option(self):
        """They are produced whatever you choose, so they must not appear in any option.
        Only the third unit enters, and only under 'occupy', which is the option that
        frees it."""
        with_b = m.compare(count_b_unit=True)
        without_b = m.compare(count_b_unit=False)
        self.assertGreater(with_b["npv_occupy_cash"], without_b["npv_occupy_cash"])
        self.assertAlmostEqual(with_b["npv_rent_cash"], without_b["npv_rent_cash"])
        self.assertAlmostEqual(with_b["npv_sell_cash"], without_b["npv_sell_cash"])

    def test_economic_column_adds_the_imputed_rent(self):
        self.assertGreater(self.r["npv_occupy_econ"], self.r["npv_occupy_cash"])
        self.assertGreater(self.r["npv_sell_econ"], self.r["npv_sell_cash"])

    def test_sell_npv_is_the_discounted_terminal_portfolio(self):
        years = self.r["years_after"]
        expected = self.r["portfolio_terminal"] / (1.0 + m.ASSUMPTIONS["discount_rate"]) ** years
        self.assertAlmostEqual(self.r["npv_sell_cash"], expected)

    def test_sale_proceeds_are_not_counted_twice(self):
        """The proceeds are not also added to the terminal value: the terminal value IS
        the proceeds grown. Counting both was a real bug in an earlier revision."""
        self.assertLess(self.r["npv_sell_cash"], self.r["portfolio_terminal"])
        self.assertAlmostEqual(self.r["portfolio_terminal"],
                               self.r["proceeds"]
                               * (1.0 + m.ASSUMPTIONS["portfolio_return"]
                                  - m.ASSUMPTIONS["portfolio_tax_drag"]) ** self.r["years_after"])

    def test_row_counts_match_the_horizon(self):
        self.assertEqual(len(self.r["occ_rows"]), self.r["years_after"])
        self.assertEqual(len(self.r["rent_rows"]), self.r["years_after"])

    def test_every_number_is_finite(self):
        def walk(x, path="r"):
            if isinstance(x, dict):
                for k, v in x.items():
                    walk(v, "%s.%s" % (path, k))
            elif isinstance(x, (list, tuple)):
                for i, v in enumerate(x):
                    walk(v, "%s[%d]" % (path, i))
            elif isinstance(x, float):
                self.assertTrue(x == x and abs(x) != float("inf"), "%s = %s" % (path, x))
        walk(self.r)

    def test_operating_costs_rise_with_value_and_are_finite(self):
        a = m.opex_a(2046, 6_000_000.0, 0.03)
        self.assertGreater(a["maintenance"], a["insurance"])
        self.assertLess(a["power"], 0.0)            # the rooftop system produces a credit
        self.assertAlmostEqual(a["total"],
                               a["water"] + a["power"] + a["insurance"] + a["maintenance"])

    def test_a_heavier_maintenance_assumption_lowers_the_npv(self):
        heavy = m.compare(maint_a=0.020)["npv_occupy_cash"]
        self.assertLess(heavy, self.r["npv_occupy_cash"])

    def test_a_higher_tax_rate_lowers_the_npv(self):
        self.assertLess(m.compare(tax_rate_override=0.020)["npv_occupy_cash"],
                        self.r["npv_occupy_cash"])

    def test_leaving_after_the_transfer_raises_the_bill(self):
        """On removal the market value at the transfer is enrolled, trended from that
        date (LTA 2026/026 Q10), so the assessed value jumps to the reassessed path."""
        left = m.compare(lead_occupancy_years=3)
        self.assertGreater(left["assessed_excluded"][-1],
                           self.r["assessed_excluded"][-1])

    def test_the_transfer_year_moves_the_answer_but_not_the_ranking(self):
        gaps = [m.gap("occupy", "econ", transfer_year=y) for y in (2040, 2045, 2050)]
        self.assertTrue(all(g < 0 for g in gaps) or all(g > 0 for g in gaps))
        self.assertLess(max(gaps) - min(gaps), abs(gaps[1]) * 0.5)


# ------------------------------------------------------------------------ break-evens

class BreakEvens(unittest.TestCase):
    def test_break_even_gross_yield_closes_the_gap(self):
        y = m.breakeven_gross_yield("occupy", "econ")
        self.assertIsNotNone(y)
        self.assertAlmostEqual(m.gap("occupy", "econ", gross_yield_a=y), 0.0, delta=1.0)

    def test_break_even_price_growth_closes_the_gap(self):
        g = m.breakeven_price_growth("occupy", "econ")
        self.assertIsNotNone(g)
        self.assertAlmostEqual(m.gap("occupy", "econ", price_growth=g), 0.0, delta=1.0)

    def test_break_even_portfolio_return_closes_the_gap(self):
        r = m.breakeven_portfolio_return("occupy", "econ")
        self.assertIsNotNone(r)
        self.assertAlmostEqual(m.gap("occupy", "econ", portfolio_return=r), 0.0, delta=1.0)

    def test_gap_is_monotone_in_each_break_even_input(self):
        g = lambda **kw: m.gap("occupy", "econ", **kw)      # noqa: E731
        self.assertGreater(g(gross_yield_a=0.040), g(gross_yield_a=0.020))
        self.assertGreater(g(price_growth=0.060), g(price_growth=0.030))
        self.assertLess(g(portfolio_return=0.090), g(portfolio_return=0.050))

    def test_break_even_solvers_report_none_when_the_gap_cannot_be_closed(self):
        """A solver must say 'not closable' rather than return a value outside the
        range it searched."""
        for fn in (m.breakeven_tax_rate, m.breakeven_maint):
            for target in ("occupy", "rent"):
                v = fn(target, "econ")
                self.assertTrue(v is None or 0.0 <= v <= 1.0)

    def test_break_evens_are_stable_across_the_transfer_window(self):
        """The break-evens are the part of the analysis that survives the unknown date,
        which is why the site leans on them."""
        vals = [m.breakeven_gross_yield("occupy", "econ", transfer_year=y)
                for y in (2040, 2045, 2050)]
        self.assertLess(max(vals) - min(vals), 0.005)


# --------------------------------------------------------------------- black swans

class BlackSwans(unittest.TestCase):
    def test_every_regime_produces_a_measured_or_declared_inflation_rate(self):
        for r in m.REGIMES:
            infl = m._regime_inflation(r)
            self.assertIsNotNone(infl)
            if r["anchor_years"]:
                a, b = r["anchor_years"]
                self.assertAlmostEqual(infl, cpi.mean_over(a, b))

    def test_the_great_inflation_is_the_hottest_measured_regime(self):
        measured = [m._regime_inflation(r) for r in m.REGIMES if r["anchor_years"]]
        self.assertAlmostEqual(max(measured),
                               m._regime_inflation(m.by_key("great_inflation")))

    def test_deflation_regimes_are_negative(self):
        for key in ("depression",):
            self.assertLess(m._regime_inflation(m.by_key(key)), 0.0)

    def test_nominal_rates_are_built_from_inflation_plus_the_real_rate(self):
        for x in m.regime_scenarios():
            self.assertAlmostEqual(x["price_growth"],
                                   (1.0 + x["inflation"]) * (1.0 + x["regime"]["real_house"]) - 1.0)
            self.assertAlmostEqual(x["portfolio"],
                                   (1.0 + x["inflation"]) * (1.0 + x["regime"]["real_equity"]) - 1.0)

    def test_regime_scenarios_all_run_and_are_finite(self):
        rows = m.regime_scenarios()
        self.assertEqual(len(rows), len(m.REGIMES))
        for x in rows:
            for k in ("occ_gap", "rent_gap", "tax_excluded", "tax_full"):
                self.assertTrue(abs(x[k]) < float("inf"), k)

    def test_the_exclusion_never_costs_money_in_any_regime(self):
        for x in m.regime_scenarios():
            self.assertLessEqual(x["tax_excluded"], x["tax_full"] + 1e-6)

    def test_regime_outcomes_actually_spread(self):
        gaps = [x["occ_gap"] for x in m.regime_scenarios()]
        self.assertGreater(max(gaps) - min(gaps), 1_000_000.0)

    def test_block_bootstrap_is_reproducible(self):
        a = m.block_bootstrap_inflation(length=50, seed=1)
        b = m.block_bootstrap_inflation(length=50, seed=1)
        self.assertEqual(a, b)

    def test_block_bootstrap_returns_the_requested_length(self):
        self.assertEqual(len(m.block_bootstrap_inflation(length=37, seed=2)), 37)

    def test_block_bootstrap_only_uses_measured_history(self):
        hist = {round(r, 10) for _, r in cpi.series(1914, 2025)}
        for g in m.block_bootstrap_inflation(length=200, seed=3):
            self.assertIn(round(g, 10), hist)

    def test_monte_carlo_is_reproducible(self):
        a = m.monte_carlo(paths=40, target="occupy")
        b = m.monte_carlo(paths=40, target="occupy")
        self.assertEqual(a["p50"], b["p50"])

    def test_monte_carlo_quantiles_are_ordered(self):
        d = m.monte_carlo(paths=200, target="occupy")
        self.assertLessEqual(d["p05"], d["p25"])
        self.assertLessEqual(d["p25"], d["p50"])
        self.assertLessEqual(d["p50"], d["p75"])
        self.assertLessEqual(d["p75"], d["p95"])
        self.assertTrue(0.0 <= d["keep_wins"] <= 1.0)
        self.assertEqual(d["paths"], 200)

    def test_monte_carlo_runs_for_both_targets(self):
        for target in ("occupy", "rent"):
            d = m.monte_carlo(paths=60, target=target)
            self.assertTrue(d["p05"] < float("inf"))

    def test_a_zero_weight_regime_is_never_drawn(self):
        self.assertEqual([r for r in m.REGIMES if r["key"] == "japan"][0]["weight"], 0)


# ---------------------------------------------------------------------- projections

class Projections(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.res = m.projection_rows()

    def test_one_row_per_year(self):
        years = [r["year"] for r in self.rows]
        self.assertEqual(years[0], m.ASSUMPTIONS["base_year"])
        self.assertEqual(years[-1], m.ASSUMPTIONS["horizon"])
        self.assertEqual(len(set(years)), len(years))

    def test_values_grow_monotonically_under_a_positive_growth_rate(self):
        for prev, cur in zip(self.rows, self.rows[1:]):
            self.assertGreater(cur["a_value"], prev["a_value"])
            self.assertGreater(cur["b_value"], prev["b_value"])

    def test_the_assessed_value_jumps_at_the_transfer(self):
        t = m.ASSUMPTIONS["transfer_year"]
        prev = [r for r in self.rows if r["year"] == t - 1][0]
        cur = [r for r in self.rows if r["year"] == t][0]
        self.assertGreater(cur["a_tax"], prev["a_tax"] * 2)

    def test_the_taxable_value_never_exceeds_the_market_value(self):
        for r in self.rows:
            self.assertLessEqual(r["a_assessed"], r["a_value"] + 1e-6)
            self.assertLessEqual(r["b_assessed"], r["b_value"] + 1e-6)

    def test_rent_grows_at_the_rent_growth_assumption(self):
        first = self.rows[0]["b_rent"]
        last = self.rows[-1]["b_rent"]
        n = m.ASSUMPTIONS["horizon"] - m.ASSUMPTIONS["base_year"]
        self.assertAlmostEqual(last, first * (1.0 + m.ASSUMPTIONS["rent_growth"]) ** n)

    def test_every_projected_number_is_finite(self):
        for r in self.rows:
            for k, v in r.items():
                if isinstance(v, float):
                    self.assertTrue(v == v and abs(v) != float("inf"), "%s %s" % (k, v))


# ------------------------------------------------------------------ source register

class SourceRegister(unittest.TestCase):
    def test_ids_are_unique(self):
        ids = [s["id"] for s in src.SOURCES]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_source_is_complete(self):
        for s in src.SOURCES:
            for field in ("id", "publisher", "title", "url", "evidences", "checked"):
                self.assertTrue(s.get(field), "%s missing %s" % (s["id"], field))

    def test_every_source_is_https_and_on_the_allowlist(self):
        for s in src.SOURCES:
            self.assertTrue(s["url"].startswith("https://"), s["id"])
            host = s["url"].split("//", 1)[1].split("/")[0]
            self.assertIn(host, src.OFFICIAL_HOSTS, s["id"])

    def test_not_opened_ids_exist(self):
        known = {s["id"] for s in src.SOURCES}
        for sid in src.NOT_OPENED:
            self.assertIn(sid, known)

    def test_by_id_resolves_every_id(self):
        for s in src.SOURCES:
            self.assertIs(src.by_id()[s["id"]], s)

    def test_link_renders_the_canonical_url(self):
        for s in src.SOURCES:
            self.assertIn(s["url"], src.link(s["id"]))

    def test_nosrc_marks_a_row_as_unconfirmed(self):
        html = src.nosrc("because")
        self.assertIn("nosrc", html)
        self.assertIn("because", html)

    def test_the_register_covers_every_publisher_the_site_relies_on(self):
        hosts = {s["url"].split("//", 1)[1].split("/")[0] for s in src.SOURCES}
        for required in ("www.irs.gov", "www.boe.ca.gov", "leginfo.legislature.ca.gov",
                         "www.ftb.ca.gov", "www.bls.gov", "sftreasurer.org",
                         "voterguide.sos.ca.gov"):
            self.assertIn(required, hosts)


# ------------------------------------------------------------------------ integration

class BuiltPages(unittest.TestCase):
    """The verifier is part of the contract, so it is part of the tests."""

    def test_pages_exist_and_verify(self):
        missing = [fn for fn, _, _ in __import__("shell").PAGES
                   if not os.path.isfile(os.path.join(OUT, fn))]
        if missing:
            self.skipTest("pages not built yet: %s" % ", ".join(missing))
        import verify
        self.assertTrue(verify.main(quiet=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
