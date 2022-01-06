import requests as requests
from bs4 import BeautifulSoup

url = "https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/"
results = requests.get(url)
src = results.content
soup = BeautifulSoup(src, "lxml")

#intializing instance of the table
table = soup.find("table")
table_rows = table.find_all("tr")

table_rows_list = []

#acessing table rows
for tr in table_rows:
    td = tr.find_all("td")
    row = [i.text for i in td]
    table_rows_list.append(row)
del table_rows_list[0]

ticker_list = []
ticker_list_uncleaned = []
last_price_list = []
rating_list = []
volume_list = []

#adding specs from table to seperate lists
for i in range(0,100):
    last_price_list.append(table_rows_list[i][1])
for i in range(0,100):
    rating_list.append(table_rows_list[i][4])
for i in range(0,100):
    volume_list.append(table_rows_list[i][5])
for i in range(0,100):
    ticker_list_uncleaned.append(table_rows_list[i][0])

#trying to clean extra spaces form tickers
def list_cleaner(uncleaned_list):
    clean_tickers_list = []
    for tickers in uncleaned_list:
        t = tickers.strip("\n")
        clean_tickers_list.append(t)
    return clean_tickers_list

ticker_list = list_cleaner(ticker_list_uncleaned)

#zipping values together for dictionary
stats_list = list(zip(last_price_list, rating_list, volume_list))
#zipping tickers as keys and stats as values together for one big dictionary
final_dictionary = dict(zip(ticker_list, stats_list))
