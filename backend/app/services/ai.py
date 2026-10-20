from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

df = pd.read_csv("../../data/movies(stemd).csv")


llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", max_output_tokens=200)

template = PromptTemplate(
    template="Generate a concise 2–3 sentence easy to comprehend movie summary from this text: {stemmed_text}. focus on the movie's plot, themes, and genre, and do not invent unsupported details. Return only the summary.",
    input_variables=["stemmed_text"],
)


def generate_summary(movie_id: int) -> str:
    stemmed_text = df.query(f"tmdb_id == {movie_id}").combined.values[0]
    chain = template | llm
    result = chain.invoke({"stemmed_text": stemmed_text})
    return result.text
