#importing os, time, and pywin to make things run a little smoother, more specifically pywin gets rid of usb
#errors, os helps path of webdriver be called faster, and time allows for rest periods while data loads
import pywin
import os
import time

#various selenium webdriver imports for the various commands used including the Exceptions list
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException

#importing bs4 even though it wasn't used I am afraid to touch this program and mess it up
#as well as importing pandas to create and export data frames of data pulled
from bs4 import BeautifulSoup
import pandas as pandas

#various urls from tradingviews website used to extract data from, each url has about 8 seperate tables that 
#data is pulled from
urls = [
    'https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/',
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-active/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-losers/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-most-volatile/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-overbought/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-oversold/'
       ]

#initiating driver instance and sending that instance the path where the driver is stored
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(7)
driver.maximize_window()

#iterating through different urls from tradingviews dynamic website
for url in urls:
    driver.get(url)

    #Categories of each seperate table
    categories = [
        'Overview', 'Performance', 'Valuation', 'Dividends', 'Margins', 'Income Statement',
        'Balance Sheet', 'Oscillators', 'Trend-Following'
        ]

    #naming excel file something relevant
    file_base_name = url.split('/')[-2]

    #creating instance of pandas xlwriter
    xlwriter = pandas.ExcelWriter(file_base_name + '.xlsx')

    #iterating through categories
    for category in categories:
        #giving some sense to what the program is doing at a given moment
        print(f"Processing report: {category}")

        #clicking on the category and passing if element not found
        try:
            element_tab = driver.find_element_by_xpath(f'//div[text()="{category}"]')
            
            #important click and PAUSE moment needed for ajax table to fully load in
            try:
                    element_tab.click()
                    time.sleep(4)
            except ElementNotInteractableException:
                pass

            #creating instance of dataframe and storing second listed table in it, tradingview has
            #one blank table which they use to try confuse/stop people like me
            df = pandas.read_html(driver.page_source)[1]
            df.replace('-', '', inplace=True)
            df.to_excel(xlwriter, sheet_name=category, index=False)

        #once again bringing time standards to the program so I can know 'how things are going'
        except (NoSuchElementException, TimeoutException):
            print(f"Report {category} is not found")
            continue
        driver.implicitly_wait(2)
        
    #saving dataframe to excel file in current folder
    xlwriter.save()

    #ending the webdriving instance
    driver.quit()