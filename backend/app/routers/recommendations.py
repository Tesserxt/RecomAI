from typing import Annotated

from fastapi import APIRouter, Query

from ..services.recommender import recommend_movies

router = APIRouter(
    prefix="/api/recommendations",
    tags=["recommend"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{movie_id}", description="Recommend list of related movies.")
def get_recommendations(
    movie_id: int,
    k: Annotated[int, Query(gt=0, lt=50, description="k movies to recommend")] = 20,
) -> list[int]:
    movies_tmdb_idx: list[int] = recommend_movies(movie_id, k)
    return movies_tmdb_idx
