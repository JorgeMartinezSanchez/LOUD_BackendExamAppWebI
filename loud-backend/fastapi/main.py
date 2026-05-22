from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hola"}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/api/v1/events/")
def list_events():
    return {"results": [], "count": 0}