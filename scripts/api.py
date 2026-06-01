from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from config import API_KEY, llm
from router import router_engine

app = FastAPI()

REASONING_PROMPT = """You are a personal AI assistant for James, a CS senior in Los Angeles actively job searching in AI operations, defense, and systems engineering roles.

You have access to James's documents and a database of his job applications.

Original question: {question}

Retrieved information: {raw_answer}

Using the retrieved information, provide a concise, personal, and analytical response. 
Speak directly to James. Contextualize numbers, flag anything worth his attention, and be honest if the data is limited.
No more than 3-4 sentences."""

class Query(BaseModel):
    question: str

@app.post("/query")
def query(payload: Query, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    raw = router_engine.query(payload.question)
    raw_answer = str(raw)

    prompt = REASONING_PROMPT.format(
        question=payload.question,
        raw_answer=raw_answer
    )
    reasoned = llm.complete(prompt)

    return {
        "answer": str(reasoned),
        "raw": raw_answer
    }

@app.get("/health")
def health():
    return {"status": "ok"}
