
import { useEffect, useState } from "react";
import { searchMovies, getPopularMovies, getRecommendations, searchMovieById, generateSummary, getAiRecommendations } from "../services/api"
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
  const [aiSummary, setAiSummary] = useState("");

  useEffect(() => {
    let current = true;

    setMovie(null);
    setAiSummary("");

    if (!movieId) return;

    const loadMovie = async () => {
      try {
        const data = await searchMovieById(movieId);

        if (current) {
          setMovie(data);
        }
      } catch (error) {
        if (current) {
          console.error("Failed to fetch movie:", error);
        }
      }
    };

    const loadAiSummary = async () => {
      try {
        await generateSummary(movieId, (chunk) => {
          if (!current) return;
          setAiSummary((prev) => prev + chunk);
        });
      } catch (error) {
        if (current) {
          console.error("Failed to generate AI summary:", error);
        }
      }
    };

    loadMovie();
    // loadAiSummary();

    return () => {
      current = false;
    };
  }, [movieId]);
  // console.log(aiSummary)

  if (!movie) {
    return <p>Loading movie...</p>;
  }

  const year = movie.release_date?.slice(0, 4) || "N/A";
  const genres = movie.genres.map((genre, index) => <li key={index}>{genre.name}</li>);
  const rating = movie.vote_average ? movie.vote_average.toFixed(1) : "N/A";
  const trailerUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(
    `${movie.title} ${year} official trailer`
  )}`;

  return (
    <section className="main">

      <div className="left">
        <img src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`} alt={movie.title} />
      </div>


      <div className="right">

        <div className="detail">
          <li>{movie.title}</li>
          <ol>
            <li>{year}</li>
            {genres}
          </ol>

          {/* </ol> */}

          <div>⭐ {rating}/10</div>

          <div className="buttons">
            <button onClick={() => window.location.href=trailerUrl}>▶ Watch Trailer</button>
            <button>+ Add to Watchlist</button>
          </div>

          <div className='information'>{movie.overview}</div>
          <div className="card">
            <div className='sidebyside'>
              <img src="https://cdn-icons-png.flaticon.com/128/2965/2965335.png" alt="" />
              <h2>AI Summary</h2>
            </div>
            <li><p>{aiSummary}</p></li>
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
  const [AiRecommendedMovies, setAiRecommendations] = useState([]);

  // Render all at once
  // useEffect(() => {
  //   const loadMovies = async () => {
  //     const movie_ids_array = await getRecommendations(movieId);

  //     const movies = await Promise.all(
  //       movie_ids_array.map(id => searchMovieById(id))
  //     );

  //     setRecommendations(movies)

  //   };

  //   loadMovies();
  // }, [movieId]);


  // Render one by one 
  useEffect(() => {
    let isCurrent = true
    setRecommendations([])

    const loadMovies = async () => {
      const movie_ids_array = await getRecommendations(movieId);

      for (const id of movie_ids_array) {

        if (!isCurrent) break;
        const movie = await searchMovieById(id);

        if (isCurrent) {
          setRecommendations(prev => [...prev, movie]);
        } else {
          break;
        }
      }
    };

    const loadAiMovies = async () => {
      const ai_recoms = await getAiRecommendations(movieId)
      const movie_array = ai_recoms.ranked_candidates.ranked_candidates

      setAiRecommendations(movie_array)


    }


    loadMovies();
    loadAiMovies();

    return () => {
      isCurrent = false;
    };
  }, [movieId]);




  // const aiMovieIds = new Set(AiRecommendedMovies.map(aiMovie => aiMovie.tmdb_id));
  // const ai_movies = RecommendedMovies.filter(movie => aiMovieIds.has(movie.id));

  const movieLookup = new Map(
    RecommendedMovies.map(movie => [movie.id, movie])
  );

  const nnn = AiRecommendedMovies
    .map(aiMovie => {
      const fullMovie = movieLookup.get(aiMovie.tmdb_id);

      return fullMovie
        ? {
          ...fullMovie,
          rank: aiMovie.rank,
          reason: aiMovie.reason,
        }
        : null;
    })
    .filter(Boolean);
  console.log(nnn)

  return (
    <>
      {/* <Navbar /> */}
      <Main movieId={movieId} />
      <div className="similar">
        <img src="https://cdn-icons-png.flaticon.com/128/13963/13963168.png" width="30px" height="30px" alt="" />
        <h2>AI Recommended</h2>
      </div>

      <div className="movies-grid">

        {nnn.map(movie => (
          <MovieCard movie={movie} key={movie.id} />
        ))}
      </div>

      <div className="similar">
        <img src="https://cdn-icons-png.flaticon.com/128/13963/13963168.png" width="30px" height="30px" alt="" />
        <h2>similar movies</h2>
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