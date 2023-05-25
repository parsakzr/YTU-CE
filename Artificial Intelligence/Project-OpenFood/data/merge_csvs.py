import csv
import pandas as pd

FILES = [
    'ah-test-1.csv',
    'ah-test-2.csv',
    'ah-test-3.csv',
]

dataframes = []

for filename in FILES:
    df = pd.read_csv(filename)
    dataframes.append(df)

df = pd.concat(dataframes)

df.to_csv('ah.csv', index=False)