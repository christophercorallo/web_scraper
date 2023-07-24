def scrape_game_stats(game_soup, df):
    """add STARTER and RESERVE stats for BOTH teams"""
    
    # get table for AWAY team
    with open('soup.html', 'w') as f:
        away_soup = ((game_soup.find_all("div", class_="stats-box full lineup visitor clearfix"))[0])
        f.write(str(away_soup.prettify()))

    # get AWAY team name
    away_team_name = away_soup.h2.string

    # add AWAY starters
    away_starters_row = away_soup.find("strong", string = "STARTERS")
    away_first_starter = (away_starters_row.parent.parent).find_next_sibling("tr")
    append_player_stats(away_first_starter, away_team_name, True, df)

    # add AWAY reserves
    away_reserves_row = away_soup.find("strong", string = "RESERVES")
    away_first_reserve = (away_reserves_row.parent.parent).find_next_sibling("tr")
    append_player_stats(away_first_reserve, away_team_name, False, df)

    # get table for HOME team
    with open('soup.html', 'w') as f:
        home_soup = ((game_soup.find_all("div", class_="stats-box full lineup home clearfix"))[0])
        f.write(str(home_soup.prettify()))

    # get HOME team name
    home_team_name = home_soup.h2.string

    # add HOME starters
    home_starters_row = home_soup.find("strong", string = "STARTERS")
    home_first_starter = (home_starters_row.parent.parent).find_next_sibling("tr")
    append_player_stats(home_first_starter, home_team_name, True, df)

    # add HOME reserves
    home_reserves_row = home_soup.find("strong", string = "RESERVES")
    home_first_reserve = (home_reserves_row.parent.parent).find_next_sibling("tr")
    append_player_stats(home_first_reserve, home_team_name, False, df)

    



def append_player_stats(player, team_name, starter, df):
    while player != None:
        number_stats = player.find_all("td")
        # add player data to a dictionary
        new_row = {
            'Team': team_name,
            'Player': player.find("a", class_="player-name").string,
            'Number': player.find("span", class_="uniform").string,
            'Position': player.find("span", class_="position").string,
            'Starter': starter,
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

        # skipping TEAM row in reserves table
        if starter == False:
            if player.find("a", class_="player-name") == None:
                break