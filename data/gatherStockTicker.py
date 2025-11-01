# This file aims to gather the top 3000 stock tickers - ranked by company value (could be changed to higher or lower amounts in the future depending on this test)
# Data is collected from companiesmarketcap.com
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import pandas as pd



# Only used this part to test that everything worked in terms of scraping -> is no longer needed but i'll keep it :)
# def testScrape():
#
#     url = "https://example.com"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     print(soup)



def scrapeStocks():
    allStocksList = []
    i = 0
    driver = webdriver.Chrome()  
    for pageNumber in range(1, 31):
        time.sleep(1) 
        url=f"https://companiesmarketcap.com/page/{pageNumber}/"


        print(f"Currently scraping the following page: {pageNumber}")
        try: 
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rank-td"))
            )
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            stockRows = soup.find('tbody').find_all('tr')
            print(f"Found {len(stockRows)} rows with that class.")
            for row in stockRows:
                i+= 1
                print(f"{i}")
                try:
                    # This following section grabs the name, ticker, rank and market cap of the companies for each of the n pages on companiesmarketcap.com
                    nameElement = row.select_one('td.name-td div.name-div div.company-name')
                    if nameElement:
                        stockName = nameElement.text.strip()
                    stockRank = row.find('td', class_="rank-td td-right d-none").text.strip()
                    tickerElement = row.select_one('td.name-td div.name-div div.company-code')
                    if tickerElement:
                        removeUnnecessarySpan = tickerElement.find('span', class_='rank')
                        if removeUnnecessarySpan:
                            removeUnnecessarySpan.decompose()
                        stockTicker = tickerElement.text.strip()

                    data_tds = row.select('td.td-right:not(.rank-td)')
                    if data_tds:
                        marketCapElement = data_tds[0] 
                        stockMarketCap = int(marketCapElement['data-sort'])

                    allStocksList.append({'Rank': stockRank, 'Name': stockName, 'Ticker': stockTicker, 'MarketCap': stockMarketCap})
                    print(f"Successfully gathered row {i}")
                except:
                    print(f"error has occured on row: {row}")
                    pass
        except:
            print(f"Error has occured!!!!!!!! on page: {pageNumber} :(")
    df = pd.DataFrame(allStocksList)
    df.to_csv("stockTickers.csv", index=False)
if(__name__ == '__main__'):
    scrapeStocks()
