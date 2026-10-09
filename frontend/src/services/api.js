const API_KEY = "e62093398aef57e164bffbc5cc87ce6f";
const BASE_URL = "https://api.themoviedb.org/3";



export const getPopularMovies = async () => {
    const response = await fetch("http://127.0.0.1:8000/api/movies/popular");
    return await response.json()
}

export const searchMovies = async (query) => {
  const response = await fetch(`http://127.0.0.1:8000/api/movies/search?movie_name=${query}`
  );
  return await response.json();
};

export const getRecommendations = async (movie_id) => {
    const response = await fetch(`http://127.0.0.1:8000/api/recommendations/${movie_id}`);
    return await response.json()
}

export const searchMovieById = async (movie_id) => {
  const response = await fetch(`http://127.0.0.1:8000/api/movies/search?movie_id=${movie_id}`);
  return await response.json();
};