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
        EC.presence_of_element_located((By.XPATH, "//*[text() = 'Sat Feb 25']"))
    )
    date.click()

except:
    print('Date is not visible')
    driver.quit()

# create stats dataframe
df = pd.DataFrame(columns = ['Date','Notes','Home Team','Away Team','Score','Player Team','Player','Number','Position','Starter','MIN','FGM-A','3PM-A','FTM-A','OREB','DREB','REB','AST','STL','BLK','TO','PF','PTS'])

# find all games with a box score on page
num_games = len(WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//span[text() = 'Box Score']"))
))

for i in range(num_games):
    # find all gaems with a box score on page again (selenium object not valid after leaving page)
    # scroll down to for visibility of box score button
    driver.execute_script(f"window.scrollTo(0,{i*200});")
    # grab notes of game (normally type of game and/or league)
    try:
        notes = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, f"(//span[text() = 'Box Score']/../../..//span[contains(@class, 'notes')])[{i+1}]"))
        ).text
    except:
        notes = None
    # click on box score
    box_score = driver.find_element(By.XPATH, f"(//span[text() = 'Box Score']/..)[{i+1}]")
    box_score.click()
    # create soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    scrape_game_stats(soup,notes,df)
    driver.back()
    # print('HOORAY!!')

driver.quit()