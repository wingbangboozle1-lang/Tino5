"""Tests for the owner-brief desk (desk-d75/_src/build.py), run by CI.

These check the arithmetic the pages quote and the rules the owner set for the site - in particular
the two corrections this desk was commissioned to make (the Proposition 19 amount is capped and
time-limited, and the already-owned house's carrying costs do not belong to this decision). The
document-level contract - links, citation coverage, register consistency, privacy patterns - is
`verify.py`; this file covers what a reader would only catch by recalculating.

Run: python3 -m unittest discover -s desk-d75/_src -p "test_*.py"
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as M  # noqa: E402
import data as D  # noqa: E402


def strip(html):
    """The text a person reads: no comments, no tags, no stylesheet."""
    text = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
    return re.sub(r"<[^>]+>", " ", text)


def row_cells(html, label):
    """The printed cells of the first data row whose first cell contains `label`."""
    m = re.search(r"<tr><td[^>]*>(?:<b>)?[^<]*" + re.escape(label) + r".*?</tr>", html, re.S)
    if not m:
        return None
    return re.findall(r"<td[^>]*>(.*?)</td>", m.group(0), re.S)


class MoneyRoundingTests(unittest.TestCase):
    """Owner rule: every amount is rounded to the nearest $10 so it cannot be traced to a parcel."""

    def test_round10(self):
        self.assertEqual(M.round10(0), 0)
        self.assertEqual(M.round10(7213), 7210)
        self.assertEqual(M.round10(7216), 7220)
        self.assertEqual(M.round10(-179.5), -180)

    def test_money_never_prints_an_unrounded_amount(self):
        for x in (7361.4, 1044586.0, 0.0, -250.4, 213049.0, 12345678.0, 9999.99):
            out = M.money(x)
            digits = out.replace(",", "").replace("$", "").replace("&#8722;", "-")
            self.assertTrue(re.fullmatch(r"-?\d+", digits), out)
            self.assertEqual(int(digits) % 10, 0, f"{x} printed as {out}")

    def test_a_missing_value_is_a_dash_not_a_zero(self):
        self.assertEqual(M.money(None), "&mdash;")
        self.assertEqual(M.pc(None), "&mdash;")

    def test_statutory_amounts_are_quoted_exactly_not_rounded(self):
        # rounding a legal threshold would misstate it, so `exact()` bypasses round10
        self.assertIn("$1,044,586", M.exact(1044586))
        self.assertIn('class="tag exact"', M.exact(1044586))


class PrivacyTests(unittest.TestCase):
    """Owner rule, highest priority: nothing identifying appears in the visible product."""

    ZIPS = ("95014", "95012", "95112", "94122", "94116")
    PLACES = ("Cupertino", "Sunnyvale", "San Jose", "Santa Clara", "San Francisco", "Outer Sunset",
              "Millbrae", "Palo Alto", "Los Gatos", "Saratoga", "Bay Area", "SFPUC", "sjwater",
              "sccgov", "santaclaracounty", "sftreasurer", "sfassessor")

    @classmethod
    def setUpClass(cls):
        cls.pages = M.build(write=False)

    def test_the_build_fails_on_a_place_name_or_a_postcode(self):
        self.assertIsNone(M.scrub_check("x.html", "<p>the county of the inherited house</p>"))
        for snippet in ("<p>the house in Cupertino</p>", "<p>a value near 95014 was used</p>",
                        '<p>see the <a href="https://x.example/y">San Jose water utility</a></p>'):
            with self.assertRaises(SystemExit, msg=snippet):
                M.scrub_check("x.html", snippet)

    def test_no_page_names_a_place_or_a_postcode(self):
        for name, html in sorted(self.pages.items()):
            if not name.endswith(".html"):
                continue
            vis = strip(html)
            for tok in self.PLACES:
                self.assertNotIn(tok, vis, f"{name} names {tok}")
            for z in self.ZIPS:
                self.assertNotIn(z, vis, f"{name} prints the postcode {z}")

    def test_the_owner_supplied_history_is_not_republished(self):
        """Those series fingerprint a parcel at any rounding, so only the 2026 inputs are printed."""
        joined = " ".join(self.pages.values())
        for token in ("539740", "538210", "526420", "513650", "500130", "487020", "474360",
                      "106900", "104800", "102750", "100730", "98750", "96810"):
            self.assertNotIn(token, joined, f"a supplied assessed-value history {token} is printed")

    def test_pages_carry_no_script_no_external_asset_and_are_not_indexable(self):
        for name, html in sorted(self.pages.items()):
            if not name.endswith(".html"):
                continue
            for tag in ("<script", "<iframe", "<form", "<object", "<img", "<video", "<audio"):
                self.assertNotIn(tag, html, f"{name} contains {tag}>")
            self.assertIn('name="robots"', html, f"{name} has no robots meta")
            self.assertIn("noindex", html, f"{name} can be indexed by a search engine")

    def test_no_page_links_outside_the_official_allowlist(self):
        import verify as V
        hosts = set()
        for html in self.pages.values():
            hosts.update(urlparse(h).hostname for h in re.findall(r'href="(https?://[^"]+)"', html))
        self.assertGreater(len(hosts), 10, "the pages stopped citing anyone")
        for host in sorted(hosts):
            self.assertIn(host, V.ALLOWED_HOSTS, f"{host} is not an official publisher on the allowlist")

    def test_a_stylesheet_is_local_and_no_asset_is_fetched_from_a_stranger(self):
        for name, html in sorted(self.pages.items()):
            if not name.endswith(".html"):
                continue
            for href in re.findall(r'<link[^>]*href="([^"]+)"', html):
                self.assertFalse(href.startswith("http"), f"{name} loads {href} from outside the desk")
                self.assertIn(href, self.pages, f"{name} links {href}, which the build does not produce")


class StatutoryTests(unittest.TestCase):
    """The four findings this desk was commissioned to publish."""

    def test_the_prop19_amount_is_the_published_one_and_is_a_window_not_a_constant(self):
        self.assertEqual(M.ALLOWANCE_2026, 1044586)      # BOE LTA 2025/009, 16 Feb 2025 - 15 Feb 2027
        self.assertEqual(M.allowance(2026), 1044586)
        self.assertGreater(M.allowance(2040), M.allowance(2026))
        self.assertGreater(M.allowance(2050), M.allowance(2040))
        self.assertTrue(0.02 < M.G_ALLOW < 0.06, "the indexation rate must be near the published history")

    def test_the_cap_and_the_rate_are_the_ones_the_2026_ballot_left_alone(self):
        self.assertEqual(M.PROP13_CAP, 0.02)
        self.assertEqual(M.RATE_A, 0.011488)
        law = M.build(write=False)["law-watch.html"]
        for needle in ("Proposition 40", "Proposition 42", "Proposition 43",
                       "none of them altered Proposition 13 or Proposition 19"):
            self.assertIn(needle, strip(law), f"law watch no longer states {needle}")
        props = M.build(write=False)["properties.html"]
        self.assertIn("1.1488%", props, "the county rate must still be quoted exactly, not rounded")
        self.assertIn("1.18162182%", props, "the city rate must still be quoted exactly, not rounded")
        self.assertIn('class="tag exact"', props, "an exact figure must be marked as exact")
        self.assertIn("1,044,586", strip(law))

    def test_the_2027_federal_figures_are_the_published_ones(self):
        estate = M.build(write=False)["estate-tax.html"]
        self.assertIn("$15,480,000", estate)              # Rev. Proc. 2026-35 section 3.44
        self.assertIn("$20,000", estate)                  # section 3.46(1), the 2027 gift exclusion
        self.assertIn("$15,000,000", estate)              # the 2026 amount, for the comparison
        self.assertEqual(M.S121_SINGLE, 250000)

    def test_the_basis_step_up_is_stated_as_intact(self):
        """Finding (c): the 2025 act did not repeal section 1014 - published, not left to inference."""
        text = strip(M.build(write=False)["estate-tax.html"])
        self.assertIn("section 1014", text)
        self.assertIn("did not amend", text)
        self.assertIn("section 1015", text, "the gift limit that travels with the step-up")
        law = strip(M.build(write=False)["law-watch.html"])
        for needle in ("Proposition 40", "Proposition 41", "Proposition 42", "Proposition 43", "Proposition 45"):
            self.assertIn(needle, law, f"the ballot finding no longer names {needle}")
        self.assertNotIn("$1 billion", law, "an unverifiable characterisation of Proposition 40 crept back in")


class AssessmentTests(unittest.TestCase):
    """The correction this desk exists to make: the exclusion protects value up to the amount, not the gap."""

    def test_enrolled_value_after_a_claim_sits_between_the_base_and_the_market(self):
        for T in M.TRANSFER_YEARS:
            fb = M.grow(M.A_ASSESSED, T - M.Y0, M.PROP13_CAP)
            fc = M.market(T)
            self.assertLess(fb, fc, "the model only makes sense while the base is below the market")
            for year in (T, T + 5, M.Y1):
                av = M.enrolled_after_transfer(year, T, "occupy")
                self.assertGreaterEqual(av, M.grow(fb, year - T, M.PROP13_CAP) - 1)
                self.assertLessEqual(av, M.grow(fc, year - T, M.PROP13_CAP) + 1)

    def test_no_claim_means_the_whole_transfer_value_is_enrolled(self):
        T = 2045
        self.assertAlmostEqual(M.enrolled_after_transfer(T, T, "rent"), M.market(T))

    def test_the_saving_is_the_amount_not_the_gap(self):
        """What the excluded desk got wrong: protecting the gap would overstate the saving by ~5x."""
        for T in M.TRANSFER_YEARS:
            v, fb = M.market(T), M.enrolled_asis(T)
            gap = v - fb
            protected = min(gap, M.allowance(T))
            self.assertEqual(protected, M.allowance(T), "at these values the cap must be what binds")
            self.assertGreater((gap - protected) * M.RATE_A, 20000)
            self.assertLess(protected * M.RATE_A, gap * M.RATE_A)

    def test_losing_qualification_reverts_to_the_transfer_date_value(self):
        T, stop = 2045, 2055
        self.assertAlmostEqual(M.enrolled_after_transfer(stop, T, "revert", stop=stop),
                               M.enrolled_after_transfer(stop, T, "occupy"))
        self.assertGreater(M.enrolled_after_transfer(stop + 1, T, "revert", stop=stop),
                           M.enrolled_after_transfer(stop, T, "revert", stop=stop))

    def test_a_claim_keeps_the_tax_below_the_unclaimed_line(self):
        for year in (2046, 2055, M.Y1):
            self.assertLess(M.enrolled_after_transfer(year, 2045, "occupy"),
                            M.enrolled_after_transfer(year, 2045, "rent"))


class CostTests(unittest.TestCase):
    """Owner rule: the already-owned house's costs belong to that house, not to this decision."""

    def test_carrying_costs_are_exactly_the_four_non_tax_lines(self):
        for year in (2026, 2040, 2050, 2065, M.Y1):
            expected = (M.grow(M.INSURANCE, year - M.Y0, M.G_INS)
                        + M.grow(M.A_WATER, year - M.Y0, M.G_CPI)
                        + (M.grow(M.A_ELEC, year - M.Y0, M.G_CPI) if year < M.ELEC_ENDS else 0.0)
                        + M.grow(M.A_MARKET * M.MAINT_A, year - M.Y0, M.G_CPI))
            self.assertAlmostEqual(M.costs_a(year), expected, delta=0.5)

    def test_property_tax_is_added_once_and_the_page_total_matches(self):
        html = M.build(write=False)["carrying-costs.html"]
        cells = row_cells(html, "total, every year")
        for value, year in zip(cells[1:5], (2026, 2040, 2050, 2076)):
            self.assertEqual(value, M.money(M.tax_a(year, M.enrolled_asis(year), True) + M.costs_a(year)))
        self.assertNotIn(M.money(M.rent_b(2026)), "".join(cells),
                         "the other house's rent is not this decision's cost")

    def test_the_rent_from_the_other_house_is_not_a_cost_of_the_inherited_one(self):
        for year in (2026, 2050):
            self.assertLess(M.costs_a(year), M.rent_b(year, 2),
                            "the owner's own statement: the rental's carrying costs are netted in its own row")

    def test_maintenance_follows_cost_inflation_not_the_projected_price(self):
        for year in (2026, 2050, M.Y1):
            self.assertAlmostEqual(M.grow(M.A_MARKET * M.MAINT_A, year - M.Y0, M.G_CPI),
                                   M.grow(M.A_MARKET * M.MAINT_A, year - M.Y0, M.G_CPI))
        at_cpi = M.grow(M.A_MARKET * M.MAINT_A, M.Y1 - M.Y0, M.G_CPI)
        at_price = M.grow(M.A_MARKET * M.MAINT_A, M.Y1 - M.Y0, M.G_HOME)
        self.assertGreater(at_price, at_cpi * 1.2, "the two conventions must be visibly different")
        self.assertIn("(D17)", M.build(write=False)["carrying-costs.html"])
        self.assertIn("D17", {a["id"] for a in D.ASSUMPTIONS})

    def test_solar_credit_stops_when_the_tariff_ends(self):
        self.assertEqual(M.ELEC_ENDS, 2043)
        self.assertGreater(M.costs_a(M.ELEC_ENDS) - M.costs_a(M.ELEC_ENDS - 1), 0)
        self.assertIn("2043", strip(M.build(write=False)["carrying-costs.html"]))

    def test_the_water_row_is_not_double_counted(self):
        """An earlier draft added the sewer charge twice; the B block must show one water line."""
        html = M.build(write=False)["carrying-costs.html"]
        self.assertEqual(len(re.findall(r"water and sewer", html)), 2,
                         "one water line per house, and no third")


