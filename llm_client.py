import logging
from langchain_openai import ChatOpenAI
from functools import lru_cache
from langchain_core.messages import AIMessage
from config import TEMPERATURE, MAX_TOKENS, CACHE_TTL, OPENAI_API_KEY

if OPENAI_API_KEY is None:
    raise RuntimeError("OPENAI_API_KEY is not set. Please set it in the environment variables.")

@lru_cache(maxsize=5)    
def _get_chat(model_name:str) -> ChatOpenAI:
    """Initialize the OpenAIChat model with caching"""
    logging.info(f"Initializing model: {model_name}")
    return ChatOpenAI(model=model_name, 
                      temperature=TEMPERATURE, 
                      max_tokens=MAX_TOKENS,
                      openai_api_key=OPENAI_API_KEY)

def chat(model_name:str, prompt:str) -> str:
    """Get a response from the LLM for a given prompt"""
    logging.info(f"Generating response for model: {model_name}")
    chat_llm = _get_chat(model_name)
    response = chat_llm.invoke([AIMessage(content=prompt)])
    return response.content.strip()
