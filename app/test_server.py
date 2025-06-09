from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AI Bug Reporter Backend is running!"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend is healthy"}
