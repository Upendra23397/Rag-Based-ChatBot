# Agentic AI eBook RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions **strictly from the Agentic AI eBook** ([PDF](https://konverge.ai/pdf/Ebook-Agentic-AI.pdf)). It retrieves the most relevant parts of the PDF, generates a short answer from them, and returns the answer together with the retrieved chunks and a confidence score. If the eBook does not contain the answer, the bot says so instead of guessing.

## Tech Stack

| Component | Technology |
|---|---|
| Pipeline / orchestration | LangGraph, LangChain |
| Embeddings | Google Gemini (`gemini-embedding-001`) |
| Vector database | Pinecone |
| LLM (answer generation) | Groq |
| API | FastAPI (request validation with Pydantic) |

## How It Works

**Ingestion (run once):** PDF → chunks → Gemini embeddings → Pinecone

**Query (every request):**

```
question → retrieve → score >= 0.70? ─ yes → generate → answer
                                     └ no  → fallback → "not found in the eBook"
```

See [docs/architecture.md](docs/architecture.md) for details.

## Setup

1. Clone the repository:
```bash
   git clone https://github.com/Upendra23397/Rag-Based-ChatBot.git
   cd Rag-Based-ChatBot
```
2. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # macOS / Linux
```
3. Install the dependencies:
```bash
   python -m pip install -r requirements.txt
```
4. Create your `.env` file from the template and fill in your keys:
```bash
   copy .env.example .env         # Windows
   cp .env.example .env           # macOS / Linux
```
   Variables:
```
   GOOGLE_API_KEY=
   GROQ_API_KEY=
   PINECONE_API_KEY=
   PINECONE_INDEX_NAME=
   LLM_MODEL=
```
5. Make sure the eBook is saved as `data/Ebook-Agentic-AI.pdf`.
6. Run ingestion **once**. It chunks the PDF, creates the embeddings and stores them in Pinecone:
```bash
   python -m app.ingest
```
   Ingestion takes a couple of minutes because it is rate-limited (see Limitations). Running it again is safe: chunks have fixed IDs, so they are overwritten, not duplicated.
7. Start the server:
```bash
   python -m uvicorn app.main:app --reload
```
8. Open http://127.0.0.1:8000/docs, use **POST /chat** → **Try it out**, and ask a question.

## API Usage

**Endpoint:** `POST /chat`

**Request body:**

```json
{ "question": "What is agentic AI?" }
```

**Response:** the final `answer`, the `confidence` score, and the retrieved chunks (each with `text`, `page` and `score`).

**Example request**

![Swagger request](docs/images/inputAPIExample.png)

**Example response**

![Swagger response](docs/images/outputAPIExample.png)

## Sample Queries

Six sample queries with their answers, confidence scores and source pages (including one out-of-scope question that triggers the fallback) are in [docs/sample_queries.md](docs/sample_queries.md).

## Design Decisions

- **Chunking (size 1000, overlap 200):** chunks are small enough for precise retrieval, and the overlap keeps a sentence or idea from being cut in half at a chunk boundary.
- **Embedding dimension 3072:** the default output size of `gemini-embedding-001`. The Pinecone index uses the same dimension and cosine similarity.
- **Threshold 0.70:** chosen from measured scores, not guessed. Questions covered by the eBook scored 0.76 to 0.83, AI-related questions the eBook does not cover scored 0.62 to 0.65, and unrelated questions scored 0.50 to 0.55.

  ![Similarity scores for in-scope, out-of-scope and tricky questions](docs/images/sampleQueriesAnswer.png)

- **Two-layer grounding:**
  1. If the top similarity score is below the threshold, the LLM is not called and a fixed fallback message is returned.
  2. Otherwise, the prompt instructs the LLM to answer only from the retrieved context, and to use the fallback message if the answer is not there.
- **Confidence:** the cosine similarity of the top retrieved chunk. It shows how closely the chunk matches the question. It is a similarity score, not a probability that the answer is correct.
- **Separate ingestion:** the PDF does not change, so it is embedded once instead of on every server start.

## Limitations

- The Gemini free tier limits embedding requests per minute, so ingestion runs in batches with pauses.
- The threshold was tuned on a small set of test questions. Very short or vague questions may score below it and get the fallback message.
- Answers are only as complete as the retrieved chunks (top 4).

## Project Structure

```
app/
  config.py       settings and environment variables
  ingest.py       PDF → chunks → embeddings → Pinecone
  retriever.py    Pinecone similarity search with scores
  prompts.py      grounding prompt and fallback message
  graph.py        LangGraph pipeline (retrieve, route, generate, fallback)
  main.py         FastAPI app (POST /chat)
docs/
  architecture.md
  sample_queries.md
  images/
```