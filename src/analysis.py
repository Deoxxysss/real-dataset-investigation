"""Analysis helpers for the UCR 1960-1962 dataset.

Just the calculations that show up more than once. No plotting, no I/O.
"""

import pandas as pd


# Public-order offense codes: 210 DUI, 220 liquor, 230 drunkenness,
# 240 disorderly conduct, 250 vagrancy.
PUBLIC_ORDER = ['210', '220', '230', '240', '250']

# Age bracket widths in years. Single-year brackets are 1,
# the 25-29 through 50-54 brackets are 5.
AGE_WIDTH = {
    '3': 2, '4': 1, '5': 1, '6': 1, '8': 1, '9': 1, '10': 1, '11': 1,
    '12': 1, '13': 1, '14': 1, '15': 5, '16': 5, '17': 5, '18': 5,
    '19': 5, '20': 5,
}


def totals_by_year(df):
    """Arrests per year, plus how many agencies reported."""
    g = df.groupby('YEAR').agg(
        agencies=('ORI', 'nunique'),
        total=('total_arrests', 'sum'),
    )
    g['per_agency'] = g['total'] / g['agencies']
    return g


def public_order_share(df, by):
    """Public-order arrests as a share of total, grouped by `by`."""
    def share(group):
        po = group.loc[group['OFF'].isin(PUBLIC_ORDER), 'total_arrests'].sum()
        return po / group['total_arrests'].sum()
    return df.groupby(by).apply(share)


def gender_split(df, offenses=None):
    """Female share of arrests per offense."""
    g = df.groupby('OFF')[['total_male', 'total_female']].sum()
    g['female_share'] = g['total_female'] / (g['total_male'] + g['total_female'])
    return g.loc[offenses] if offenses is not None else g


def age_per_year(df, age_cols):
    """Arrests per year-of-age for each bracket. Skips M24/F24 (no age)."""
    cols = [c for c in age_cols if not c.endswith('24')]
    totals = df[cols].sum()
    return pd.Series({c: totals[c] / AGE_WIDTH[c[1:]] for c in cols}).sort_values(ascending=False)


def top_agencies(df, n=10):
    """Highest-arrest agencies in the dataset."""
    return df.groupby(['ORI', 'ST', 'GRP'])['total_arrests'].sum().nlargest(n)