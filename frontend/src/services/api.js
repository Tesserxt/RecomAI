const API_BASE_URL = import.meta.env.VITE_API_URL ?? "";

const request = async (path) => {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request to ${path} failed with status ${response.status}`);
  }
  return response.json();
};

export const getPopularMovies = () => request("/api/movies/popular");

export const searchMovies = (query) =>
  request(`/api/movies/search?movie_name=${encodeURIComponent(query)}`);
