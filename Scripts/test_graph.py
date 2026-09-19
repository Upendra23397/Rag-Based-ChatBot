# this is a test file for the graph module
from app.graph import graph

for q in ["What is agentic AI?", "What is the price of Bitcoin?"]:
    result = graph.invoke({"question": q})
    print(q)
    print("score:", result["score"])
    print("answer:", result["answer"])
    print()