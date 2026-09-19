from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

from app.config import SCORE_THRESHOLD, GROQ_API_KEY, LLM_MODEL
from app.prompts import rag_prompt, FALLBACK_MESSAGE
from app.retriever import retrieve_chunks


class GraphState(TypedDict, total=False):
    question: str
    chunks: list
    score: float
    answer: str


llm = ChatGroq(
    model=LLM_MODEL,
    api_key=GROQ_API_KEY,
    temperature=0
)


def retrieve(state: GraphState):

    results = retrieve_chunks(state["question"])

    if not results:
        return {
            "chunks": [],
            "score": 0.0
        }

    chunks = []
    for doc, score in results:
          chunks.append({
            "text": doc.page_content,
            "page": int(doc.metadata["page"]) + 1,
            "score": score,
            })

    best_score = results[0][1]

    return {
        "chunks": chunks,
        "score": best_score,
    }


def route(state: GraphState):

    if state["score"] >= SCORE_THRESHOLD:
        return "generate"

    return "fallback"


def generate(state: GraphState):

    context = "\n\n".join([c["text"] for c in state["chunks"]])

    messages = rag_prompt.invoke({
        "context": context,
        "question": state["question"]
    })

    response = llm.invoke(messages)

    return {
        "answer": response.content
    }


def fallback(state: GraphState):

    return {
        "answer": FALLBACK_MESSAGE
    }


builder = StateGraph(GraphState)

builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_node("fallback", fallback)

builder.add_edge(START, "retrieve")

builder.add_conditional_edges(
    "retrieve",
    route,
    {
        "generate": "generate",
        "fallback": "fallback"
    }
)

builder.add_edge("generate", END)
builder.add_edge("fallback", END)

graph = builder.compile()