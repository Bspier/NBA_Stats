import zmq

context = zmq.Context()

socket_team_opt = context.socket(zmq.REQ)
socket_team_opt.connect('tcp://localhost:9755')

socket_player_opt = context.socket(zmq.REQ)
socket_player_opt.connect('tcp://localhost:5556')

'''socket3 = context.socket(zmq.REP)
socket3.bind('tcp://*:5557')

socket4 = context.socket(zmq.REP)
socket4.bind('tcp://*:5558')'''


def get_team_options():
    try:
        while True:
            socket_team_opt.send_string("Retrieve data")
            data = socket_team_opt.recv_pyobj()
            if 'seasons' in data:
                seasons = data['seasons']
                season_types = data['season_types']
                teams = data['teams']
                break
    
    finally:
        socket_team_opt.close()
        context.term()
        '''print(seasons, season_types, teams)'''
        return seasons, season_types, teams


def choose_team(seasons, season_types, teams):
    print("Choose a season:")
    for i, season in enumerate(seasons):
        print(f"{i+1}. {season}")
    season_choice = seasons[int(input("Your choice: ")) - 1]

    print("\nChoose a season type:")
    for i, season_type in enumerate(season_types):
        print(f"{i+1}. {season_type}")
    season_type_choice = season_types[int(input("Your choice: ")) - 1]

    print("\nChoose a team:")
    for i, (acronym, team) in enumerate(teams.items):
        print(f"{i+1}. {team}")
    team_index = int(input("Your choice: ")) - 1
    team_choice = list(teams.keys())[team_index]

    return season_choice, season_type_choice, team_choice

def get_players(season_choice, season_type_choice, team_choice):
    data = (season_choice, season_type_choice, team_choice)
    try:
        socket_player_opt.send_pyobj(data)
        
        while "Error" in players:
            print("Error: no data for selections please choose another team")
            seasons, season_types, teams = get_team_options()
            season_choice, season_type_choice, team_choice = choose_team(seasons, season_types, teams)
            get_players(season_choice, season_type_choice, team_choice)
            break

        players = socket_player_opt.recv_json()  
                
    finally:
        socket_player_opt.close()
        context.term()
        return players

def choose_player(team_data):
    player_names = [player['PLAYER'] for player in team_data]

    """Print players name for user to choose"""
    print("Choose a player: ")
    for i, name in enumerate(player_names, 1):
        print(f"{i}. {name}")

    """ask user to choose player"""
    player_choice = player_names[int(input("Your choice: ")) - 1]

    chosen_player = next(player for player in team_data if player['PLAYER'] == player_choice)

    print(f"\nStats for {chosen_player['PLAYER']}:")
    for stat, value in chosen_player.items():
        if stat != 'PLAYER':
            print(f"{stat}: {value}")

