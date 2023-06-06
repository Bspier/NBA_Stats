import pandas as pd
import requests
import time
import json

pd.set_option('display.max_columns', None)

NBA_leaders = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2022-23&SeasonType=Playoffs&StatCategory=PTS'
req = requests.get(url=NBA_leaders).json()
table_headers = req['resultSet']['headers']

data = {
    "data": {
    }
}

season_type = ['Playoffs', 'Regular Season']
seasons = ['2018-19']

for year in seasons:
    data["data"][year] = {}
    for season in season_type:
        data["data"][year][season] = {}
        season_formatted = year + ' ' + season.replace('%20', ' ')
        league_leaders_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season='+year+'&SeasonType='+season+'&StatCategory=PTS'
        r = requests.get(url=league_leaders_url).json()
        
        data_frame1 = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
        data_frame2 = pd.DataFrame({'Year': [year for i in range(len(data_frame1))], 'Season_type': [season_formatted for i in range(len(data_frame1))]})
        data_frame3 = pd.concat([data_frame2, data_frame1], axis=1)
        
        team_groups = data_frame3.groupby('TEAM')
        for team, df in team_groups:
            team_data = df.to_dict(orient='records')
            data["data"][year][season][team] = team_data
        
        time.sleep(5)
        print('Finished scraping year:', year, 'Season:', season_formatted)

with open('nba_stats_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print(data)