# get table for away team
with open('soup.html', 'w') as f:
    soup = ((soup.find_all("div", class_="stats-box full lineup visitor clearfix"))[0])
    f.write(str(soup.prettify()))
# get team name
team_name = soup.h2.string
# locate starters table row
starters_row = soup.find("strong", string = "STARTERS")
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
reserves_row = soup.find("strong", string = "RESERVES")
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

