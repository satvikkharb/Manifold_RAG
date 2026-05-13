#generate the prompt and use it for the next step. 
from config import DEFAULT_MODEL
TEMPLATE = """You are a helpful assistant that answers questions based on the following retrieved context.
{context}

Question: {question}
Answer:"""

def build_prompt(question: str, context: str) -> str:
    """Build the prompt for the LLM"""
    context_block = f"Context:\n{context}\n\n" if context.strip() else "No relevant context found.\n\n"
    return DEFAULT_MODEL, TEMPLATE.format(context=context_block, question=question)