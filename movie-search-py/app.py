import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
TMDB = "https://api.themoviedb.org/3"

app = Flask(__name__)


def tmdb_get(path, **params):
    """Call TMDB from the server so the API key never reaches the browser."""
    params["api_key"] = API_KEY
    r = requests.get(f"{TMDB}{path}", params=params, timeout=10)
    r.raise_for_status()
    return r.json()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search")
def search():
    if not API_KEY:
        return jsonify(error="TMDB_API_KEY is not set. See README."), 500
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    try:
        if q:
            data = tmdb_get("/search/movie", query=q, page=page)
        else:
            data = tmdb_get("/trending/movie/week", page=page)
    except requests.RequestException as e:
        return jsonify(error=f"TMDB request failed: {e}"), 502

    movies = [
        {
            "id": m["id"],
            "title": m["title"],
            "year": (m.get("release_date") or "")[:4] or "N/A",
            "rating": round(m.get("vote_average", 0), 1),
            "overview": m.get("overview", ""),
            "poster": f"https://image.tmdb.org/t/p/w342{m['poster_path']}"
            if m.get("poster_path") else None,
        }
        for m in data["results"]
    ]
    return jsonify(
        movies=movies,
        page=data["page"],
        total_pages=min(data["total_pages"], 500),
        total_results=data["total_results"],
        query=q,
    )


@app.route("/api/movie/<int:movie_id>")
def movie(movie_id):
    try:
        m = tmdb_get(f"/movie/{movie_id}")
    except requests.RequestException as e:
        return jsonify(error=str(e)), 502
    return jsonify(
        title=m["title"],
        tagline=m.get("tagline"),
        runtime=m.get("runtime"),
        genres=[g["name"] for g in m.get("genres", [])],
        overview=m.get("overview"),
    )


if __name__ == "__main__":
    app.run(debug=True)
