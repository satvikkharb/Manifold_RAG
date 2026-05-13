#file to load the data to the vector store. 
from vector_store import add_documents
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain_core.documents.base import Blob
from langchain_text_splitters import RecursiveCharacterTextSplitter

blob = Blob.from_path("/Users/satvik/Desktop/Project/personal/Manifold-RAG/data/114-BALLB-Hons-II-IV-VI-VIII-X-Semester.pdf")
parser = PyPDFParser()
documents = parser.lazy_parse(blob)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

# for i, chunk in enumerate(chunks):
#     print(f"Chunk {i}: {chunk.page_content}...")  
#     print("-" * 50)

add_documents([chunk.page_content for chunk in chunks])

print("Documents added to vector store successfully!")
