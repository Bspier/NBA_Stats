from flask import Blueprint, render_template, current_app, json


views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", var="value")

@views.route("/help")
def help():
    return render_template("help.html", var="value")

@views.route("/about")
def about():
    return render_template("about.html", var="value")

@views.route("/pipeline")
def pipeline():
    return render_template("pipeline.html", val=1)


'''player stats route'''
@views.route("/player-stats")
def player_stats():
    return render_template("player_stats.html", var="value")


@views.route("/player-name")
def player_name():
    data = current_app.config["DATA"]
    return render_template("player_name.html", data=json.dumps(data))

@views.route("/player-random")
def player_random():
    return render_template("player_random.html", var="value")

@views.route("/player-compare")
def player_compare():
    return render_template("player_comp.html", var="value")


'''Team stats routes'''
@views.route("/team-stats")
def team_stats():
    return render_template("team_stats.html", var="value")

@views.route("/team-name")
def team_name():
    return render_template("team_name.html", var="value")

@views.route("/team-random")
def team_random():
    return render_template("team_random.html", var="value")

@views.route("/team-compare")
def team_compare():
    return render_template("team_comp.html", var="value")