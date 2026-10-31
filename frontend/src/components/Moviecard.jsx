import "../css/MovieCard.css"
import { Link } from "react-router-dom";
import { useMovieContext } from "../context/MovieContext";
function MovieCard({ movie }) {
    const { isFavorite, addToFavorites, removeFromFavorites } = useMovieContext()

    const favorite = isFavorite(movie.id)

    function onFavoriteClick(e) {
        e.preventDefault()
        if (favorite) removeFromFavorites(movie.id)
        else addToFavorites(movie)
    }

    return (
        <Link to={`/movie-info/${movie.id}`}>
            <div className="movie-card" >
                <div className="movie-poster">
                    <img src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} alt={movie.title} />
                    <div className="movie-overlay">
                        <button className={`favorite-btn ${favorite ? "active" : ""}`} onClick={onFavoriteClick}>
                            ♥
                        </button>
                    </div>
                    <p>why u may like it</p>
                </div>

                <div className="movie-info">
                    <h3>{movie.title}</h3>
                    <p>{movie.release_date?.split("-")[0] || "N/A"}</p>
                </div>

                {movie.reason !== undefined ? (
                    <div className="card">
                        <div className="sidebyside">
                            <img src="https://cdn-icons-png.flaticon.com/128/2965/2965335.png" alt="AI Icon" />
                            <h3>Why its Relevant?</h3>
                        </div>
                        <li><p>{movie.reason}</p></li>
                    </div>
                ) : (
                    <p></p>
                )}


            </div>
        </Link>

    );
}

export default MovieCard;