# import asyncio
# import httpx
# import time

# API_KEY = "e62093398aef57e164bffbc5cc87ce6f"
# BASE_URL = "https://api.themoviedb.org/3"


# async def test(id, client):
#     start = time.perf_counter()
#     print(f"[{id}] start")

#     response = await client.get(f"{BASE_URL}/movie/{id}", params={"api_key": API_KEY})

#     print(f"[{id}] {response.status_code} {time.perf_counter() - start:.2f}s")


# async def main():
#     ids = [272, 3, 122, 1223, 12, 8954]

#     async with httpx.AsyncClient(timeout=20) as client:
#         await asyncio.gather(*(test(id, client) for id in ids))


# asyncio.run(main())


import asyncio
import httpx
from typing import Any

semaphore = asyncio.Semaphore(3)
client = httpx.AsyncClient(timeout=20.0)


async def search_movie_by_id(id: int) -> Any:
    url = f"{BASE_URL}/movie/{id}"
    params = {"api_key": API_KEY}

    async with semaphore:
        try:
            response = await client.get(url, params=params)
            return response.status_code, response.json()

        except httpx.TimeoutException:
            return 504, {"detail": "TMDB request timed out"}

        except httpx.HTTPError as e:
            return 502, {"detail": str(e)}
