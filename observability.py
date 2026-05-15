#logging and observability module. 
import logging
from prometheus_client import start_http_server, Histogram, Counter

# metrics
REQUEST_COUNTER = Counter('gen_ai_request_total', 'Total number of requests received')
LLM_LATENCY = Histogram('gen_ai_llm_latency_ms', 'Latency of LLM calls in ms')
RETRIEVAL_LATENCY = Histogram('gen_ai_retrieval_latency_ms', 'Latency of retrieval calls in ms')

def log(question, model_input, model_outpur,guardrail_output = None, model= "unknown", latency_ms = None,user_id = None, retrieved_latency = None):

    REQUEST_COUNTER.inc()

    logging.info("---------------AUTH LOG START---------------")
    logging.info(f"User ID: {user_id}")
    logging.info(f"Question: {question}")
    logging.info(f"Model Used: {model}")    
    logging.info(f"Model Input: {model_input}")
    logging.info(f"Model Output: {model_outpur}")
    if guardrail_output:
        logging.info(f"Guardrail Output: {guardrail_output}")
    logging.info(f"LLM Latency: {latency_ms:.2f} ms")
    if retrieved_latency:
        logging.info(f"Retrieval Latency: {retrieved_latency:.2f} ms")
    logging.info("---------------AUTH LOG END---------------\n")

def record_metrics(metric_name, value):
    if metric_name == "llm_latency":
        LLM_LATENCY.observe(value)
    elif metric_name == "retrieval_latency":
        RETRIEVAL_LATENCY.observe(value)

def start_metrics_server(port=8000):
    start_http_server(port)
    logging.info(f"Prometheus metrics server started on port {port}, at link http://localhost:{port}/metrics")