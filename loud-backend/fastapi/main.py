from fastapi import FastAPI
from api.v1 import events

app = FastAPI(title="LOUD API", version="1.0.0")

app.include_router(events.router)

@app.get("/")
def home():
    return {"message": "LOUD API is running"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}