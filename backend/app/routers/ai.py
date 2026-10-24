from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..services.ai import generate_summary

router = APIRouter(
    prefix="/api/ai",
    tags=["AI"],
    responses={404: {"description": "Not found"}},
)


@router.get("/summary/{movie_id}", description="AI generated Summary via movie_id.")
async def get_summary(movie_id: int) -> str:
    return StreamingResponse(generate_summary(movie_id), media_type="text/plain")
