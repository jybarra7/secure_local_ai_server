import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool
from config import DB_PATH, llm, embed_model
from sql_engine import sql_tool

# Set globals
Settings.llm = llm
Settings.embed_model = embed_model

# Vector store (ChromaDB)
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("documents")
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=embed_model,
)
vector_query_engine = index.as_query_engine(llm=llm)

vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description=(
        "Use for questions about documents, notes, resume, "
        "or unstructured text."
    ),
)

# Router
router_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(llm=llm),
    query_engine_tools=[vector_tool, sql_tool],
)
