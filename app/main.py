from fastapi import FastAPI
from app.models import BugReport
from app.ai_agent import generate_bug_report_from_ai

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Bug Reporter Backend is running!"}

@app.post("/analyze-log", response_model=BugReport)
def analyze_log(log: str):
    return generate_bug_report_from_ai(log)
