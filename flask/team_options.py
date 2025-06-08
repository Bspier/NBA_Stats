import zmq

context = zmq.Context()

socket_team_opt = context.socket(zmq.REP)
socket_team_opt.bind('tcp://*:9755')

seasons = ['2018-19', '2019-20', '2020-21', '2021-22', '2022-23']
season_types = ['Regular Season']
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

data = {'seasons':  seasons, 
        'season_types': season_types,
        'teams': team_dict
        }

try:
    while True:
        recieved = socket_team_opt.recv_string()
        if recieved == 'Retrieve data':
            print("request:", recieved)

            socket_team_opt.send_pyobj(data)
        elif recieved == "Close":
            break

finally:
    socket_team_opt.close()
    context.term()
    print(socket_team_opt)
    print("done")