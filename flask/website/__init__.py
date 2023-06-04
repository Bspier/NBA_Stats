from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
import json
def create_app():
    app = Flask(__name__)

    # Load data
    with open('nba_stats_data.json') as f:
        app.config["DATA"] = json.load(f)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/api/teams/<year>/<season_type>')
    def get_teams(year, season_type):
        data = app.config["DATA"]
        teams = set(player['team'] for player in data if player['year'] == year and player['season_type'] == season_type)
        return jsonify(list(teams))

    @app.route('/api/players/<year>/<season_type>/<team>')
    def get_players(year, season_type, team):
        data = app.config["DATA"]
        players = [player['name'] for player in data if player['year'] == year and player['season_type'] == season_type and player['team'] == team]
        return jsonify(players)

    @app.route('/api/player_data/<year>/<season_type>/<team>/<player>')
    def get_player_data(year, season_type, team, player):
        data = app.config["DATA"]
        player_data = [player for player in data if player['year'] == year and player['season_type'] == season_type and player['team'] == team and player['name'] == player]
        if player_data:
            return jsonify(player_data[0])
        else:
            return jsonify({})
    
    from .views import views
    app.register_blueprint(views, url_prefix="/")

    return app