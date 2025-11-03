import yfinance as yf
import pandas as pd
# At first the aim is just to gather info for an individual stock and save it to a file, later on I will attempt to do this for all stocks gathered in stockTickers.csv
def stockInfoGather(tickerName=[]):
    ticker=tickerName
    data = yf.download(ticker, start='2010-01-01', end='2025-11-03', auto_adjust=False)
    return data 

df = pd.read_csv("stockTickers.csv")
tickerList = []
# Grabs the first stock in the csv file, can obviously be changed as needed (up to 3000 and/or len(df))
for i in range(1):
    tickerList.append(df["Ticker"].iloc[i])
print(tickerList)
stockData = stockInfoGather(tickerList)
stockData.to_csv("testStockPull.csv")

