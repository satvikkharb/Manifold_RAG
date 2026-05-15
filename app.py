#fastapi pipeline
import time, uuid, logging
from fastapi import FastAPI, HTTPException, Request
from cache_store import get as cache_get, set as cache_set
from llm_client import chat as llm_call
from retrieval import retrieve_context
from postprocess import secure_output
from router import build_prompt
from guardrails import apply_guardrails
from observability import log as audit_log, record_metrics, start_metrics_server
from pydantic import BaseModel
from config import CACHE_TTL, VECTOR_STORE_K
from main import run_pipeline
from observability import start_metrics_server

app = FastAPI(
    title = "GenAI RAG Pipeline API",
    description="An API for a GenAI RAG pipeline with guardrails, caching, and observability.",
    version="1.0"
)

start_metrics_server(port = 8001)

class AskRequest(BaseModel):
    question: str
    user_id: str | None = None

class AskResponse(BaseModel):
    answer: str
    user_id: str | None = None

def run_pipeline_with_observability(question:str, user_id:str|None = None)-> str:
    """Run the full RAG pipeline for a given question with observability and logging"""
    logging.info(f"Received question: {question} from user_id: {user_id}")
    
    # Step 1: Check cache
    cached = cache_get(question)
    if cached:
        return AskResponse(answer=cached, user_id=user_id)
    
    # Step 2: Retrieve context
    start_retrieval = time.time()
    context = retrieve_context(question, VECTOR_STORE_K)
    end_retrieval = time.time()
    logging.info(f"Retrieved context: {context}")
    logging.info(f"Retrieval time: {end_retrieval - start_retrieval:.2f} seconds")
    record_metrics("retrieval_latency", end_retrieval - start_retrieval)
    
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
    guardrail_response = apply_guardrails(final_response)
    logging.info(f"Final response after post-processing: {final_response}")

    #apply log
    audit_log(question=question, model_input=prompt, model_outpur=final_response, guardrail_output=guardrail_response, model=model_name, latency_ms=(finish_llm - start_llm)*1000 + (end_retrieval - start_retrieval)*1000, retrieved_latency=(end_retrieval - start_retrieval)*1000, user_id=user_id)
    
    # Step 6: Cache the response
    cache_set(question, final_response, ttl=CACHE_TTL)
    
    return guardrail_response


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    """Ask a question to the RAG system and get an answer."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    request_id = str(uuid.uuid4())
    logging.info(f"Processing request_id: {request_id} for user_id: {request.user_id}")

    try: 
        return run_pipeline_with_observability(request.question, request.user_id)
    except Exception as e:
        logging.error(f"Error processing request_id: {request_id} - {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
    
@app.get("/")
async def root():
    return {"message": "Welcome to the GenAI RAG Pipeline API. Use the /ask endpoint to interact with the system."}

@app.get("/health")
async def health(): 
    return {"status": "ok", "message": "The GenAI RAG Pipeline API is healthy and running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8002)
