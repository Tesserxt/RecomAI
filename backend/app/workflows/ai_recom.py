import json
from pathlib import Path
from typing import TypedDict

import pandas as pd
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

load_dotenv()


CURRENT_DIR = Path(__file__).resolve().parent
DATA_PATH = CURRENT_DIR.parents[2] / "data" / "movies(stemd).csv"

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")


df = pd.read_csv(
    DATA_PATH,
    index_col="tmdb_id",
)


class Movie(BaseModel):
    rank: int = Field(ge=1)
    tmdb_id: int
    title: str
    reason: str = Field(
        description="Why i may like this movie based on its similarity "
        "to the input movie in succinct response."
    )


class RankedMovies(BaseModel):
    ranked_candidates: list[Movie]


class MState(TypedDict):
    movie_id: int
    movie_title: str | None
    candidates: dict[int, tuple[str, str]] | None

    ranked_candidates: RankedMovies | None


def retrieve_candidates(state: MState):
    response = requests.get(
        f"http://127.0.0.1:8000/api/recommendations/{state['movie_id']}",
        params={"k": 10},
        timeout=10,
    )
    response.raise_for_status()

    ids = response.json()
    title = df.loc[state["movie_id"]].title
    candidates = df.loc[ids].apply(tuple, axis=1).to_dict()

    return {"candidates": candidates, "movie_title": title}


def rank_and_explain(state: MState):

    structured_llm = llm.with_structured_output(RankedMovies)
    ranking_prompt = f"""
        You are a movie recommendation ranking system.

        Input movie: {state["movie_title"]}
        Input movie ID: {state["movie_id"]}

        Candidate movies:
        {json.dumps(state["candidates"], indent=2, ensure_ascii=False)}

        Tasks:
        1. Rank all candidate movies from most relevant to least relevant
        to a user who likes the input movie.
        2. Consider plot, genre, keywords, cast, and director in stemmed information.
        3. Assign rank 1 to the best candidate.
        4. Use only the supplied candidates. Do not invent movie IDs
        or titles.
        5. Return every candidate exactly once.
        6. Rank all candidates consecutively, starting from 1.

        Return the result using the required structured schema.
    """

    result = structured_llm.invoke(ranking_prompt)

    candidate_ids = set(state["candidates"])
    result_ids = [m.tmdb_id for m in result.ranked_candidates]

    if len(result_ids) != len(candidate_ids) or set(result_ids) != candidate_ids:
        raise ValueError("LLM returned missing, duplicate, or unknown candidate IDs")

    return {"ranked_candidates": result}


def build_graph():
    from langgraph.graph import END, START, StateGraph

    graph = StateGraph(MState)

    # Add nodes
    graph.add_node("retrieve_candidates", retrieve_candidates)
    graph.add_node("rank_and_explain", rank_and_explain)

    # Add edges to connect nodes
    graph.add_edge(START, "retrieve_candidates")
    graph.add_edge("retrieve_candidates", "rank_and_explain")
    graph.add_edge("rank_and_explain", END)

    return graph.compile()


movie_graph = build_graph()
