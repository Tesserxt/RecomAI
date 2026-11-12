from typing import Literal, TypedDict

from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")


# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal["search_movie", "recommend_movies"] = Field(
        None, description="The next step in the routing process"
    )


from pydantic import BaseModel, Field


class Search_Movie(BaseModel):
    search_query: str = Field(
        description=(
            "A concise movie title or search phrase extracted from the user's "
            "request. Remove conversational filler and preserve important "
            "movie names, spelling, and identifying details."
        )
    )


# Augment the LLM with schema for structured output
router = llm.with_structured_output(Route)


# State
class State(TypedDict):
    input: str
    decision: str
    search_query: str
    output: str


def llm_call_router(state: State):
    """Classify the user's intent."""

    # decision = router.invoke([
    #     SystemMessage(
    #         content="""
    #     You are an intent classification assistant for a movie application.

    #     Classify the user's request into exactly one of these categories:

    #     1. search_movie:
    #        The user wants to find, search for, or look up a specific movie.
    #        Examples:
    #        - Find Interstellar.
    #        - Search for Batman Begins.
    #        - Show me the movie Inception.
    #        - I want information about Oppenheimer.

    #     2. recommend_movies:
    #        The user wants movie suggestions or recommendations.
    #        Examples:
    #        - Recommend some sci-fi movies.
    #        - Suggest movies similar to Inception.
    #        - What should I watch tonight?
    #        - Recommend movies starring Leonardo DiCaprio.

    #     Important:
    #     - Looking up a specific movie is search_movie.
    #     - Asking for similar movies is recommend_movies.
    #     - Asking for suggestions based on genres, actors, moods,
    #       or preferences is recommend_movies.
    #     - Choose the most relevant intent based on the user's primary request.
    #     """
    #     ),
    #     HumanMessage(content=state["input"]),
    # ])
    # print(decision)

    return {"decision": "search_movie"}


def llm_call_1(state: State):
    """Extract movie search query."""

    structured_llm = llm.with_structured_output(Search_Movie)
    result = structured_llm.invoke([
        SystemMessage(
            content="""
        Extract the only movie title or relevant search phrase so that can be uses in react frotend search bar from the user's request.

        else say 'None' or better dont respond.
        """
        ),
        HumanMessage(content=state["input"]),
    ])
    return {"search_query": result.search_query}


def llm_call_2(state: State):
    """recommend_movies"""

    result = llm.invoke(state["input"])
    print(result)
    return {"output": result.content}


def llm_call_3(state: State):
    """Write a poem"""

    result = llm.invoke(state["input"])
    return {"output": result.content}


# Conditional edge function to route to the appropriate node
def route_decision(state: State):
    # Return the node name you want to visit next
    if state["decision"] == "search_movie":
        return "llm_call_1"
    elif state["decision"] == "recommend_movies":
        return "llm_call_2"


# Build workflow
router_builder = StateGraph(State)

# Add nodes
router_builder.add_node("llm_call_1", llm_call_1)
router_builder.add_node("llm_call_2", llm_call_2)
router_builder.add_node("llm_call_router", llm_call_router)

# Add edges to connect nodes
router_builder.add_edge(START, "llm_call_1")
# router_builder.add_conditional_edges(
#     "llm_call_router",
#     route_decision,
#     {  # Name returned by route_decision : Name of next node to visit
#         "llm_call_1": "llm_call_1",
#         "llm_call_2": "llm_call_2",
#     },
# )
router_builder.add_edge("llm_call_1", END)
# router_builder.add_edge("llm_call_2", END)

# Compile workflow
ai_direct_search_workflow = router_builder.compile()

# Show the workflow
# display(Image(router_workflow.get_graph().draw_mermaid_png()))

# Invoaw
# state = router_workflow.invoke({"input": "find me interstellar bro"})
# print(state)
