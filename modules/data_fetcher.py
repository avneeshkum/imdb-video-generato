# ============================================
#   modules/data_fetcher.py
#   TMDB se movie ka data aur images fetch karta hai
# ============================================

import os
import requests
from config import TMDB_API_KEY, TEMP_DIR

TMDB_BASE  = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w1280"


def search_movie(query: str, language: str = "en") -> dict:
    """Movie name se TMDB ID dhundho"""
    tmdb_lang = "hi-IN" if language == "hi" else "en-US"
    
    url    = f"{TMDB_BASE}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query, "language": tmdb_lang}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        raise ValueError(f"Koi movie nahi mili: '{query}'")
    return results[0]


def get_movie_details(movie_id: int, language: str = "en") -> dict:
    """Movie ID se full details + cast/crew"""
    tmdb_lang = "hi-IN" if language == "hi" else "en-US"
    
    url    = f"{TMDB_BASE}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY, 
        "append_to_response": "credits", 
        "language": tmdb_lang
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def get_movie_images(movie_id: int) -> dict:
    """Movie ke backdrop images"""
    url    = f"{TMDB_BASE}/movie/{movie_id}/images"
    params = {"api_key": TMDB_API_KEY}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()


def download_image(tmdb_path: str, filename: str) -> str:
    """TMDB image download karke temp folder mein save karo"""
    os.makedirs(TEMP_DIR, exist_ok=True)
    url      = f"{IMAGE_BASE}{tmdb_path}"
    filepath = os.path.join(TEMP_DIR, filename)
    
    try:
        # Timeout badha kar 30 kar diya hai
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        return filepath
    except Exception as e:
        print(f"      Warning: Image download fail ho gaya ({filename}): {e}")
        return None


def fetch_movie_data(movie_name: str, language: str = "en") -> dict:
    """
    Ek movie name lo, sab kuch fetch karo.
    Returns: cleaned movie dict with local image paths
    """
    print(f"\n[1/4] Movie dhundh raha hoon: '{movie_name}'")
    
    movie    = search_movie(movie_name, language)
    movie_id = movie["id"]
    print(f"      Mili: {movie['title']} ({movie.get('release_date','')[:4]})")

    details = get_movie_details(movie_id, language)
    images  = get_movie_images(movie_id)

    # --- Poster download ---
    poster_path = None
    if details.get("poster_path"):
        poster_path = download_image(details["poster_path"], "poster.jpg")
        if poster_path:
            print(f"      Poster downloaded.")

    # --- Upto 5 backdrops download ---
    backdrop_paths = []
    for i, bd in enumerate(images.get("backdrops", [])[:5]):
        path = download_image(bd["file_path"], f"backdrop_{i}.jpg")
        if path:
            backdrop_paths.append(path)
            
    print(f"      {len(backdrop_paths)} backdrop(s) downloaded.")

    # --- Cast & Director ---
    cast       = details.get("credits", {}).get("cast", [])[:5]
    cast_names = [c["name"] for c in cast]
    crew       = details.get("credits", {}).get("crew", [])
    directors = [c["name"] for c in crew if c["job"] == "Director"]

    return {
        "title":          details["title"],
        "year":           details.get("release_date", "")[:4],
        "overview":       details.get("overview", ""),
        "rating":         round(details.get("vote_average", 0), 1),
        "vote_count":     details.get("vote_count", 0),
        "genres":         [g["name"] for g in details.get("genres", [])],
        "runtime":        details.get("runtime", 120),
        "director":       directors[0] if directors else "Unknown",
        "cast":           cast_names,
        "tagline":        details.get("tagline", ""),
        "poster_path":    poster_path,
        "backdrop_paths": backdrop_paths,
    }