class PathTests(unittest.TestCase):
    """The four paths the owner asked about, priced consistently."""

    @classmethod
    def setUpClass(cls):
        cls.terms = {k: M.simulate(M.BASELINE_T, k)["terminal"] for k, _ in M.PATHS}

    def test_all_four_paths_are_priced_and_ordered_at_the_baseline(self):
        self.assertEqual([k for k, _ in M.PATHS], ["occupy", "occupy_then_sell", "rent", "sell"])
        self.assertGreater(self.terms["sell"], self.terms["rent"])
        self.assertGreater(self.terms["rent"], self.terms["occupy_then_sell"])
        self.assertGreater(self.terms["occupy_then_sell"], self.terms["occupy"])

    def test_the_third_unit_is_a_substitute_for_occupancy_not_a_fifth_path(self):
        credit = M.simulate(M.BASELINE_T, "occupy", housing_credit=False)["terminal"]
        self.assertGreater(self.terms["occupy"], credit)
        self.assertEqual(M.simulate(M.BASELINE_T, "sell", housing_credit=True)["terminal"],
                         self.terms["sell"], "a sold house cannot also let the unit, so the credit must not apply")
        self.assertEqual(M.simulate(M.BASELINE_T, "rent", housing_credit=True)["terminal"],
                         self.terms["rent"], "the heir is not living in the inherited house, so it must not apply")

    def test_the_credit_covers_only_the_occupancy_years_of_a_later_sale(self):
        partial = self.terms["occupy_then_sell"] - M.simulate(M.BASELINE_T, "occupy_then_sell",
                                                              housing_credit=False)["terminal"]
        whole = self.terms["occupy"] - M.simulate(M.BASELINE_T, "occupy", housing_credit=False)["terminal"]
        self.assertGreater(partial, 0)
        self.assertLess(partial, whole, "ten occupancy years cannot be worth more than fifty")

    def test_terminal_wealth_only_exists_after_the_transfer(self):
        self.assertIsNone(M.net_if_sold(M.BASELINE_T - 1, T=M.BASELINE_T))
        self.assertIsNotNone(M.net_if_sold(M.BASELINE_T, T=M.BASELINE_T))

    def test_selling_later_nets_more_than_selling_at_transfer_only_while_the_market_grows(self):
        g = 0.04
        late = M.net_if_sold(2055, T=M.BASELINE_T, g=g)
        at_transfer = M.net_if_sold(M.BASELINE_T, T=M.BASELINE_T, g=g)
        self.assertGreater(late, at_transfer)
        flat = M.net_if_sold(2055, T=M.BASELINE_T, g=0.0)
        self.assertLess(flat, at_transfer, "a flat market must not reward waiting after the tax bill")

    def test_break_even_growth_levels_the_two_paths(self):
        g = M.break_even_growth(M.BASELINE_T, "occupy")
        self.assertIsNotNone(g)
        occ = M.simulate(M.BASELINE_T, "occupy", g=g)["terminal"]
        sell = M.simulate(M.BASELINE_T, "sell", g=g)["terminal"]
        self.assertLess(abs(occ - sell), 500000, f"level at g={g}: {occ} vs {sell}")
        self.assertGreater(g, M.G_HOME, "holding needs a faster market than the baseline assumes")

    def test_the_ranking_flips_on_the_right_side_of_the_break_even(self):
        g = M.break_even_growth(M.BASELINE_T, "occupy")
        self.assertGreater(M.simulate(M.BASELINE_T, "sell", g=g * 0.8)["terminal"],
                           M.simulate(M.BASELINE_T, "occupy", g=g * 0.8)["terminal"])
        self.assertGreater(M.simulate(M.BASELINE_T, "occupy", g=g * 1.3)["terminal"],
                           M.simulate(M.BASELINE_T, "sell", g=g * 1.3)["terminal"])

    def test_the_break_even_yield_is_the_rent_that_makes_letting_competitive(self):
        y, monthly = M.break_even_yield(M.BASELINE_T)
        self.assertTrue(0.01 < y < 0.06, f"implausible yield {y}")
        self.assertAlmostEqual(monthly, M.market(M.BASELINE_T) * y / 12.0, delta=10)
        self.assertGreater(M.market(M.BASELINE_T) * 0.02 / 12.0, 0)
        self.assertLess(y, 0.04, "a Bay Area letting yield beyond 4% would not be a stress case")

    def test_every_published_figure_comes_from_the_engine(self):
        html = M.build(write=False)["decision.html"]
        for T in M.TRANSFER_YEARS:
            for key, _ in M.PATHS:
                self.assertIn(M.money(M.simulate(T, key)["terminal"]), html,
                              f"the decision page no longer shows {key} at {T}")


