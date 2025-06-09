from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

print("✅ Correct main.py loaded with health endpoint")

class LogRequest(BaseModel):
    log_content: str

@app.get("/")
async def root():
    return {"message": "AI Bug Reporter Backend is running!"}

@app.post("/analyze-log")
async def analyze_log(request: LogRequest):
    dummy_response = {
        "title": "Database Connection Error",
        "description": "Failed to connect to database due to timeout.",
        "steps_to_reproduce": "1. Start the app\n2. Attempt login\n3. Observe error",
        "expected_outcome": "User should log in successfully",
        "actual_outcome": "Connection timeout error",
        "priority": random.choice(["Low", "Medium", "High"]),
        "error_type": "DATABASE",
        "analysis_method": "dummy",
        "confidence_score": 0.5
    }
    return {"status": "success", "ai_bug_report": dummy_response}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend is healthy"}
