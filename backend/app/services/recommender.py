from pathlib import Path

import numpy as np
from numpy import ndarray
from scipy.sparse import csr_matrix, load_npz

BASE_DIR = Path(__file__).resolve().parents[3]
X_PATH = BASE_DIR / "artifacts" / "tfidf_X.npz"
TMDB_IDS_PATH = BASE_DIR / "artifacts" / "tmdb_ids.npy"


X: csr_matrix = load_npz(X_PATH)
TMDB_IDS = np.load(TMDB_IDS_PATH)

tmdb_to_index = {tmdb_id: index for index, tmdb_id in enumerate(TMDB_IDS)}


def recommend_movies(movie_id: int, k: int) -> list[int]:

    movie_idx = tmdb_to_index[movie_id]
    query: csr_matrix = X[movie_idx]

    scores: csr_matrix = X @ query.T
    scores: ndarray = scores.toarray().ravel()

    scores[movie_idx] = -1  # excluding the queried movie itself

    idx = scores.argpartition(-k)[-k:]
    sorted_idx = idx[np.argsort(scores[idx])[::-1]]

    return TMDB_IDS[sorted_idx]
