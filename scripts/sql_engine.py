from llama_index.core import SQLDatabase, Settings
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import QueryEngineTool
from sqlalchemy import create_engine
from config import JOBS_DB, llm, embed_model

# Set globals so nothing falls back to OpenAI
Settings.llm = llm
Settings.embed_model = embed_model

sql_engine = create_engine(f"sqlite:///{JOBS_DB}")
sql_database = SQLDatabase(sql_engine, include_tables=["applications"])

nl_sql_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["applications"],
    llm=llm,
    embed_model=embed_model,
)

sql_tool = QueryEngineTool.from_defaults(
    query_engine=nl_sql_engine,
    description=(
        "Use for structured queries about job applications, "
        "companies, status, dates, or counts."
    ),
)
