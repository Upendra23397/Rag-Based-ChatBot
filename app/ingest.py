#1.load the pdf file and return the documents
#2.chunking the documents into smaller pieces
#3.embedding the documents using Google GenAI Enmbedding model
#4.creating the Pinecone index if it does not exist
#5.storing the embeddings into Pinecone vector database
#=================================================================================
# importing the required libraries
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone ,ServerlessSpec 
from app.config import PINECONE_API_KEY, PINECONE_INDEX_NAME ,EMBEDDING_DIM
from langchain_pinecone import PineconeVectorStore
import time 
#creating the function to load the pdf file and return the documents
def load_pdf(file_path):
    loaders=PyPDFLoader(file_path)
    documnets=loaders.load()
    return documnets
#creating the function to split the documents into smaller chunks
def split_documents(documetns):
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200) # creatig the splitter object with chunk size of 1000 and overlap of 200
    chunks=splitter.split_documents(documetns) # calling the split_documents method to split the documents into smaller chunks
    return chunks
#creating the function to embed the documents using Google GenAI Embedding model
def get_embeddings():
    embeddings=GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
    )
    return embeddings

# creating the function to create the Pinecone index if it does not exist
def create_pinecone_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIM,  # wahi number jo embed_query ki len(vec) me aaya tha
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

def store_embeddings_in_pinecone(chunks, embeddings):
    pinecone_vector_store = PineconeVectorStore(index_name=PINECONE_INDEX_NAME, embedding=embeddings)
    for i in range(0, len(chunks), 50):
        batch = chunks[i:i + 50]
        ids = [f"chunk-{i + j}" for j in range(len(batch))] # creating unique ids for each chunk in the batch
        pinecone_vector_store.add_documents(batch, ids=ids) 
        time.sleep(1)
        print(f"stored {min(i + 50, len(chunks))} / {len(chunks)}") # printing the number of documents stored in Pinecone vector database
        

if __name__ == "__main__":
    docs = load_pdf("data/Ebook-Agentic-AI.pdf")
    print(len(docs))
    chunks = split_documents(docs)
    print(len(chunks))
    embeddings = get_embeddings()
    create_pinecone_index()
    vec=store_embeddings_in_pinecone(chunks, embeddings)

    