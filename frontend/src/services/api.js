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

export const getAiRecommendations = async (movie_id) => {
  const response = await fetch(`http://127.0.0.1:8000/api/ai/recommend/${movie_id}`);
  return await response.json()
}

export const generateSummary = async (movie_id, onChunk) => {
  const response = await fetch(`http://127.0.0.1:8000/api/ai/summary/${movie_id}`);


  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });

    for (const char of chunk) {
      onChunk(char)
      await sleep(DELAY)
    }
    
    

  }
 
}

const DELAY = 30; 

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));