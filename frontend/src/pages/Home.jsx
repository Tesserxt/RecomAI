import { useEffect, useState } from "react";
import { searchMovies, getPopularMovies } from "../services/api";
import MovieCard from "../components/Moviecard";
import "../css/Home.css";

function Home() {
    const [searchQuery, setSearchQuery] = useState('');
    const [homeMovies, setHomeMovies] = useState([]);
    const [searchedMovies, setSearchedMovies] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadPopularMovies = async () => {
            try {
                setLoading(true);
                const popularMovies = await getPopularMovies();
                setHomeMovies(popularMovies);
                
                await new Promise((resolve) => setTimeout(resolve, 3000));
            } catch (err) {
                setError("Failed to Load movies...");
                console.log(err);
            } finally {
                setLoading(false);
            }
        };

        loadPopularMovies();
    }, []);

    const handleSearch = async (e) => {
        e.preventDefault();

        if (!searchQuery.trim()) return;
        if (loading) return;
       
        try { 
            setLoading(true);
            const searchResults = await searchMovies(searchQuery);
            setSearchedMovies(searchResults);
            setError(null);
            
            await new Promise((resolve) => setTimeout(resolve, 3000));
        } catch(err) {
            console.log(err);
            setError("Failed to search movies...");
        } finally {
            setLoading(false);
        }
    };

   
    // If there is text in the search box and we have searched results, show them. Otherwise, show home movies.
    const moviesToDisplay = searchQuery.trim() && searchedMovies.length > 0 
        ? searchedMovies 
        : homeMovies;

    return (
        <div className="home">
            <form onSubmit={handleSearch} className="search-form">
                <input
                    value={searchQuery}
                    // If the user backspaces and clears out the input box, 
                    // we immediately wipe out old search results to show home movies again
                    onChange={(e) => {
                        setSearchQuery(e.target.value);
                        if (!e.target.value.trim()) {
                            setSearchedMovies([]);
                        }
                    }}
                    type='text'
                    placeholder="Search for movies..."
                    className="search-input"
                />
                <button type="submit" className="search-button">Search</button>
            </form>

            {error && <div className="error-message">{error}</div>}

            {loading ? (
                <div className="loading"></div>
            ) : (
                <div className="movies-grid">
                    {/* FIX 3: Map over your dynamic array variable instead of the non-existent 'movies' */}
                    {moviesToDisplay.map(movie => (
                        <MovieCard movie={movie} key={movie.id} />
                    ))}
                </div>
            )}
        </div>
    );
}

export default Home;
