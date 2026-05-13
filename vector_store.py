#implementation of vector store using Redis. 

from langchain_redis import RedisVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore.document import Document
import os
from dotenv import load_dotenv
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL","redis://localhost:6379/0")
INDEX_NAME = "genai_docs"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def add_documents(text: list[str]):
    docs = [Document(page_content=t) for t in text]
    vector_store = RedisVectorStore.from_documents(docs, embeddings, redis_url=REDIS_URL, index_name=INDEX_NAME)
    vector_store.add_documents(docs)

def get_vector_store():
    return RedisVectorStore(redis_url=REDIS_URL, index_name=INDEX_NAME, embeddings=embeddings)

def retrieve(query: str, k: int = 5) -> list[str]:
     vector_store = get_vector_store()
     results =  vector_store.similarity_search(query, k=k)
     return [d.page_content for d in results]

def retrieve_with_score(query: str, k: int = 5) -> list[tuple[str, float]]:
     vector_store = get_vector_store()
     results =  vector_store.similarity_search_with_score(query, k=k)
     return [(d.page_content, score) for d, score in results]

