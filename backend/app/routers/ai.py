from fastapi import APIRouter, HTTPException

from ..services.ai import generate_summary

router = APIRouter(
    prefix="/api/ai",
    tags=["AI"],
    responses={404: {"description": "Not found"}},
)


@router.get("/summary/{movie_id}", description="AI generated Summary via movie_id.")
def get_summary(movie_id: int) -> str:
    summary = generate_summary(movie_id)

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Movie summary could not be generated.",
        )

    return summary
