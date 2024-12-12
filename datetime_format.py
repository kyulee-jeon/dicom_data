# datetime_format.py

import pandas as pd

def datetime_form(df, dt_col):
    df[dt_col] = pd.to_datetime(df[dt_col], format='%Y-%m-%d %H:%M:%S', errors='raise')

def date_form(df, dt_col):
    df[dt_col] = pd.to_datetime(df[dt_col], format='%Y-%m-%d', errors='raise')

def datetime_to_date(df, dt_col):
    df[dt_col] = pd.to_datetime(df[dt_col], format = '%Y-%m-%d %H:%M:%S', errors='raise')
    df['date'] = pd.DatetimeIndex(df[dt_col]).date
    df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d', errors='raise')
    return df

# df['year'] = pd.DatetimeIndex(df['datetime']).year
# df['date'] = pd.DateetimeIndex(df['datetime']).date