import zmq
import pandas as pd
import requests
import os

context = zmq.Context()

socket_team_opt = context.socket(zmq.REQ)
socket_team_opt.connect('tcp://localhost:9755')

socket_player_opt = context.socket(zmq.REQ)
socket_player_opt.connect('tcp://localhost:5556')

socket_web_scrape = context.socket(zmq.REQ)
socket_web_scrape.connect('tcp://localhost:5557')

socket_user_function = context.socket(zmq.REQ)
socket_user_function.connect('tcp://localhost:5558')

socket_top_five = context.socket(zmq.REQ)
socket_top_five.connect('tcp://localhost:5559')

def start_scrape():
    '''
    Gathers player data from the nab website
    '''
    socket_web_scrape.send_string('Start scraping')

    if socket_web_scrape.recv_string == 'Done':
        return 
    
def get_user_function():
    '''
    gathers the functions available to be used
    '''
    socket_user_function.send_string('get functions')
    recieved = socket_user_function.recv_pyobj()
    
    return recieved

def choose_user_function(user_functions):
    '''
    takes functions available and list them in order with an assigned value
    that a user can then enter to choose which function they want to try 
    '''
    while True:
        print("Choose a option:")
        for i, function in enumerate(user_functions):
            print(f"{i+1}. {function}")
        print(f"{len(user_functions) + 1}. Quit")

        choice = int(input("Your choice: "))

        if choice == 3:
            return "Quit"

        elif choice > len(user_functions) + 1 or choice < 0:
            print('Please choose one of the values listed')
            continue
        
        else:
            break
    
    return choice

def get_team_options():
    '''
    Gathers the team filters that a user can pick through to eventually choose a player 
    who's stats they want to see
    '''
    socket_team_opt.send_string("Retrieve data")
    data = socket_team_opt.recv_pyobj()

    seasons = data['seasons']
    season_types = data['season_types']
    teams = data['teams']
            
    return seasons, season_types, teams


def choose_team(seasons, season_types, teams):
    '''
    Uses info from get_team_options to allow usere to pick which team filters they want
    '''

    while True:
        print("Choose a season:")
        for i, season in enumerate(seasons):
            print(f"{i+1}. {season}")
        print(f"{len(seasons) + 1}. Go back to home page")
        choice = int(input("Your choice: ")) - 1
        if choice == len(seasons):
            return "back to home"
        elif choice > len(seasons) or choice < 0:
            print('Please choose one of the values listed')
            continue
        else:
            season_choice = seasons[choice]


        while True:
            print("\nChoose a season type:")
            for i, season_type in enumerate(season_types):
                print(f"{i+1}. {season_type}")
            print(f"{len(season_types) + 1}. Go back to home page")
            print(f"{len(season_types) + 2}. Redo previous choice")
            choice = int(input("Your choice: ")) - 1
            if choice == len(season_types):
                return "back to home"
            elif choice == len(season_types) + 1:
                break
            elif choice > len(season_types) + 1 or choice < 0:
                print('Please choose one of the values listed')
                continue
            else:
                season_type_choice = season_type[choice]    

            while True:
                print("\nChoose a team:")
                for i, (_, team) in enumerate(teams.items()):
                    print(f"{i+1}. {team}")
                print(f"{len(teams) + 1}. Go back to home page")
                print(f"{len(teams) + 2}. Redo previous choice")
                choice = int(input("Your choice: ")) - 1
                if choice == len(teams):
                    return "back to home"
                elif choice == len(teams) + 1:
                    break
                elif choice > len(teams) + 1 or choice < 0:
                    print('Please choose one of the values listed')
                    continue
                else:
                    team_choice = list(teams.keys())[choice]

                return season_choice, season_type_choice, team_choice

def get_players(season_choice, season_type_choice, team_choice):
    '''
    Once thee user has picked which team filters this function gathers the players from that chosen
    season, season type, and team
    '''
    while True: 
        data = (season_choice, season_type_choice, team_choice)

        socket_player_opt.send_pyobj(data)
        players = socket_player_opt.recv_json()  

        return players

def choose_player(team_data):
    '''
    allows users to pick a player from the data get teams retrieved
    '''
    player_names = [player['PLAYER'] for player in team_data]

    print("Choose a player: ")
    for i, name in enumerate(player_names, 1):
        print(f"{i}. {name}")
    print(f"{len(player_names) + 1}. Go back to home page")
    print(f"{len(player_names) + 2}. Redo team choices")

    choice = int(input("Your choice: "))

    if choice == len(player_names) + 1:
        return "back to home"
    
    elif choice == len(player_names) + 2:
        return "redo"
    
    else:
        player_choice = player_names[choice - 1]
        chosen_player = next(player for player in team_data if player['PLAYER'] == player_choice)

    print(f"\nStats for {chosen_player['PLAYER']}:")
    for stat, value in chosen_player.items():
        if stat != 'PLAYER':
            print(f"{stat}: {value}")

def top_five_ui():
    '''
    Groupmates microservice
    '''

    pd.set_option('display.max_columns', None)
    NBA_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2022-23&SeasonType=Playoffs&StatCategory=PTS'
    data = requests.get(url=NBA_url).json()
    table_headers = data['resultSet']['headers']

    socket_top_five.send_pyobj(('PTS', data))

    resposnse = socket_top_five.recv_string()
    print(resposnse)

if __name__ == "__main__":
    '''start_scrape()'''

    while True:
        os.system('cls')
        print("NBA Players Stats")
        user_functions = get_user_function()

        function_choice = choose_user_function(user_functions)
        if function_choice == 'Quit':
            socket_user_function.send_string("Close")

            socket_team_opt.send_string("Close")
            socket_player_opt.send_pyobj(["Close"])
            socket_top_five.send_pyobj(["Close"])

            print("Thanks for using NBA Player Stats")
            break
            
        
        elif function_choice == 1:
            os.system('cls')
            while True:
                seasons, season_types, teams = get_team_options()
                choose_team_data = choose_team(seasons, season_types, teams)
                if choose_team_data == 'back to home':
                    break
                else: 
                    season_choice, season_type_choice, team_choice = choose_team_data

                choose_team_data = get_players(season_choice, season_type_choice, team_choice)
                print('')

                player_data = choose_player(choose_team_data)
                if player_data == 'back to home':
                    break

                if player_data == 'redo':
                    continue
                
                print("\nChoose Option")
                print("1. Choose another team")
                print("2. Go to main menu")
                user_choice = int(input("Your choice: "))
                while user_choice != 1 and user_choice != 2:
                    print("\nChoose a Valid Option")
                    print("1. Choose another team")
                    print("2. Go to main menu")
                    user_choice = int(input("Your choice: "))

                os.system('cls')

                if user_choice == 1:
                    continue
                elif user_choice == 2:
                    break

            
        elif function_choice == 2:
            os.system('cls')
            while True:
                top_five_ui()
                print("Input 1 to go to main menu")
                print("1. Main Menu")
                user_choice = int(input("Your choice: "))
                while user_choice != 1:
                    print("Input 1 to go to main menu")
                    print("1. Main Menu")
                    user_choice = int(input("Your choice: "))
                if user_choice == 1:
                    break 
        
        os.system('cls')




