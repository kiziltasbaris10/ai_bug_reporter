from fastapi import FastAPI
from pydantic import BaseModel
from app.log_analyzer import analyze_log
from app.ai_agent import generate_bug_report_from_ai
from app.models import BugReport



app = FastAPI()

class BugReport(BaseModel):
    title: str
    description: str
    log: str

@app.get("/")
async def root():
    return {"message": "AI Bug Reporter Backend is running!"}

@app.post("/report-bug")
async def report_bug(bug: BugReport):
    print("Yeni Bug Raporu Geldi:")
    print(f"Başlık: {bug.title}")
    print(f"Açıklama: {bug.description}")
    print(f"Log: {bug.log}")

    # 🧠 Log analizini çalıştır
    analysis_result = analyze_log(bug.log)

    return {
        "message": "Bug report received successfully!",
        "analysis": analysis_result
    }
@app.post("/ai-report")
async def ai_report(bug: BugReport):
    report = generate_bug_report_from_ai(bug.log)
    return {
        "message": "AI bug report generated successfully",
        "report": report.dict()
    }


    

