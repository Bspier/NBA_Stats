import pandas as pd
import requests
import time
import json
import zmq

context = zmq.Context()
socket_start_scraping = context.socket(zmq.REP)
socket_start_scraping.bind('tcp://*:5557')

try:   
    while True:    
        recieved = socket_start_scraping.recv_string()
        if recieved == "Close":
            break
        elif recieved =='Start scraping':

            pd.set_option('display.max_columns', None)

            NBA_leaders = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2022-23&SeasonType=Playoffs&StatCategory=PTS'
            req = requests.get(url=NBA_leaders).json()
            table_headers = req['resultSet']['headers']

            data = {
                "data": {
                }
            }

            season_type = ['Regular Season']
            seasons = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23']

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
            
            socket_start_scraping.send_string('Done')

finally:
    socket_start_scraping.close()
    context.term()
