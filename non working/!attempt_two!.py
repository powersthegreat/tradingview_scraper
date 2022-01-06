import os
import time
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pandas
import pywin

urls = [
    'https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/',
    'https://www.tradingview.com/markets/stocks-usa/market-movers-active/', 
    'https://www.tradingview.com/markets/stocks-usa/market-movers-losers/', 
    'https://www.tradingview.com/markets/stocks-usa/market-movers-most-volatile/', 
    'https://www.tradingview.com/markets/stocks-usa/market-movers-overbought/', 
    'https://www.tradingview.com/markets/stocks-usa/market-movers-oversold/'
    ]

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(7)
driver.maximize_window()

url = 'https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/'
driver.get(url)

cookies_button = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/article/div[2]/div/button')
cookies_button.click()
time.sleep(2)

cyber_monday_button = driver.find_element_by_xpath('//*[@id="overlap-manager-root"]/div/div[2]/div/div/div/div[2]')
cyber_monday_button.click()
time.sleep(2)

categories = [
    'Overview', 'Performance', 'Valuation', 'Dividends', 'Margins', 'Income Statement',
    'Balance Sheet', 'Oscillators', 'Trend-Following'
    ]

file_base_name = url.split('/')[-2]

xlwriter = pandas.ExcelWriter(file_base_name + '.xlsx')

for category in categories:
    print(f"Processing report: {category}")

    try:
        element_tab = driver.find_element_by_xpath(f'//div[text()="{category}"]')
        try:
                element_tab.click()
                time.sleep(4)
        except ElementNotInteractableException:
            pass

        df = pandas.read_html(driver.page_source)[1]
        df.replace('-', '', inplace=True)
        df.to_excel(xlwriter, sheet_name=category, index=False)


    except (NoSuchElementException, TimeoutException):
        print(f"Report {category} is not found")
        continue
    driver.implicitly_wait(2)
xlwriter.save()

driver.quit()

