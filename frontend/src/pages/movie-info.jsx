
import { useEffect, useState } from "react";
import { searchMovies, getPopularMovies, getRecommendations, searchMovieById } from "../services/api"
import MovieCard from "../components/Moviecard";
import "../css/movie-info.css";
import { useParams } from "react-router-dom";

function Navbar() {
  return (
    <nav className='nav1'>
      <a href="#home">home</a>
      <img src="https://cdn-icons-png.flaticon.com/128/8213/8213522.png" alt="" />
      <a href="#movie">movie</a>
      <img src="https://cdn-icons-png.flaticon.com/128/8213/8213522.png" alt="" />
      <a href="#interseller">interseller</a>
    </nav>
  )
}

function Main({ movieId }) {
  const [movie, setMovie] = useState(null);
  console.log(movie);
  useEffect(() => {
    if (!movieId) return;

    const loadMovie = async () => {
      try {
        const data = await searchMovieById(movieId);
        setMovie(data);
      } catch (error) {
        console.error("Failed to fetch movie:", error);
      }
    };

    loadMovie();
  }, [movieId]);



  if (!movie) {
    return <p>Loading movie...</p>;
  }

  return (
    <section className="main">

      <div className="left">
        <img src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} alt={movie.title} />
      </div>


      <div className="right">

        <div className="detail">
          <li>{movie.title}</li>
          <ol>
            <li>{movie.release_date?.split("-")[0] || "N/A"}</li>
            {movie.genres.map((genre, index) => <li key={index}>{genre.name}</li>)}
          </ol>

        {/* </ol> */}

        <div>⭐ {Math.round(movie.vote_average)}/10</div>

        <div className="buttons">
          <button>▶ Watch Trailer</button>
          <button>+ Add to Watchlist</button>
        </div>

        <div className='information'>{movie.overview}</div>
        <div className="card">
          <div className='sidebyside'>
            <img src="https://cdn-icons-png.flaticon.com/128/2965/2965335.png" alt="" />
            <h2>AI Summary</h2>
          </div>
          <li>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Explicabo reiciendis est dolorum amet perspiciatis beatae consequuntur quisquam quidem et error? Corrupti ad praesentium necessitatibus voluptas dolore? Aperiam, ipsum?</li>
        </div>

      </div>

      <div className="cast">
        <h2>Cast</h2>

        <div className='card1'>
          <div className="imgcast"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEmSOQIobgum-NlWvYCVn-4JUARQWSJi1wQdvQzCaSbA&s=10" alt="" /></div>
          <div className="castname">
            <h3>Mattew McConaughey</h3>
            <li>Cooper</li>
          </div>
        </div>
        <div className='card1'>
          <div className="imgcast"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEmSOQIobgum-NlWvYCVn-4JUARQWSJi1wQdvQzCaSbA&s=10" alt="" /></div>
          <div className="castname">
            <h3>Anne Hathaway</h3>
            <li>Brand</li>
          </div>
        </div>
        <div className='card1'>
          <div className="imgcast"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEmSOQIobgum-NlWvYCVn-4JUARQWSJi1wQdvQzCaSbA&s=10" alt="" /></div>
          <div className="castname">
            <h3>Jessica Chastain</h3>
            <li>Murph</li>
          </div>
        </div>

      </div>

    </div>




    </section >

  )
}

function Movie() {

  const { movieId } = useParams()
  const [RecommendedMovies, setRecommendations] = useState([]);

  useEffect(() => {
    const loadMovies = async () => {
      const movie_ids_array = await getRecommendations(movieId);

      const movies = await Promise.all(
        movie_ids_array.map(id => searchMovieById(id))
      );

      setRecommendations(movies)

    };

    loadMovies();
  }, [movieId]);

  // useEffect(() => {
  //   setRecommendations([])
  //   const loadMovies = async () => {
  //     const movie_ids_array = await getRecommendations(movieId);

  //     for (const id of movie_ids_array) {
  //       const movie = await searchMovieById(id);

  //       setRecommendations(prev => [...prev, movie]);
  //     }
  //   };

  //   loadMovies();
  // }, [movieId]);

  // console.log(movies)


  return (
    <>
      {/* <Navbar /> */}
      <Main movieId={movieId} />

      <div className="similar">
        <img src="https://cdn-icons-png.flaticon.com/128/13963/13963168.png" width="30px" height="30px" alt="" />
        <h2>similar movies</h2>
        <li>( AI Recommended )</li>
      </div>

      <div className="movies-grid">

        {RecommendedMovies.map(movie => (
          <MovieCard movie={movie} key={movie.id} />
        ))}
      </div>
    </>
  );
}
export default Movie