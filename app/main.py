from fastapi import FastAPI
from pydantic import BaseModel

from app.graph import graph

app = FastAPI()


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(request: ChatRequest):
    result = graph.invoke({"question": request.question})
    return {"answer": result["answer"], "confidence": result["score"], "chunks": result["chunks"]}