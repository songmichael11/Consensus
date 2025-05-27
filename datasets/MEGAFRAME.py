import pandas as pd
import numpy as np

gini_df = pd.read_csv('datasets/GINI.csv')
tax_union_df = pd.read_csv('datasets/tax_union_data.csv')
gov_spending_df = pd.read_csv('datasets/gov_spending.csv')
unemp_intrate_df = pd.read_csv('datasets/OECD_LONGTERM_UNEMPLOYMENT_CLEANED.csv')
pop_gdp_inf_df = pd.read_csv('datasets/pop_gdp_inf.csv')


# rename necessary columns
gini_df = gini_df.rename(columns={'value': 'GINI', 'date': 'TIME_PERIOD', 'country': 'Reference area'})

megaframe = pd.merge(gini_df, tax_union_df, on=['Reference area', 'TIME_PERIOD'])
megaframe = megaframe.drop(columns='Unnamed: 0')

print(megaframe)