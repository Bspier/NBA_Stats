import zmq
import json

context = zmq.Context()
socket_players = context.socket(zmq.REP)
socket_players.bind('tcp://*:5556')

try:
    while True:
        recieved = socket_players.recv_pyobj()
        if isinstance(recieved, tuple) and len(recieved) == 3:
            print("request:", recieved)
            
            season, season_type, team = recieved

            with open('nba_stats_data.json') as f:
                data = json.load(f)

        season_data = data.get("data", {}).get(season, {})
        season_type_data = season_data.get(season_type, {})
        team_data = season_type_data.get(team, {})

        socket_players.send_json(team_data)

finally:
    socket_players.close()
    context.term()
    print(socket_players)
    print("done")