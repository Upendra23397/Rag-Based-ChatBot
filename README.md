1. Title and Summary(Rag Based Chatbot)
in this chatbot we are chat with the LLM which is connected with the external source pdf of the company and we can ask question from the pdf and LLM will generate a brief answer.
2.Techstack
we have used Langchain , LangGraph , pinecone(vectorDB), Google gemini model(Embeddings) , groq Model (generating context aware answer) , Pydantic , Retriver .
3.Architecture 

question → retrieve → score ≥ 0.70? → generate → answer
                          └ no → fallback
4. Setup instructions
- Clone the repo from the GtiHub
- Create and activate a venv
- pip install -r requirements.txt
- Copy .env.example to .env and fill in the keys. List every variable name (Google, Groq, Pinecone, index name, model name)
- Run ingestion once: python -m app.ingest (so that embeddings are generated and once the embeddings are store in vectoreDB run the main.py file )
- Start the server: python -m uvicorn app.main:app --reload
- Open http://127.0.0.1:8000/docs(check the question written in docs file)

5. API usage
- Endpoint: POST /chat
- Request body: {"question": "..."}
- Response: answer, confidence, and the retrieved chunks (with page and score)
6. Design decisions
- Chunk size 1000, overlap 200 (because of the capturing the meaning so that meaning of text cannot be broken)
- Embedding dimension 3072 (or 768, if you can switch)
- Threshold 0.70: I measured it . In-scope scores were 0.76 to 0.83, AI-related but out-of-book 0.62 to 0.65, unrelated 0.50 to 0.55.
- Two-layer grounding: the score threshold blocks the LLM call, and the prompt forces "answer only from context, otherwise fallback".
- Confidence = the top chunk's cosine similarity. Say clearly that it is a similarity score, not a probability.
