```markdown
# Real Dataset Investigation — UCR Arrest Patterns, 1960–1962

An end-to-end data analysis project built on a real, messy, historical dataset:
the FBI's **Uniform Crime Reporting (UCR) Program** data, published by ICPSR.

The goal isn't to make charts. It's to show the full analytical process —
picking a question worth answering, auditing data quality, cleaning it with
documented decisions, exploring what's there, and landing on findings that
mean something.

**[→ Read the findings report](report/findings.md)**

## The Data

| Field | Value |
|---|---|
| **Source** | [ICPSR Study 02538 — Uniform Crime Reporting Program Data](https://www.icpsr.umich.edu/web/NACJD/studies/2538) |
| **Archive** | National Archive of Criminal Justice Data (NACJD), University of Michigan |
| **Format** | Stata `.dta`, one file per year |
| **Years covered** | 1960, 1961, 1962 |
| **Rows (after cleaning)** | 68,486 agency × offense records |
| **Columns (after cleaning)** | 53 |
| **License** | Public-use, no affiliation required |

Data was obtained directly from the ICPSR archive at the University of Michigan.
The study bundles the raw files with a single codebook that decodes all 72 original
column names — essential, because the variables are cryptically named (`M1`, `F17`,
`JW`, `AO1`) and the format changed mid-study.

## What This Project Covers

### The research question

Does the public-order share of arrests vary by region and agency size, and is
it stable across 1960–1962? Secondary question: does the gender split by offense
vary by region or agency size?

### The workflow

Four notebooks, each a distinct stage:

1. **`01_data_inspection.ipynb`** — Read-only audit. Loaded all three years,
   confirmed identical schemas, decoded every column against the codebook,
   catalogued nulls, duplicates, dtype mismatches, and 18 all-zero columns.
2. **`02_data_cleaning.ipynb`** — Applied the fixes. Dropped 19 dead columns,
   resolved 2 duplicate keys, cast `DIV` to string, converted `YEAR` to
   four digits, stacked into one clean frame.
3. **`03_exploratory_analysis.ipynb`** — Open-ended look. Univariate and
   bivariate patterns, top offenses, state and age distributions, gender
   splits, public-order shares. Ended with a list of questions worth
   investigating.
4. **`04_final_analysis.ipynb`** — Focused analysis. Answered the research
   questions with region and agency-size comparisons, and produced the
   figures used in the findings report.

### The findings

- **More than half of all arrests (55–56%) in every year were public-order
  offenses** — drunkenness, disorderly conduct, DUI, liquor laws, vagrancy.
- **The public-order share varied sharply by region** — Southern divisions
  at 62–64%, Middle Atlantic and West North Central at ~45%.
- **Agency size had no effect.** Small towns and big cities enforced
  public-order offenses at similar rates.
- **The pattern held steady across all three years.** No region flipped.
- **Gender split by offense was offense-driven** — prostitution near parity,
  robbery under 10% — and stable across regions, agency sizes, and years.

Full write-up with tables and caveats: **[Here](Notebooks/04_final_analysis.ipynb)**

## Repository Structure

```
real-dataset-investigation/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── Data/
│   ├── Raw/            ← original .dta files, untouched
│   └── Filtered/       ← cleaned CSV output
│
├── Notebooks/
│   ├── 01_data_inspection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   └── 04_final_analysis.ipynb
│
├── src/
│   ├── data_cleaning.py
│   └── analysis.py
│
└── figures/            ← exported charts referenced in the report
```

## Tools

- **Python 3** — pandas for data work, matplotlib for plotting
- **Jupyter** — for the four investigation notebooks
- **VS Code** — development environment

The `src/` folder holds reusable Python functions — cleaning pipeline and
analysis helpers — so the same logic isn't rewritten across notebooks.

## Reproducing the Analysis

```bash
pip install -r requirements.txt

# then open the notebooks in order, 01 through 04
jupyter notebook Notebooks/
```

Raw data must be downloaded separately from ICPSR (link above). The cleaned
CSV is included in `Data/Filtered/` so the analysis notebooks can be run
without re-downloading the source.

## Why This Project Exists

To demonstrate genuine data analysis on a real, imperfect dataset. The UCR
files are old, cryptic, and full of quirks — 18 entirely empty columns, a
mid-study format change, duplicate keys, category mismatches across years.
Working with them required every stage of the analytical pipeline, from
reading the codebook to writing the final report.

The deliverable isn't a chart. It's a defensible answer to a question, with
the evidence and reasoning shown.

## Data Source

Raw data: [ICPSR 02538](https://www.icpsr.umich.edu/web/NACJD/studies/2538),
National Archive of Criminal Justice Data. Public-use, distributed under
ICPSR's terms of use.
```