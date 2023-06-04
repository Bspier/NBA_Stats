import json


def load_data(season, season_type):
    with open('nba_stats_data.json') as f:
        data = json.load(f)

    season_data = data.get('data', {}).get(season, {})
    season_type_data = season_data.get(season_type, {})
    
    return season_type_data

def get_data_year(data, year):