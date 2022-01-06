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


urls = [
    'https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/',
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-active/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-losers/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-most-volatile/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-overbought/', 
    # 'https://www.tradingview.com/markets/stocks-usa/market-movers-oversold/'
    ]


user_agent = "Moxilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
FirefoxDriverPath = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
FirefoxProfile = webdriver.FirefoxProfile()
FirefoxProfile.set_preference("general.useragent.override", user_agent)
browser = webdriver.Firefox(executable_path=FirefoxDriverPath)
browser.implicitly_wait(7)
browser.maximize_window()

for url in urls:
    #url = "https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/"
    browser.get(url)



    file_base_name = url.split('/')[-2]

    print(f"Scraping {url}...")

    xlwriter = pd.ExcelWriter(file_base_name + '.xlsx')

    categories = [
        'Overview', 'Preformance', 'Valuation', 'Dividends', 'Margins', 'Income Statement',
        'Balance Sheet', 'Oscillators', 'Trend-Following']

    for category in catagories:
        print(f"Processing report: {category}")

        try:
            element_tab = browser.find_element_by_xpath(f'//div[text()="{category}"]')
            try:
                element_tab.click()
            except ElementNotInteractableException:
                pass
            #'tv-data-table'
            time.sleep(3.5)

            df = pd.read_html(browser.page_source)[0]
            df.replace('-', '', inplace=True)
            df.to_excel(xlwriter, sheet_name=category, index=False)


        except (NoSuchElementException, TimeoutException):
            print(f"Report {category} is not found")
            continue
    xlwriter.save()

browser.quit()