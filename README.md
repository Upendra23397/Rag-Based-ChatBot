# Agentic AI eBook RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions **strictly from the Agentic AI eBook** ([PDF](https://konverge.ai/pdf/Ebook-Agentic-AI.pdf)). It retrieves the most relevant parts of the PDF, generates a short answer from them, and returns the answer together with the retrieved chunks and a confidence score. If the eBook does not contain the answer, the bot says so instead of guessing.

5. API usage
- Endpoint: POST /chat
**Request**

![Swagger request](docs/images/inputAPIExample.png)

- Request body: {"question": "..."}
- Response: answer, confidence, and the retrieved chunks (with page and score)
**Response**

![Swagger response](docs/images/outputAPIExample.png)
7. Design decisions
- Chunk size 1000, overlap 200 (because of the capturing the meaning so that meaning of text cannot be broken)
- Embedding dimension 3072 (or 768, if you can switch)
- Threshold 0.70: I measured it . In-scope scores were 0.76 to 0.83, AI-related but out-of-book 0.62 to 0.65, unrelated 0.50 to 0.55.
- Two-layer grounding: the score threshold blocks the LLM call, and the prompt forces "answer only from context, otherwise fallback".
- Confidence = the top chunk's cosine similarity. Say clearly that it is a similarity score, not a probability.
