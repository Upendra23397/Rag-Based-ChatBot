import os
from dotenv import load_dotenv
load_dotenv()  # open file and put the values in the environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")
EMBEDDING_DIM = 3072
SCORE_THRESHOLD = 0.70 # we are getting this value form the similarity score
# print(PINECONE_API_KEY, PINECONE_INDEX_NAME, GOOGLE_API_KEY, GROQ_API_KEY)