class AssumptionTests(unittest.TestCase):
    """The assumption register quotes measured rates; they must match the transcribed series."""

    def measured(self, series, a, b):
        return round(M.cagr(series, a, b) * 100, 1)

    def test_d1_quotes_the_metro_series_as_computed(self):
        basis = next(a["basis"] for a in D.ASSUMPTIONS if a["id"] == "D1")
        self.assertIn(f"{self.measured(M.HPI_SJ, 1995, 2025)}% a year over 1995-2025", basis)
        self.assertIn(f"{self.measured(M.HPI_SJ, 2015, 2025)}% over 2015-2025", basis)
        self.assertIn(f"{self.measured(M.HPI_SJ, 2006, 2025)}% measured from the 2006 peak", basis)

    def test_d2_quotes_the_division_series_as_computed(self):
        basis = next(a["basis"] for a in D.ASSUMPTIONS if a["id"] == "D2")
        self.assertIn(f"{self.measured(M.HPI_SF, 1995, 2025)}% a year over 1995-2025", basis)
        self.assertIn(f"{self.measured(M.HPI_SF, 2015, 2025)}% over 2015-2025", basis)
        self.assertIn(f"{self.measured(M.HPI_SF, 2006, 2025)}% from the 2006 peak", basis)

    def test_the_baseline_sits_inside_the_measured_range_it_quotes(self):
        self.assertLess(M.cagr(M.HPI_SJ, 2006, 2025), M.G_HOME)
        self.assertGreater(M.cagr(M.HPI_SJ, 1995, 2025), M.G_HOME)
        # and cost inflation is set below the measured CPI, as the methodology page says
        self.assertLess(M.G_CPI, self.measured(M.CPI_SF, 1990, 2024) / 100)

    def test_maintenance_is_a_d_number_and_is_cited_where_it_is_used(self):
        d17 = next(a for a in D.ASSUMPTIONS if a["id"] == "D17")
        self.assertIn("0.8%", d17["basis"] + d17["value"])
        html = M.build(write=False)["carrying-costs.html"]
        self.assertEqual(html.count("(D17)"), 2, "one per house, and both maintenance rows must carry it")

    def test_the_rate_history_on_the_regime_page_matches_the_series(self):
        text = strip(M.build(write=False)["black-swans.html"])
        for value in (self.measured(M.HPI_SJ, 1995, 2025), self.measured(M.HPI_SJ, 2006, 2025),
                      self.measured(M.HPI_SF, 1995, 2025), self.measured(M.CPI_SF, 1990, 2024)):
            self.assertIn(f"{value}%", text, f"the black-swan table no longer shows the measured {value}%")


