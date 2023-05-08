import pandas as pd
import requests
import time
import numpy as np
pd.set_option('display.max_columns', None)
NBA_leaders = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2022-23&SeasonType=Playoffs&StatCategory=PTS'
req = requests.get(url = NBA_leaders).json()
table_headers = req['resultSet']['headers']

data_frame_col = ['Year', 'Season_type'] + table_headers
data_frame = pd.DataFrame(columns=data_frame_col)

season_type = ['Regular%20Season', 'Playoffs']
seasons = ['2022-23']

for year in seasons:
    for season in season_type:
        league_leaders_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season='+year+'&SeasonType='+season+'&StatCategory=PTS'
        r = requests.get(url = league_leaders_url).json()
        
        data_frame1 = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
        data_frame2 = pd.DataFrame({'Year' : [year for i in range(len(data_frame1))], 'Season_type': [season for i in range(len(data_frame1))]})
        data_frame3 = pd.concat([data_frame2, data_frame1], axis = 1)
        data_frame = pd.concat([data_frame, data_frame3], axis = 0)
        time.sleep(5)
        print('finished scraping year: ', year, ' Season: ', season)

data_frame.to_json(r'C:/Users\bspie\Documents/GitHub/cs361-course-project/flask/nba_stats_data.json', orient = 'table' )
print(data_frame)

