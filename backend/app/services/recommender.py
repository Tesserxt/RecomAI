from pathlib import Path

import numpy as np
from numpy import ndarray
from scipy.sparse import csr_matrix, load_npz

BASE_DIR = Path(__file__).resolve().parents[3]
X_PATH = BASE_DIR / "artifacts" / "tfidf_X.npz"

X: csr_matrix = load_npz(X_PATH)


def recommend_movies(movie_id: int, k: int) -> list[int]:
    query: csr_matrix = X[movie_id]

    scores: csr_matrix = X @ query.T
    scores: ndarray = scores.toarray().ravel()

    scores[movie_id] = -1  # excluding the queried movie itself

    idx = scores.argpartition(-k)[-k:]
    sorted_idx = idx[np.argsort(scores[idx])[::-1]]
    return sorted_idx
