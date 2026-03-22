import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Local Ollama setup
llm = Ollama(model="gemma3:4b", base_url="http://127.0.0.1:11434")
embed_model = OllamaEmbedding(model_name="nomic-embed-text", 
base_url="http://127.0.0.1:11434")

# ChromaDB local storage
client = chromadb.PersistentClient(path="/Users/james/rag-project/db")
collection = client.get_or_create_collection("documents")
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Load and index documents
documents = SimpleDirectoryReader("/Users/james/rag-project/docs").load_data()
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model,
    llm=llm
)

print("Ingestion complete.")
