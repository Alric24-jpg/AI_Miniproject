from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def create_movie_profile(movie):

    genres = " ".join(movie.get("genres", []))

    cast = " ".join(
        person["name"]
        for person in movie.get("cast", [])
    )

    directors = " ".join(
        movie.get("directors", [])
    )

    overview = movie.get("overview", "")

    return " ".join([
        genres,
        cast,
        directors,
        overview
    ])


def calculate_similarity(target_movie, movies):

    if not movies:
        return []

    target_profile = create_movie_profile(target_movie)

    profiles = [
        create_movie_profile(movie)
        for movie in movies
    ]

    all_profiles = [target_profile] + profiles

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        all_profiles
    )

    similarities = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    recommendations = []

    for movie, score in zip(movies, similarities):

        movie_copy = movie.copy()

        movie_copy["similarity"] = round(
            float(score),
            3
        )

        recommendations.append(movie_copy)

    recommendations.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return recommendations