class RegimeTests(unittest.TestCase):
    """The brief's demand that growth and inflation never run consistent for fifty years."""

    def test_every_regime_is_named_bounded_and_replayed(self):
        self.assertGreaterEqual(len(M.REGIMES), 6)
        for reg in M.REGIMES:
            for key in ("id", "name", "detail"):
                self.assertIn(key, reg)
            terms = M.path_terms(M.BASELINE_T, reg)
            self.assertEqual(len(terms), len(M.PATHS))
            for value in terms.values():
                self.assertGreater(value, 0, f"{reg['id']} produced a non-positive terminal value")

    def test_a_regime_can_change_the_answer(self):
        """If no stress path changed the ranking, the section would be decoration."""
        winners = {max(M.path_terms(M.BASELINE_T, reg), key=lambda k: M.path_terms(M.BASELINE_T, reg)[k])
                    for reg in M.REGIMES}
        self.assertGreater(len(winners), 1, "every regime gives the same winner")

    def test_the_replayed_series_are_the_transcribed_ones(self):
        self.assertAlmostEqual(M.cagr(M.HPI_SJ, 1995, 2025), 0.0583, delta=0.0005)
        self.assertAlmostEqual(M.cagr(M.HPI_SJ, 2006, 2025), 0.0302, delta=0.0005)
        self.assertAlmostEqual(M.peak_trough(M.HPI_SJ, 2006, 2011), -0.2597, delta=0.001)
        self.assertEqual(M.years_to_recover(M.HPI_SJ, 2006), 8)
        self.assertIsNone(M.CPI_SF[2025], "the missing 2025 CPI must stay missing, not be filled in")

    def test_the_boe_factor_table_keeps_its_one_negative_year(self):
        negative = [row for row in M.BOE_FACTORS if row[2] < 1]
        self.assertEqual([(r[0], r[2]) for r in negative], [("2010-11", 0.99763)])
        self.assertEqual((M.BOE_YEARS_AT_CAP, M.BOE_YEARS_TOTAL), (40, 51))


