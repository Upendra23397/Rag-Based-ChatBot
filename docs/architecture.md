# Architecture

The system has two separate parts: a one-time **ingestion pipeline** and a **query pipeline** that runs on every request.

## 1. Ingestion pipeline (`app/ingest.py`)

Run once with `python -m app.ingest`.

1. Load the Agentic AI eBook PDF (60 pages).
2. Split it into 119 chunks (chunk size 1000, overlap 200).
3. Generate an embedding for each chunk using the Google Gemini embedding model.
4. Store the embeddings in a Pinecone index (cosine similarity).

Notes:
- Chunks are sent in batches of 50 with a short sleep between batches, because the Gemini free tier limits embedding requests per minute.
- Every chunk gets a fixed ID (`chunk-0`, `chunk-1`, ...), so running ingestion again overwrites the same vectors instead of creating duplicates.so taht it will not gnerate the duplicated embeddings 

## 2. Query pipeline (`app/graph.py`)

The pipeline is built with LangGraph. A shared **state** (a `TypedDict` with `question`, `chunks`, `score`, `answer`) is passed from node to node. Each node returns only the fields it changed, and LangGraph merges them into the state.

### Nodes
- **retrieve:** searches Pinecone for the top 4 chunks most similar to the question. It stores the chunks (text, page, score) and the top similarity score in the state.
- **generate:** joins the chunk texts into a context and sends it, with the question, to the Groq LLM (`temperature=0`). The answer is stored in the state.
- **fallback:** returns a fixed message saying the answer was not found in the eBook. The LLM is not called.

### Conditional edge
- **route:** a plain Python check, not an LLM. If the top score is >= 0.70 it goes to `generate`, otherwise to `fallback`.

### Flow

    question -> retrieve -> score >= 0.70?
                              |-- yes -> generate -> answer
                              |-- no  -> fallback -> fixed message

## 3. API layer (`app/main.py`)

FastAPI exposes `POST /chat`. It takes `{"question": "..."}`, runs the graph, and returns the answer, the confidence (top chunk similarity score) and the retrieved chunks with page numbers and scores.

## 4. Design decisions

- **Two-layer grounding:** the score threshold stops the LLM from being called on unrelated questions, and the prompt tells the LLM to answer only from the given context.
- **Threshold 0.70:** chosen from test questions. In-scope questions scored 0.76 to 0.83, AI-related questions not covered by the eBook scored 0.62 to 0.65, and unrelated questions scored 0.50 to 0.55.
- **Confidence** is the cosine similarity of the top chunk. It is a similarity score, not a probability.
- **Separate ingestion:** the PDF does not change, so it is embedded once instead of on every server start.