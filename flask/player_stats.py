import json

with open('flask/nba_stats_data.json') as f:
    data = json.load(f)

player_name = 'Joel Embiid'
temp_data = None

for player_data in data['data']:
    if player_data['PLAYER'] == player_name:
        if player_data['Season_type'] == "Regular%20Season":
            player_data['Season_type'] = "Regular Season"
        temp_data = player_data
        break

temp_data.pop('index')
temp_data.pop('TEAM_ID')
temp_data.pop('EFF')
temp_data.pop('PLAYER_ID')
print(temp_data)
