import os
import json
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from models import BugReport
from log_analyzer import analyze_log_advanced

# ✅ Debug satırı buraya:
print("🔐 API Key (ilk 5 karakter):", os.getenv("OPENAI_API_KEY")[:5])

# OpenAI istemcisi başlat
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_bug_report_from_ai(log_content: str) -> BugReport:
    rule_based_analysis = analyze_log_advanced(log_content)
    
    prompt = f"""You are an expert QA engineer. Analyze the following technical log and generate a bug report. Respond ONLY with valid JSON matching this format:

{{
  "title": "Short, descriptive title",
  "description": "Detailed description",
  "steps_to_reproduce": "Step-by-step instructions",
  "expected_outcome": "What should happen",
  "actual_outcome": "What actually happened",
  "priority": "Low | Medium | High | Critical",
  "error_type": "Backend | Frontend | API | Network | User Error | Database | Configuration | AI Processing Error"
}}

Context from rule-based analysis:
- Category: {rule_based_analysis.get('category')}
- Reason: {rule_based_analysis.get('reason')}
- Suggestion: {rule_based_analysis.get('suggestion')}

Log content:
```log
{log_content[:2000]}
```"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a technical bug report generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        print("Response of AI:", content)
        bug_data = json.loads(content)
        return BugReport(**bug_data)

    except Exception as e:
        return BugReport(
            title="AI Analysis Failed",
            description=str(e),
            steps_to_reproduce="N/A",
            expected_outcome="N/A",
            actual_outcome="N/A",
            priority="Medium",
            error_type="AI_PROCESSING_ERROR",
            analysis_method="fallback",
            confidence_score=0.2
        )

log_content = """
[ERROR] 2024-05-25 14:02:17 - API call to /get-user failed with status 500.
Traceback (most recent call last):
  File "app.py", line 42, in <module>
    response = requests.get(url)
  File "requests/api.py", line 75, in get
    return request("get", url, params=params, **kwargs)
requests.exceptions.HTTPError: 500 Server Error
"""


def analyze_log_advanced(log):
    return {
        "category": "API Error",
        "reason": "Internal Server Error (500)",
        "suggestion": "Check backend API route /get-user and server logs"
    }

bug_report = generate_bug_report_from_ai(log_content)
print("🪲 AI Bug Report:")
print(bug_report)
