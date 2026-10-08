from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import movies, recommendations

app = FastAPI()

origins = ["http://127.0.0.1:5173", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(recommendations.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
