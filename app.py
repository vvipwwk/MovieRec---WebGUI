"""INTI Movie Recommendation System — Web GUI (IMDb-powered)."""

import os
import secrets

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session

from movierec import FUN_FACTS, MOOD_RESPONSES, STARS, detect_genre, get_age_group, is_surprise_request

load_dotenv()

import imdb_service

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "inti-movie-rec-secret-change-in-production")
SESSION_API_KEYS = {}


def _imdb_error_response(exc: Exception):
    msg = str(exc)
    if "OMDB_API_KEY" in msg:
        return jsonify({
            "error": msg,
            "setup_required": True,
        }), 503
    return jsonify({"error": msg}), 502


def _save_api_key(api_key: str) -> None:
    key_id = session.get("api_key_id") or secrets.token_urlsafe(24)
    session["api_key_id"] = key_id
    SESSION_API_KEYS[key_id] = api_key


def _session_api_key() -> str | None:
    return SESSION_API_KEYS.get(session.get("api_key_id", ""))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/session", methods=["POST"])
def start_session():
    data = request.get_json(force=True)
    name = (data.get("name") or "Guest").strip() or "Guest"
    age = data.get("age")
    omdb_api_key = (data.get("omdbApiKey") or "").strip()

    try:
        age = int(age)
    except (TypeError, ValueError):
        return jsonify({"error": "Please enter a valid age (1–100)."}), 400

    if not 1 <= age <= 100:
        return jsonify({"error": "Please enter a valid age (1–100)."}), 400

    if not omdb_api_key:
        return jsonify({
            "error": "Please enter your OMDb API key to start.",
            "setup_required": True,
        }), 400

    try:
        imdb_service.validate_api_key(omdb_api_key)
    except RuntimeError as exc:
        return _imdb_error_response(exc)
    except LookupError:
        return jsonify({"error": "That OMDb API key was rejected. Please check the key and try again."}), 400

    age_group = get_age_group(age)
    session["name"] = name
    session["age"] = age
    session["age_group"] = age_group
    session["watchlist"] = []
    _save_api_key(omdb_api_key)

    genres = imdb_service.get_all_genres(age_group)

    greeting = (
        f"Hey {name}! At {age}, you've got access to our full IMDb catalogue."
        if age_group == "adult"
        else f"Awesome! You're {age} — we've got family-friendly picks from IMDb for you!"
    )

    return jsonify({
        "name": name,
        "age": age,
        "age_group": age_group,
        "greeting": greeting,
        "genres": genres,
        "source": "IMDb via OMDb API",
    })


def _require_session():
    if "age_group" not in session:
        return None, None, (jsonify({"error": "Session expired. Please refresh and sign in again."}), 401)
    api_key = _session_api_key()
    if not api_key:
        return None, None, (jsonify({"error": "OMDb API key expired. Please refresh and sign in again."}), 401)
    return session["age_group"], api_key, None


@app.route("/api/genres")
def list_genres():
    age_group, _, err = _require_session()
    if err:
        return err
    return jsonify({"genres": imdb_service.get_all_genres(age_group)})


@app.route("/api/movies")
def list_movies():
    age_group, api_key, err = _require_session()
    if err:
        return err

    query = request.args.get("q", "").strip()
    genre = request.args.get("genre", "").strip()

    try:
        if genre:
            if not imdb_service.is_genre_available(genre, age_group):
                return jsonify({
                    "movies": [],
                    "blocked": True,
                    "message": (
                        f"{genre} movies contain mature content and are reserved for viewers 18+."
                    ),
                })
            movies = imdb_service.search_by_genre(genre, age_group, api_key=api_key)
            return jsonify({
                "movies": movies,
                "genre": genre,
                "mood_response": MOOD_RESPONSES.get(genre, ""),
                "fun_fact": FUN_FACTS.get(genre, ""),
            })

        if query:
            movies = imdb_service.search_movies(query, age_group, api_key=api_key)
            return jsonify({"movies": movies, "count": len(movies)})

        movies = imdb_service.browse_popular(age_group, api_key=api_key)
        return jsonify({"movies": movies, "count": len(movies)})
    except RuntimeError as exc:
        return _imdb_error_response(exc)
    except LookupError as exc:
        return jsonify({"error": str(exc), "movies": [], "count": 0})


