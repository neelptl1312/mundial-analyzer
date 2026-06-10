import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, render_template, request, make_response
from flask_cors import CORS
from dotenv import load_dotenv

from data_fetcher import get_wc_matches, get_competition_info, GROUPS_DATA
from analytics.form_model import get_all_teams_form, get_group_teams, calculate_form_score
from analytics.xg_model import match_probabilities
from analytics.parlay_engine import build_parlay, suggest_best_picks

load_dotenv()
app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
CORS(app)

def no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def index():
    r = make_response(render_template("index.html"))
    return no_cache(r)

@app.route("/api/groups")
def api_groups():
    return jsonify(GROUPS_DATA)

@app.route("/api/teams")
def api_teams():
    teams = get_all_teams_form()
    return jsonify(teams)

@app.route("/api/teams/<group>")
def api_teams_group(group):
    return jsonify(get_group_teams(group))

@app.route("/api/team/<name>")
def api_team(name):
    return jsonify(calculate_form_score(name))

@app.route("/api/match/analyze")
def api_match_analyze():
    home = request.args.get("home", "")
    away = request.args.get("away", "")
    if not home or not away:
        return jsonify({"error": "Parámetros home y away requeridos"}), 400
    result = match_probabilities(home, away)
    result["best_picks"] = suggest_best_picks(home, away)
    return jsonify(result)

@app.route("/api/parlay", methods=["POST"])
def api_parlay():
    data = request.get_json()
    picks = data.get("picks", [])
    if not picks:
        return jsonify({"error": "Sin picks"}), 400
    return jsonify(build_parlay(picks))

@app.route("/api/matches/live")
def api_matches_live():
    matches = get_wc_matches()
    return jsonify(matches if isinstance(matches, list) else [])

@app.route("/api/status")
def api_status():
    info = get_competition_info()
    return jsonify({
        "status": "ok",
        "competition": info.get("name") if info else "Mundial 2026",
        "teams_loaded": sum(len(v) for v in GROUPS_DATA.values()),
        "version": "3.0"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
