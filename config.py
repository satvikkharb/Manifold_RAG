import os
from dotenv import load_dotenv

load_dotenv()   

#Environment variables for the project.
OPENAI_API_KEY: str|None = os.getenv("OPENAI_API_KEY")    
REDIS_URL: str = os.getenv("REDIS_URL","redis://localhost:6379/0")

#Model configuration
DEFAULT_MODEL = "gpt-4.1-nano"
TEMPERATURE = 0.2
MAX_TOKENS = 512

#CACHE
CACHE_TTL = 3600  # Time to live for cache entries in seconds (1 hour)
VECTOR_STORE_K = 2  # Number of top relevant documents to retrieve from the vector store

