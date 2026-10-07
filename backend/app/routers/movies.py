from typing import Any

from fastapi import APIRouter, HTTPException

from ..services.tmdb import get_popular_movies, search_movie

router = APIRouter(
    prefix="/api/movies",
    tags=["movies"], 
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/popular",
    summary="Get popular movies",
    description="Retrieve a list of currently popular movies from TMDB.",
)
async def get_popular_movies_endpoint() -> list[dict[str, Any]]:
    movies = await get_popular_movies()
    return movies


@router.get("/search")
async def get_movie(
    movie_id: int | None = None,
    movie_name: str | None = None,
):
    if movie_id is not None and movie_name is not None:
        raise HTTPException(
            status_code=400,
            detail="Provide either movie_id or movie_name, not both",
        )

    # if movie_id is not None:
    #     return await get_movie_by_id(movie_id)

    if movie_name is not None:
        return await search_movie(movie_name)

    raise HTTPException(
        status_code=400,
        detail="Provide movie_id or movie_name",
    )
