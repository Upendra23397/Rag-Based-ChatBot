# this is a test file for the pinecone module
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
print(pc.list_indexes().names())
from pinecone import ServerlessSpec

INDEX_NAME = "agentic-ai-ebook"
DIMENSION = 3072      # wahi number jo embed_query ki len(vec) me aaya tha

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

print(pc.list_indexes().names())