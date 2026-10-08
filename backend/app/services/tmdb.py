from typing import Any

import httpx
from httpx._models import Response

API_KEY = "e62093398aef57e164bffbc5cc87ce6f"
BASE_URL = "https://api.themoviedb.org/3"


async def get_popular_movies():
    url: str = f"{BASE_URL}/movie/popular?api_key={API_KEY}"

    async with httpx.AsyncClient() as client:
        response: Response = await client.get(url)

    return response.status_code, response.json()


async def search_movie_by_name(movie_name: str) -> Any:
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": movie_name}

    async with httpx.AsyncClient() as client:
        response: Response = await client.get(url, params=params)

    return response.status_code, response.json()


async def search_movie_by_id(id: int) -> Any:
    print(type(id))
    url = f"{BASE_URL}/movie/{id}"
    print(url)
    params = {"api_key": API_KEY}

    async with httpx.AsyncClient() as client:
        response: Response = await client.get(url, params=params)

    return response.status_code, response.json()
