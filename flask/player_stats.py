import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*5555")

while True:
    json_data = socket.recv_string()

    user_choices = json.loads(json_data)
    print(user_choices)

    season = user_choices['season']
    season_type = user_choices['season_type']
    team = user_choices['team']




def load_data(season, season_type, team):
    with open('nba_stats_data.json') as f:
        data = json.load(f)

    season_data = data.get('data', {}).get(season, {})
    season_type_data = season_data.get(season_type, {})
    team_data = season_type_data.get(team, {})
    
    return team_data






