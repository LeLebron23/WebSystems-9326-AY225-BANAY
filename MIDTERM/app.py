from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from scraper import run_scraper, load_games, BASE_URL, DATA_FILE, CSV_FILE

app = Flask(__name__)

@app.route("/")
def index():
    games = load_games()
    return render_template("index.html", games=games, total=len(games))

@app.route("/scrape", methods=["POST"])
def scrape():
    data     = request.get_json(silent=True) or {}
    base_url = data.get("base_url", BASE_URL).strip() or BASE_URL
    limit    = int(data.get("limit", 15))
    limit    = max(10, min(limit, 30))
    try:
        games = run_scraper(base_url=base_url, limit=limit)
        return jsonify({"success": True, "count": len(games), "games": games})
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500

@app.route("/games")
def games_api():
    query    = request.args.get("q", "").lower()
    platform = request.args.get("platform", "").lower()
    games    = load_games()
    if query:
        games = [g for g in games if query in g.get("title","").lower()
                 or query in g.get("developer","").lower()
                 or query in g.get("genre","").lower()]
    if platform:
        games = [g for g in games if platform in g.get("platforms","").lower()]
    return jsonify(games)

@app.route("/download/json")
def download_json():
    if os.path.exists(DATA_FILE):
        return send_file(DATA_FILE, as_attachment=True, download_name="metacritic_games.json")
    return "No data yet. Run a scrape first.", 404

@app.route("/download/csv")
def download_csv():
    if os.path.exists(CSV_FILE):
        return send_file(CSV_FILE, as_attachment=True, download_name="metacritic_games.csv")
    return "No data yet. Run a scrape first.", 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)