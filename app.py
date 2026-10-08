from flask import Flask, render_template, request, jsonify

from services.tmdb import (
    search_movies,
    get_movie,
    discover_movies,
    get_genres
)

from services.recommender import calculate_similarity


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/api/search")
def search():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "error": "Search query is required"
        }), 400

    try:

        results = search_movies(query)

        return jsonify({
            "results": results
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


@app.route("/api/movie/<int:movie_id>")
def movie_details(movie_id):

    try:

        movie = get_movie(movie_id)

        return jsonify(movie)

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


@app.route("/api/genres")
def genres():

    try:

        return jsonify({
            "genres": get_genres()
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


@app.route("/api/discover")
def discover():

    filters = {}

    genre = request.args.get("genre")

    if genre:
        filters["with_genres"] = genre

    language = request.args.get("language")

    if language:
        filters["with_original_language"] = language

    minimum_rating = request.args.get("min_rating")

    if minimum_rating:
        filters["vote_average.gte"] = minimum_rating

    minimum_votes = request.args.get("min_votes")

    if minimum_votes:
        filters["vote_count.gte"] = minimum_votes

    year_from = request.args.get("year_from")

    if year_from:
        filters["primary_release_date.gte"] = f"{year_from}-01-01"

    year_to = request.args.get("year_to")

    if year_to:
        filters["primary_release_date.lte"] = f"{year_to}-12-31"

    runtime_min = request.args.get("runtime_min")

    if runtime_min:
        filters["with_runtime.gte"] = runtime_min

    runtime_max = request.args.get("runtime_max")

    if runtime_max:
        filters["with_runtime.lte"] = runtime_max

    sort_by = request.args.get(
        "sort",
        "popularity.desc"
    )

    filters["sort_by"] = sort_by

    page = request.args.get("page", 1)

    filters["page"] = page

    try:

        results = discover_movies(filters)

        return jsonify(results)

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


@app.route("/api/recommend/<int:movie_id>")
def recommend(movie_id):

    try:

        target_movie = get_movie(movie_id)

        # Get candidate movies from TMDB.
        candidates = discover_movies({
            "sort_by": "popularity.desc",
            "vote_count.gte": 100
        })

        recommendations = calculate_similarity(
            target_movie,
            candidates["movies"]
        )

        return jsonify({
            "movie": target_movie,
            "recommendations": recommendations[:10]
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )