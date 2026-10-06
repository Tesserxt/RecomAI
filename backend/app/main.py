from fastapi import FastAPI

from .routers.movies import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
