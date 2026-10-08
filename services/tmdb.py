import requests

from config import (
    TMDB_API_KEY,
    TMDB_BASE_URL,
    POSTER_BASE_URL,
    BACKDROP_BASE_URL
)


def make_request(endpoint, params=None):

    if params is None:
        params = {}

    params["api_key"] = TMDB_API_KEY

    response = requests.get(
        f"{TMDB_BASE_URL}{endpoint}",
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def search_movies(query, page=1):

    data = make_request(
        "/search/movie",
        {
            "query": query,
            "page": page,
            "include_adult": False
        }
    )

    return format_movies(data.get("results", []))


def get_movie(movie_id):

    movie = make_request(
        f"/movie/{movie_id}",
        {
            "append_to_response": "credits,videos"
        }
    )

    return format_movie(movie)


def discover_movies(filters):

    data = make_request(
        "/discover/movie",
        filters
    )

    return {
        "page": data.get("page"),
        "total_pages": data.get("total_pages"),
        "total_results": data.get("total_results"),
        "movies": format_movies(data.get("results", []))
    }


def get_genres():

    data = make_request("/genre/movie/list")

    return data.get("genres", [])


def format_movies(movies):

    formatted = []

    for movie in movies:

        formatted.append({
            "id": movie.get("id"),
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
            "rating": movie.get("vote_average"),
            "vote_count": movie.get("vote_count"),
            "popularity": movie.get("popularity"),
            "poster": (
                f"{POSTER_BASE_URL}{movie['poster_path']}"
                if movie.get("poster_path")
                else None
            ),
            "backdrop": (
                f"{BACKDROP_BASE_URL}{movie['backdrop_path']}"
                if movie.get("backdrop_path")
                else None
            ),
            "genre_ids": movie.get("genre_ids", [])
        })

    return formatted


def format_movie(movie):

    credits = movie.get("credits", {})

    cast = [
        {
            "id": person.get("id"),
            "name": person.get("name"),
            "character": person.get("character")
        }
        for person in credits.get("cast", [])[:10]
    ]

    directors = [
        person.get("name")
        for person in credits.get("crew", [])
        if person.get("job") == "Director"
    ]

    return {
        "id": movie.get("id"),
        "title": movie.get("title"),
        "original_title": movie.get("original_title"),
        "overview": movie.get("overview"),
        "release_date": movie.get("release_date"),
        "runtime": movie.get("runtime"),
        "rating": movie.get("vote_average"),
        "vote_count": movie.get("vote_count"),
        "popularity": movie.get("popularity"),

        "genres": [
            genre.get("name")
            for genre in movie.get("genres", [])
        ],

        "poster": (
            f"{POSTER_BASE_URL}{movie['poster_path']}"
            if movie.get("poster_path")
            else None
        ),

        "backdrop": (
            f"{BACKDROP_BASE_URL}{movie['backdrop_path']}"
            if movie.get("backdrop_path")
            else None
        ),

        "cast": cast,
        "directors": directors
    }