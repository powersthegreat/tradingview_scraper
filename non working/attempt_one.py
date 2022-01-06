#importing selenium tools to use webdriver including: webdriver initialization
#key board use, and click/scroll abilities 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pandas
from bs4 import BeautifulSoup

#elminates USB error when running chrome webdriver
#error doesn't cause a problem it just takes up space
import pywin

#initializing webdriver instance and specifizing chrome as browser
PATH = "C:\Program Files (x86)\chromedriver.exe"
#loading to tradingview large-cap stocks page
driver = webdriver.Chrome(PATH)
driver.get("https://www.tradingview.com/markets/stocks-usa/market-movers-large-cap/")
driver.implicitly_wait(5)

# bf_sale_button = driver.find_element_by_xpath('//*[@id="overlap-manager-root"]/div/div[2]/div/div/div/div[2]')
# bf_sale_button.click()

# cookies_button = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/article/div[2]/div/button')
# cookies_button.click()

oscillators_button = driver.find_element_by_xpath('//*[@id="js-screener-container"]/div[2]/div[5]/div/div/div[8]/div')
oscillators_button.click()
time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'lxml')

tables = soup.find_all('table')

dfs = pandas.read_html(str(tables))

print(f'Total Tables: {len(dfs)}')
print(dfs[1])

driver.close()



