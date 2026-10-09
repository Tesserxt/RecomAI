import asyncio
from typing import Any

import httpx
from httpx._models import Response

API_KEY = "e62093398aef57e164bffbc5cc87ce6f"
BASE_URL = "https://api.themoviedb.org/3"

client = httpx.AsyncClient(timeout=10.0)


async def get_popular_movies():
    url: str = f"{BASE_URL}/movie/popular?api_key={API_KEY}"

    response: Response = await client.get(url)

    return response.status_code, response.json()


async def search_movie_by_name(movie_name: str) -> Any:
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": movie_name}

    response: Response = await client.get(url, params=params)

    return response.status_code, response.json()


import time


semaphore = asyncio.Semaphore(3)


async def search_movie_by_id(id: int) -> Any:
    url = f"{BASE_URL}/movie/{id}"
    params = {"api_key": API_KEY}

    # start = time.perf_counter()

    # print(f"[{id}] waiting for semaphore")

    async with semaphore:
        #  print(f"[{id}] acquired semaphore")
        #  start = time.perf_counter()

        try:
            response = await client.get(url, params=params)

            # elapsed = time.perf_counter() - start
            # print(f"[{id}] TMDB request finished in {elapsed:.2f}s")

            return response.status_code, response.json()

        except httpx.TimeoutException:
            # elapsed = time.perf_counter() - start
            #  print(f"[{id}] TIMEOUT after {elapsed:.2f}s")

            return 504, {"detail": "TMDB request timed out"}

        except httpx.HTTPError as e:
            # elapsed = time.perf_counter() - start
            # print(f"[{id}] ERROR after {elapsed:.2f}s: {e}")

            return 502, {"detail": str(e)}
