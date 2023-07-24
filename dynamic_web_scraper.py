from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd

from bs4 import BeautifulSoup

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

# loop for AWAY team
# get table for away team
with open('soup.html', 'w') as f:
    visitor_soup = ((soup.find_all("div", class_="stats-box full lineup visitor clearfix"))[0])
    f.write(str(visitor_soup.prettify()))
# get team name
team_name = visitor_soup.h2.string
# locate starters table row
starters_row = visitor_soup.find("strong", string = "STARTERS")
# get table row element of first player in starters tab
player = (starters_row.parent.parent).find_next_sibling("tr")
# while loop for when player var is not empty
while player != None:
    number_stats = player.find_all("td")
    # add player data to a dictionary
    new_row = {
        'Team': team_name,
        'Player': player.find("a", class_="player-name").string,
        'Number': player.find("span", class_="uniform").string,
        'Position': player.find("span", class_="position").string,
        'Starter': True,
        'MIN': number_stats[0].string,
        'FGM-A': number_stats[1].string,
        '3PM-A': number_stats[2].string,
        'FTM-A': number_stats[3].string,
        'OREB': number_stats[4].string,
        'DREB': number_stats[5].string,
        'REB': number_stats[6].string,
        'AST': number_stats[7].string,
        'STL': number_stats[8].string,
        'BLK': number_stats[9].string,
        'TO': number_stats[10].string,
        'PF': number_stats[11].string,
        'PTS': number_stats[12].string
    }
    # add player data to dataframe
    df.loc[len(df)] = new_row
    # look for next player (will return None if there isn't one)
    player = player.find_next_sibling("tr")

# locate reserves table row
reserves_row = visitor_soup.find("strong", string = "RESERVES")
# get table row element of first player in starters tab
player = (reserves_row.parent.parent).find_next_sibling("tr")
# while loop for when player var is not empty
while player != None:
    number_stats = player.find_all("td")
    # add player data to a dictionary
    new_row = {
        'Team': team_name,
        'Player': player.find("a", class_="player-name").string,
        'Number': player.find("span", class_="uniform").string,
        'Position': player.find("span", class_="position").string,
        'Starter': False,
        'MIN': number_stats[0].string,
        'FGM-A': number_stats[1].string,
        '3PM-A': number_stats[2].string,
        'FTM-A': number_stats[3].string,
        'OREB': number_stats[4].string,
        'DREB': number_stats[5].string,
        'REB': number_stats[6].string,
        'AST': number_stats[7].string,
        'STL': number_stats[8].string,
        'BLK': number_stats[9].string,
        'TO': number_stats[10].string,
        'PF': number_stats[11].string,
        'PTS': number_stats[12].string
    }
    # add player data to dataframe
    df.loc[len(df)] = new_row
    # look for next player (will return None if there isn't one)
    player = player.find_next_sibling("tr")

    # skipping TEAM row in table
    if player.find("a", class_="player-name") == None:
        break

# loop for HOME team
# get table for home team
with open('soup.html', 'w') as f:
    home_soup = ((soup.find_all("div", class_="stats-box full lineup home clearfix"))[0])
    f.write(str(home_soup.prettify()))
# get team name
team_name = home_soup.h2.string
# locate starters table row
starters_row = home_soup.find("strong", string = "STARTERS")
# get table row element of first player in starters tab
player = (starters_row.parent.parent).find_next_sibling("tr")
# while loop for when player var is not empty
while player != None:
    number_stats = player.find_all("td")
    # add player data to a dictionary
    new_row = {
        'Team': team_name,
        'Player': player.find("a", class_="player-name").string,
        'Number': player.find("span", class_="uniform").string,
        'Position': player.find("span", class_="position").string,
        'Starter': True,
        'MIN': number_stats[0].string,
        'FGM-A': number_stats[1].string,
        '3PM-A': number_stats[2].string,
        'FTM-A': number_stats[3].string,
        'OREB': number_stats[4].string,
        'DREB': number_stats[5].string,
        'REB': number_stats[6].string,
        'AST': number_stats[7].string,
        'STL': number_stats[8].string,
        'BLK': number_stats[9].string,
        'TO': number_stats[10].string,
        'PF': number_stats[11].string,
        'PTS': number_stats[12].string
    }
    # add player data to dataframe
    df.loc[len(df)] = new_row
    # look for next player (will return None if there isn't one)
    player = player.find_next_sibling("tr")

# locate reserves table row
reserves_row = home_soup.find("strong", string = "RESERVES")
# get table row element of first player in starters tab
player = (reserves_row.parent.parent).find_next_sibling("tr")
# while loop for when player var is not empty
while player != None:
    number_stats = player.find_all("td")
    # add player data to a dictionary
    new_row = {
        'Team': team_name,
        'Player': player.find("a", class_="player-name").string,
        'Number': player.find("span", class_="uniform").string,
        'Position': player.find("span", class_="position").string,
        'Starter': False,
        'MIN': number_stats[0].string,
        'FGM-A': number_stats[1].string,
        '3PM-A': number_stats[2].string,
        'FTM-A': number_stats[3].string,
        'OREB': number_stats[4].string,
        'DREB': number_stats[5].string,
        'REB': number_stats[6].string,
        'AST': number_stats[7].string,
        'STL': number_stats[8].string,
        'BLK': number_stats[9].string,
        'TO': number_stats[10].string,
        'PF': number_stats[11].string,
        'PTS': number_stats[12].string
    }
    # add player data to dataframe
    df.loc[len(df)] = new_row
    # look for next player (will return None if there isn't one)
    player = player.find_next_sibling("tr")

    # skipping TEAM row in table
    if player.find("a", class_="player-name") == None:
        break

print('HOORAY!!')