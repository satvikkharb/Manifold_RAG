#Retrieve the necessary data for the project
from vector_store import retrieve, retrieve_with_score
from config import VECTOR_STORE_K

def retrieve_context(query: str, k: int = VECTOR_STORE_K) -> str:
    """Get relevant documents for a query"""
    results = retrieve(query, k)   
    return "\n\n".join(results)