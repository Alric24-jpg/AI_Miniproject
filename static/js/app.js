async function searchMovies() {

    const query =
        document.getElementById("movieSearch").value.trim();

    if (!query) {
        return;
    }

    const container =
        document.getElementById("searchResults");

    container.innerHTML =
        `<p>Searching...</p>`;

    try {

        const response = await fetch(
            `/api/search?q=${encodeURIComponent(query)}`
        );

        const data = await response.json();

        if (data.error) {
            container.innerHTML =
                `<p>${data.error}</p>`;
            return;
        }

        displayMovies(
            data.results,
            "searchResults"
        );

    } catch (error) {

        container.innerHTML =
            `<p>Something went wrong.</p>`;
    }
}


async function discoverMovies() {

    const params = new URLSearchParams();


    const genre =
        document.getElementById("genre").value;

    const language =
        document.getElementById("language").value;

    const rating =
        document.getElementById("rating").value;

    const yearFrom =
        document.getElementById("yearFrom").value;

    const yearTo =
        document.getElementById("yearTo").value;

    const runtimeMin =
        document.getElementById("runtimeMin").value;

    const runtimeMax =
        document.getElementById("runtimeMax").value;

    const sort =
        document.getElementById("sort").value;


    if (genre)
        params.append("genre", genre);

    if (language)
        params.append("language", language);

    if (rating)
        params.append("min_rating", rating);

    if (yearFrom)
        params.append("year_from", yearFrom);

    if (yearTo)
        params.append("year_to", yearTo);

    if (runtimeMin)
        params.append("runtime_min", runtimeMin);

    if (runtimeMax)
        params.append("runtime_max", runtimeMax);

    if (sort)
        params.append("sort", sort);


    const container =
        document.getElementById("discoverResults");

    container.innerHTML =
        `<p>Finding movies...</p>`;


    try {

        const response = await fetch(
            `/api/discover?${params.toString()}`
        );

        const data = await response.json();

        if (data.error) {
            container.innerHTML =
                `<p>${data.error}</p>`;
            return;
        }

        displayMovies(
            data.movies,
            "discoverResults"
        );

    } catch (error) {

        container.innerHTML =
            `<p>Something went wrong.</p>`;
    }
}


function displayMovies(movies, containerId) {

    const container =
        document.getElementById(containerId);

    container.innerHTML = "";


    if (!movies.length) {

        container.innerHTML =
            `<p>No movies found.</p>`;

        return;
    }


    movies.forEach(movie => {

        const poster =
            movie.poster ||
            "https://via.placeholder.com/500x750?text=No+Poster";


        const rating =
            movie.rating
                ? movie.rating.toFixed(1)
                : "N/A";


        const card = document.createElement("div");

        card.className =
            "col-6 col-md-4 col-lg-3";


        card.innerHTML = `

            <div class="movie-card">

                <img
                    src="${poster}"
                    class="movie-poster"
                    alt="${movie.title}"
                >

                <div class="movie-info">

                    <div class="movie-title">
                        ${movie.title}
                    </div>

                    <div class="rating">
                        ★ ${rating}
                    </div>

                    <small class="text-muted">
                        ${movie.release_date || "Unknown"}
                    </small>

                    <button
                        class="btn btn-outline-light btn-sm mt-3 w-100"
                        onclick="showMovie(${movie.id})"
                    >
                        Details
                    </button>

                </div>

            </div>
        `;


        container.appendChild(card);

    });
}


async function showMovie(movieId) {

    try {

        const response =
            await fetch(`/api/movie/${movieId}`);

        const movie =
            await response.json();


        const cast =
            movie.cast
                .slice(0, 5)
                .map(person => person.name)
                .join(", ");


        const genres =
            movie.genres.join(", ");


        document.getElementById(
            "movieDetails"
        ).innerHTML = `

            <div class="row g-4">

                <div class="col-md-4">

                    <img
                        src="${movie.poster}"
                        class="img-fluid modal-poster rounded"
                    >

                </div>


                <div class="col-md-8">

                    <h2>
                        ${movie.title}
                    </h2>

                    <p class="rating">
                        ★ ${movie.rating?.toFixed(1) || "N/A"}
                    </p>

                    <p>
                        ${movie.overview || "No description available."}
                    </p>

                    <p>
                        <strong>Genres:</strong>
                        ${genres || "N/A"}
                    </p>

                    <p>
                        <strong>Director:</strong>
                        ${movie.directors.join(", ") || "N/A"}
                    </p>

                    <p>
                        <strong>Cast:</strong>
                        ${cast || "N/A"}
                    </p>

                    <p>
                        <strong>Runtime:</strong>
                        ${movie.runtime || "N/A"} minutes
                    </p>


                    <button
                        class="btn btn-primary"
                        onclick="getRecommendations(${movie.id})"
                    >
                        🤖 Get AI Recommendations
                    </button>

                </div>

            </div>
        `;


        const modal =
            new bootstrap.Modal(
                document.getElementById("movieModal")
            );

        modal.show();

    } catch (error) {

        console.error(error);

    }
}


async function getRecommendations(movieId) {

    try {

        const response =
            await fetch(
                `/api/recommend/${movieId}`
            );

        const data =
            await response.json();


        if (data.error) {

            alert(data.error);

            return;
        }


        const modalBody =
            document.getElementById(
                "movieDetails"
            );


        let html = `

            <h3>
                Because you liked
                ${data.movie.title}
            </h3>

            <hr>

            <div class="row g-4">
        `;


        data.recommendations.forEach(movie => {

            html += `

                <div class="col-6 col-md-4">

                    <div class="movie-card">

                        <img
                            src="${movie.poster}"
                            class="movie-poster"
                        >

                        <div class="movie-info">

                            <div class="movie-title">
                                ${movie.title}
                            </div>

                            <div class="rating">
                                Similarity:
                                ${movie.similarity}
                            </div>

                        </div>

                    </div>

                </div>
            `;

        });


        html += `
            </div>
        `;


        modalBody.innerHTML = html;


    } catch (error) {

        console.error(error);

    }
}


/* Load genres when page opens */

async function loadGenres() {

    try {

        const response =
            await fetch("/api/genres");

        const data =
            await response.json();


        const select =
            document.getElementById("genre");


        data.genres.forEach(genre => {

            const option =
                document.createElement("option");

            option.value = genre.id;

            option.textContent = genre.name;

            select.appendChild(option);

        });

    } catch (error) {

        console.error(error);

    }
}


document.addEventListener(
    "DOMContentLoaded",
    loadGenres
);