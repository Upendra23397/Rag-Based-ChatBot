from langchain_pinecone import PineconeVectorStore

from app.config import PINECONE_INDEX_NAME
from app.ingest import get_embeddings


def retrieve_chunks(query):

    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=get_embeddings()
    )

    results = vector_store.similarity_search_with_score(
        query,
        k=4
    )

    return results
