# Movie Search (Python + Flask + TMDB API)

A Flask backend that calls the TMDB API and serves a small search UI.
The API key stays on the server.

## Setup
1. Get a free API key: https://www.themoviedb.org/settings/api
2. Create a virtual environment and install dependencies:

       python -m venv .venv
       source .venv/bin/activate        # Windows: .venv\Scripts\activate
       pip install -r requirements.txt

3. Copy `.env.example` to `.env` and put your key in it:

       TMDB_API_KEY=your_real_key

4. Run:

       python app.py

   Open http://127.0.0.1:5000

## Endpoints
- `GET /api/search?q=inception&page=1`  search (empty `q` = trending)
- `GET /api/movie/<id>`                  movie details
