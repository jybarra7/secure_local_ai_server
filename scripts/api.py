from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from config import API_KEY
from router import router_engine

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/query")
def query(payload: Query, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response = router_engine.query(payload.question)
    return {"answer": str(response)}

@app.get("/health")
def health():
    return {"status": "ok"}
