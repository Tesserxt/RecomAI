import { Route, Routes } from "react-router-dom";
import "./css/App.css";
import "./css/movie-info.css"
import MovieCard from './components/Moviecard'
import Home from "./pages/Home";
import Favorites from "./pages/Favorites";
import MovieInfo from "./pages/movie-info"
import NavBar from "./components/NavBar";
import { MovieProvider } from "./context/MovieContext";


function App() {

  return (

    <MovieProvider>
      <NavBar />

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/favorites" element={<Favorites />} />
          <Route path="/movie-info/:movieId" element={<MovieInfo />} />
        </Routes>
      </main>
    </MovieProvider>

  );
}

export default App;
