
import { useEffect, useState } from "react";
import { searchMovies, getPopularMovies } from "../services/api"
import MovieCard from "../components/Moviecard";
import "../css/movie-info.css";

function Navbar() {
  return (
    <nav className='nav1'>
      <a href="/">home</a>
      <img src="https://cdn-icons-png.flaticon.com/128/8213/8213522.png" alt="" />
      <a href="#movie">movie</a>
      <img src="https://cdn-icons-png.flaticon.com/128/8213/8213522.png" alt="" />
      <a href="#interseller">interseller</a>
    </nav>
  )
}

function Main() {
  return (
    <section className="main">

      <div className="left">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEmSOQIobgum-NlWvYCVn-4JUARQWSJi1wQdvQzCaSbA&s=10" alt="" />
      </div>


      <div className="right">

        <div className="detail">
          <li>Interseller</li>
          <ol>
            <li>2014</li>
            <li>scifi</li>
            <li>Drama</li>
            <li>Adventure</li>
          </ol>

          <div>⭐ 8.8/10</div>

          <div className="buttons">
            <button>▶ Watch Trailer</button>
            <button>+ Add to Watchlist</button>
          </div>

          <div className='information'>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Qui unde a asperiores ea maiores optio quidem illo nihil tenetur consequatur aut et ratione ut distinctio laboriosam voluptatem, tempora minima similique.</div>

          <div className="card">
            <div className='sidebyside'>
              <img src="https://cdn-icons-png.flaticon.com/128/2965/2965335.png" alt="" />
              <h2>Summary</h2>
            </div>
            <li> Lorem, ipsum dolor sit amet consectetur adipisicing elit. Explicabo reiciendis est dolorum amet perspiciatis beatae consequuntur quisquam quidem et error? Corrupti ad praesentium necessitatibus voluptas dolore? Aperiam, ipsum?</li>
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




    </section>

  )
}

function Movie() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    const loadMovies = async () => {
      const popularMovies = await getPopularMovies(); setMovies(popularMovies);
      // console.log(popularMovies);
    };
    loadMovies();
  }, []);

  // console.log(movies)


  return (
    <>
      <Navbar />
      <Main />

      <div className="similar">
        <img src="https://cdn-icons-png.flaticon.com/128/13963/13963168.png" width= "30px" height="30px" alt="" />
        <h2>similar movies</h2>
        <li>( AI Recommendent )</li>
      </div>

      <div className="movies-grid">
        {/* FIX 3: Map over your dynamic array variable instead of the non-existent 'movies' */}
        {movies.map(movie => (
          <MovieCard movie={movie} key={movie.id} />
        ))}
      </div>
    </>
  );
}
export default Movie