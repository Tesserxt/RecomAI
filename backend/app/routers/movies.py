from typing import Any

from fastapi import APIRouter

from ..services.tmdb import get_popular_movies, search_movie

from app.services.tmdb import getCast

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
    # if movie_id is not None:
    #     return await get_movie_by_id(movie_id)

    if movie_name is not None:
        return await search_movie(movie_name)

    return {"error": "Provide movie_id or movie_name"}

@router.get("/{movie_id}/cast")
async def get_movie_cast(movie_id:int):
    cast = await getCast(movie_id)
    return cast