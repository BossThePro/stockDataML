import pandas as pd 

df = pd.read_parquet("../../data/stockPull.parquet")
df = df.drop(["Adj Close"], axis=1)

# Flattening the ticker symbols since it was multiindexed before, in order to easily access the tickers 
df_flat = df.stack(level=1).reset_index()
df_flat = df_flat.rename(columns={'level_1': 'Ticker'})

df_flat = df_flat.dropna()
df_flat.to_parquet("../../data/stockPullClean.parquet")
