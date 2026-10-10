from typing import Any

from fastapi import APIRouter, HTTPException

from app.services.tmdb import getCast

from ..services.tmdb import get_popular_movies, search_movie_by_id, search_movie_by_name

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
    status_code, data = await get_popular_movies()

    if status_code != 200:
        raise HTTPException(status_code=502, detail=data)
    return data["results"]


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

    if movie_id is not None:
        status_code, data = await search_movie_by_id(movie_id)

        if status_code != 200:
            raise HTTPException(status_code=status_code, detail=data)
        return data

    if movie_name is not None:
        status_code, data = await search_movie_by_name(movie_name)

        if status_code != 200:
            raise HTTPException(status_code=status_code, detail=data)
        return data["results"]

    raise HTTPException(
        status_code=400,
        detail="Provide movie_id or movie_name",
    )


@router.get("/{movie_id}/cast")
async def get_movie_cast(movie_id: int):
    cast = await getCast(movie_id)
    return cast