@app.route("/api/movie/<imdb_id>")
def movie_detail(imdb_id):
    _, api_key, err = _require_session()
    if err:
        return err

    genre = request.args.get("genre")
    try:
        movie = imdb_service.get_movie_details(imdb_id, genre, api_key)
        return jsonify({"movie": movie})
    except RuntimeError as exc:
        return _imdb_error_response(exc)
    except LookupError as exc:
        return jsonify({"error": str(exc)}), 404


@app.route("/api/chat", methods=["POST"])
def chat():
    age_group, api_key, err = _require_session()
    if err:
        return err

    data = request.get_json(force=True)
    user_text = (data.get("message") or "").strip()

    if not user_text:
        return jsonify({"reply": "Tell me what mood you're in, or pick a genre from the sidebar!"})

    try:
        if is_surprise_request(user_text):
            movie = imdb_service.surprise_movie(age_group, api_key)
            if not movie:
                return jsonify({"reply": "No movies available for your age group right now."})
            return jsonify({
                "reply": f"How about {movie['title']} ({movie['year']}) — {movie['genre']}?",
                "type": "surprise",
                "movie": movie,
            })

        genre = detect_genre(user_text)
        if genre is None:
            movies = imdb_service.search_movies(user_text, age_group, api_key=api_key)
            if movies:
                return jsonify({
                    "reply": f"I found {len(movies)} IMDb match(es) for your search:",
                    "type": "search",
                    "movies": movies,
                })
            return jsonify({
                "reply": (
                    "Hmm, I'm not sure what you're looking for. "
                    "Try words like funny, scary, romantic, action, sci-fi, fantasy, or anime — "
                    "or click a genre on the left!"
                ),
                "type": "unknown",
            })

        if not imdb_service.is_genre_available(genre, age_group):
            return jsonify({
                "reply": (
                    f"{genre} movies contain mature content (violence, adult themes, etc.). "
                    "They're reserved for viewers 18+. How about Comedy, Animation, Fantasy, or Sci-Fi?"
                ),
                "type": "blocked",
                "genre": genre,
            })

        movies = imdb_service.search_by_genre(genre, age_group, api_key=api_key)
        return jsonify({
            "reply": MOOD_RESPONSES.get(genre, "Here are some picks from IMDb!"),
            "type": "genre",
            "genre": genre,
            "movies": movies,
            "fun_fact": FUN_FACTS.get(genre, ""),
        })
    except RuntimeError as exc:
        return _imdb_error_response(exc)
    except LookupError as exc:
        return jsonify({"reply": str(exc), "type": "error"})


@app.route("/api/surprise", methods=["POST"])
def api_surprise():
    age_group, api_key, err = _require_session()
    if err:
        return err

    try:
        movie = imdb_service.surprise_movie(age_group, api_key)
        if not movie:
            return jsonify({"error": "No movies available."}), 404
        return jsonify({"movie": movie})
    except RuntimeError as exc:
        return _imdb_error_response(exc)


@app.route("/api/watchlist", methods=["GET", "POST"])
def watchlist():
    _, _, err = _require_session()
    if err:
        return err

    if request.method == "GET":
        items = session.get("watchlist", [])
        return jsonify({"watchlist": items})

    data = request.get_json(force=True)
    title = data.get("title")
    genre = data.get("genre")
    your_rating = data.get("your_rating", 0)
    imdb_id = data.get("imdb_id", "")

    if not title or not genre:
        return jsonify({"error": "Missing movie details."}), 400

    rating_val = int(your_rating) if your_rating else 0
    entry = {
        "title": title,
        "genre": genre,
        "imdb_id": imdb_id,
        "your_rating": rating_val,
        "stars": STARS[rating_val] if rating_val else "",
    }
    wl = session.get("watchlist", [])
    wl.append(entry)
    session["watchlist"] = wl
    session.modified = True

    return jsonify({
        "message": f"Added '{title}' to your watchlist!",
        "watchlist": wl,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
