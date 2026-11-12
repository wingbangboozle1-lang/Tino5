# Data provenance — `swan-3a49/data/`

Session `arena-3a49d618`, retrieved 12 November 2026.

The sandbox this session runs in cannot reach these hosts from the command line, so the
files were typed from the text returned by the session's page-fetch tool. They are
transcriptions, not downloads. Anyone can reproduce them by opening the URLs below.

| File | Official source | URL |
| --- | --- | --- |
| `fred_hpi_annual.csv` | FHFA all-transactions House Price Index (San Jose metro, San Francisco metro division, California), fourth-quarter value of each year, served by the Federal Reserve Bank of St. Louis (FRED) | <https://fred.stlouisfed.org/graph/fredgraph.csv?id=ATNHPIUS41940Q,ATNHPIUS41884Q,CASTHPI&fq=Annual,Annual,Annual&fam=eop,eop,eop> |
| `fred_cpi_rates_annual.csv` | BLS CPI-U U.S. city average; BLS CPI-U San Francisco area, all items and rent of primary residence; Federal Reserve 10-year Treasury yield and 3-month Treasury bill rate; annual averages, served by FRED. Rows before 1975 were not copied. | <https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS,CUURA422SA0,CUURA422SEHA,GS10,TB3MS&fq=Annual,Annual,Annual,Annual,Annual&fam=avg,avg,avg,avg,avg> |
| `erp2026_sp500.csv` | Economic Report of the President 2026, Tables B-55 and B-56: S&P composite index at end of year and S&P dividend-price ratio | <https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026-table55.pdf>, <https://www.govinfo.gov/content/pkg/ERP-2026/pdf/ERP-2026-table56.pdf> |
| `boe_lta2026_002_factors.csv` | California State Board of Equalization, Letter to Assessors 2026/002, enclosed table of final inflation factors | <https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf> |

## Correction on record

Commit `ee7d6ec` added a file `swan-3a49/_build/series.py` whose header said every value
had been copied from the cited pages. That statement was false: the pages were not available
when the file was written and most values were entered from recall. Its "cross-check" lists
were copies of the same numbers. The file was removed in commit `261f544`.

After the pages were fetched again, the removed file was compared value by value with the
official figures in this directory (520 series values plus the BOE table). Three values
differed, all of them values the official response does not contain or states differently:

| Series | Year | Official response | Removed file had |
| --- | --- | --- | --- |
| FHFA HPI, San Jose metro | 1975 | blank | 19.14 |
| FHFA HPI, San Francisco metro division | 1975 | blank | 19.28 |
| CPI-U U.S. city average | 2025 | 321.943 | 321.9 |

Nothing in the published pages was ever built from the removed file.

## Known irregularities in the sources

- The metro house price series have no annual 1975 value in this response, so the first
  usable yearly change is 1976 to 1977.
- BLS did not collect October 2025 prices (federal shutdown; see BOE LTA 2026/002). An
  earlier request in this session returned a blank 2025 annual average for `CPIAUCNS`;
  the request on 12 November 2026 returned 321.943. The 2025 averages are therefore based
  on incomplete months.
- Table B-55, as returned, has no earnings-price column for 1971-2003; in those rows the
  last cell is the dividend-price ratio and the cell before it is the Nasdaq index. The
  S&P value is the cell directly after the Dow Jones value in every row. The four years
  that appear in both tables (2000-2003) agree.
