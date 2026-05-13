#Orchestration of the full pipeline along with observability and monitoring. 

import time 
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', 
                    handlers=[logging.FileHandler("pipeline.log"),
                    logging.StreamHandler()])

from cache_store import get as cache_get, set as cache_set
from retrieval import retrieve_context
from router import build_prompt
from llm_client import chat as llm_call
from postprocess import secure_output
from config import CACHE_TTL, VECTOR_STORE_K

def run_pipeline(question:str)-> str:
    """Run the full RAG pipeline for a given question"""
    logging.info(f"Received question: {question}")
    
    # Step 1: Check cache
    cached_response = cache_get(question)
    if cached_response:
        logging.info(f"Cache hit for user question: {question}")
        return cached_response
    
    # Step 2: Retrieve context
    start_retrieval = time.time()
    context = retrieve_context(question, VECTOR_STORE_K)
    end_retrieval = time.time()
    logging.info(f"Retrieved context: {context}")
    logging.info(f"Retrieval time: {end_retrieval - start_retrieval:.2f} seconds")
    
    # Step 3: Build prompt
    model_name, prompt = build_prompt(question, context)
    logging.info(f"Assembled prompt: {prompt}")
    
    # Step 4: Call LLM
    start_llm = time.time()
    raw_response = llm_call(model_name, prompt)
    finish_llm = time.time()
    logging.info(f"Raw response from LLM: {raw_response}")
    logging.info(f"LLM call time: {finish_llm - start_llm:.2f} seconds")
    
    # Step 5: Post-process response
    final_response = secure_output(raw_response)
    logging.info(f"Final response after post-processing: {final_response}")
    
    # Step 6: Cache the response
    cache_set(question, final_response, ttl=CACHE_TTL)
    
    return final_response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the RAG pipeline with a user question.")
    parser.add_argument("question", type=str, help="The question to ask the RAG system.")
    args = parser.parse_args()
    
    answer = run_pipeline(args.question)
    print(f"Answer: {answer}")
