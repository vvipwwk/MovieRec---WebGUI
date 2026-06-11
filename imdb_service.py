"""Fetch movie data from IMDb via the OMDb API (https://www.omdbapi.com)."""

from __future__ import annotations

import os
import random
import re
from urllib.parse import quote

import requests

from movierec import MOOD_MAP, MOOD_RESPONSES, FUN_FACTS, stars

OMDB_BASE = "https://www.omdbapi.com/"
YOUTUBE_SEARCH = "https://www.youtube.com/results?search_query="
YOUTUBE_WATCH = "https://www.youtube.com/watch?v="

# OMDb search terms per genre (IMDb-sourced catalogue)
GENRE_SEARCH = {
    "Sci-Fi": "sci-fi",
    "Comedy": "comedy",
    "Fantasy": "fantasy",
    "Action": "action",
    "Animation": "animation",
    "Romance": "romance",
    "Horror": "horror",
}

ADULT_ONLY_GENRES = {"Action", "Romance", "Horror"}

CHILD_BLOCKED_RATINGS = {"R", "NC-17", "TV-MA", "X", "Not Rated"}

def _api_key() -> str:
    key = os.environ.get("OMDB_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "OMDB_API_KEY is not set. Get a free key at https://www.omdbapi.com/apikey.aspx "
            "and set it as an environment variable before running the app."
        )
    return key


def _omdb(params: dict) -> dict:
    params = {**params, "apikey": _api_key()}
    resp = requests.get(OMDB_BASE, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data.get("Response") == "False":
        raise LookupError(data.get("Error", "OMDb request failed"))
    return data


def _parse_rating(value: str | None) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _normalize_detail(item: dict, genre: str | None = None, include_trailer: bool = False) -> dict:
    rating = _parse_rating(item.get("imdbRating"))
    poster = item.get("Poster", "")
    if poster in ("", "N/A"):
        poster = f"https://placehold.co/300x450/1a1a2e/e94560?text={quote(item.get('Title', 'Movie'))}"

    genres = item.get("Genre", genre or "")
    primary_genre = genre or (genres.split(",")[0].strip() if genres else "General")

    movie = {
        "imdb_id": item.get("imdbID", ""),
        "title": item.get("Title", "Unknown"),
        "year": item.get("Year", "N/A"),
        "rating": rating,
        "stars": stars(rating) if rating else "☆☆☆☆☆",
        "desc": item.get("Plot", "No description available."),
        "poster": poster,
        "genre": primary_genre,
        "rated": item.get("Rated", "N/A"),
        "genres": genres,
        "director": item.get("Director", "N/A"),
        "actors": item.get("Actors", "N/A"),
    }
    if include_trailer:
        movie["trailer_url"] = find_trailer_url(movie["title"], movie["year"])
    return movie


def _is_allowed_for_age(movie: dict, age_group: str) -> bool:
    if age_group == "adult":
        return True
    rated = (movie.get("rated") or "").upper()
    for blocked in CHILD_BLOCKED_RATINGS:
        if blocked.upper() in rated:
            return False
    return True


def get_movie_details(imdb_id: str, genre: str | None = None) -> dict:
    data = _omdb({"i": imdb_id, "plot": "full"})
    return _normalize_detail(data, genre, include_trailer=True)


def search_omdb(query: str, page: int = 1) -> list[dict]:
    data = _omdb({"s": query, "type": "movie", "page": page})
    results = []
    for hit in data.get("Search", []):
        try:
            detail = get_movie_details(hit["imdbID"])
            results.append(detail)
        except LookupError:
            continue
    return results


def search_by_genre(genre: str, age_group: str, limit: int = 10) -> list[dict]:
    term = GENRE_SEARCH.get(genre, genre)
    data = _omdb({"s": term, "type": "movie", "page": 1})
    movies = []
    for hit in data.get("Search", [])[: limit + 5]:
        try:
            detail = get_movie_details(hit["imdbID"], genre)
            if _is_allowed_for_age(detail, age_group):
                movies.append(detail)
            if len(movies) >= limit:
                break
        except LookupError:
            continue
    return movies


def search_movies(query: str, age_group: str, limit: int = 12) -> list[dict]:
    if not query.strip():
        return browse_popular(age_group, limit)

    detected = None
    text = query.lower()
    for genre, keywords in MOOD_MAP.items():
        if genre.lower() in text or any(kw in text for kw in keywords):
            detected = genre
            break

    if detected:
        if detected in ADULT_ONLY_GENRES and age_group == "child":
            return []
        return search_by_genre(detected, age_group, limit)

    data = _omdb({"s": query, "type": "movie", "page": 1})
    movies = []
    for hit in data.get("Search", [])[: limit + 5]:
        try:
            detail = get_movie_details(hit["imdbID"])
            if _is_allowed_for_age(detail, age_group):
                movies.append(detail)
            if len(movies) >= limit:
                break
        except LookupError:
            continue
    return movies


def browse_popular(age_group: str, limit: int = 12) -> list[dict]:
    """Mix results from several genres for 'browse all'."""
    pool: list[dict] = []
    genres = list(GENRE_SEARCH.keys())
    if age_group == "child":
        genres = [g for g in genres if g not in ADULT_ONLY_GENRES]

    random.shuffle(genres)
    for genre in genres[:4]:
        pool.extend(search_by_genre(genre, age_group, limit=4))

    seen = set()
    unique = []
    for m in pool:
        if m["imdb_id"] not in seen:
            seen.add(m["imdb_id"])
            unique.append(m)
    return unique[:limit]


def surprise_movie(age_group: str) -> dict | None:
    genres = list(GENRE_SEARCH.keys())
    if age_group == "child":
        genres = [g for g in genres if g not in ADULT_ONLY_GENRES]
    if not genres:
        return None

    genre = random.choice(genres)
    movies = search_by_genre(genre, age_group, limit=8)
    return random.choice(movies) if movies else None


def get_all_genres(age_group: str) -> list[dict]:
    genres = []
    for name in GENRE_SEARCH:
        available = name not in ADULT_ONLY_GENRES or age_group == "adult"
        count = "IMDb" if available else "18+"
        genres.append({
            "name": name,
            "available": available,
            "count": count,
            "mood_response": MOOD_RESPONSES.get(name, ""),
            "fun_fact": FUN_FACTS.get(name, ""),
        })
    return genres


def is_genre_available(genre: str, age_group: str) -> bool:
    if genre in ADULT_ONLY_GENRES and age_group == "child":
        return False
    return genre in GENRE_SEARCH


def find_trailer_url(title: str, year: str) -> str:
    """Resolve a YouTube trailer URL for the movie."""
    query = f"{title} {year} official trailer"
    search_url = YOUTUBE_SEARCH + quote(query)

    try:
        resp = requests.get(
            search_url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            timeout=12,
        )
        match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', resp.text)
        if match:
            return YOUTUBE_WATCH + match.group(1)
    except requests.RequestException:
        pass

    return search_url
