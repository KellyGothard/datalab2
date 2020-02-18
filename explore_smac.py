# Script to explore SMAC dataset

import pandas as pd

digital = pd.read_csv('smac/digital.csv', nrows = 100)

print(digital.columns)