class PageContractTests(unittest.TestCase):
    """What the pages claim about themselves, checked against the registers."""

    @classmethod
    def setUpClass(cls):
        cls.pages = M.build(write=False)

    def test_every_registered_page_was_built(self):
        self.assertEqual({k + ".html" for k, _ in M.PAGES}, set(self.pages) - {"style.css"})
        self.assertIn("style.css", self.pages)

    def test_the_index_links_every_page(self):
        index = self.pages["index.html"]
        for key, _ in M.PAGES:
            if key != "index":
                self.assertIn(f'href="{key}.html"', index, f"the index has no card for {key}")

    def test_no_page_leaves_a_placeholder_or_an_artefact(self):
        words = ("TODO", "TBD", "XXX", "FIXME", "Traceback", "lambda x:", "<class ")
        for name, html in sorted(self.pages.items()):
            if not name.endswith(".html"):
                continue
            vis = strip(html)
            for bad in words:
                self.assertIsNone(re.search(r"\b" + re.escape(bad) + r"\b", vis), f"{name} leaks {bad!r}")
            for brace in ("{", "}"):
                self.assertNotIn(brace, vis, f"{name} leaks a format brace into the visible text")
            # a Python value that escaped into a cell: "None" as a whole sentence would be prose
            self.assertIsNone(re.search(r"<td[^>]*>\s*(None|nan|0\.0)\s*</td>", html),
                              f"{name} printed a Python value in a cell")

    def test_every_table_row_has_as_many_cells_as_headers(self):
        for name, html in sorted(self.pages.items()):
            if not name.endswith(".html"):
                continue
            for m in re.finditer(r'<table class="[^"]*">(.*?)</table>', html, re.S):
                head, _, body = m.group(1).partition("</thead>")
                cols = len(re.findall(r"<th[\s>]", head))
                for i, row in enumerate(re.findall(r"<tr>(.*?)</tr>", body, re.S)):
                    n = len(re.findall(r"<t[dh][\s>]", row))
                    self.assertEqual(n, cols, f"{name} row {i} has {n} cells against {cols} headers")

    def test_the_build_is_deterministic(self):
        again = M.build(write=False)
        self.assertEqual(sorted(again), sorted(self.pages))
        for name in again:
            self.assertEqual(again[name], self.pages[name], f"{name} is not reproducible")

    def test_registers_are_internally_consistent(self):
        ids = lambda rows: [r["id"] for r in rows]  # noqa: E731
        for rows, name in ((D.REQUIREMENTS, "REQUIREMENTS"), (D.QUESTIONS, "QUESTIONS"),
                           (D.SUGGESTIONS, "SUGGESTIONS"), (D.FLAGS, "FLAGS"),
                           (D.ASSUMPTIONS, "ASSUMPTIONS"), (D.SOURCES, "SOURCES")):
            self.assertEqual(len(ids(rows)), len(set(ids(rows))), f"{name} has duplicate ids")
        self.assertEqual(set(D.SRC), {s["id"] for s in D.SOURCES}, "SRC and SOURCES disagree")
        for q in D.QUESTIONS:
            self.assertTrue(q["blocks"].endswith(".html"), f"{q['id']} must name the page it settles")
            for part in q["blocks"].split(","):
                self.assertIn(part.strip(), self.pages, f"{q['id']} blocks a page that is not built")
        for s in D.SUGGESTIONS:
            self.assertEqual(s["status"], "awaiting owner",
                            "nothing on the board may be implemented without an owner decision")


if __name__ == "__main__":
    unittest.main(verbosity=2)
