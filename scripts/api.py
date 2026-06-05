from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from config import API_KEY, llm
from router import router_engine
import os

def get_api_key(request: Request):
    return request.headers.get("x-api-key", get_remote_address(request))

limiter = Limiter(key_func=get_api_key)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

REASONING_PROMPT = """You are a personal AI assistant for James, a CS senior in Los Angeles actively job searching in AI operations, defense, and systems engineering roles.

You have access to James's documents and a database of his job applications.

Original question: {question}

Retrieved information: {raw_answer}

Using the retrieved information, provide a concise, personal, and analytical response.
Speak directly to James. Contextualize numbers, flag anything worth his attention, and be honest if the data is limited.
No more than 3-4 sentences."""

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return FileResponse(os.path.join(STATIC_DIR, "chat.html"))

@app.post("/query")
@limiter.limit("10/minute")
def query(request: Request, payload: Query, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    raw = router_engine.query(payload.question)
    raw_answer = str(raw)

    source = "sql" if any(c.isdigit() for c in raw_answer) or "application" in raw_answer.lower() else "vector"

    prompt = REASONING_PROMPT.format(
        question=payload.question,
        raw_answer=raw_answer
    )
    reasoned = llm.complete(prompt)

    return {
        "answer": str(reasoned),
        "raw": raw_answer,
        "engine": source
    }

@app.get("/health")
@limiter.limit("100/minute")
def health(request: Request):
    return {"status": "ok"}
