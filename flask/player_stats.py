import json
import zmq

context = zmq.Context()
socket_player_opt = context.socket(zmq.REP)
socket_player_opt.bind("tcp://*:5556")

try:
    while True:
        
        recieved = socket_player_opt.recv_pyobj()
        print(type(recieved))
        if recieved == ["Close"]:
            break
        elif recieved is not None: 
            print('recieved')

            user_choices = recieved
            print(user_choices)

            season = user_choices[0]
            season_type = 'Regular Season'
            team = user_choices[2]

            with open('nba_stats_data.json') as f:
                data = json.load(f)

            season_data = data.get('data', {}).get(season, {})
            season_type_data = season_data.get(season_type, {})
            team_data = season_type_data.get(team, {})
        socket_player_opt.send_json(team_data) 
finally:
    socket_player_opt.close()
    context.term()
    print("done")




    







