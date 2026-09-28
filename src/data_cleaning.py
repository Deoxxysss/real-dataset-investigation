"""Cleaning pipeline for the UCR 1960-1962 detail files.

This module is the reusable version of notebooks/02_data_cleaning.ipynb.
Every step here goes back to a finding in 01_data_inspection.ipynb —
if you're wondering why something is dropped or cast, look there.

Input:  three raw .dta files in Data/Raw/
Output: one cleaned, stacked DataFrame
"""

from pathlib import Path
import pandas as pd


# Columns dropped because they carry no information in any year.
# CASEID is 100% null. The other 18 are all-zero across 1960, 1961, and 1962.
# See 01_data_inspection.ipynb — Data Quality Issues, "Critical" section.
DEAD_COLUMNS = [
    'CASEID',
    'M1', 'M2', 'M7', 'M21', 'M22', 'M23',
    'F1', 'F2', 'F7', 'F21', 'F22', 'F23',
    'JW', 'JB', 'JI', 'JO1', 'JH', 'JN',
]

# Filenames by year. Kept explicit so the mapping is obvious.
FILES = {
    1960: '../Data/Raw/02538-0002-Data1960.dta',
    1961: '../Data/Raw/02538-0004-Data1961.dta',
    1962: '../Data/Raw/02538-0006-Data1962.dta',
}


def load_one(path):
    """Load a single year's .dta file from disk."""
    return pd.read_stata(path)


def drop_dead_columns(df):
    """Remove CASEID and the 18 all-zero columns.
    """
    return df.drop(columns=DEAD_COLUMNS)


def resolve_duplicates(df):
    """Drop duplicate ORI + YEAR + OFF keys, keeping the first.

    Inspection found 2 duplicate keys in 1960 and none in 1961/1962.
    The pairs were identical rows, so keeping one is lossless.
    """
    before = len(df)
    df = df.drop_duplicates(subset=['ORI', 'YEAR', 'OFF'], keep='first')
    dropped = before - len(df)
    if dropped:
        print(f"  dropped {dropped} duplicate row(s)")
    return df


def cast_div(df):
    """Cast DIV from category to str.

    DIV is category in all three years but the value sets differ — 1960
    includes "Possessions," the other years don't. Concatenating category
    columns with mismatched sets can downgrade them to object,
    depending on the pandas version. Casting to str makes the behavior
    predictable.
    """
    df = df.copy()
    df['DIV'] = df['DIV'].astype(str)
    return df


def fix_year(df):
    """Convert two-digit YEAR (60, 61, 62) to four-digit in place."""
    df = df.copy()
    df['YEAR'] = df['YEAR'] + 1900
    return df


def clean_one(df):
    """Apply every cleaning step to a single year's frame."""
    df = drop_dead_columns(df)
    df = resolve_duplicates(df)
    df = cast_div(df)
    df = fix_year(df)
    return df


def load_and_clean_all(raw_dir, years=(1960, 1961, 1962)):
    """Full pipeline. Load each year, clean it, stack into one frame.

    Returns a single DataFrame with all years combined.
    """
    raw_dir = Path(raw_dir)
    frames = []

    for year in years:
        path = raw_dir / FILES[year]
        print(f"Loading {year}: {path.name}")
        df = load_one(path)
        df = clean_one(df)
        print(f"  {df.shape[0]} rows, {df.shape[1]} columns")
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    print(f"\nCombined: {combined.shape[0]} rows, {combined.shape[1]} columns")
    return combined