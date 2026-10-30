from collections.abc import AsyncIterable
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from ..workflows.ai_recom import movie_graph

load_dotenv()


BASE_DIR = Path(__file__).resolve().parents[3]
CSV_PATH = BASE_DIR / "data" / "movies(stemd).csv"

df = pd.read_csv(CSV_PATH, usecols=["tmdb_id", "combined"], index_col="tmdb_id")

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", max_output_tokens=200)

template = PromptTemplate(
    template="Generate a concise 2–3 sentence easy to comprehend movie summary from this stemmed text: {stemmed_text}. focus on the movie's plot, themes, and genre, and do not invent unsupported details. Return only the summary.",
    input_variables=["stemmed_text"],
)


# def generate_summary(movie_id: int) -> str:
#     stemmed_text = df.query(f"tmdb_id == {movie_id}").combined.values[0]
#     chain = template | llm
#     result = chain.invoke({"stemmed_text": stemmed_text})
#     return result.text


async def generate_summary(movie_id: int) -> AsyncIterable[str]:
    stemmed_text = df.query(f"tmdb_id == {movie_id}").combined.values[0]
    chain = template | llm
    async for chunk in chain.astream({"stemmed_text": stemmed_text}):
        print(
            "Chunk content:", chunk.content, chunk.text
        )  # Debugging line to check the chunk content
        yield chunk.text


def generate_ai_recoms(movie_id: int):
    state = {"movie_id": movie_id}
    result = movie_graph.invoke(state)
    return result
