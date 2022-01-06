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
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-active/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-losers/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-most-volatile/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-overbought/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-oversold/'
    ]

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(7)
driver.maximize_window()

for url in urls:
    driver.get(url)
    file_base_name = url.split('/')[-2]
    xlwriter = pandas.ExcelWriter(file_base_name + '.xlsx')

    categories = driver.find_elements_by_xpath('//div[starts-with(@class, "item-EE_m_Lmj")]')

    for category in categories:
        print(f'Processing Report: {category.text}')
        try:
            try:
                driver.find_element_by_xpath(f'//div[text()="{category.text}"]').click()
            except ElementNotInteractableException:
                pass
            df = pandas.read_html(driver.page_source)[1]
            df.replace('-', '', inplace=True)
            df.to_excel(xlwriter, sheet_name=category.text, index=False)

        except (NoSuchElementException, TimeoutException):
            print(f"Report {category.text} is not found.")
            continue
    print('Excel file saved at {0}'.format(file_base_name + '.xlsx'))
    xlwriter.save()

driver.quit()
