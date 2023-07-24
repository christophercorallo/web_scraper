from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd

from bs4 import BeautifulSoup

from functions import scrape_game_stats

url = "https://usports.ca/en/ticker"
driver = webdriver.Firefox(service=FirefoxService(
    GeckoDriverManager().install()
))
driver.get(url)
driver.maximize_window()

# scroll dowm
driver.execute_script("window.scrollTo(0,document.body.scrollHeight/12);")

# Switch to correct frame  id
driver.switch_to.frame('embed')

# change sport to Men's Basketball
sport_list = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'sport-filter')]"))
    )
sport_list.click()
sport = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'sport-filter')]/select/option[text() = \"Men's Basketball\"]"))
    )
sport.click()

# wait for date to be visible
try:
    date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[text() = 'Fri Mar 03']"))
    )
    date.click()

except:
    print('Date is not visible')
    driver.quit()

# click boxscore of game
boxscore = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "(//*[text() = 'Box Score']/..)"))
)
boxscore.click()

# create soup
soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.quit()

df = pd.DataFrame(columns = ['Team','Player','Number','Position','Starter','MIN','FGM-A','3PM-A','FTM-A','OREB','DREB','REB','AST','STL','BLK','TO','PF','PTS'])

scrape_game_stats(soup, df)

print('HOORAY!!')