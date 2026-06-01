import os
from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

load_dotenv()

OLLAMA_BASE  = os.getenv("OLLAMA_BASE", "http://127.0.0.1:11434")
DB_PATH      = os.getenv("DB_PATH",     "/Users/james/rag-project/db")
DOCS_PATH    = os.getenv("DOCS_PATH",   "/Users/james/rag-project/docs")
JOBS_DB      = os.getenv("JOBS_DB",     "/Users/james/rag-project/jobs.db")
API_KEY      = os.getenv("API_KEY",     "jachty")

llm = Ollama(model="gemma3:4b", base_url=OLLAMA_BASE)
embed_model = OllamaEmbedding(model_name="nomic-embed-text", base_url=OLLAMA_BASE)
