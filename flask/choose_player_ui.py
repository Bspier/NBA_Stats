import zmq
import json


seasons = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23']
season_types = ['Playoffs', 'Regular Season']
team_dict = {
    "ATL": "Atlanta Hawks",
    "BOS": "Boston Celtics",
    "BKN": "Brooklyn Nets",
    "CHA": "Charlotte Hornets",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DAL": "Dallas Mavericks",
    "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons",
    "GSW": "Golden State Warriors",
    "HOU": "Houston Rockets",
    "IND": "Indiana Pacers",
    "LAC": "Los Angeles Clippers",
    "LAL": "Los Angeles Lakers",
    "MEM": "Memphis Grizzlies",
    "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks",
    "MIN": "Minnesota Timberwolves",
    "NOP": "New Orleans Pelicans",
    "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder",
    "ORL": "Orlando Magic",
    "PHI": "Philadelphia 76ers",
    "PHX": "Phoenix Suns",
    "POR": "Portland Trail Blazers",
    "SAC": "Sacramento Kings",
    "SAS": "San Antonio Spurs",
    "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz",
    "WAS": "Washington Wizards"
}


def choose_team():
    print("Choose a season:")
    for i, season in enumerate(seasons):
        print(f"{i+1}. {season}")
    season_choice = seasons[int(input("Your choice: ")) - 1]

    print("\nChoose a season type:")
    for i, season_type in enumerate(season_types):
        print(f"{i+1}. {season_type}")
    season_type_choice = season_types[int(input("Your choice: ")) - 1]

    print("\nChoose a team:")
    for i, (acronym, team) in enumerate(team_dict.items()):
        print(f"{i+1}. {team}")
    team_index = int(input("Your choice: ")) - 1
    team_choice = list(team_dict.keys())[team_index]
    print(season_choice, season_type_choice, team_choice)

def load_team(season, season_type, team):
    with open('nba_stats_data.json') as f:
        data = json.load(f)
    
    #print("load_data",season)

    season_data = data.get("data", {}).get(season, {})
    season_type_data = season_data.get(season_type, {})
    team_data = season_type_data.get(team, {})

    return team_data
    
    #print(player_names)

def choose_player():
    team_data = load_team('2018-19', 'Playoffs', 'GSW')
    player_names = [player['PLAYER'] for player in team_data]

    """Print players name for user to choose"""
    print("Choose a playeer: ")
    for i, name in enumerate(player_names, 1):
        print(f"{i}, {name}")

    """ask user to choose player"""
    player_choice = player_names[int(input("Your choice: ")) - 1]

    chosen_player = next(player for player in team_data if player['PLAYER'] == player_choice)

    print(f"\nStats for {chosen_player['PLAYER']}:")
    for stat, value in chosen_player.items():
        if stat != 'PLAYER':
            print(f"{stat}: {value}")



    print(player_names)

choose_player()



