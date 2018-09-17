import pandas as pd

pairs = pd.read_csv('candidate_pairs.csv', index_col=False)

print(pairs.head())
