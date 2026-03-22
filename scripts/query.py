import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Local Ollama setup
llm = Ollama(model="gemma3:4b", base_url="http://127.0.0.1:11434")
embed_model = OllamaEmbedding(model_name="nomic-embed-text", 
base_url="http://127.0.0.1:11434")

# Load ChromaDB
client = chromadb.PersistentClient(path="/Users/james/rag-project/db")
collection = client.get_or_create_collection("documents")
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Load index
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=embed_model,
    llm=llm
)

# Query
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("What roles is James targeting?")
print(response)
