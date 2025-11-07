import yfinance as yf
import pandas as pd
import time
# At first the aim is just to gather info for an individual stock and save it to a file, later on I will attempt to do this for all stocks gathered in stockTickers.csv
def stockInfoGather(tickerName=[], batchLimit=100):
    allStockList = []
    for i in range(0, len(tickerName), batchLimit):
        currentBatch = tickerList[i: i+batchLimit]
        batchNumber = (i // batchLimit) + 1
        totalBatches = (len(tickerList) // batchLimit) + 1 
        print(f"Getting batch: {batchNumber} / {totalBatches}")
        try:
            ticker = currentBatch
            data = yf.download(ticker, start='2010-01-01', end='2025-11-07', rounding=True)
            allStockList.append(data)
            time.sleep(10)
        except:
            print(f"Error occured on batch: {batchNumber}")


    finalData = pd.concat(allStockList, axis=1)
    return finalData




if __name__ == "__main__":
    df = pd.read_csv("stockTickers.csv")
    tickerList = []
    # Grabs the stock tickers in the csv file 
    for i in range(len(df["Ticker"])):
        tickerList.append(df["Ticker"].iloc[i])
    print(tickerList)
    stockData = stockInfoGather(tickerList)
    # Pulling it into a parquet file as this handles lots of data a lot better than csv files
    stockData.to_parquet("testStockPull.parquet")

