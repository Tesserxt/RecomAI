from collections.abc import AsyncIterable

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.services.csv_loader import movies_df as df

from ..workflows.ai_recom import movie_graph
from ..workflows.ai_search import ai_direct_search_workflow

load_dotenv()


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


async def search_movie_directly(input: str):
    result = await ai_direct_search_workflow.ainvoke({"input": input})
    return result
